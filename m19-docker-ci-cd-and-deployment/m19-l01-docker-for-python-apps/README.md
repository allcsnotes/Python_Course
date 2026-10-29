# M19-L01 · Docker for Python Apps

> Video: Module 19, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What an image, a container, a Dockerfile and a registry are, with the real commands (`docker run`, `ps`, `logs`, `exec`, `stop`, `rm`)
- How to write a small, safe Dockerfile: a naive one first (huge, holds a secret, runs as root), then a two-stage one (small, no secret, normal user)
- Layers and the build cache: why you copy the package list first and your code last
- Why `localhost` inside a container is not your laptop
- Docker Compose: one `compose.yaml` that starts the database, Redis, the mail catcher, the migration, the API and the worker, in order, with health checks
- Volumes: `docker compose down` keeps your data, `down -v` deletes it

## Before you start

- Python 3.14 or newer is NOT needed on the host for the Docker parts. Docker (Docker Desktop or Docker Engine, with `docker compose`) must be running. Check with `docker --version`.
- This lesson packs the enrollment email worker from M18-B12. The folder `allcs/` already holds that project plus the Dockerfiles and `compose.yaml`.
- Images used (pinned): `python:3.14` and `python:3.14-slim`, `redis:8`, `postgres:17.11`, `axllent/mailpit:v1.32.0`, `ghcr.io/astral-sh/uv:0.13`. The first build downloads them.
- All passwords and keys are demo values (`demo-secret-not-real-12345`). Ports used: 8195 (API), 19401 (Redis demo), 19501 (Postgres demo), 19511 (mail web page).

Everything below runs in the `allcs/` folder. Create the demo secret file once (it is in `.gitignore` on purpose):

```bash
cd allcs
echo "SECRET_KEY=demo-secret-not-real-12345" > .env
```

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/Dockerfile.naive` | The first Dockerfile most beginners write: one stage, `COPY . .` |
| `allcs/Dockerfile` | The better one: two stages, cache-friendly order, a normal user |
| `allcs/.dockerignore` | Keeps `.git`, `.venv`, `.env`, caches, `tests` and the Dockerfiles out of the build |
| `allcs/requirements.txt` | Made with `uv export` (only for the naive Dockerfile) |
| `allcs/compose.yaml` | The whole system: `db`, `redis`, `mail`, `migrate`, `api`, `worker` |
| `allcs/pyproject.toml`, `uv.lock` | The project and its exact locked packages |
| `allcs/app/`, `migrations/`, `alembic.ini`, `tests/`, `make_admin.py`, `get_token.py` | The backend of M18-B12 |

## Follow along

### 1. The problem: "it works on my laptop"

Priya's laptop cannot download a new Python. On such a machine, installing the project stops at once:

```bash
uv sync
```

```
error: No interpreter found for Python >=3.14 in managed installations or search path
```

(Your message may differ, it depends on your machine; the idea is that the right Python, Postgres, Redis, ports and five commands in the right order are a lot to ask. Docker packs all of it.) Python 3.14 runs fine inside a container, whatever the host has:

```bash
docker run --rm python:3.14-slim python -c "import sys; print(sys.version)"
```

```
3.14.9 (main, Oct 21 2026, 22:34:08) [GCC 14.2.0]
```

(Your patch version may be newer.)

### 2. The container life cycle, with Redis

```bash
docker run -d --name pyrepo-m19-l01-redis -p 19401:6379 redis:8
docker ps --filter name=pyrepo-m19-l01-redis --format 'table {{.Image}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}'
```

```
IMAGE     STATUS         PORTS                                           NAMES
redis:8   Up 2 seconds   0.0.0.0:19401->6379/tcp, [::]:19401->6379/tcp   pyrepo-m19-l01-redis
```

`-d` runs it in the background, `--name` names it, and `-p 19401:6379` is a door: traffic to port 19401 on your laptop goes to port 6379 inside. Look inside:

```bash
docker logs pyrepo-m19-l01-redis
docker exec pyrepo-m19-l01-redis redis-cli ping
docker exec pyrepo-m19-l01-redis redis-cli set course "Python Basics"
docker exec pyrepo-m19-l01-redis redis-cli get course
```

```
...Ready to accept connections tcp
PONG
OK
Python Basics
```

Stop it. Is it gone?

```bash
docker stop pyrepo-m19-l01-redis
docker ps -a --filter name=pyrepo-m19-l01-redis --format 'table {{.Image}}\t{{.Status}}\t{{.Names}}'
```

```
IMAGE     STATUS                    NAMES
redis:8   Exited (0) 1 second ago   pyrepo-m19-l01-redis
```

Not gone: `stop` only ends the program. `docker rm pyrepo-m19-l01-redis` removes the container for good (and with it, any data not stored in a volume).

### 3. The naive Dockerfile: three problems

`Dockerfile.naive`:

```dockerfile
FROM python:3.14
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

For this demo only, move `.dockerignore` out of the way (the video builds the naive image before that file exists), then build:

```bash
mv .dockerignore .dockerignore.off
docker build -t m19l01-naive -f Dockerfile.naive .
docker images m19l01-naive
```

