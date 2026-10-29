# M19-B13 · Build a Deployment Pipeline

> Video: Module 19, Build 13. Watch it first, then follow along here.

## What you'll build

The road from a `git push` to a running server, for the allcsvideos backend:

- A GitHub Actions workflow (`pipeline.yml`): lint, type check, tests on Python 3.13 and 3.14, then an `image` job that builds one image tagged with the commit and pushes it to a registry, then a `deploy` job that sends one command to the server
- A server that runs two copies of the API ("blue" and "green") behind Caddy. A new version starts in the idle colour, runs a migration, passes a smoke test through a private door, and only then gets the visitors
- A smoke test (`smoke.sh`) of five real requests, a rollback command, and a "visitor who never stops" script that proves nothing fails during a release

The four rules: a push to `main` reaches the server by itself once the checks are green; visitors never see a failed request during a release; a broken version is stopped before any visitor meets it; going back is one command.

## Read this first: what is verified and what is captured

- **Verified by running it for this README**: the whole app test suite with coverage, `ruff`, building the image with a version tag and running it, `deploy/smoke.sh` against that container (five checks pass), and `bash -n` on every deploy script.
- **Captured, not re-run**: the full rehearsal (the workflow run with `act` against a "server" that is a Docker-in-Docker container, five releases) and the AWS session. Outputs marked "captured" were recorded in the video session and are copied as they were. The AWS part ran in a playground account with one `t3.small` server, and everything was deleted in the same session (instances 0, repositories 0, role, security group and volumes gone). This repo creates no cloud resources and contains no account ids, keys or addresses.
- If you do the AWS part yourself it costs real money and opens a server to the internet. Use an account you own, read every command first, and finish with the clean-up checklist at the end. Nothing in this lesson is needed for the rest of the course.

## Before you start

