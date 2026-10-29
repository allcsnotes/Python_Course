# M18-B12 · Build an Enrollment Email Worker

> Video: Module 18, Build 12. Watch it first, then follow along here.

## What you'll build

A separate worker that sends the welcome email when a student enrolls, on top of the secure backend from build 10:

- The enroll route saves the enrollment, puts a job on a Redis queue and answers at once, even when the mail server is down
- A Celery worker sends the email over SMTP to Mailpit, a fake mail server that catches every message (nothing is sent to the real world)
- A failed send is retried three times with growing waits (1, 2, 4 seconds)
- A job that still fails goes to the dead letters (a Redis list), and an admin can list and replay them
- An idempotency key makes sure one enrollment sends one email, even if the job is delivered twice
- 9 new tests

The six rules (each one is a test): enroll answers without waiting for the mail; one enrollment sends one welcome email; a failed send is retried three times with growing waits; a job that still fails goes to the dead letters with everything needed to replay it; an admin can list and replay dead letters; the same job twice sends one email.

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- You should have done M18-L02 (Celery), M18-L03 (events, idempotency) and M17-B10 (the secure backend). This folder holds the finished project (`allcs/`).
- Three containers: Redis 8 (port 18412, holds the jobs), Mailpit (SMTP on 18625, web page on 18626) and Postgres 17 (port 18512). All values are demo values. Every email address is `@example.com`.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/app/mailer.py` | `welcome_message()` builds an `EmailMessage`, `send()` sends it with `smtplib` to Mailpit (5 second time out) |
| `allcs/app/worker.py` | The Celery app, the `EmailTask` base class (`on_failure` pushes to the dead letters), and the task `send_welcome_email` with retries and the idempotency key |
| `allcs/app/routers/enrollments.py` | The enroll route, with one new line: `send_welcome_email.delay(...)` |
| `allcs/app/routers/admin.py` | Two new admin routes: `GET /admin/dead-letters` and `POST /admin/dead-letters/replay` |
| `allcs/try_mail.py`, `allcs/send_one.py` | Send one welcome email directly with the mailer |
| `allcs/deliver_twice.py` | Queues the same job twice, like a broker that delivers a job twice |
| `allcs/tests/test_email.py`, `conftest.py` | 9 new tests; Celery in eager mode, a fake mailbox, Redis database 15 |
| `allcs/migrations/`, `app/` (the rest), `make_admin.py`, `get_token.py` | The secure backend of build 10 |

## Run it

```bash
docker run -d --name pyrepo-m18-b12-redis -p 18412:6379 redis:8
docker run -d --name pyrepo-m18-b12-mail -p 18625:1025 -p 18626:8025 axllent/mailpit:v1.32.0
docker run -d --name pyrepo-m18-b12-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 18512:5432 postgres:17.11
cd allcs
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install celery==5.6.3 redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 httpx==0.28.1 pytest==9.1.1
export DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:18512/allcs
export SECRET_KEY=demo-only-not-a-real-secret-4f2a
alembic upgrade head
```

(The video uses `uv add celery redis` and `uv run`.) Start the server in one terminal and the worker in another (the worker needs the same environment variables):

```bash
uvicorn app.main:app --port 8692                                                              # terminal 1
celery -A app.worker worker -n worker1@allcs --loglevel=info --pool=threads --concurrency=2   # terminal 2
```

The worker prints its banner, with the task `app.worker.send_welcome_email`, and `worker1@allcs ready.`.

## Build it step by step

### Step 1: setup

Start from the project of build 10 and add two packages (`uv add celery redis`, or the `pip install` above). Start the three containers (see Run it). Check them:

```bash
docker exec pyrepo-m18-b12-redis redis-cli ping
```

```
PONG
```

The Mailpit web page at `http://localhost:18626` is empty. Create the people and courses of build 10 (the server must be running; the first admin is made by a script):

```bash
curl -s --json '{"name": "Priya", "email": "priya@example.com", "password": "priya-demo-pw"}' localhost:8692/students
curl -s --json '{"name": "Lukas", "email": "lukas@example.com", "password": "lukas-demo-pw"}' localhost:8692/students
python make_admin.py
```

```
{"name":"Priya","email":"priya@example.com","id":1,"role":"student","courses":[]}
{"name":"Lukas","email":"lukas@example.com","id":2,"role":"student","courses":[]}
admin created: asha@example.com
```

Log in as Asha (`python get_token.py asha@example.com asha-demo-pw access_token` prints the token; put it in `ASHA`), create Meera the instructor, then log in as Meera (`MEERA`) and create three courses:

```bash
curl -s -H "Authorization: Bearer $ASHA" --json '{"name": "Meera", "email": "meera@example.com", "password": "meera-demo-pw", "role": "instructor"}' localhost:8692/admin/students
curl -s -H "Authorization: Bearer $MEERA" --json '{"title": "Python Basics", "price": 499}' localhost:8692/courses
curl -s -H "Authorization: Bearer $MEERA" --json '{"title": "SQL in Two Weeks", "price": 599}' localhost:8692/courses
curl -s -H "Authorization: Bearer $MEERA" --json '{"title": "Git and GitHub", "price": 299}' localhost:8692/courses
```