```
REPOSITORY     TAG       SIZE
m19l01-naive   latest    1.96GB
```

(`-t` names the image, `-f` names the file, the `.` is the folder to copy from. The first build takes a minute or two, the time depends on your network and machine.) Nearly 2 GB for a small server. Now look inside:

```bash
docker run --rm m19l01-naive whoami
docker run --rm m19l01-naive cat .env
docker run --rm m19l01-naive ls -A
```

```
root
SECRET_KEY=demo-secret-not-real-12345
.dockerignore.off .env .gitignore Dockerfile Dockerfile.naive alembic.ini app compose.yaml get_token.py migrations pyproject.toml requirements.txt tests uv.lock ...
```

The three problems: it is huge; it holds the secret (`COPY . .` does not read `.gitignore`, it copied everything, and images get shared); and it runs as `root`. Put the file back: `mv .dockerignore.off .dockerignore`.

### 4. Layers: build in the right order

Each line of a Dockerfile makes a layer. Docker reuses a layer if its line and everything above it did not change. In the naive file `COPY . .` comes before `pip install`, so a one-comment change in your code reinstalls every package (about a minute). The fix is the order: copy only the package list, install, and copy your code last.

### 5. The better Dockerfile

`Dockerfile`:

```dockerfile
FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

FROM python:3.14-slim
RUN useradd --create-home app
WORKDIR /app
COPY --from=build /app/.venv .venv
COPY app app
COPY migrations migrations
COPY alembic.ini .
ENV PATH="/app/.venv/bin:$PATH"
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

Stage one (the workshop) installs the packages with uv from the lock file. Stage two (the shop window) starts from a clean slim Python, creates a normal user `app`, copies only the finished virtual environment and the named folders, and runs as `app`. The `.dockerignore` keeps `.git`, `.venv`, `.env`, caches, `tests` and `Dockerfile*` out of the build. Build and compare:

```bash
docker build -t m19l01-api .
docker images
docker run --rm m19l01-api whoami
docker run --rm m19l01-api cat .env
docker run --rm m19l01-api ls -A
docker run --rm m19l01-api sh -c "env | grep -c SECRET"
```

```
REPOSITORY     TAG       SIZE
m19l01-api     latest    450MB
m19l01-naive   latest    1.96GB
app
cat: .env: No such file or directory
.venv alembic.ini app migrations
0
```

More than four times smaller, a normal user, no secret. Change one line of code (a comment) and build again: the package layers say `CACHED` and the rebuild takes about a second instead of a minute (times depend on your machine).

### 6. Running the image: secrets arrive at start, and `localhost` is a trap

```bash
docker run --rm -p 8195:8000 m19l01-api
```

```
  File "/app/app/tokens.py", line 6, in <module>
    SECRET = os.environ["SECRET_KEY"]
...
KeyError: 'SECRET_KEY'
```

The image holds no secret, on purpose: it must arrive when the container starts, with `-e`. Start a Postgres, then the API with the secret and a database address pointing at `localhost`:

```bash
docker run -d --name pyrepo-m19-l01-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 19501:5432 postgres:17.11
docker exec pyrepo-m19-l01-pg pg_isready -U allcs
docker run -d --name pyrepo-m19-l01-lonely -p 8195:8000 -e SECRET_KEY=demo-secret-not-real-12345 -e DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:19501/allcs m19l01-api
curl -s -o /dev/null -w "docs %{http_code}\n" localhost:8195/docs
curl -s -o /dev/null -w "courses %{http_code}\n" localhost:8195/courses
docker logs pyrepo-m19-l01-lonely 2>&1 | tail -1
```

```
/var/run/postgresql:5432 - accepting connections
docs 200
courses 500
...OperationalError: connection failed: connection to server at "127.0.0.1", port 19501 failed: Connection refused
```

Postgres is right there, but inside a container `localhost` means the container itself. Containers need a network and names. Clean these two up: `docker rm -f -v pyrepo-m19-l01-lonely pyrepo-m19-l01-pg`. That is exactly the job of Compose.

### 7. Docker Compose: the whole system

Read `compose.yaml`. A shared block `x-app` (build from this folder, image `m19l01-api`, settings) is reused by `migrate`, `api` and `worker`. The database address uses the service name: `db`, port `5432`, not `localhost`. Postgres keeps its files in the named volume `dbdata`, and health checks (`pg_isready`, `redis-cli ping`) tell Compose when a service is ready. `migrate` runs `alembic upgrade head` once, when the database is healthy; `api` waits for `migrate` to finish successfully and for Redis to be healthy; `worker` runs `celery -A app.worker worker --loglevel=info`.

```bash
docker compose config --services
docker compose up -d
docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"
```

```
mail
db
migrate
redis
worker
api
 Container m19l01-api-1 Started
