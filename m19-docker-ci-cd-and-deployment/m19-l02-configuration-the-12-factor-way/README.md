# M19-L02 · Configuration the 12-Factor Way

> Video: Module 19, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What configuration is (whatever differs from one place to another), and why it must live outside the code and outside the image
- One `Settings` class (`pydantic-settings`) that reads, converts and checks every value when the program starts, and fails fast with all problems named
- The order of power: real environment variables beat the `.env` file, which beats secret files, which beat the default
- Why secrets must never be in an image (not in `ENV`, not even "copied and deleted"), and how to pass them as files in `/run/secrets`
- Feature flags (`SIGNUP_OPEN`), logs to stdout, and three pitfalls (a switch that is never off, a secret with a default, a secret in a log)

## Before you start

- Python 3.14 or newer on the host for the small scripts and tests (`python --version`), and Docker with `docker compose` running.
- This lesson continues the project from M19-L01. The folder `allcs/` is that project with the new `app/settings.py`, the env files and the compose secrets.
- Containers use the ports 19502 (Postgres), 19402 (Redis), 8192, 9192 and 9292. All keys, passwords and values here are fake demo values.
- On Linux, `host.docker.internal` (used by the env files) may need `--add-host=host.docker.internal:host-gateway` on each `docker run`.

Start Postgres and Redis on your laptop (the boxes in this lesson reach them through `host.docker.internal`), create the databases and install the packages:

```bash
docker run -d --name pyrepo-m19-l02-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 19502:5432 postgres:17.11
docker run -d --name pyrepo-m19-l02-redis -p 19402:6379 redis:8
docker exec pyrepo-m19-l02-pg psql -U allcs -c "create database allcs_prod"
docker exec pyrepo-m19-l02-pg psql -U allcs -c "create database allcs_test"

cd allcs
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install celery==5.6.3 redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 pydantic-settings==2.16.1 httpx==0.28.1 pytest==9.1.1
export SECRET_KEY=demo-only-not-a-real-secret-4f2a REDIS_URL=redis://localhost:19402/1
for db in allcs allcs_prod; do DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:19502/$db alembic upgrade head; done
unset SECRET_KEY REDIS_URL
```

