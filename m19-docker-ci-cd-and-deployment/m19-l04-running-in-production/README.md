# M19-L04 · Running in Production

> Video: Module 19, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Why a naive redeploy makes requests fail, and how to run the server like production does: gunicorn with several uvicorn workers, and a crash that heals itself
- How many workers to start, and the trap that "workers times pool size times boxes" must stay below the Postgres connection limit
- Health checks: live (is the process alive?) against ready (can it do its job?), and a Docker `HEALTHCHECK`
- A graceful shutdown (`SIGTERM`, `CMD` in list form, a long enough grace period) for a web server and for a Celery worker
- A rolling deploy behind an nginx proxy with zero failed requests
- Proxy headers (`X-Forwarded-For`): why every caller looked the same, and why you must trust only your own proxy

## Before you start

- Docker with `docker compose` running, and Python 3.14 on the host (`python --version`) with `httpx` for the small client scripts: `pip install httpx==0.28.1`.
- This lesson continues the project from M19-L02 and L03. The folder `allcs/` is the backend with a gunicorn config, health routes, a probe script and a few demo-only routes (`app/demo.py`: `/version`, `/whoami`, `/slow`, `/dbslow`, `/spin`).
- Images: `python:3.14-slim`, `ghcr.io/astral-sh/uv:0.13`, `postgres:17.11`, `redis:8`, `nginx:1.29-alpine`. The compose stack uses fixed container names `m19l04-*`, the network `m19l04-net` (subnet `172.29.194.0/24`, so nginx and the apps have fixed addresses) and the ports 8191, 8193, 8194, 19504 and 19404. If that subnet is already used on your machine, change it in `stack/compose.yml`, `stack/conf/default.conf` and the `FORWARDED_ALLOW_IPS` value in step 8.
- Timing numbers (milliseconds, how many requests fail, how long a burst takes) depend on your computer, so yours will differ. The pattern is what counts.
- All passwords and keys are demo values.

Build the image and start Postgres and Redis (everything below runs from this lesson folder):

```bash
docker build -t m19l04-allcs:1 allcs
cd stack
docker compose up -d --wait postgres redis
ENVS=(-e DATABASE_URL=postgresql+psycopg://allcs:allcs@postgres:5432/allcs -e REDIS_URL=redis://redis:6379/0 -e SECRET_KEY=demo-only-not-a-real-secret-4f2a)
docker run --rm --network m19l04-net "${ENVS[@]}" m19l04-allcs:1 alembic upgrade head
docker run --rm --network m19l04-net "${ENVS[@]}" -v $PWD/seed.py:/app/seed.py:ro m19l04-allcs:1 python seed.py
cd ..
```

(The `ENVS=(...)` line is zsh/bash array syntax; on Windows use Git Bash or WSL. `alembic upgrade head` prints the migrations, ending with `Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens`; `seed.py` prints `seeded`: Lukas, Priya, Meera and two courses, demo password `<name>-demo-pass`.)

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/Dockerfile` | The two-stage image, with a `HEALTHCHECK` (runs `python -m app.probe`) and `CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]` |
| `allcs/gunicorn.conf.py` | Workers (from `WEB_CONCURRENCY`), `UvicornWorker`, `graceful_timeout`, `max_requests`, access log, `forwarded_allow_ips` (from `FORWARDED_ALLOW_IPS`) |
| `allcs/app/health.py`, `app/probe.py` | `/health/live` and `/health/ready` (checks Postgres with `select 1` and pings Redis), and the three-line Docker probe |
| `allcs/app/demo.py` | Lesson-only routes: `/version`, `/whoami`, `/slow?seconds=N`, `/dbslow` (a 2 second `pg_sleep`), `/spin` (CPU work) |
| `allcs/app/settings.py`, `db.py` | Adds `POOL_SIZE` (default 5) and `MAX_OVERFLOW` (default 10) for the connection pool |
| `stack/compose.yml` | Postgres, Redis, two app boxes (`app1`, `app2`) and an nginx proxy, with fixed addresses |
| `stack/conf/default.conf` | The nginx config: an upstream with two servers, `proxy_next_upstream`, and the `X-Forwarded-For` line |
| `stack/roll.sh` | The rolling deploy script, one box at a time |
| `stack/seed.py` | Demo data |
| `stack/shell.Dockerfile` | An image with `CMD` in shell form (the classic mistake of step 6) |
| `files/loop.py`, `burst.py`, `login.py`, `whoami.py` | Client scripts: 200 requests in a row, a burst, a login series, and "who am I?" |

## Follow along

### 1. The hook: a naive redeploy fails requests

Start one box with version 1, run the client (200 requests, one every 0.1 second), and two seconds in, replace the box with `--force-recreate`:

```bash
cd stack
V1=1 docker compose up -d --force-recreate --wait app1
cd ..
(sleep 2; cd stack && V1=2 docker compose up -d --force-recreate app1) &
python files/loop.py http://localhost:8191 200
```

```
ok 177 failed 23 versions {'1': 20, '2': 157}
```

The numbers above are from the video; on one test run here the result was `ok 196 failed 4`. How many fail depends on your timing, but some always do: the old box is gone, and the new one is still starting, so each request waits a second and gets no answer. Clean up: `cd stack && docker compose stop app1 && docker rm -f m19l04-app1`.

### 2. Workers: one process is one cook

```bash
docker run -d --name m19l04-p1 --network m19l04-net "${ENVS[@]}" m19l04-allcs:1 uvicorn app.main:app --host 0.0.0.0
docker logs m19l04-p1
```

```
INFO:     Started server process [1]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