SERVICE   STATUS                    PORTS
api       Up 12 seconds             0.0.0.0:8195->8000/tcp, [::]:8195->8000/tcp
db        Up 15 seconds (healthy)   5432/tcp
mail      Up 15 seconds (healthy)   0.0.0.0:19511->8025/tcp, [::]:19511->8025/tcp
redis     Up 15 seconds (healthy)   6379/tcp
worker    Up 12 seconds             8000/tcp
```

(The order of the service names and the seconds differ.) Five things that used to be started by hand, started by one command, in the right order. The logs tell the story:

```bash
docker compose logs migrate
docker compose logs api
docker compose logs worker
```

```
migrate-1  | INFO  [alembic.runtime.migration] Running upgrade  -> cb9aa85a3921, courses and lessons
migrate-1  | INFO  [alembic.runtime.migration] Running upgrade cb9aa85a3921 -> 6d1d3956ce21, students and enrollments
migrate-1  | INFO  [alembic.runtime.migration] Running upgrade 6d1d3956ce21 -> f149f9b699de, passwords roles owners
migrate-1  | INFO  [alembic.runtime.migration] Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens
api-1  | INFO:     Application startup complete.
worker-1  | [...: INFO/MainProcess] celery@... ready.
```

### 8. Use it

Asha signs up and is promoted to admin with one line of SQL inside the database container; she creates Meera the instructor; Meera creates a course; Lukas signs up and enrolls:

```bash
curl -s --json '{"name": "Asha", "email": "asha@example.com", "password": "asha-demo-pw"}' localhost:8195/students
docker compose exec db psql -U allcs -c "update students set role = 'admin' where email = 'asha@example.com'"
```

```
{"name":"Asha","email":"asha@example.com","id":1,"role":"student","courses":[]}
UPDATE 1
```

Log in as Asha (`curl -s -d "username=asha@example.com&password=asha-demo-pw" localhost:8195/auth/login` returns an `access_token`; put it in `ASHA`), then:

```bash
curl -s -H "Authorization: Bearer $ASHA" --json '{"name": "Meera", "email": "meera@example.com", "password": "meera-demo-pw", "role": "instructor"}' localhost:8195/admin/students
curl -s -H "Authorization: Bearer $MEERA" --json '{"title": "Python Basics", "price": 499}' localhost:8195/courses
curl -s --json '{"name": "Lukas", "email": "lukas@example.com", "password": "lukas-demo-pw"}' localhost:8195/students
curl -s -X POST -H "Authorization: Bearer $LUKAS" localhost:8195/courses/1/enrollments
```

(Log in as Meera and Lukas the same way to get `MEERA` and `LUKAS`.)

```
{"name":"Meera","email":"meera@example.com","id":2,"role":"instructor","courses":[]}
{"title":"Python Basics","price":499,"level":"beginner","id":1,"owner_id":2,"lessons":[]}
{"name":"Lukas","email":"lukas@example.com","id":3,"role":"student","courses":[]}
{"student_id":3,"course_id":1,"enrolled_on":"2026-10-29"}
```

(`enrolled_on` is today's date.) The enroll call answers at once. The worker logs `Task app.worker.send_welcome_email[...] received`, `welcome email sent to lukas@example.com` and `succeeded`, and the mail catcher has the message (open `http://localhost:19511`, or):

```bash
curl -s localhost:19511/api/v1/messages | python3 -c "import sys,json;d=json.load(sys.stdin);print('messages:',d['total']);[print('To:',m['To'][0]['Address'],'Subject:',m['Subject']) for m in d['messages']]"
```

```
messages: 1
To: lukas@example.com Subject: Welcome to Python Basics
```

### 9. Data: `down` keeps it, `down -v` deletes it

```bash
docker compose down
docker volume ls --format '{{.Name}}'
docker compose up -d
sleep 8
curl -s localhost:8195/courses
```

```
m19l01_dbdata
{"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1,"owner_id":2,"lessons":[]}],"total":1,"limit":10,"offset":0}
```

The containers were thrown away but the volume stayed, so the new database container found its files again: one course. Now the dangerous flag (this `-v` is not the one from `docker run`: here it means "remove the volumes too"):

```bash
docker compose down -v
docker compose up -d
sleep 10
curl -s localhost:8195/courses
```

```
{"items":[],"total":0,"limit":10,"offset":0}
```

Everything is gone: use `down -v` only when you want a fresh start.

## Common mistakes

- Using `localhost` in a container to reach another container. Use the service name (`db`, `redis`).
- Putting secrets in the image or in the Dockerfile. Pass them at start (`-e`, `environment:`, later: a settings class, next lesson). Keep `.env` in `.dockerignore`.
- `COPY . .` before `pip install`: every code change reinstalls all packages.
- Running as root in the container. Add a user and `USER app`.
- Using the tag `latest`. Pin the version (`python:3.14-slim`, `postgres:17.11`).
- Running more than one job in a container. One job per container: the API and the worker are separate services from the same image.
- `docker compose down -v` when you wanted to keep the data.

## Clean up

```bash
docker compose down -v --remove-orphans
docker rmi m19l01-naive m19l01-api
rm -f .env
```

## Next

[M19-L02 · Configuration the 12-Factor Way](../m19-l02-configuration-the-12-factor-way/README.md)