Student ids: Priya 1, Lukas 2, Asha 3, Meera 4. Courses: 1 Python Basics, 2 SQL in Two Weeks, 3 Git and GitHub. Log in as `LUKAS` and `PRIYA` the same way.

### Step 2: the mailer, on its own

`mailer.py` builds the message with the standard library and sends it over SMTP with a time out. Try it before any queue:

```bash
python try_mail.py
```

```
sent to lukas@example.com
```

Open `http://localhost:18626`: one message to Lukas, subject `Welcome to Python Basics`, text:

```
Hi Lukas,

You are enrolled in Python Basics.
Your first lesson is ready.

The allcsvideos team
```

(Delete the message in the Mailpit page, or with `curl -X DELETE localhost:18626/api/v1/messages`, between steps.)

### Step 3: the task and the enroll route

`worker.py` has a Celery app with Redis as broker and the task `send_welcome_email`. It takes plain values (student id, course id, name, email, title), never objects. The enroll route calls `send_welcome_email.delay(student_id=..., course_id=..., name=..., email=..., title=...)` after the enrollment is saved. With the worker running, Lukas enrolls in Python Basics:

```bash
curl -s -i -H "Authorization: Bearer $LUKAS" -X POST localhost:8692/courses/1/enrollments -w "\ntime: %{time_total}s\n"
```

```
HTTP/1.1 201 Created
content-type: application/json

{"student_id":2,"course_id":1,"enrolled_on":"2026-10-27"}
time: 0.452661s
```