One process uses one core. (`uvicorn ... --workers 3` starts a parent and three servers: `Started parent process [1]` and three `Started server process [...]`.) Remove it: `docker rm -f m19l04-p1`. Gunicorn is the veteran manager: it starts the workers, replaces any that die, retires a worker after a number of requests and shuts everything down in order. Run the real image (its `CMD` is gunicorn) with four workers:

```bash
docker run -d --name m19l04-g4 --network m19l04-net -p 8191:8000 "${ENVS[@]}" -e WEB_CONCURRENCY=4 m19l04-allcs:1
sleep 4
docker logs m19l04-g4 2>&1 | grep -E "Starting|Listening|Using worker|Booting"
```

```
[2026-10-27 13:01:37 +0000] [1] [INFO] Starting gunicorn 26.2.0
[2026-10-27 13:01:37 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2026-10-27 13:01:37 +0000] [1] [INFO] Using worker: uvicorn_worker.UvicornWorker
[2026-10-27 13:01:37 +0000] [7] [INFO] Booting worker with pid: 7
[2026-10-27 13:01:37 +0000] [8] [INFO] Booting worker with pid: 8
[2026-10-27 13:01:37 +0000] [9] [INFO] Booting worker with pid: 9
[2026-10-27 13:01:38 +0000] [10] [INFO] Booting worker with pid: 10
```

(Times and pids differ.) Kill one worker on purpose with `kill -9` (the signal that cannot be ignored) and look at the log:

```bash
docker exec m19l04-g4 sh -c "kill -9 8"
sleep 2
docker logs m19l04-g4 2>&1 | grep -E "SIGKILL|Booting" | tail -2
```

```
[2026-10-27 13:01:39 +0000] [1] [ERROR] Worker (pid:8) was sent SIGKILL! Perhaps out of memory?
[2026-10-27 13:01:39 +0000] [210] [INFO] Booting worker with pid: 210
```

The manager noticed at once and started a new worker; the server never stopped. Remove the box (`docker rm -f m19l04-g4`).

### 3. How many workers?

`/spin` is CPU work, `/slow?seconds=1` only waits. Eight requests at once, with 1, 2 and 4 workers (start the box with `-e WEB_CONCURRENCY=N` as above, then):

```bash
python files/burst.py http://localhost:8191/spin 8
python files/burst.py http://localhost:8191/slow?seconds=1 8
```

The "heavy" burst of eight took (video, 10 cores): about 4.9 s with 1 worker, 3.9 s with 2 and 2.9 s with 4; on one run here, 6.7 s, 5.7 s and 4.6 s. The waiting route took about 1.1 s every time (a worker can wait for several requests at once with async code). More cores, more speed, but not perfectly even: each worker is a full copy of the app, with its own memory. Output format:

```
8 requests in 4.9 s, codes [200]
```