(Each `alembic upgrade head` prints the migrations it runs, the last line is `Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens`. The video uses `uv run`.)

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/app/settings.py` | The `Settings` class: required `database_url`, `redis_url`, `secret_key` (`SecretStr`, 16+ characters), defaults, a prod validator, `get_settings()` with `lru_cache` |
| `allcs/app/tokens.py`, `db.py`, `worker.py`, `mailer.py`, `main.py`, `routers/students.py` | Now read their values from `get_settings()` instead of `os.environ` (and `/about`, the sign-up switch, log lines) |
| `allcs/tests/test_settings.py` | Five tests for the settings rules |
| `allcs/env/dev.env`, `prod.env`, `zero.env`, `compose.env` | Environment files (fake values) for the dev box, the prod box, the "zero seconds" demo and compose |
| `allcs/.env.example` | The template you commit; copy it to `.env` for local work (never commit `.env`) |
| `allcs/Dockerfile` | The two-stage image from L01 (image tag `m19l02-api:v1`) |
| `allcs/Dockerfile.leaky`, `Dockerfile.leaky2`, `secret.env` | Two WRONG ways to put a secret in an image (a demo with a made-up key) |
| `allcs/compose.yaml`, `allcs/secrets/` | The new compose file: secret files mounted at `/run/secrets` (the files hold fake demo values) |
| `allcs/showcfg.py`, `booltrap.py`, `me.py`, `priya.json`, `lukas.json` | Small demo scripts and request bodies |
| `variants/v0/app/` | The six app files as they were BEFORE this lesson (`os.environ` all over), for the first demo |

## Follow along

### 1. The hook: a setting nobody checks

Build the "before" image from a scratch copy (the old app files, without `settings.py`), run it with `env/zero.env` (it sets `ACCESS_SECONDS=0`, like Priya did), sign Priya up and look at her profile:

```bash
cd ..
cp -r allcs /tmp/allcs_v0
cp -r variants/v0/app/* /tmp/allcs_v0/app/
rm /tmp/allcs_v0/app/settings.py
(cd /tmp/allcs_v0 && docker build -q -t m19l02-api:v0 .)
cd allcs
docker run -d --name pyrepo-m19-l02-v0 --env-file env/zero.env -p 8192:8000 m19l02-api:v0
curl -si localhost:8192/students --json @priya.json | sed -n 1p
python me.py
```

```
HTTP/1.1 201 Created
login: 200
me: 401 {'error': {'code': 'not_authenticated', 'message': 'Token expired'}}
```

Login works, but the token dies the moment it is born: zero seconds is not "no limit", and nothing complained when the box started. Now search the old code for the environment:

```bash
docker rm -f -v pyrepo-m19-l02-v0
(cd ../variants/v0 && grep -rn environ app)
```

```
app/db.py:9:URL = os.environ.get(
app/tokens.py:6:SECRET = os.environ["SECRET_KEY"]
app/tokens.py:8:ACCESS_SECONDS = int(os.environ.get("ACCESS_SECONDS", "900"))
app/worker.py:10:BROKER = os.environ.get(
app/mailer.py:5:SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
app/mailer.py:6:SMTP_PORT = int(os.environ.get("SMTP_PORT", "18625"))
```

Six lines, four files, each with its own default, nothing checked.

### 2. One image, two environments

Build the image once and start two boxes from it, one per env file:

```bash
docker build -q -t m19l02-api:v1 .
cat env/dev.env env/prod.env
docker run -d --name pyrepo-m19-l02-dev --env-file env/dev.env -p 8192:8000 m19l02-api:v1
docker run -d --name pyrepo-m19-l02-prod --env-file env/prod.env -p 9192:8000 m19l02-api:v1
curl -s localhost:8192/about; echo
curl -s localhost:9192/about; echo
docker ps --filter name=pyrepo-m19-l02-dev --filter name=pyrepo-m19-l02-prod --format '{{.Names}}  {{.Image}}'
```

```
{"environment":"dev","database":"host.docker.internal/allcs","signup_open":true,"log_level":"DEBUG"}
{"environment":"prod","database":"host.docker.internal/allcs_prod","signup_open":false,"log_level":"INFO"}
pyrepo-m19-l02-dev  m19l02-api:v1
pyrepo-m19-l02-prod  m19l02-api:v1
```

(`/about` shows the settings that are safe to show: never secrets. `docker ps` lists the boxes in the order Docker likes.) Both boxes come from one image: nobody rebuilt anything for prod. That is factor five of the 12-factor app: the image is built once, the environment decides.

### 3. The Settings class fails fast

Read `app/settings.py`. `secret_key` has no default, so it is required. `access_seconds` must be above zero. `signup_open` is a `bool`. `model_config` also reads a `.env` file and secret files from `/run/secrets` if that folder exists. A validator forbids `prod` with `DEBUG` logs. Start the image with nothing at all (the last lines of the output are shown):

```bash
docker run --rm m19l02-api:v1 2>&1 | tail -12
```

```
pydantic_core._pydantic_core.ValidationError: 3 validation errors for Settings
database_url
  Field required [type=missing, input_value={}, input_type=dict]
...
redis_url
  Field required [type=missing, input_value={}, input_type=dict]
...
secret_key
  Field required [type=missing, input_value={}, input_type=dict]
...
```

Three problems at once, each by name, and the program stops before it serves anything (exit code 1). Now wrong values (the dev file, but with a bad environment name, a short key and zero seconds):

```bash
docker run --rm --env-file env/dev.env -e ENVIRONMENT=production -e SECRET_KEY=short -e ACCESS_SECONDS=0 m19l02-api:v1 2>&1 | tail -11
docker run --rm --env-file env/prod.env -e LOG_LEVEL=DEBUG m19l02-api:v1 2>&1 | tail -3
```

```
pydantic_core._pydantic_core.ValidationError: 3 validation errors for Settings
environment
  Input should be 'dev', 'test' or 'prod' [type=literal_error, input_value='production', input_type=str]
...
secret_key
  Value should have at least 16 items after validation, not 5 [type=too_short, input_value='short', input_type=str]
...
access_seconds
  Input should be greater than 0 [type=greater_than, input_value='0', input_type=str]
...
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
  Value error, prod must not log at DEBUG [type=value_error, input_value={'environment': 'prod', ...}, input_type=dict]
```

A wrong setting stops the box at the start, where a person is watching, not later at midnight. Five small tests keep the rules alive (they build `Settings(_env_file=None, ...)` so a file on someone's laptop cannot change the result):

```bash
pytest -q tests/test_settings.py
pytest -q
```

```
.....                                                                    [100%]
5 passed in 0.07s
......................................                                   [100%]
38 passed in 3.43s
```

(The times differ. The full suite needs the `allcs_test` database from the setup.)

### 4. The `.env` file for your laptop, and who wins

For local work, a file named `.env` holds one `NAME=value` per line. It is in `.gitignore` and `.dockerignore`. Commit `.env.example` (placeholder values) instead. Create a `.env` with a 60 second login:

```bash
printf 'DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:19502/allcs\nREDIS_URL=redis://localhost:19402/0\nSECRET_KEY=local-dev-secret-key-1234\nACCESS_SECONDS=60\n' > .env
python showcfg.py
ACCESS_SECONDS=300 python showcfg.py
rm .env
```

```
access_seconds = 60
secret_key     = **********
access_seconds = 300
secret_key     = **********
```

A real environment variable beats the `.env` file. The order, strongest to weakest: values passed in code, real environment variables, the `.env` file, secret files, the default in the class. The secret prints as stars because it is a `SecretStr`.

### 5. Secrets never go in the image

Wrong way 1: `ENV SECRET_KEY=...` in the Dockerfile (`Dockerfile.leaky`). Wrong way 2: copy the file and delete it in the next step (`Dockerfile.leaky2`).

```bash
docker build -q -f Dockerfile.leaky -t m19l02-api:leaky .
docker history --no-trunc --format "{{.CreatedBy}}" m19l02-api:leaky | grep SECRET
docker run --rm m19l02-api:leaky env | grep SECRET
docker build -q -f Dockerfile.leaky2 -t m19l02-api:leaky2 .
docker history --no-trunc --format "{{.CreatedBy}}" m19l02-api:leaky2 | grep secret
docker history --no-trunc --format "{{.CreatedBy}}" m19l02-api:v1 | grep -c SECRET
```

```
ENV SECRET_KEY=demo-baked-in-secret-key-1357
SECRET_KEY=demo-baked-in-secret-key-1357
RUN /bin/sh -c rm /tmp/secret.env # buildkit
COPY --chown=app:app secret.env /tmp/secret.env # buildkit
0
```

(The `sha256:` ids that `docker build -q` prints are left out.) The secret is in the history in plain text, and the deleted file's `COPY` step is still in the history. Anyone who can pull the image has the secret. The real image has no secret in its history (`0`). Remove the demo images: `docker rmi m19l02-api:leaky m19l02-api:leaky2`.

A running box is better but not perfect: `docker inspect` lists its environment for anyone who can talk to Docker on that machine:

```bash
docker inspect pyrepo-m19-l02-dev --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -E "SECRET|DATABASE"
```

```
DATABASE_URL=postgresql+psycopg://allcs:allcs@host.docker.internal:19502/allcs
SECRET_KEY=dev-only-not-a-real-secret-1234
```

### 6. Secrets as files with Compose

`compose.yaml` mounts the secret files into every service that asks for them. The shared block says: use this image, take plain values from `env/compose.env`, and receive the secrets `database_url` and `secret_key`. The Postgres image reads its password from a file too (`POSTGRES_PASSWORD_FILE`). At the bottom each secret names its file on the host, in `secrets/` (fake demo values here; real ones are never committed, and in production the platform creates them). Our `Settings` class already knows what to do: `secrets_dir` points to `/run/secrets` and each file name is a setting name.

```bash
docker compose up -d
sleep 14
docker compose ps --format "table {{.Service}}\t{{.Status}}"
curl -s localhost:9292/about; echo
docker inspect m19l02c-api-1 --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -E "SECRET|DATABASE" || echo none
docker compose exec api ls /run/secrets
docker compose down -v --remove-orphans
```

```
SERVICE   STATUS
api       Up 14 seconds
db        Up 17 seconds (healthy)
redis     Up 17 seconds
{"environment":"prod","database":"db/allcs","signup_open":true,"log_level":"INFO"}
none
database_url
secret_key
```

The secrets are not in the environment (`none`): they are files that exist only inside this box.

### 7. A feature flag

`SIGNUP_OPEN` is a switch that turns a feature on or off without a new image. The sign-up route checks it in two lines. Prod has it `false` (reset the data of the dev and prod databases first if you ran the earlier demos: `docker exec pyrepo-m19-l02-pg psql -U allcs -d allcs -c "TRUNCATE students RESTART IDENTITY CASCADE"`, and the same for `allcs_prod`):

```bash
curl -si localhost:9192/students --json @lukas.json | sed -n '1p;$p'
curl -si localhost:8192/students --json @lukas.json | sed -n '1p;$p'
```

```
HTTP/1.1 403 Forbidden
{"error":{"code":"forbidden","message":"Sign-ups are closed"}}
HTTP/1.1 201 Created
{"name":"Lukas","email":"lukas@example.com","id":1,"role":"student","courses":[]}
```

(The user id is 1 or 2 depending on earlier demos.) To open the doors in prod, nobody edits code or builds an image: restart the box with the switch set to true:

```bash
docker rm -f -v pyrepo-m19-l02-prod
docker run -d --name pyrepo-m19-l02-prod --env-file env/prod.env -e SIGNUP_OPEN=true -p 9192:8000 m19l02-api:v1
sleep 4
curl -si localhost:9192/students --json @lukas.json | sed -n '1p;$p'
```

```
HTTP/1.1 201 Created
{"name":"Lukas","email":"lukas@example.com",...}
```

(The settings are read once at start, so a restart is needed.) Logs go to stdout; the platform collects them. The dev box (DEBUG) shows a debug line with the student's email, the prod box (INFO) does not:

```bash
docker logs --tail 4 pyrepo-m19-l02-dev
docker logs --tail 3 pyrepo-m19-l02-prod
```

```
DEBUG allcs: sign-up request for lukas@example.com
INFO:     192.168.65.1:42373 - "POST /students HTTP/1.1" 201 Created
...
INFO:     192.168.65.1:54601 - "POST /students HTTP/1.1" 403 Forbidden
```

(Addresses and ports differ.) That is why the validator forbids DEBUG in prod: debug lines can hold personal data.

### 8. Pitfall: a switch that is never off

```bash
python booltrap.py
```

```
plain: True
Settings: False
```

The text `false` is not empty, so plain `bool("false")` is `True`. `Settings` understands `false`, `no`, `off` and `0`.

## Common mistakes

- Reading `os.environ` in many files, each with its own default: nothing is checked and a typo hides.
- Giving a secret a default value in the class: a forgotten variable in production would not fail, it would start with a key everyone can read on GitHub. Required, no default.
- Writing a secret into a Dockerfile (`ENV`) or copying and deleting it: the image history keeps it.
- Committing `.env`. Commit `.env.example` with placeholders.
- Printing a secret or logging a whole settings object. `SecretStr` prints as stars; call `get_secret_value()` in one place only.
- Using `bool(os.environ[...])` for a flag.

## Clean up

```bash
docker rm -f -v pyrepo-m19-l02-dev pyrepo-m19-l02-prod pyrepo-m19-l02-pg pyrepo-m19-l02-redis
docker rmi m19l02-api:v1 m19l02-api:v0
rm -rf /tmp/allcs_v0 .venv .env
```

## Next

[M19-L03 · CI/CD with GitHub Actions](../m19-l03-ci-cd-with-github-actions/README.md)
