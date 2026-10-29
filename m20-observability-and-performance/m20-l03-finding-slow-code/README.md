# M20-L03 · Finding Slow Code

> Video: Module 20, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- How to send a pretend crowd with Locust (a user class, wait time, weighted tasks) and read P50, P95 and P99
- How to look inside a running server with `py-spy` (`top`, `dump`, `record` for a flame graph), without a restart
- How to ask Postgres what it was asked: `pg_stat_statements` (how many queries, how long) and `EXPLAIN ANALYZE`
- The finding: one dashboard request sends about 2000 tiny queries (the N+1 problem) plus 8 sequential scans
- Four pitfalls: testing with small data, believing one run, the wrong profiler on a live server, and the wrong target for a load test

## Before you start

- Docker with `docker compose` running, and Python 3.14 on the host (`python --version`) with Locust if you want it on the host: `pip install locust==2.47.0` (the video's version). A Docker alternative for Locust is shown in step 2.
- This lesson continues the backend of M20-L02. The folder `allcs/` is that backend plus a deliberately slow route `GET /me/dashboard` (`app/routers/dashboard.py`). The FIX comes in the next lesson.
- Images (pinned): `postgres:17.11`, `redis:8`, `locustio/locust:2.37.14` (optional), `ghcr.io/astral-sh/uv:0.13`. The compose project is `m20l03`; ports API 8203 (gunicorn with two workers), Postgres 20503, Redis 20403. All passwords and keys are demo values.
- Everything runs on your laptop and every number in the video was real; your numbers will differ (often by a factor of two, depending on what else the computer is doing). What matters is the shape of the story. Only load test your own system: the same crowd aimed at someone else's website is an attack.

Build the two images, start the stack, create the tables and load the data:

```bash
docker build -t m20l03-api:base allcs
docker build -t m20l03-api:profile -f allcs/Dockerfile.profile allcs
docker compose -f stack/compose.yml up -d --wait
docker exec m20l03-api alembic upgrade head
docker cp stack/seed.sql m20l03-pg:/seed.sql
docker exec m20l03-pg psql -U allcs -d allcs -q -f /seed.sql
docker cp stack/passwords.py m20l03-api:/app/passwords.py
docker exec m20l03-api python /app/passwords.py
docker exec m20l03-pg psql -U allcs -d allcs -X -c "select (select count(*) from students) as students, (select count(*) from courses) as courses, (select count(*) from enrollments) as enrollments, (select count(*) from enrollments where course_id <= 8) as meera"
```

```
passwords set
 students | courses | enrollments | meera 
----------+---------+-------------+-------
    20003 |     109 |      193324 |  2000
(1 row)
```

`allcs/Dockerfile.profile` adds `py-spy` to the image, and the API container gets one extra permission (`cap_add: [SYS_PTRACE]` in `stack/compose.yml`), which Linux requires before one process may look inside another. The compose file also turns off worker recycling (`GUNICORN_CMD_ARGS`) so profiles stay clean, and loads `pg_stat_statements` into Postgres. Meera (an instructor) owns 8 courses with 250 students each: 2000 enrollments. Priya (an instructor) has one tiny course with 3 students.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/app/routers/dashboard.py` | The slow route: for each course Meera owns, one query for the enrollments, then `row.student.name` for EVERY enrollment (a lazy load per row) |
| `allcs/Dockerfile`, `Dockerfile.profile` | The API image, and the same image with `py-spy` added |
| `stack/compose.yml` | Postgres (with `pg_stat_statements`), Redis, and the API (with `SYS_PTRACE`) |
| `stack/seed.sql`, `stack/passwords.py` | 20,003 students, 109 courses, 193,324 enrollments (a fixed random seed), and the demo passwords (`<name>-demo-pass`) |
| `locustfile.py` | One pretend visitor: logs in as Meera, then browses |

## Follow along

### 1. The problem: fine alone, slow in a crowd

The dashboard route alone (Meera, one request) and Priya's tiny dashboard:

```bash
TOK=$(curl -s -d "username=meera@example.com&password=meera-demo-pass" localhost:8203/auth/login | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
for i in 1 2 3; do curl -s -o /dev/null -w "%{time_total}s\n" -H "Authorization: Bearer $TOK" localhost:8203/me/dashboard; done
```

On the video machine one request took about 0.29 to 0.37 seconds (0.43 to 0.49 on a busier laptop); on one run here, 0.86 to 1.1 seconds. A list of courses takes a few milliseconds. In the evening twenty teachers and students are on the site at once: how slow does it get, and where does the time go? A picture: a shop owner invites fifty friends at the same time and watches the queue (a load test), then watches the counter while it is busy and writes down what the clerk is doing (a profiler on the running process, not a stopped one). Today's steps: 1) a load test, 2) look inside the running server, 3) ask the database what it was asked.

### 2. Step one: Locust

`locustfile.py`:

```python
class Visitor(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):   # log in as Meera, keep the token
        ...

    @task(6)
    def list_courses(self): self.client.get("/courses", name="/courses")

    @task(3)
    def one_course(self): self.client.get("/courses/12", name="/courses/{id}")

    @task(1)
    def dashboard(self): self.client.get("/me/dashboard", headers=self.headers, name="/me/dashboard")
```

A visitor is one pretend user. `wait_time` is the pause between actions, like a person reading a page. Each task has a weight: listing courses 6, one course 3, the dashboard 1 (so one in ten actions is the heavy one). Run 20 users for one minute (the video's command; `-r 5` adds 5 users per second):

```bash
locust -f locustfile.py --host http://localhost:8203 --headless -u 20 -r 5 -t 60s
```

If you do not want Locust on your host, run it from Docker (the stack's network and the API's internal address):

```bash
docker run --rm --name pyrepo-m20-l03-locust --network m20l03_default -v "$PWD":/mnt/locust locustio/locust:2.37.14 -f /mnt/locust/locustfile.py --host http://api:8000 --headless -u 20 -r 5 -t 60s --only-summary
```

Captured output of the video run (shortened):

```
Type     Name                  # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
POST     /auth/login               20     0(0.00%) |    759     163    1730    690 |    0.33        0.00
GET      /courses                 525     0(0.00%) |     47       2    1250     12 |    8.78        0.00
GET      /courses/{id}            285     0(0.00%) |     33       2     783     11 |    4.76        0.00
GET      /me/dashboard             92     0(0.00%) |   2497     356    7709   1900 |    1.54        0.00
         Aggregated               922     0(0.00%) |    302       2    7709     15 |   15.41        0.00

Response time percentiles (approximated)
                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100%
GET      /courses                  12     23     33     42     98    160    480    790   1300   1300   1300
GET      /courses/{id}             11     18     25     33     54    110    270    760    780    780    780
GET      /me/dashboard           1900   2900   3800   4500   6200   6800   7600   7700   7700   7700   7700
         Aggregated                15     30     51     95    590   1800   4500   6200   7700   7700   7700
```

Percentiles: P50 is the median (half of the requests were faster), P95 means 95 in 100 were faster, P99 the same for 99. The total row looks healthy (median 15 ms, zero failures), but the P95 is 1.8 seconds, and the dashboard row says why: median 1.9 seconds, P95 6.8 seconds, while a request alone took 0.3 seconds. Nothing crashed; the error column says zero. (My own run on a busy Docker Desktop gave different numbers and a few connection resets after a profiler run: see the pitfalls.) Locust can also write an HTML report (`--html report.html`) with the same numbers and charts: the requests per second climb to about 18, and the P95 line jumps up while the median stays flat. What if more people arrive? The same file with 5, 10, 20 and 40 users for 35 seconds each (video run):

| Users | Dashboard requests per second | Dashboard P50 (ms) | Dashboard P95 (ms) |
|-------|-------------------------------|--------------------|--------------------|
| 5 | 0.59 | 400 | 970 |
| 10 | 1.11 | 360 | 850 |
| 20 | 1.97 | 590 | 1700 |
| 40 | 2.06 | 3900 | 6200 |

The dashboard requests per second stop growing at about 2: the server can only do about two dashboards a second. More users only wait longer.

### 3. Step two: which line? `py-spy`

`py-spy` is a sampling profiler: it looks at your program 50 times a second and writes down which function is running, without changing the program. Our server is gunicorn with a main process and two workers; point the tool at one worker. The server can tell you its process number (`/version` returns the `pid`):

```bash
for i in $(seq 20); do curl -s localhost:8203/version; echo; done | sort -u
```

(Take one pid, here `7`.) With the load test running (step 2, 75 seconds), run `py-spy top` inside the container; it works like a task manager, a live table updated every second (it needs a real terminal):

```bash
docker exec -it m20l03-api py-spy top --pid 7
```

Captured (video run, shortened):

```
  %Own   %Total  OwnTime  TotalTime  Function (filename)
 39.00%  55.00%    3.27s     4.15s   wait (psycopg/connection.py)
 18.00%  19.00%    1.99s     2.38s   run (asyncio/runners.py)
  7.00%   7.00%   0.430s    0.430s   _send_query_prepared (psycopg/_cursor_base.py)
  4.00%  87.00%   0.130s     5.69s   _emit_lazyload (sqlalchemy/orm/strategies.py)
```

Not our code: the first row is `wait` in the database driver: the program is waiting for the database. `%Own` is the share of time inside the function itself, `%Total` includes everything it calls: `_emit_lazyload` (SQLAlchemy loading a related row) is 87 percent in total. `py-spy dump` is one photograph of every thread, right now:

```bash
docker exec m20l03-api py-spy dump --pid 7
```

Captured, the busy thread (shortened from the bottom up; the first line is what it is doing at this moment):

```
Thread 1263 (active)
    wait (psycopg/connection.py:495)
    execute (psycopg/cursor.py:114)
    ...
    _emit_lazyload (sqlalchemy/orm/strategies.py:1113)
    _load_for_state (sqlalchemy/orm/strategies.py:1022)
    __get__ (sqlalchemy/orm/attributes.py:575)
    dashboard (app/routers/dashboard.py:25)
    _run_sync_endpoint (fastapi/telemetry/_api.py:244)
```

(On a quiet moment you get the idle main thread instead; take a few photographs until you catch the busy one.) Line 25 of our own file: `dashboard (app/routers/dashboard.py:25)`. And `py-spy record` writes a flame graph (20 seconds, 50 samples a second; a few samples cannot be read):

```bash
docker exec m20l03-api py-spy record --pid 7 -d 20 -r 50 -f flamegraph -o /tmp/flame.svg
docker cp m20l03-api:/tmp/flame.svg flame.svg
```

```
py-spy> Sampling process 50 times a second for 20 seconds. Press Control-C to exit.
py-spy> Wrote flamegraph data to '/tmp/flame.svg'. Samples: 1432 Errors: 398
```

Open `flame.svg` in a browser. The whole program is the top box, each row is called by the row above, wide boxes are where the time goes. In the video the box for `dashboard (dashboard.py:25)` was 85.3 percent of all samples (line 24, the enrollments query, only 2.4 percent), `_emit_lazyload` 83.7 percent and `wait (psycopg)` 71.9 percent. One line of code, 85 percent of the time: you stop guessing. (Honest note from my verification run on Docker Desktop with two busy workers: a 50-per-second `record` made the process fall behind (`py-spy> 22.68s behind in sampling`), and a worker was restarted. See pitfall 3.)

### 4. Step three: the code, and what the database was asked

`app/routers/dashboard.py`:

```python
for course in session.scalars(mine).all():
    query = select(Enrollment).where(Enrollment.course_id == course.id)
    rows = session.scalars(query).all()
    names = [row.student.name for row in rows]
```

For every course Meera owns (8), one query for the enrollments; then, for every enrollment, `row.student.name`, which looks like a plain attribute but is a relationship: the first time you touch it SQLAlchemy quietly sends a query to load that student (a lazy load, the N+1 problem). How many queries does ONE dashboard request send? Ask Postgres with `pg_stat_statements`:

```bash
docker exec m20l03-pg psql -U allcs -d allcs -X -c "select pg_stat_statements_reset()"
curl -s -o /dev/null -H "Authorization: Bearer $TOK" localhost:8203/me/dashboard
docker exec m20l03-pg psql -U allcs -d allcs -X -c "select calls, left(regexp_replace(query, '\s+', ' ', 'g'), 60) as query from pg_stat_statements where query ~* 'from\s+(students|enrollments)\s+where' order by calls desc limit 3"
```

```
 calls |                            query                             
-------+--------------------------------------------------------------
  2001 | SELECT students.id, students.name, students.email, students.
     8 | SELECT enrollments.student_id, enrollments.course_id, enrollments.
(2 rows)
```

(2001 student lookups here, 2000 in the video's count plus one for the login's token check; and the 8 enrollment queries.) Over the whole minute of load (video run; reset the counters with `select pg_stat_statements_reset()` before the load):

```
 calls  | mean_ms | total_ms |                          query
--------+---------+----------+----------------------------------------------------------
    744 |    8.00 |     5954 | SELECT enrollments.student_id, enrollments.course_id, en
 186113 |    0.01 |     2195 | SELECT students.id, students.name, students.email, stude
```

No single student query is slow (0.01 ms each); there are just far too many, each one a trip to the database and back plus ORM work in Python. A second finding: the enrollments query, 8 ms each. `EXPLAIN ANALYZE` (module 16):

```bash
docker exec m20l03-pg psql -U allcs -d allcs -X -c "explain analyze select * from enrollments where course_id = 3"
docker exec m20l03-pg psql -U allcs -d allcs -X -c "explain analyze select * from students where id = 12345"
```

```
 Seq Scan on enrollments  (cost=0.00..3461.55 rows=221 width=12) (actual time=8.358..8.434 rows=250 loops=1)
   Filter: (course_id = 3)
   Rows Removed by Filter: 193074
 Execution Time: 8.466 ms

 Index Scan using students_pkey on students  (cost=0.29..8.30 rows=1 width=565) (actual time=0.020..0.021 rows=1 loops=1)
 Execution Time: 0.038 ms
```

(Times differ.) Postgres read all 193,000 rows for 250: the primary key of `enrollments` is `(student_id, course_id)`, so `course_id` alone cannot use it. Three problems found: about 2000 student lookups one at a time, a sequential scan on `enrollments` 8 times per request, and 2000 rows loaded just to count them and show three names. The fixes are in the next lesson (M20-L04).

### 5. Pitfalls

**Small data.** Priya teaches too, but her course has 3 students. Her dashboard, the same code on the same server:

```bash
PT=$(curl -s -d "username=priya@example.com&password=priya-demo-pass" localhost:8203/auth/login | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
for i in 1 2 3; do curl -s -o /dev/null -w "%{time_total}s\n" -H "Authorization: Bearer $PT" localhost:8203/me/dashboard; done
```

About 6 to 15 milliseconds every time, against 280 to 560 ms for Meera (about 0.01 s here against about 0.9 s). The problem is invisible with small data: test with data of production size.

**Believing one run.** The same 20-user file gave a dashboard median of 1900 ms in the one-minute run and 590 ms in a shorter one. Run more than once, and compare like with like.

**The wrong profiler on a live server.** `cProfile` slows the whole program (module 11). `py-spy` is light, but by default it still pauses the process for a moment at every sample. The dashboard average in the video: 711 ms without `py-spy`, 884 ms with `py-spy record`, 676 ms with `py-spy record --nonblocking` (the flag reads memory without pausing; the picture may be slightly less exact). On a busy small server use a low rate (`-r 10`) and short runs.

**The wrong target.** Twenty pretend users on your own test copy is a test. The same crowd aimed at someone else's website is an attack. Only load test systems you own or have written permission to test.

## Common mistakes

- Looking at the average or the total row only. Read P95 and P99 per route.
- Guessing instead of measuring: the slow line was not the one anyone expected (the query is fast, the 2000 trips are not).
- Testing on a tiny database.
- Profiling with a tool that is heavy on a live server, or forgetting that Linux needs `SYS_PTRACE` for `py-spy` in a container.
- Reading one load test run as the truth.
- A load test against a system that is not yours.

## Clean up

```bash
docker rm -f pyrepo-m20-l03-locust 2>/dev/null
docker compose -f stack/compose.yml down -v
docker rmi m20l03-api:base m20l03-api:profile
rm -f flame.svg
```

## Next

[M20-L04 · Making It Faster](../m20-l04-making-it-faster/README.md)
