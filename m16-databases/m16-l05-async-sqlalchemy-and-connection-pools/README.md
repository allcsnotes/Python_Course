# M16-L05 · Async SQLAlchemy and Connection Pools

> Video: Module 16, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- Why an `async def` endpoint with a normal (blocking) session still handles requests one by one
- The async engine and `AsyncSession`, and the habits: `await` every database call, open sessions with `async with`
- How a connection pool lends connections, what happens when it runs dry, and how to size it
- `pool_pre_ping`, `text()` with bound values, and when plain SQL beats the ORM
- Three mistakes: a missing `await`, lazy loading in async code, and holding a connection while waiting

## Before you start

- Python 3.14 or newer: `python --version`
- Docker running (pinned image `postgres:17`)
- Lessons M16-L02 to M16-L04 (engine, session, relationships, N+1). This folder is self-contained
- A virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Versions in the video: SQLAlchemy 2.1.6, psycopg 3.3.6, FastAPI 0.162.0, uvicorn 0.54.0. The password `secret` is a demo value for a throw-away container.
The async driver is psycopg itself (the same package as before, used in its async mode), so the URL stays `postgresql+psycopg://`.

## Files in this folder

| File | What it is |
|------|------------|
| `requirements.txt` | Pinned packages |
| `db.py` | Async engine and `SessionLocal` (`expire_on_commit=False`), port 15405 |
| `models.py`, `seed.py` | Course / Lesson / Student / Enrollment models and a script that fills 10 courses and 6 students |
| `payments.py` | A `Payment` model and 50,000 fake payment rows |
| `app_slow.py`, `burst.py` | Three versions of a one-second report endpoint, and Priya's stopwatch script |
| `why_pool.py` | 50 queries with and without a pool |
| `async_demo.py` | The first async query |
| `app_db.py`, `ask_course.py` | An async endpoint with a session dependency, and a script that calls it |
| `pool_small.py`, `conns.py` | A tiny pool running dry; counting real connections |
| `helpers.py`, `stale.py` | Closing idle connections on purpose, and `pool_pre_ping` |
| `bound.py`, `compare.py` | `text()` with bound values; ORM versus plain rows |
| `no_await.py`, `lazy.py`, `lazy_fix.py` | Mistakes one and two, and the fix |
| `app_hold.py`, `app_hold_fix.py`, `codes.py` | Mistake three (holding a connection) and its fix |

## Follow along

### 1. Start Postgres and fill the tables

```bash
docker run --name m16l05-pg -e POSTGRES_PASSWORD=secret -p 15405:5432 -d postgres:17
docker exec m16l05-pg psql -U postgres -c "CREATE DATABASE allcs"
python seed.py
python payments.py
```

Both Python scripts print nothing. (If the first `psql` command fails, wait a second: Postgres is still starting.)

### 2. The hook: `async def` that still queues up

`app_slow.py` has three versions of the same report (the query is `SELECT pg_sleep(1)`, a one-second wait):
`/report/blocked` is `async def` with the normal session, `/report/def` is a plain `def` with the normal session,
`/report/async` is `async def` with the async session. Start the server in one terminal:

```bash
uvicorn app_slow:app --port 8165
```

In a second terminal, `burst.py` sends a number of requests at the same moment and times them:

```bash
python burst.py /report/blocked 10
python burst.py /report/def 10
python burst.py /report/async 10
```

```text
/report/blocked: 10 requests, 10.1 seconds
/report/def: 10 requests, 1.1 seconds
/report/async: 10 requests, 1.1 seconds
```

The word `async` did not help the first one: the normal driver waits without saying `await`, so the whole event loop stands still. The cure is not to block the loop, either with a plain `def` (FastAPI runs it in a thread) or with the async session.
The async version is not faster than the plain `def`: Postgres still needs its second. You gain a free event loop while a query waits.

### 3. Why a pool

```bash
python why_pool.py
```

```text
new connection each time  50 queries took 0.36 seconds
connections from a pool   50 queries took 0.07 seconds
```

The seconds depend on your computer (video: 0.20 and 0.03). The pool wins by a wide margin even with Postgres next door. The pool has three settings: `pool_size` (connections kept ready, default 5), `max_overflow` (extra connections allowed when busy, default 10) and `pool_timeout` (seconds to wait for a free one, default 30).

### 4. The async engine and session

Read `db.py`: `create_async_engine`, and `async_sessionmaker(engine, expire_on_commit=False)`. The last argument stops SQLAlchemy from forgetting values after a commit, which would need a query that async code cannot do quietly.

```bash
python async_demo.py
```

```text
1 Python Basics 499
2 Functions 599
3 Data Structures 699
```

Two habits: every call that talks to the database gets an `await` (`execute`, `get`, `commit`, `refresh`), and a session is always opened with `async with`.

### 5. A session dependency in FastAPI

Stop the first server (Ctrl+C), then:

```bash
uvicorn app_db:app --port 8165
```

In another terminal:

```bash
python ask_course.py
```

```text
200 {'id': 2, 'title': 'Functions', 'price': 599}
404 {'detail': 'Course not found'}
```