A starting rule: for heavy work about one worker per core the container may use; for mostly waiting work two to four. Then measure.

### 4. Connection pools multiply

Every worker has its own pool of database connections (`POOL_SIZE` 5, plus up to `MAX_OVERFLOW` 10). Postgres allows 100 connections by default. Start two boxes with four workers each and send each 120 slow database requests (`/dbslow`, a 2 second `pg_sleep`) at the same time:

```bash
docker run -d --name m19l04-x1 --network m19l04-net -p 8191:8000 "${ENVS[@]}" -e WEB_CONCURRENCY=4 m19l04-allcs:1
docker run -d --name m19l04-x2 --network m19l04-net -p 8193:8000 "${ENVS[@]}" -e WEB_CONCURRENCY=4 m19l04-allcs:1
sleep 5
python files/burst.py http://localhost:8191/dbslow 120 &
python files/burst.py http://localhost:8193/dbslow 120
wait
docker logs m19l04-x1 2>&1 | grep "too many clients" | head -1
```

```
120 requests in 6.5 s, codes [200, 500]
120 requests in 6.6 s, codes [200, 500]
psycopg.OperationalError: connection failed: connection to server at "172.29.194.2", port 5432 failed: FATAL:  sorry, too many clients already
```

(In the video, 200 requests per box: 42 failed with a 500.) Postgres ran out of connections: workers (4 + 4) times 15 connections is 120, more than 100. The fix is smaller pools: restart both boxes with `-e MAX_OVERFLOW=5`. Then 8 workers times 10 connections is 80, below 100, with room for a migration or a person with `psql`, and the same load runs with no 500s (`codes [200]`, a bit slower). Remove both boxes (`docker rm -f m19l04-x1 m19l04-x2`).

### 5. Live and ready

```bash
cd stack
V1=1 docker compose up -d --force-recreate --wait app1
cd ..
docker stop m19l04-pg
curl -s -w ' %{http_code}\n' localhost:8191/health/live
curl -s -w ' %{http_code}\n' localhost:8191/health/ready
docker start m19l04-pg
```

```
{"status":"alive"} 200
{"status":"not ready","postgres":"down","redis":"ok"} 503
```

Liveness asks "is the process alive?" (if not, restart it). Readiness asks "can it do its job right now?": it runs `select 1` on Postgres and pings Redis, and answers `503` if one fails. A proxy should send customers only to ready servers. Docker can ask the same question itself: the Dockerfile has a `HEALTHCHECK` that runs `python -m app.probe` (a slim image has no `curl`). Watch the state while you stop and start Postgres:

```bash
watch -n 1 "docker inspect -f '{{.State.Health.Status}}' m19l04-app1"      # or run the inspect command in a loop
```

```
starting   (a few seconds)
healthy
(Postgres stopped)  -> unhealthy
(Postgres started)  -> healthy
```

