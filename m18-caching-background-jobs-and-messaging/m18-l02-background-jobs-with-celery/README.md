# M18-L02 · Background Jobs with Celery

> Video: Module 18, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Why a FastAPI background task loses the job when the server stops, and why slow work should leave the request
- Producer, broker and worker: a task is a normal Python function plus a message; `delay` sends it
- Running a Celery worker, and seeing jobs wait safely in Redis while the worker is off
- Retries with backoff, and why every task must be idempotent (safe to run twice)
- Scheduled jobs with `celery beat`
- Using Celery in the allcsvideos backend (202 Accepted and a job id), and how to test tasks without a queue

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- This lesson continues the backend from the previous lesson (`../m18-l01-redis-and-caching/`). The folder `allcs/` is the secure backend plus `app/worker.py` and a reports router.
- Two containers: Redis 8 on port 18402 (the broker) and Postgres 17 on port 18502. Demo passwords only. No real email is sent: the "mail service" is a `time.sleep(2)`.

```bash
docker run -d --name pyrepo-m18-l02-redis -p 18402:6379 redis:8
docker run -d --name pyrepo-m18-l02-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 18502:5432 postgres:17.11
docker exec pyrepo-m18-l02-pg psql -U allcs -c "create database allcs_test"

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install celery==5.6.3 redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 httpx==0.28.1 pytest==9.1.1
export DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:18502/allcs
export SECRET_KEY=demo-only-not-a-real-secret-4f2a
```

(The video uses `uv add celery redis`; `pip` works the same. On a machine where you run as the root user, also `export C_FORCE_ROOT=1`.)

## Files in this folder

| File | What it is |
|------|------------|
| `files/lost_app.py`, `files/lost.py` | The bad day: a FastAPI background task, and a script that kills the server half a second later |
| `files/tasks.py` | The Celery app (broker and result backend on Redis) and the task `send_welcome_email` |
| `files/send.py`, `files/three.py` | A producer that waits for one result, and one that queues three emails |
| `files/retry_tasks.py`, `files/retry_send.py` | `send_flaky`: fails twice with `ConnectionError`, with `autoretry_for` and backoff |
| `files/idem_tasks.py`, `files/idem_send.py` | The naive task (sends twice on a retry) and the safe task (`SET ... NX` mark) |
| `files/beat_tasks.py` | A schedule: `count_enrollments` every 4 seconds |
| `files/pitfall.py` | Passing an object to `delay` |
| `allcs/app/worker.py` | The Celery app and two tasks for the backend: `send_welcome_email` (with retries) and `build_report` |
| `allcs/app/routers/reports.py` | `POST /reports/enrollments` (202 Accepted, admin only) and `GET /reports/{job_id}` |
| `allcs/app/routers/enrollments.py` | One new line: `send_welcome_email.delay(...)` after the enrolment is saved |
| `allcs/jobs_demo.py` | A script that plays Lukas (enrols) and Asha (starts a report) |
| `allcs/tests/test_jobs.py` | Five tests: call the task, fake `delay`, test retries with `apply` |
| `seed.py` | Resets the database to Lukas, Priya, Asha (demo password `demo-password-1`) and two courses |

## Follow along

### 1. A background task dies with the server

```bash
cd files
python lost.py
```

```
reply: 201 {'enrolled': 'lukas@example.com'}
email lines: 0
```

The script starts the server, Lukas enrols and the reply arrives; half a second later the server is killed, like a crash or a deploy. The email (2 seconds of work) was never sent: `lost.log` has no "email sent" line. Delete `lost.log` afterwards.

### 2. The first task and a worker

The task (`tasks.py`) is a normal function with one decorator: `@celery_app.task`. Start a worker in terminal 1:

```bash
cd files
celery -A tasks worker -n worker1@allcs --loglevel=info --pool=threads --concurrency=2
```

It prints a banner (app, transport `redis://localhost:18402/0`, concurrency, the task list) and ends with `worker1@allcs ready.`. In terminal 2:

```bash
python send.py
```

```
queued: 92d5add0-08f1-48a8-b5f7-36da90078fc8
state: PENDING
answer: sent: Python Basics
state: SUCCESS
```

(The id differs for you.) `delay` returned a receipt at once; `get` waited only because this script wants to show the answer. Never call `get` inside a web endpoint. In the worker terminal:

```
Task tasks.send_welcome_email[92d5add0-...] received
tasks.send_welcome_email[92d5add0-...]: sending to lukas@example.com
Task tasks.send_welcome_email[92d5add0-...] succeeded in 2.0133857091423124s: 'sent: Python Basics'
```

(Each line starts with a time stamp.)

### 3. Jobs wait in Redis while the worker is off

Stop the worker (Ctrl+C), then:

```bash
python three.py
docker exec pyrepo-m18-l02-redis redis-cli llen celery
```

```
three tasks queued
3
```

Nobody is working, and nothing failed: the three jobs are a list called `celery` inside Redis. Start the worker again (same command as step 2). With two threads it works on two at once (Lukas, Priya), and after two seconds on Asha. Then:

```bash
docker exec pyrepo-m18-l02-redis redis-cli llen celery
```

```
0
```

A background task lives in the server's memory and dies with it. A queued job lives in Redis, so the producer and the worker can crash and restart independently.

### 4. Retries with backoff

Stop the worker and start one for `retry_tasks`:

```bash
celery -A retry_tasks worker -n worker1@allcs --loglevel=info --pool=threads --concurrency=2
```