We never wrote a close: the dependency with `yield` opens and closes each session. The session borrows a connection when it first talks to the database and keeps it until it closes.

### 6. A hundred requests

Start `app_slow` again (`uvicorn app_slow:app --port 8165`) and run:

```bash
python burst.py /report/def 100
python burst.py /report/async 100
```

```text
/report/def: 100 requests, 7.2 seconds
/report/async: 100 requests, 7.2 seconds
```

Not one second, but about seven: that is the pool. 5 connections plus 10 overflow is 15 at a time, and 100 requests in groups of 15 is about 7 rounds.

### 7. Watch a pool run dry

`pool_small.py` uses `pool_size=2, max_overflow=0, pool_timeout=1`. Four visitors borrow a connection for two seconds each.

```bash
python pool_small.py
```

```text
C: TimeoutError after 1.0 s
D: TimeoutError after 1.0 s
B: done after 2.0 s
A: done after 2.0 s
```

(The order of A/B and C/D can differ.) C and D waited one second at the desk and gave up. In a server the message reads `QueuePool limit of size 2 overflow 0 reached, connection timed out`.

Each pooled connection is a real connection inside Postgres, which has a limit:

```bash
python conns.py
```

```text
Postgres allows 100, this program uses 15
```

Forty visits ran, but only 15 got a connection; 25 waited. Remember: every worker process has its own pool. Four workers with 15 each is already 60 of 100.

### 8. Dead connections: `pool_pre_ping`

```bash
python stale.py
python stale.py --ping
```

Without `--ping` the second query fails (the last lines of the traceback):

```text
first query: 10
database closed our idle connection
...
sqlalchemy.exc.OperationalError: (psycopg.errors.AdminShutdown) terminating connection due to administrator command
[SQL: SELECT count(*) FROM courses]
```

With `--ping` (`pool_pre_ping=True`) the pool tests a connection before lending it:

```text
first query: 10
database closed our idle connection
second query: 10
```

A related setting is `pool_recycle` (seconds), which throws away connections older than that.

### 9. When not to use the ORM

```bash
python bound.py
```

The log shows the SQL sentence with its holes and the values next to it, then the rows (the first lines are SQLAlchemy's start-up queries):

```text
... SELECT id, amount FROM payments
WHERE student_id = %(student)s AND amount > %(limit)s
ORDER BY id LIMIT 3
... [generated in 0.00022s] {'student': 2, 'limit': 800}
13 899
84 899
101 899
```

```bash
python compare.py
```

```text
Load every payment
  ORM objects    50000 rows   266.0 ms
  text() rows    50000 rows    25.9 ms
Total paid per student
  ORM query          6 rows     4.2 ms
  text() query       6 rows     4.8 ms
```

The milliseconds are yours to differ (video: 191.2 and 19.9). The pattern is the same: building 50,000 Python objects costs about ten times more, while a report that returns a few rows costs the same either way. Use the ORM for everyday create, read, update and delete of single things. Use `text()` (values in a dictionary) for heavy reports.

### 10. Three mistakes

Mistake 1, a missing `await`:

```bash
python no_await.py
```

```text
...
AttributeError: 'coroutine' object has no attribute 'scalars'
<sys>:0: RuntimeWarning: coroutine 'AsyncSession.execute' was never awaited
```

Mistake 2, lazy loading in async code:

```bash
python lazy.py
python lazy_fix.py
```

```text
Python Basics
...
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/21/xd2s)
```

```text
Python Basics
3 lessons
```

The quiet extra query of lesson 3 has nobody to await it. The fix is the same as in lesson 3: `selectinload` up front.

Mistake 3, holding a connection while you wait. `app_hold.py` reads a course and then sleeps two seconds (a slow email service) with the session still open, on a tiny pool (size 2, timeout 1).

```bash
uvicorn app_hold:app --port 8165
python codes.py
```

```text
{500: 1, 200: 2}
all three answered after 2.1 seconds
```

In the server window: `sqlalchemy.exc.TimeoutError: QueuePool limit of size 2 overflow 0 reached, connection timed out, timeout 1.00`. The third visitor never got a connection. Now stop the server and run the fix, which opens late and closes early (the `async with` block ends before the sleep):

```bash
uvicorn app_hold_fix:app --port 8165
python codes.py
```

```text
{200: 3}
all three answered after 2.1 seconds
```

## Common mistakes

- Believing `async def` alone makes blocking code fast.
- A missing `await` on a database call.
- Lazy loading in async code (`MissingGreenlet`): load relationships up front.
- Keeping a session (and so a connection) open while waiting for something slow.
- Forgetting that every worker has its own pool: workers times pool size must stay under Postgres's `max_connections`.
- No `pool_pre_ping` on a server that runs for days.

## Clean up

Stop any running uvicorn server with Ctrl+C, then:

```bash
docker rm -f -v m16l05-pg
deactivate
rm -rf .venv
```

## Next

[M16-B09 · Build allcsvideos Backend v1](../m16-b09-build-allcsvideos-backend-v1/)