Docker never restarts the container: `unhealthy` is only a label (Compose's `--wait` and other tools use it). Stop the box: `cd stack && docker compose stop app1`.

### 6. Closing time: graceful shutdown

`docker stop` sends `SIGTERM` ("please finish and stop"), waits 10 seconds by default, then sends `SIGKILL`. Start a box, ask for a request that takes 4 seconds, and one second in run `docker stop`:

```bash
docker run -d --name m19l04-sh --network m19l04-net -p 8191:8000 "${ENVS[@]}" m19l04-allcs:1
sleep 4
(sleep 1; time docker stop m19l04-sh) &
curl -sS -w ' <- %{http_code} after %{time_total}s\n' 'localhost:8191/slow?seconds=4'
wait
docker inspect -f '{{.State.ExitCode}}' m19l04-sh
docker rm m19l04-sh
```

```
{"slept":4.0,"pid":8} <- 200 after 4.023231s
0
```

The client still gets its answer (`200`, after 4 seconds), the log shows `Handling signal: term` while the request was still running, the stop took about 3.4 seconds and the exit code is 0. Now the rude way, `docker kill` (SIGKILL at once):

```
 <- 000 after 1.019181scurl: (52) Empty reply from server
```

The customer's request was cut in half (exit code 137). If it was a payment, nobody knows what happened. A classic mistake: a `CMD` written as plain text (shell form) runs through a shell, and the shell becomes process 1 and does not pass `SIGTERM` on. Docker waits the full 10 seconds, then kills. Try it with `stack/shell.Dockerfile`:

```bash
docker build -t m19l04-allcs:shell -f stack/shell.Dockerfile stack
docker run -d --name m19l04-sh --network m19l04-net -p 8191:8000 "${ENVS[@]}" m19l04-allcs:shell
# same request and docker stop as above: the request is answered, but docker stop takes about 10 seconds and the exit code is 137
```

Use the list form: `CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]`. Remove the box. A Celery worker does a warm shutdown on `SIGTERM`: it takes no new jobs and finishes the running one. Run one (with the longer grace period) and stop it while an 8 second job runs:

```bash
docker run -d --name m19l04-worker --network m19l04-net --stop-timeout 30 "${ENVS[@]}" m19l04-allcs:1 celery -A app.worker.celery_app worker --loglevel=info --concurrency 2
sleep 7
docker exec m19l04-worker python -c "from app.worker import slow_job; slow_job.delay(8)"
sleep 2
time docker stop m19l04-worker
docker logs m19l04-worker 2>&1 | grep -E "received|started|Warm|finished|succeeded"
docker rm m19l04-worker
```

```
worker: Warm shutdown (MainProcess)
[13:05:03 INFO/MainProcess] Task app.worker.slow_job received
[13:05:03 INFO/ForkPoolWorker-1] app.worker.slow_job: slow job started (8 s)
[13:05:11 INFO/ForkPoolWorker-1] app.worker.slow_job: slow job finished
[13:05:11 INFO/ForkPoolWorker-1] Task app.worker.slow_job succeeded in 8.035180212000341s: 'done'
```

The stop took about 8 to 9 seconds and exited with code 0: the job finished before the worker went home.

### 7. Rolling deploy behind a proxy

Run two boxes behind nginx. `stack/conf/default.conf`:

```nginx
upstream api {
    server 172.29.194.11:8000;  # app1
    server 172.29.194.12:8000;  # app2
}

server {
    listen 80;
    location / {
        proxy_pass http://api;
        proxy_connect_timeout 300ms;
        proxy_next_upstream error timeout http_502 http_503;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```

Every request goes to one of the two servers; if one refuses the connection or does not answer in 300 ms, nginx tries the other. `roll.sh` replaces one box at a time: mark it `down` in the config and reload nginx, recreate the box and wait until it is healthy, put it back, then the next box. Run the same client and the same deploy two seconds in:

```bash
cd stack
V1=1 V2=1 docker compose up -d --force-recreate --wait app1 app2 proxy
curl -s localhost:8194/version
(sleep 2; ./roll.sh 2) &
python ../files/loop.py http://localhost:8194 200
wait
curl -s localhost:8194/version
```

```
{"version":"1","pid":7}
ok 200 failed 0 versions {'1': 93, '2': 107}
{"version":"2","pid":7}
```

Zero requests failed (before: 23), and the versions switch with no gap. (The counts per version and the pids differ.) Two honest notes: for a short time both versions run together, so a database migration must work with both (add the new column first, switch the code, remove the old column later); and a new box must pass its readiness check before it gets traffic (that is what `--wait` does). `roll.sh` edits `conf/default.conf` and leaves a `default.conf.bak` file: delete it, and check that `app1` and `app2` have no `down` after a failed run.

### 8. Proxy headers: who is calling?

Behind the proxy every caller seems to have the same address: the proxy's. Two callers ask "who am I?", the attacker from the laptop and Lukas from another container:

```bash
python ../files/whoami.py http://localhost:8194
docker run --rm --network m19l04-net -v $PWD/../files:/files:ro m19l04-allcs:1 python /files/whoami.py http://m19l04-proxy
```

```
{'client': '172.29.194.10', 'x_forwarded_for': '192.168.65.1'}
{'client': '172.29.194.10', 'x_forwarded_for': '172.29.194.4'}
```

(Your laptop's address, here the Docker Desktop gateway `192.168.65.1`, differs; on Linux it is the bridge gateway.) The server sees `172.29.194.10` (the proxy) for both. The login limit of M18-L04 counts failures by address and email, so the attacker trying Lukas's email seven times locks Lukas out of his own account:

```bash
docker exec m19l04-redis redis-cli FLUSHALL
python ../files/login.py http://localhost:8194 'guess-{n}' 7
docker run --rm --network m19l04-net -v $PWD/../files:/files:ro m19l04-allcs:1 python /files/login.py http://m19l04-proxy lukas-demo-pass 1
```

```
try 1: 401
try 2: 401
try 3: 401
try 4: 401
try 5: 401
try 6: 429
try 7: 429
try 1: 429
```

Lukas, with the right password, gets `429`: to the server, they are one caller. The fix has two halves: the proxy writes the real caller into the header (that line is already in the nginx file), and the server is told which proxy to believe: gunicorn's `forwarded_allow_ips`, here from `FORWARDED_ALLOW_IPS`. Restart the boxes with the proxy's address and try again:

```bash
FORWARDED_ALLOW_IPS=172.29.194.10 docker compose up -d --force-recreate --wait app1 app2
docker exec m19l04-redis redis-cli FLUSHALL
python ../files/whoami.py http://localhost:8194
docker run --rm --network m19l04-net -v $PWD/../files:/files:ro m19l04-allcs:1 python /files/whoami.py http://m19l04-proxy
python ../files/login.py http://localhost:8194 'guess-{n}' 7
docker run --rm --network m19l04-net -v $PWD/../files:/files:ro m19l04-allcs:1 python /files/login.py http://m19l04-proxy lukas-demo-pass 1
```

```
{'client': '192.168.65.1', 'x_forwarded_for': '192.168.65.1'}
{'client': '172.29.194.4', 'x_forwarded_for': '172.29.194.4'}
try 1: 401
...
try 6: 429
try 7: 429
try 1: 200
```

Each caller shows their own address; the attacker is still blocked after five tries, and Lukas gets `200`. One warning, a big one: trust only your own proxy. With `FORWARDED_ALLOW_IPS='*'` anybody can write any address into the header. A direct request that forges `X-Forwarded-For: 1.2.3.4`:

```bash
FORWARDED_ALLOW_IPS='*' docker compose up -d --force-recreate --wait app1
curl -s -H 'X-Forwarded-For: 1.2.3.4' localhost:8191/whoami
FORWARDED_ALLOW_IPS=172.29.194.10 docker compose up -d --force-recreate --wait app1
curl -s -H 'X-Forwarded-For: 1.2.3.4' localhost:8191/whoami
```

```
{"client":"1.2.3.4","x_forwarded_for":"1.2.3.4"}
{"client":"192.168.65.1","x_forwarded_for":"1.2.3.4"}
```

With `*` the forged address is believed; with only the proxy trusted, it is ignored.

### 9. Checklist before you deploy

1. Workers times pool size times boxes stays below the database limit.
2. The proxy sends requests only to boxes that are ready, not merely alive.
3. `CMD` is in list form, so `SIGTERM` reaches the server.
4. The grace period is longer than your longest request or job.
5. Trust only your own proxy for forwarded addresses.
6. A migration works with the old and the new version at once.

## Common mistakes

- `docker compose up --force-recreate` on the only box: a gap where every request fails.
- Choosing the worker count without measuring, or forgetting that each worker has its own connection pool.
- Using the live check as the readiness check: a server whose database is down is alive but not ready.
- `CMD gunicorn ...` in shell form: `SIGTERM` is not passed on, and Docker kills the server after 10 seconds.
- A grace period shorter than the longest request.
- `forwarded_allow_ips = "*"`: anybody can fake their address.
- Running the migration in a way that the old version cannot read the new schema during a rolling deploy.

## Clean up

```bash
cd stack
docker compose down -v --remove-orphans
rm -f conf/default.conf.bak
cd ..
docker rm -f m19l04-p1 m19l04-g4 m19l04-x1 m19l04-x2 m19l04-sh m19l04-worker 2>/dev/null
docker rmi m19l04-allcs:1 m19l04-allcs:shell
```

(Check with `git diff conf/default.conf` or by eye that `stack/conf/default.conf` has no `down` word, if you ran `roll.sh`.)

## Next

[M19-B13 · Build a Deployment Pipeline](../m19-b13-build-a-deployment-pipeline/README.md)