- Python 3.14, Docker, and (for the rehearsal) `act` (`brew install act`). You should have done M19-L01 to L04.
- The folder `allcs/` holds the whole project at the end of the video: the backend, the `Dockerfile`, the workflow and the `deploy/` folder.
- All passwords in this lesson are demo values (`demo-admin-pw`) or generated on the server and never shown.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/.github/workflows/pipeline.yml` | The pipeline: `lint`, `typecheck`, `test` (matrix, services), `image` (needs the three, tag = first 7 letters of the commit), `deploy` (main only, `environment: production`) |
| `allcs/Dockerfile`, `.dockerignore` | The two-stage image. `ARG APP_VERSION` becomes the environment variable the app reports at `/version`. `.dockerignore` keeps `deploy`, `tests`, `.git`, `.env` and more out of the image |
| `allcs/deploy/remote.sh` | Runs on the CI machine: sends one command to the server (`MODE=exec` for the rehearsal, `ssh` or `ssm` on AWS) |
| `allcs/deploy/deploy.sh` | Runs on the server: `deploy TAG`, `rollback`, `status` |
| `allcs/deploy/smoke.sh` | Five real requests; any failure stops the deploy |
| `allcs/deploy/compose.yaml` | The server's compose file: `caddy`, `postgres`, `redis`, `api-blue`, `api-green`, and the one-shot `migrate` and `seed` |
| `allcs/deploy/Caddyfile` | The door: port 80 is public, port 8081 is a private preview door for the new colour |
| `allcs/deploy/install_app.sh` | Prepares `/opt/allcs` on a fresh server: generates the secret key and database password, deploys the first version |
| `allcs/deploy/hammer.sh` | A visitor who asks for `/version` every 50 ms and counts failures |
| `allcs/app/`, `tests/`, `migrations/` | The backend (with `app/seed.py`: the first admin and two demo courses) and its 42 tests |
| `rehearsal/server_up.sh`, `rehearsal/ci.sh` | The local rehearsal: a registry and a "server" container; and `act push` (these need `act`, a network, and edits for your machine, see step 3) |

## Follow along

### 1. The design

A factory builds the product and packs it in a box with a label: that box is the Docker image and the label is its tag. A warehouse keeps every labelled box: the registry (on AWS, ECR). The shop is the server. A push to `main` runs the checks, the `image` job builds and pushes the image, and the `deploy` job sends one command to the server. On the server, Caddy is the door (a proxy); two colours of the API sit behind it, and `deploy.sh` decides which colour gets the visitors.

### 2. Read the code, in order

1. `pipeline.yml`, job `image`: `needs: [lint, typecheck, test]`, so it never starts on a red change. The tag is the first seven letters of the commit; the same value goes into `--build-arg APP_VERSION=...` so the running app can report its own version; then `docker push`.
2. Job `deploy`: `needs: image`, `if: github.ref == 'refs/heads/main'`, `environment: production` (on GitHub, a person can be asked to approve here). It runs one script: `bash deploy/remote.sh deploy <tag>`. The variable `MODE` says how to reach the server.
3. `remote.sh`: in the rehearsal the server is a container, so `docker exec` is enough. On AWS it is `ssh ec2-user@$HOST sudo bash /opt/allcs/deploy.sh <action>` (port 22 open to one single address; the keys are temporary, from EC2 Instance Connect), or SSM Run Command where an account allows it (no open port at all).
4. `compose.yaml` on the server: both API services share one block (`ENVIRONMENT`, `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY` from variables, `WEB_CONCURRENCY: 2`, `stop_grace_period: 30s`). `api-blue` and `api-green` differ only in their image tag (`BLUE_TAG` and `GREEN_TAG`), so one colour can run version 1 while the other runs version 2, and they only start when the deploy script asks (`profiles: ["apps"]`).
5. `Caddyfile`: `:80` imports `active.caddy` (which colour gets the visitors); `:8081` is a private door open only inside the server, importing `preview.caddy` (the new colour). That is where the new version is tested before any visitor sees it.
6. `deploy.sh deploy TAG`: pull the new image into the idle colour; run the migration with the new image BEFORE anything starts (if it fails, the script aborts and visitors notice nothing); on the very first deploy also run the seed; start the idle colour; point the preview door at it; wait until Docker says healthy; run `smoke.sh` on the private door; then switch (Caddy reloads gracefully) and run `smoke.sh` again through the public door. If that fails, it switches back by itself. The old colour keeps running, so the rollback target is already warm.
7. `smoke.sh`: is it alive (`/health/live`), is it ready with `"postgres":"ok"`, does `/version` equal the tag, does `/courses?limit=5` answer 200 with `"items"`, and is a login required (`/me` gives 401)? One failure stops the deploy with exit code 1, so in a pipeline the deploy job turns red.

### 3. Check the pieces on your laptop (verified)

```bash
cd allcs
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install celery==5.6.3 redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 pydantic-settings==2.16.1 httpx==0.28.1 pytest==9.1.1 pytest-cov ruff==0.17.3
docker run -d --name pyrepo-m19-b13-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs_test -p 19513:5432 postgres:17.11
docker run -d --name pyrepo-m19-b13-redis -p 19413:6379 redis:8
export DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:19513/allcs_test
export REDIS_URL=redis://localhost:19413/15
for f in deploy/*.sh; do bash -n "$f" && echo "syntax ok $f"; done
ruff check .
ruff format --check .
pytest -q --cov --cov-fail-under=90
```

```
syntax ok deploy/deploy.sh
...
All checks passed!
36 files already formatted
TOTAL                          532     32     34      8    93%
Required test coverage of 90% reached. Total coverage: 92.93%
42 passed in 3.29s
```

(The video shows 41 passed in the first release, before the later changes; the final tree has 42 tests. Times differ.) Now build the image with a version tag, run it, and run the smoke test against it:

```bash
docker build -t m19b13-allcs:abc1234 --build-arg APP_VERSION=abc1234 .
docker run -d --name pyrepo-m19-b13-app -p 8703:8000 -e ENVIRONMENT=prod -e DATABASE_URL=postgresql+psycopg://allcs:allcs@host.docker.internal:19513/allcs_test -e REDIS_URL=redis://host.docker.internal:19413/0 -e SECRET_KEY=demo-only-not-a-real-secret-4f2a -e FORWARDED_ALLOW_IPS='*' m19b13-allcs:abc1234
sleep 12
curl -s localhost:8703/version; echo
curl -s localhost:8703/health/ready; echo
bash deploy/smoke.sh http://localhost:8703 abc1234
```

```
{"version":"abc1234","environment":"prod"}
{"status":"ready","postgres":"ok","redis":"ok"}
smoke test on http://localhost:8703
  ok    live (200)
  ok    ready (200)
  ok    version is abc1234 (200)
  ok    course list (200)
  ok    login is required (401)
SMOKE PASSED
```

(The image is about 453 MB. On Linux add `--add-host=host.docker.internal:host-gateway` to `docker run`.) The tests ran against an empty database, so the five checks pass here. Remove everything: `docker rm -f -v pyrepo-m19-b13-app pyrepo-m19-b13-pg pyrepo-m19-b13-redis` and `docker rmi m19b13-allcs:abc1234`.

### 4. The rehearsal (captured)

Before the real cloud, the same workflow ran on the laptop with `act push`: the same workflow file, a local registry on port 19050 (`REGISTRY` defaults to `localhost:19050`), and a "server" that is a Docker-in-Docker container, so `MODE=exec` and `docker exec` are enough. `rehearsal/server_up.sh` builds that server (a privileged container, a registry, and what the AWS user-data does: install tools, copy `deploy/`, run `install_app.sh`); `rehearsal/ci.sh` runs `act push` (adapt the architecture flag and the runner image to your machine; the script also downloads the Docker Compose plugin from the internet for the "server", which is why it is not run for this README). A rehearsal is free, you can repeat it, and a mistake costs nothing.

Captured, release 1 (a push to `main`): every job green, 41 tests on each Python version, and in the last job:

```
DEPLOY 9d51324 -> blue (active now: none)
INFO  [alembic.runtime.migration] Running upgrade  -> cb9aa85a3921, courses and lessons
INFO  [alembic.runtime.migration] Running upgrade cb9aa85a3921 -> 6d1d3956ce21, students and enrollments
INFO  [alembic.runtime.migration] Running upgrade 6d1d3956ce21 -> f149f9b699de, passwords roles owners
INFO  [alembic.runtime.migration] Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens
smoke test on http://127.0.0.1:8081
  ok    live (200)
  ok    ready (200)
  ok    version is 9d51324 (200)
  ok    course list (200)
  ok    login is required (401)
SMOKE PASSED
(the same five checks through the public door)
SMOKE PASSED
DEPLOY OK: 9d51324 live on blue (previous: none )
```

(The commit tag `9d51324` is just the example.) Release 2 (a small honest change) with a visitor who never stops (`hammer.sh http://localhost:8703 170 log`): `requests=2261 failures=0`, and the versions in the visitor log switch with no gap (`1387` answers from the old tag, then `874` from the new one).

**A trap to meet in the rehearsal, not in production.** Release 3 adds a column `phone` that may not be empty, with no default for the old rows. The tests run on an empty database, so every check is green. In the deploy job the migration reaches the real database, which already has students, and stops (captured):

```
psycopg.errors.NotNullViolation: column "phone" of relation "students" contains null values
[SQL: ALTER TABLE students ADD COLUMN phone VARCHAR(20) NOT NULL]
ABORT: migration failed - visitors still get green, untouched
active=green blue= green=fa6ce83
```

The job is red and the visitors saw nothing. Release 4 fixes the migration with a default for old rows and goes live.

### 5. Failures and rollback (captured from the rehearsal)

Release 5 adds a route `/popular` that no test and no smoke test calls, and which reads a column that does not exist. It passes every check and goes live: `curl -w ' -> %{http_code}\n' localhost:8703/popular` gives `Internal Server Error -> 500`. Not every bug is caught before the switch, so we go back:

```bash
bash /opt/allcs/deploy.sh rollback      # on the server (here: docker exec m19b13-server bash /opt/allcs/deploy.sh rollback)
```

```
ROLLBACK: green (bde1b1c) -> blue (63e656b)
... smoke test ... SMOKE PASSED
(the last lines of the broken container's log, ending with:)
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) column "popularity" does not exist
ROLLBACK DONE: serving 63e656b from blue
```

The rollback switches to the other colour, which is still running, and prints the log of the broken one so you can see the reason. Afterwards `/popular` answers `404` (the route no longer exists) and `deploy.sh status` shows only the old colour. The visitor never stopped (`requests=2212 failures=0`; versions `1361` old, `5` broken, `846` old again):

```
active=blue blue=63e656b green=
NAMES              IMAGE                         STATUS
allcs-api-blue-1   registry:5000/allcs:63e656b   Up 2 minutes (healthy)
allcs-postgres-1   postgres:17.11                Up 8 minutes (healthy)
allcs-redis-1      redis:8                       Up 8 minutes
allcs-caddy-1      caddy:2                       Up 8 minutes
```

(The video's capture shows `postgres:17`; this repo pins `postgres:17.11`.)

### 6. The real cloud (captured, optional)

All of it ran from CloudShell (a terminal inside the AWS web page) with the AWS command line, in a playground account: one `t3.small` (2 vCPU, 2 GiB, `CpuCredits=standard`), one 20 GB `gp3` disk, one region (`us-east-1`). The order of the steps, with the key commands:

1. Which account am I in, and is it empty? `aws sts get-caller-identity` and `aws ec2 describe-instances --filters Name=instance-state-name,Values=pending,running,stopping,stopped`.
2. A repository for the images: `aws ecr create-repository --repository-name allcs --image-scanning-configuration scanOnPush=true`.
3. Build for the server's architecture and push: `aws ecr get-login-password | docker login --username AWS --password-stdin $REG`, `docker build --platform linux/amd64 -t $REG/allcs:v1 --build-arg APP_VERSION=v1 .`, `docker push $REG/allcs:v1` (the image was 287 MB).
4. A firewall (a security group) that opens port 80 to everybody, a role that lets the server pull from ECR with no password stored on it, and one `aws ec2 run-instances` with a boot script (user-data) that installs Docker and Compose, copies `deploy/`, and runs `install_app.sh $REG v1`.
5. Wait for the first deploy, then check from outside with `curl http://<ip>/version`, `/health/ready` and `/courses`, and log in as the seeded admin.
6. Release v2 with a visitor loop running: 1586 requests, 0 failures (280 from v1, then 1306 from v2, no gap). A deliberately broken tag (`bad`): `FAIL  course list: wanted 200 with "items", got 500`, `SMOKE FAILED`, `ABORT: smoke test failed on the new version - visitors still get green, untouched`, exit code 1. A bug the smoke test cannot see (v3, `/popular -> 500`), then `deploy.sh rollback`: `ROLLBACK DONE: serving v2 from ...`, `/popular -> 404`.
7. Clean-up, in the same session, in order: terminate the instance; delete the instance profile, detach and delete the role; delete the security group; delete the repository (`--force`); then check that the counts are zero (instances, repositories, role, security groups, volumes).

Two honest things that happened in the real session:

- **The first boot failed.** The archive made on a Mac contained 47 extra files whose names start with `._` (macOS adds them to archives). Alembic tried to load `migrations/versions/._*.py` and crashed with `source code string cannot contain null bytes`. `deploy.sh` did the right thing: `ABORT: migration failed - visitors still get nothing, untouched`. The fix: delete those files, build and push the image again, deploy again. Lesson: ship only what you mean to ship (a clean archive, and a `.dockerignore` next to the `Dockerfile`).
- **SSM Run Command was blocked** in that playground, so the AWS deploys ran over SSH (`ssh ec2-user@IP sudo bash /opt/allcs/deploy.sh <action>`), with port 22 open to one single address (a `/32` rule) and EC2 Instance Connect keys that live for a minute. SSM (no open port) is the better choice where the account allows it.

The same deploy script and the same smoke test ran in a container on the laptop and on a computer in Virginia. Only three things changed: the registry address, the server, and one setting, `MODE`.

## Common mistakes

- A migration that is safe for the new version only (a `NOT NULL` column with no default). The old colour keeps running during a release and is your rollback target: add the column with a default and ship it, use it in the next release, remove the old one in a later release.
- SSH open to the whole world: it is attacked within minutes. Open port 22 to one address, use short-lived keys, or use SSM.
- Deploying `latest`. Deploy exact tags (version or commit), so `status` always says what runs and a rollback knows where to go.
- A smoke test that only checks `/health`. Add a real request (here: the course list) so a broken release is stopped before the switch.
- Shipping junk files (`._*`, `.env`, caches) into the image. Keep a `.dockerignore`.
- Leaving cloud resources running. List what you created, delete in order, and check that every count is zero.

## Clean up

Local (if you ran steps 3 and 4):

```bash
docker rm -f -v pyrepo-m19-b13-app pyrepo-m19-b13-pg pyrepo-m19-b13-redis
docker rmi m19b13-allcs:abc1234
rm -rf allcs/.venv allcs/.coverage allcs/.pytest_cache allcs/.ruff_cache
# rehearsal only:
docker rm -f m19b13-registry m19b13-server
docker volume rm m19b13-dind
docker network rm m19b13-net
```

On AWS (only if you did step 6): terminate the instance and delete the instance profile, the role, the security group and the repository, then check that the counts are zero.

## Next

[M20-L01 · Health Checks, Metrics and Dashboards](../../m20-observability-and-performance/m20-l01-health-checks-metrics-and-dashboards/README.md)
