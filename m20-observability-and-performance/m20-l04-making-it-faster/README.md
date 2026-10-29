# M20-L04 · Making It Faster

> Video: Module 20, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- A loop for performance work: measure, change exactly one thing, measure again with the same test, and keep a table
- Five fixes for the slow dashboard, one at a time: load the students in advance (`selectinload`), an index on `enrollments(course_id)`, one SQL query with `count` and `array_agg`, a short-lived Redis cache with delete-on-write, and a bigger connection pool (which did NOT help)
- Why the order matters (the index alone would have changed nothing) and why the planner may ignore an index
- Four more tools for other kinds of slow code: `asyncio.gather` for waiting, batching writes, a background job for work the caller need not wait for, and fast libraries (`orjson`, `polars`), plus when they do not matter

## Before you start

- Docker with `docker compose` running, `zsh` (the helper scripts are zsh scripts; macOS has it, on Linux install it), and Python 3.14 on the host with a few packages: `pip install locust==2.47.0 httpx==0.28.1 "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 polars==2.1.0 orjson==3.13.0` (the video's versions).
- This lesson continues M20-L03 (the slow `GET /me/dashboard`). Same data: 20,003 students, 109 courses, 193,324 enrollments; Meera owns 8 courses with 250 students each.
- Work on a COPY of this folder (`cp -r m20-l04-making-it-faster /tmp/l04 && cd /tmp/l04`): `apply.sh` rewrites files in `allcs/`.
- Images (pinned): `postgres:17.11`, `redis:8`, `ghcr.io/astral-sh/uv:0.13`. Compose project `m20l04`; ports API 8204, Postgres 20504, Redis 20404. Demo passwords only (`<name>-demo-pass`).
- Timings depend on what else the computer is doing. In the video the same load test gave different numbers an hour later (the baseline, run again at the end of the session, had a dashboard P50 of 630 ms and P95 of 1.8 s instead of 320 and 660), so only compare numbers from ONE session. Yours will differ a lot, but the shape should match.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/` | The backend in its STARTING state (step 0: the slow dashboard of L03) |
| `steps/v0` ... `steps/v5` | The changed files of each step. `v0` the slow one, `v1` eager loading, `v2` the index (model and migration; same dashboard as v1), `v3` one SQL query, `v4` the Redis cache, `v5` cache plus delete-on-write in `enrollments.py` |
| `steps/vx/` | Extra routes for the "four more tools" part: a fake ratings call, an inline export and an export as a Celery job |
| `apply.sh vN` | Copies step N into `allcs/` and builds the image `m20l04-api:vN` |
| `use.sh TAG [POOL_SIZE] [MAX_OVERFLOW]` | Starts the API container from image `TAG` and waits until it is ready |
| `run_step.sh TAG CSV_PREFIX [POOL_SIZE] [MAX_OVERFLOW]` | The SAME Locust run for every step: 20 users, 5 new users per second, 60 seconds; prints one line per route |
| `build_vx.sh` | Builds the image `m20l04-api:vx` (v5 plus the extra routes) |
| `try.sh`, `bench.py` | Quick checks: a few single requests, and the median of 20 requests |
| `locustfile.py` | The load test from L03 (login as Meera, then the same task mix) |
| `files/qcount.sh`, `count.sh` | How many SQL statements does ONE dashboard request run? (`pg_stat_statements`) |
| `files/explain_course.sql`, `explain_dashboard.sql` | `EXPLAIN ANALYZE` for the enrollments query and for the dashboard query |
| `files/stale.py` | The stale-cache demo: enroll a student, ask the dashboard before and after |
| `files/summary.py` | Prints a Locust stats CSV as a small table |
| `files/gather.py`, `bulk.py`, `export.py`, `fast.py` | The four extra tools |
| `stack/` | `compose.yml` (Postgres with `pg_stat_statements`, Redis, API, worker), `seed.sql`, `passwords.py` |

## Follow along

### 1. Set up

```bash
cp -r . /tmp/l04 && cd /tmp/l04            # run this from the lesson folder
for v in v0 v1 v2 v3 v4 v5; do ./apply.sh $v; done     # builds the six images (the first build takes a while)
./build_vx.sh                                           # the extra image
cd stack
TAG=v0 docker compose up -d --wait postgres redis
TAG=v0 docker compose run --rm --no-deps api alembic upgrade head
cd ..
docker cp stack/seed.sql m20l04-pg:/seed.sql
docker exec m20l04-pg psql -U allcs -q -f /seed.sql
(cd stack && TAG=v0 docker compose run --rm --no-deps -v "$PWD/passwords.py:/app/passwords.py" api python /app/passwords.py)
docker exec m20l04-pg psql -U allcs -tA -c "select 'students ' || (select count(*) from students) || ', courses ' || (select count(*) from courses) || ', enrollments ' || (select count(*) from enrollments) || ', meera ' || (select count(*) from enrollments where course_id <= 8)"
```

```
passwords set
students 20003, courses 109, enrollments 193324, meera 2000
```

(`apply.sh` ends by building the image, with a long `sha256:` line. The seed prints a `NOTICE` about `refresh_tokens`.) The index migration belongs to step 2: the images `v2` to `v5` contain it, but the database only gets it when you run `alembic upgrade head` with one of those images (step 4 below). Start from the baseline, without the index.

### 2. The method

Fast does not come from guessing. A programmer who guesses fixes the wrong line, and the code gets harder to read for nothing. The loop: measure; change exactly one thing; measure again with the same test; write a row in a table. The table has the dashboard's P50 and P95, the P95 of all requests together (the dashboard is only one request in ten, but its slow answers pull the total P95 up), and how many SQL statements one request runs. The test is always the same command (the helper `run_step.sh`):

```bash
./use.sh v0
./run_step.sh v0 f0_base
```

```
f0_base    /auth/login         20 rps   0.3 p50   110 p95   170 p99   170 fail 0
f0_base    /courses           654 rps  11.6 p50     7 p95    12 p99    25 fail 0
f0_base    /courses/{id}      321 rps   5.7 p50     5 p95     9 p99    11 fail 0
f0_base    /me/dashboard      106 rps   1.8 p50   320 p95   660 p99  1100 fail 0
f0_base    Aggregated        1136 rps  19.2 p50     4 p95   310 p99   510 fail 0
```

(The dashboard and aggregate lines are the video's baseline; your own numbers will differ, for example 1300 and 2500 for the dashboard on a busy machine.) Count the SQL statements of ONE request:

```bash
files/qcount.sh
```

```
2013
```

(about 2000: the video counted 2010.) `qcount.sh` resets `pg_stat_statements`, sends one dashboard request and sums the calls of the SELECT statements.

### 3. Change 1: load the students in advance

The cure for the N+1 problem (M16-L03): one new line in the enrollments query, `.options(selectinload(Enrollment.student))` (`steps/v1/dashboard.py`). Eight courses, each asking the database twice (enrollments, then its students), plus one question for the logged-in user and one for the list of courses.

```bash
./use.sh v1
files/qcount.sh                  # 18
./run_step.sh v1 f1_eager
```

```
f1_eager   /me/dashboard      110 rps   1.9 p50    66 p95    99 p99   120 fail 0
f1_eager   Aggregated        1186 rps  20.0 p50     4 p95    75 p99   100 fail 0
```

2010 queries before, 18 now. The dashboard P50 falls from 320 to 66 ms and the P95 from 660 to 99 ms; all requests together have a P95 of 75 ms instead of 310 ms. A single request alone: `python bench.py 20` gave a median of 336 ms for v0 and 58 ms for v1 (video).

### 4. Change 2: an index

`EXPLAIN ANALYZE` in L03 showed a sequential scan: to find the enrollments of one course Postgres reads the whole table (193,074 rows removed to find 250). The primary key is `(student_id, course_id)`, so `course_id` alone cannot use it. An index is a sorted list, like the index at the back of a book. The model gets `Index("enrollments_course_id_idx", "course_id")` and a migration (`steps/v2/migrations/a7c3e1f09b52_index_enrollments_course.py`: `op.create_index(...)`, and the downgrade drops it). Plan before and after:

```bash
docker exec -i m20l04-pg psql -U allcs -tA < files/explain_course.sql
(cd stack && TAG=v2 docker compose run --rm --no-deps api alembic upgrade head)
docker exec m20l04-pg psql -U allcs -tA -c "analyze enrollments"
docker exec -i m20l04-pg psql -U allcs -tA < files/explain_course.sql
```

```
Seq Scan on enrollments (actual rows=250 loops=1)
  Filter: (course_id = 3)
  Rows Removed by Filter: 193074
Planning Time: 0.157 ms
Execution Time: 3.966 ms
INFO  [alembic.runtime.migration] Running upgrade d1a467cf69aa -> a7c3e1f09b52, index enrollments by course
Bitmap Heap Scan on enrollments (actual rows=250 loops=1)
  Recheck Cond: (course_id = 3)
  Heap Blocks: exact=3
  ->  Bitmap Index Scan on enrollments_course_id_idx (actual rows=250 loops=1)
        Index Cond: (course_id = 3)
Planning Time: 0.122 ms
Execution Time: 0.035 ms
```

(The plan lines are shortened; the milliseconds differ for you: here 4.2 ms and 0.08 ms.) From about 4 ms to 0.04 ms: about 100 times faster for that query. Under load (`./use.sh v2; ./run_step.sh v2 f2_index`) the video's dashboard P50 went from 66 to 38 ms and the P95 from 99 to 140 ms (a noisy run: P95 is the slowest few). A surprise: had we added this index FIRST (on the slow dashboard) it would have changed almost nothing (video: one request 336 ms without the index, 298 ms with), because the 2000 student lookups were the cost. Fix the biggest cost first.

### 5. Change 3: one query, count and `array_agg` in the database

The page shows, for each course, a title, a count, a revenue figure and three names, but the code loaded thousands of rows to compute that. `steps/v3/dashboard.py` asks Postgres for exactly that:

```python
first = aggregate_order_by(Student.name, Student.id)
names = func.array_agg(first)
query = (
    select(Course.title, Course.price, func.count(), names)
    .join(Enrollment, Enrollment.course_id == Course.id)
    .join(Student, Student.id == Enrollment.student_id)
    .where(Course.owner_id == user.id)
    .group_by(Course.id)
    .order_by(Course.id)
)
```

Does Postgres use the new index for this query? Look at the plan:

```bash
docker exec -i m20l04-pg psql -U allcs -tA < files/explain_dashboard.sql | grep -E "Seq Scan|Index|Execution"
```

```
                    ->  Seq Scan on enrollments e (actual rows=193324 loops=1)
                          ->  Seq Scan on courses c (actual rows=8 loops=1)
                    ->  Seq Scan on students s (actual rows=20003 loops=1)
Execution Time: 12.517 ms
```

No: for eight courses the planner decides that reading the table once is cheaper than the extra steps of an index (it is allowed to be wrong about your wishes, and it is usually right). Count again, and run the test:

```bash
./use.sh v3
files/qcount.sh                  # 2: the user, and the report
./run_step.sh v3 f3_oneq
```

```
f3_oneq    /me/dashboard      ...    p50    17 p95    73 ...
```

In the video the dashboard P50 fell from 38 to 17 ms and the all-requests P95 to 30 ms; a single request took about 10 ms (video) here 18 ms.

### 6. Change 4: the fastest query is the one you do not run (a cache)

The dashboard changes only when somebody enrolls, but we computed it on every request. `steps/v4/dashboard.py` is cache-aside (M18-L01): look for `dashboard:<user id>` in Redis; on a miss compute and store it with `ex=30`.

```bash
./use.sh v4
files/qcount.sh                  # 1 (just the user)
./run_step.sh v4 f4_cache        # dashboard P50 about 4 ms, P95 about 10 ms
```

But a cache can be wrong. Meera's first course has 250 students. Lukas enrolls in it, and we ask the dashboard before and after:

```bash
python files/stale.py lukas 1
```

```
the dashboard says: 250 students
lukas enrolls: 201
the dashboard says: 250 students
```

Still 250: for up to 30 seconds Meera sees old data. A cache trades freshness for speed. The fix (`steps/v5/enrollments.py`): when somebody enrolls, delete that instructor's key (`r.delete(f"dashboard:{course.owner_id}")`, one line). The next request is a miss and computes a fresh answer. With the same script on version 5 (use a student who is not yet enrolled in that course; the random seed data may already have one, which gives `409`):

```bash
./use.sh v5
python files/stale.py lukas 2
```

```
the dashboard says: 250 students
lukas enrolls: 201
the dashboard says: 251 students
```

(In the video Priya enrolled in Meera's first course; here Lukas in the second.) The 30 second lifetime stays as a safety net.

### 7. Change 5: a bigger connection pool (it did not help)

Maybe the requests were waiting for a database connection? Run the version before the cache again with a big pool:

```bash
./run_step.sh v3 f5_pool 20 20       # POOL_SIZE=20, MAX_OVERFLOW=20, on the version without the cache
```

The video measured P50 17 ms and P95 73 ms with the default pool, and P50 18 ms and P95 50 ms with the big pool: no gain (the requests were not waiting for connections). Keep only what moves the number.

### 8. The whole table (video session)

| Step | What changed | Dashboard P50 (ms) | Dashboard P95 (ms) | All requests P95 (ms) | SQL statements per request |
|------|--------------|--------------------|--------------------|-----------------------|----------------------------|
| 0 | baseline | 320 | 660 | 310 | about 2010 |
| 1 | load the students in advance | 66 | 99 | 75 | 18 |
| 2 | index on `enrollments(course_id)` | 38 | 140 | 48 | 18 |
| 3 | one query (count and `array_agg`) | 17 | 73 | 30 | 2 |
| 4 | Redis cache, 30 s | 4 | 10 | 12 | 1 |
| 5 | bigger pool (on step 3, no gain) | 18 | 50 | 37 | 2 |
| (baseline again at the end) | the same code as step 0 | 630 | 1800 | 570 | about 2010 |

The dashboard's P95 fell from 660 ms to 10 ms and the statements from about 2010 to 1. Loading the students in advance and counting in the database gave the big steps; the index gave a smaller step, and only after the first fix; the cache gave the last step but costs freshness (delete-on-write); the bigger pool gave nothing. The last row is the honest note: the baseline re-run at the end of the session was slower than the first one, because the laptop was busier, so compare only within one session.

### 9. Four more tools for other kinds of slow code

Start the `vx` image (v5 plus three extra routes) and the worker:

```bash
cd stack && TAG=vx docker compose up -d --wait api worker && cd ..       # or: ./use.sh vx
```

**Waiting for other services: `asyncio.gather`.** The route `/demo/rating/{id}` waits 0.2 s, standing in for a separate ratings service. Eight calls one by one, or together:

```bash
python files/gather.py
```

```
one by one: 1.64 s
gather:     0.22 s
```

**Writing many rows: batches.** 2000 new students, one commit each, one commit for all, and one call with all rows (this script talks to Postgres on port 20504 and removes its rows afterwards):

```bash
python files/bulk.py
```

```
one_commit_each      0.97 s
one_commit_for_all   0.30 s
one_call_for_all     0.03 s
```

**Work the caller does not need to wait for: a job.** Exporting all enrollments as a file, inline in the request, or queued as a Celery job (M18-L02):

```bash
python files/export.py
```

```
inline    200  0.45 s  {'rows': 193324}
as a job  202  0.05 s  {'job': '05cb818b-9db6-4f52-9e39-f8cc444cf00c'}
```

(The row count grows if you enrolled more students; the job id differs.) **Libraries written in Rust or C.**

```bash
python files/fast.py
```

```
json.dumps, 193 thousand rows    30.8 ms
orjson.dumps, same rows           3.8 ms
193 thousand rows  python loop     5.2 ms   polars    0.8 ms
4.8 million rows   python loop   135.5 ms   polars   15.3 ms
json.dumps, 8-item report         4.4 us
orjson.dumps, 8-item report       0.6 us
```

(Times differ.) Honest part: for the dashboard's own report, with eight items, the standard library takes 4.4 microseconds and `orjson` 0.6: that saves four microseconds per request, nothing. Fast libraries matter where the data is big, not where it is small.

### 10. How to decide

Speed matters where the time is. The profile (L03) tells you which line, the load test tells you what the users feel. Six habits: measure first with a load test; find the slow line with a profile, not a guess; fix the biggest cost first, and ask the database before you write Python; change one thing at a time and write the table; keep only what moves the number; compare numbers from one session only.

## Common mistakes

- Optimising without a measurement, or changing several things at once (you cannot tell which one helped).
- Adding an index first: the biggest cost (2000 lazy loads) was elsewhere.
- Expecting the planner to use every index: ask `EXPLAIN ANALYZE`.
- A cache without delete-on-write: stale data for up to the whole lifetime.
- Making the pool bigger "just in case": more connections can hurt Postgres (M19-L04).
- Comparing numbers from different sessions or different machines.
- Reaching for a fast library when the data is eight items long.

## Clean up

```bash
cd /tmp/l04/stack
TAG=v0 docker compose down -v --remove-orphans
docker rmi m20l04-api:v0 m20l04-api:v1 m20l04-api:v2 m20l04-api:v3 m20l04-api:v4 m20l04-api:v5 m20l04-api:vx
rm -rf /tmp/l04
```

## Next

This is the last lesson of the performance module. Next in the course: [M21-L01 · Command-Line Tools](../../m21-packaging-clis-and-libraries/m21-l01-command-line-tools/README.md).