```bash
python retry_send.py
```

```
answer: sent to lukas@example.com
took 3 seconds
```

(You may also see a harmless `ImportError: sys.meta_path is None` message when the script exits.) The first two attempts raise `ConnectionError`, and the worker log shows the backoff (`retry_backoff=1`, no jitter):

```
retry_tasks.send_flaky[...]: attempt 1 for lukas@example.com
Task retry_tasks.send_flaky[...] retry: Retry in 1s: ConnectionError('mail service is down')
retry_tasks.send_flaky[...]: attempt 2 for lukas@example.com
Task retry_tasks.send_flaky[...] retry: Retry in 2s: ConnectionError('mail service is down')
retry_tasks.send_flaky[...]: attempt 3 for lukas@example.com
Task retry_tasks.send_flaky[...] succeeded ...: 'sent to lukas@example.com'
```

The client waited 1 + 2 = 3 seconds. Retry only errors that can go away (a network failure, a time-out), never a wrong password. After `max_retries` the task is marked as failed.

### 5. Idempotent tasks

Reset Redis (`docker exec pyrepo-m18-l02-redis redis-cli flushall`), start a worker for `idem_tasks`:

```bash
celery -A idem_tasks worker -n worker1@allcs --loglevel=info --pool=threads --concurrency=2
```

```bash
python idem_send.py naive
```

```
outbox: ['lukas@example.com', 'lukas@example.com']
```

The email "left", then the connection "dropped" before Celery heard, so Celery retried and the email left again: two identical emails. The fault is in the task. Now the safe version (flush Redis first):

```bash
docker exec pyrepo-m18-l02-redis redis-cli flushall
python idem_send.py safe
```

```
outbox: ['lukas@example.com']
```

`store.set(f"sent:{email}", 1, nx=True)` only succeeds the first time (`nx` = set if not exists), so only the first run sends. Honest note: the mark is set before sending, so a crash between the two could lose an email instead of doubling it; build 12 adds the full story.

### 6. Scheduled jobs with celery beat

```bash
celery -A beat_tasks worker -n worker1@allcs --loglevel=info --pool=threads --concurrency=2
celery -A beat_tasks beat --loglevel=info          # a second terminal
```

Every 4 seconds beat logs `Scheduler: Sending due task count-every-four-seconds (beat_tasks.count_enrollments)` and the worker logs `counting enrollments` and `succeeded ... 'counted'`. Beat is only a clock that sends messages. Run only ONE beat, or every task is sent twice. Stop both and delete the `celerybeat-schedule` file it created.

### 7. In the backend

Create the tables and the demo data first:

```bash
cd ../allcs
alembic upgrade head
cd ..
python seed.py
cd allcs
```

```
INFO  [alembic.runtime.migration] Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens
courses [1, 2] students [1, 2, 3]
```

Then start the worker and the server from `allcs/`, each in its own terminal:

```bash
celery -A app.worker worker -n worker1@allcs --loglevel=info --pool=threads --concurrency=2     # terminal 1
uvicorn app.main:app --port 8182                                                                 # terminal 2
```

Then in terminal 3, from `allcs/`:

```bash
python jobs_demo.py
```

```
enrol: 201 in 0.07 seconds
report: 202
poll: /reports/b3148cf4-50ed-417e-9b2a-4fce003257d1
status: STARTED 
status: STARTED 
status: STARTED 
status: SUCCESS {'enrollments': 3}
```

The enrol reply takes a fraction of a second (yours will differ) although the email takes 2 seconds, and starting a report answers `202 Accepted` with a job id and a status address. The worker log shows `mail sent to lukas@example.com`, then `build_report ... succeeded ...: {'enrollments': 3}`. Habits: pass only plain values (an email, a number) to a task, never a database object; keep the job id as the receipt; the worker is a different program and needs the same code and settings.

### 8. Test it without a queue

```bash
pytest -v tests/test_jobs.py
pytest -q
```

```
tests/test_jobs.py::test_task_is_a_plain_function PASSED
tests/test_jobs.py::test_enrol_queues_the_email PASSED
tests/test_jobs.py::test_report_answers_202_with_a_job_id PASSED
tests/test_jobs.py::test_students_cannot_start_a_report PASSED
tests/test_jobs.py::test_retries_until_the_mail_service_works PASSED
5 passed
.............................
29 passed
```

(The tests need Postgres but no worker and no Redis queue: the first calls the task as a plain function, the second replaces `delay` with a function that records its arguments, the last runs the task with `apply`.)

### 9. Pitfall: passing an object

```bash
cd ../files
python pitfall.py 2>&1 | tail -1
```

```
kombu.exceptions.EncodeError: Object of type Student is not JSON serializable
```

It fails at once, in the producer. A task message is JSON text, so pass plain values.

## Common mistakes

- Passing an object (a model, a session) to `delay`. Pass an email, a number or an id.
- Editing a task and expecting the running worker to notice. Restart the worker after every code change.
- Calling `result.get()` inside an endpoint: the request waits again. Return the job id and let the client poll.
- Starting the worker without the same code, database address and settings as the server.
- Retrying errors that never go away, or writing tasks that are not idempotent.
- Running two `celery beat` programs.

## Clean up

```bash
docker rm -f -v pyrepo-m18-l02-redis pyrepo-m18-l02-pg
rm -rf .venv files/celerybeat-schedule* files/lost.log
```

## Next

[M18-L03 · Events and Messages](../m18-l03-events-and-messages/README.md)