(`enrolled_on` is today's date and the time differs for you; the first call is slow because it also opens the Redis connection, later calls take a few hundredths of a second.) The worker log:

```
Task app.worker.send_welcome_email[5c19204d-...] received
app.worker.send_welcome_email[5c19204d-...]: welcome email sent to lukas@example.com
Task app.worker.send_welcome_email[5c19204d-...] succeeded in 0.0285s: None
```

(With a time stamp on every line.) Mailpit has Lukas's email, sent by the worker and not by the request.

### Step 4: retry

The task has `autoretry_for=(OSError,)` (a refused connection and every SMTP error are kinds of `OSError`), `retry_backoff=1`, `retry_jitter=False` and `max_retries=3`. Stop the mail server for real and enroll:

```bash
docker stop pyrepo-m18-b12-mail
curl -s -i -H "Authorization: Bearer $LUKAS" -X POST localhost:8692/courses/2/enrollments
```

The request still answers `201 Created`: the enrollment works while the mail server is gone. The worker log shows the waits growing:

```
Task app.worker.send_welcome_email[fb3070c4-...] retry: Retry in 1s: ConnectionRefusedError(61, 'Connection refused')
Task app.worker.send_welcome_email[fb3070c4-...] retry: Retry in 2s: ConnectionRefusedError(61, 'Connection refused')
Task app.worker.send_welcome_email[fb3070c4-...] retry: Retry in 4s: ConnectionRefusedError(61, 'Connection refused')
Task app.worker.send_welcome_email[fb3070c4-...] raised unexpected: ConnectionRefusedError(61, 'Connection refused')
```

(The error number is 61 on macOS and 111 on Linux.) After the last try the task has failed and the email is gone: only a log line remembers it. A retry survives a short outage, not a long one.

### Step 5: dead letters

`EmailTask.on_failure` runs when a task fails for good. It stores the task id, the arguments and the error as JSON on the Redis list `dead_letters:email`, and logs `gave up on <email>`. The task uses it with `base=EmailTask`. Restart the worker (it loads the code only when it starts). With the mail server still down, Priya enrolls in SQL in Two Weeks and Lukas in Git and GitHub (a student can enroll in a course once, so use courses you have not used for that student yet), then wait about 10 seconds:

```bash
docker exec pyrepo-m18-b12-redis redis-cli LLEN dead_letters:email
docker exec pyrepo-m18-b12-redis redis-cli LRANGE dead_letters:email 0 -1
```

```
2
{"task_id": "8828b530-...", "kwargs": {"student_id": 2, "course_id": 3, "name": "Lukas", "email": "lukas@example.com", "title": "Git and GitHub"}, "error": "ConnectionRefusedError(61, 'Connection refused')"}
{"task_id": "a5942265-...", "kwargs": {"student_id": 1, "course_id": 2, "name": "Priya", "email": "priya@example.com", "title": "SQL in Two Weeks"}, "error": "ConnectionRefusedError(61, 'Connection refused')"}
```

The dead letter holds exactly the arguments, as JSON, so anybody can read it and run the job again later.

### Step 6: the idempotency key

Start the mail server again (`docker start pyrepo-m18-b12-mail`). `deliver_twice.py` queues the same job twice:

```bash
python deliver_twice.py
```

```
queued the same job twice
```

Without a key, Mailpit gets two identical emails for Priya. The task claims a key `welcome:<student_id>:<course_id>` with `redis.set(key, 1, nx=True, ex=WEEK)` before sending; only the first run gets a yes, the other logs `skipped welcome:1:1, already sent` and returns. Because the key is claimed before the send, a failed send gives the claim back (`redis.delete(key)`) and raises the error again, so the retry can try. Restart the worker, clear Mailpit, and run the script again:

```bash
python deliver_twice.py
docker exec pyrepo-m18-b12-redis redis-cli GET welcome:1:1
docker exec pyrepo-m18-b12-redis redis-cli TTL welcome:1:1
```

```
queued the same job twice
1
604784
```

One email in Mailpit; the worker log has one `welcome email sent to priya@example.com` and one `skipped welcome:1:1, already sent`. The TTL is about a week and counts down. Honest note: the key is claimed before the send, so if the whole worker dies between the claim and the send, that email is lost. We chose that on purpose: a double email is more common than a dead worker at exactly that moment.

### Step 7: the admin routes

`GET /admin/dead-letters` reads the list with `LRANGE`; `POST /admin/dead-letters/replay` pops each item and queues the job again with its saved arguments. Both are behind the admin guard. Lukas asks, then Asha asks, then Asha replays (the mail server is back):

```bash
curl -s -i -H "Authorization: Bearer $LUKAS" localhost:8692/admin/dead-letters
curl -s -H "Authorization: Bearer $ASHA" localhost:8692/admin/dead-letters
curl -s -i -H "Authorization: Bearer $ASHA" -X POST localhost:8692/admin/dead-letters/replay
curl -s -H "Authorization: Bearer $ASHA" localhost:8692/admin/dead-letters
```

```
HTTP/1.1 403 Forbidden
{"error":{"code":"forbidden","message":"Your role may not do this"}}
[{"task_id":"...","kwargs":{"student_id":2,...,"title":"Git and GitHub"},"error":"ConnectionRefusedError(61, 'Connection refused')"},{...}]
HTTP/1.1 200 OK
{"replayed":2}
[]
```

The worker log shows `welcome email sent to` Lukas and Priya, Mailpit has both emails, and the dead letters are empty again. (Replay only works for dead letters whose key is not already claimed; the key was given back after the failed sends.)

### Step 8: tests

The tests use their own database (`allcs_test`), Redis database 15, Celery in eager mode (`delay` runs the task right away, inside the test) and a fake mailbox, so no containers other than Postgres and Redis are needed. Create the test database and run:

```bash
docker exec pyrepo-m18-b12-pg psql -U allcs -c "create database allcs_test"
pytest -q
pytest -v tests/test_email.py
```

```
.................................                                                            [100%]
33 passed in 5.02s
tests/test_email.py::test_enrolling_sends_one_welcome_email PASSED
tests/test_email.py::test_a_second_enrollment_sends_no_second_email PASSED
tests/test_email.py::test_enrolling_works_when_the_mail_server_is_down PASSED
tests/test_email.py::test_a_task_that_fails_twice_still_sends PASSED
tests/test_email.py::test_a_task_gives_up_after_three_retries PASSED
tests/test_email.py::test_the_same_job_twice_sends_one_email PASSED
tests/test_email.py::test_dead_letters_are_for_admins_only PASSED
tests/test_email.py::test_an_admin_lists_the_dead_letters PASSED
tests/test_email.py::test_replaying_sends_the_email_and_empties_the_list PASSED
9 passed
```

(The times differ.) 24 tests came from build 10, 9 are new: 33 in all. Do the tests guard the key? In `worker.py`, remove the three lines that claim the key and `return` when it is taken (the `if not redis.set(...)` block) and run again: one test fails, `test_the_same_job_twice_sends_one_email` (`assert 2 == 1`), the other 32 pass. Put the lines back and all 33 pass.

## What is not here yet

If Redis itself is down when the route calls `delay`, the enrollment is saved but the request fails. The outbox idea from M18-L03 fixes that, and this project does not. A worker that dies in the middle of a task, a real mail provider with real addresses, and monitoring of the dead letters are also out of scope.

## Common mistakes

- Passing objects to `delay` instead of plain values.
- Forgetting to restart the worker after changing the task: it loads the code only at start.
- Retrying without an idempotency key, so a retry sends the email twice.
- Claiming the key and not giving it back when the send fails: every retry would be "already sent".
- Running the worker without the same environment variables as the server.
- Using `localhost:18625` for a real mail server. Mailpit only catches mail on your laptop.

## Clean up

```bash
docker rm -f -v pyrepo-m18-b12-redis pyrepo-m18-b12-mail pyrepo-m18-b12-pg
rm -rf .venv
```

(Stop the server and the worker with Ctrl+C first.)

## Next

[M19-L01 · Docker for Python Apps](../../m19-docker-ci-cd-and-deployment/m19-l01-docker-for-python-apps/README.md)
