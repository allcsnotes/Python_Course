# M23-L03 · The Backend Interview Round

> Video: Module 23, Lesson 3. Watch it first, then follow along here.

## What you'll learn
- How to run a 45 minute backend design interview: questions first, then numbers, endpoints, tables, login, a background job, a cache, metrics, and "what breaks?"
- How to turn requirements into numbers (about 9 requests per second here) and let the numbers choose the design
- Idempotency keys, unique pairs in the database and `ON CONFLICT DO NOTHING`: three layers that stop a double enrollment
- When an index is needed (500 times faster here), and why keyset pages beat offset pages on long lists
- A pending row plus a retrying worker, so a certificate email is sent exactly once, even when the queue delivers a job twice
- What still works when Redis is down, and how a sweeper repairs what was missed

## Before you start
- Python 3.14 or newer (`python --version`). The project asks for `>=3.14,<3.15`.
- Docker Desktop (one Postgres container and one Redis container, removed in Clean up).
- [uv](https://docs.astral.sh/uv/) for the project environment, as in the video (`uv --version`). The exact package versions are pinned in `uv.lock`.
- `curl`. Optional but handy: a second and a third terminal window (one for the API, one for the worker).
- You built the pieces of this system in earlier lessons: FastAPI (M15), Postgres (M16), logins (M17), Redis and Celery (M18), metrics (M20). The text below names the lesson each part comes from.
- All Python commands run from inside this folder. Every password, key and email here is a demo value, nothing real.

## Files in this folder
| File | What it is |
|---|---|
| `schema.sql` | The seven tables: students, courses, lessons, enrollments, lesson_progress, certificates, idempotency_keys |
| `seed.sql` | Demo data: Lukas, Priya (students), Meera (instructor), three courses with lessons. All emails are fake (`@example.com`) |
| `main.py` | The FastAPI service: enroll, my enrollments (keyset pages), mark a lesson done, progress, popular courses, `/metrics`, `/health/ready` |
| `auth.py` | Reads the bearer token and returns the student number (demo secret, not real) |
| `tokens.py` | Prints a login token for a student number, so you can use `curl` |
| `db.py` | Connection pool for Postgres (demo password `demo`, port 23503) |
| `cache.py` | Cache-aside helper for Redis (port 23403) with a 60 second time to live; Redis down is not fatal |
| `worker.py` | The Celery task `send_certificate`: retries with backoff, checks "already sent" |
| `mailer.py` | A stand-in mail server: writes each email to `sent_mail.txt`, fails while a file named `mail_down` exists |
| `sweep.py` | Queues every certificate row still `pending` after 2 seconds |
| `bench_cache.py` | Asks the popular list 20 times without and 20 times with the cache |
| `enroll3.sh` | One enroll request (used twice at once to show the double tap) |
| `bulk_load.sql`, `rust_course.sql` | Generated demo data for the index and pagination experiments (about one million enrollments) |
| `pyproject.toml`, `uv.lock` | The project and its pinned dependencies (celery 5.6.3, fastapi 0.162.0, psycopg 3.3.6, redis 8.1.0, pyjwt 2.15.1, prometheus-client 0.26.0, httpx 0.28.1) |

## The interview: how Asha plans it
Rahul asks: "Design the enrollment and progress system of allcsvideos.com. Students enroll in courses and finish lessons.
After the last lesson, each student gets a certificate by email." There is no single right answer. Rahul listens for three
things: does she ask before she draws, does she give a reason for each choice, and does she say what can go wrong.

Asha writes the plan in the corner of the board (45 minutes go fast):
1. Questions, 5 minutes. 2. Endpoints, 7. 3. Tables, 8. 4. Login and permissions, 4. 5. The background job, 7. 6. Cache and
numbers to watch, 6. 7. Growing and breaking, 5. That is 42 minutes; the last 3 are for Rahul's questions.

**Step 1, the five questions** (and Rahul's answers):
- Who uses it? Students (enroll, learn) and instructors (look at their course).
- What does progress mean? A student marks a lesson done; the course shows a percent.
- How many people? 200,000 students, about 10,000 active on a normal day, each finishing about 3 lessons. On a launch day,
  20,000 people enroll within one hour.
- What must never go wrong? Nobody enrolls twice, no finished lesson is lost, nobody gets two certificates.
- What may be late? The certificate email. A few minutes is fine.

**The numbers.** 10,000 students times 3 lessons is 30,000 writes a day, which is 30,000 / 86,400 = about 0.35 per second.
Ten times busier on a busy day: 3.5 per second. Launch day: 20,000 enrollments in 3,600 seconds is 5.6 per second.
Together about **9 requests per second**. One ordinary Postgres handles that easily. So this system is not hard because it is
fast; it is hard because it must be correct: every double tap, dropped connection and crashed worker must leave the data right.

## Follow along
The steps follow the video, except that the large data set comes after the small experiments, so the ids in your output
match these. Output marked "yours will differ" depends on your machine.

### 1. Start Postgres and Redis, load the tables
```bash
docker run -d --name m23l03-pg -e POSTGRES_PASSWORD=demo -p 23503:5432 postgres:17
docker run -d --name m23l03-redis -p 23403:6379 redis:8
sleep 8
docker exec -i m23l03-pg psql -U postgres -c "CREATE DATABASE allcs"
docker exec -i m23l03-pg psql -U postgres -d allcs -q < schema.sql
docker exec -i m23l03-pg psql -U postgres -d allcs -q < seed.sql
docker exec m23l03-pg psql -U postgres -d allcs -c '\dt'
```
`\dt` should list seven tables: certificates, courses, enrollments, idempotency_keys, lesson_progress, lessons, students.

### 2. Install the project, start the API and the worker
```bash
uv sync --frozen
```
Open two more terminals in this folder. In the first, the API:
```bash
uv run uvicorn main:app --port 8233
```
In the second, the worker (`-P solo` runs jobs one at a time in one process, which keeps the log easy to read):
```bash
uv run celery -A worker worker -P solo --loglevel=INFO
```
Back in your first terminal, make one login token per student and check the API is ready:
```bash
export API=localhost:8233
export LUKAS="Authorization: Bearer $(uv run python tokens.py 1)"
export PRIYA="Authorization: Bearer $(uv run python tokens.py 2)"
export MEERA="Authorization: Bearer $(uv run python tokens.py 3)"
curl -s $API/health/ready
```
```
{"status":"ready"}
```

### 3. Step 2: the endpoints
The nouns (students, courses, enrollments, progress, certificates) become paths; the verbs are the methods (M15-L02).
- `POST /courses/{course_id}/enrollments`: enroll. 201 created; 404 no such course; 409 already enrolled.
- `GET /me/enrollments`: my enrollments, one page at a time.
- `PUT /enrollments/{id}/lessons/{lesson_id}`: mark a lesson done. PUT means "make it so": done twice is still done.
- `GET /enrollments/{id}/progress`: percent done.
- `GET /courses/popular`: the home page list.

Status codes are part of the design: 201 created, 401 who are you, 403 not allowed, 404 not found, 409 conflict, 422 the
request makes no sense.

### 4. The tap on the train: an idempotency key
A student taps Enroll on a train. The server saves the enrollment, but the answer is lost in a tunnel, and the app tries
again. Without a plan the second request fails for something that worked, or does the work twice. An idempotency key (M18-L02:
"safe to do twice") fixes that: the app sends one random key per tap; the server stores the key with the answer it gave and
replays that answer for the same key. The same key for a different request is refused with 422.

Lukas enrolls in course 1 with the key `k-1001`, then repeats it, then uses a new key for the same course. Guess the three codes first.
```bash
curl -si -X POST $API/courses/1/enrollments -H "$LUKAS" -H "Idempotency-Key: k-1001"
```
```
HTTP/1.1 201 Created
...
{"id":1,"course_id":1}
```
The same request again:
```bash
curl -si -X POST $API/courses/1/enrollments -H "$LUKAS" -H "Idempotency-Key: k-1001"
```
```
HTTP/1.1 201 Created
...
idempotent-replayed: true
{"id":1,"course_id":1}
```
Same enrollment number, and a header saying the answer was replayed: the server did nothing new. (The lines shown as `...`
are other headers, such as date and server; they are left out here.) A new key for the same course:
```bash
curl -si -X POST $API/courses/1/enrollments -H "$LUKAS" -H "Idempotency-Key: k-1002"
```
```
HTTP/1.1 409 Conflict
...
{"detail":"already enrolled"}
```
Two more checks. The same key for a different course is refused, and a course that does not exist is 404:
```bash
curl -si -X POST $API/courses/2/enrollments -H "$LUKAS" -H "Idempotency-Key: k-1001"
curl -si -X POST $API/courses/99/enrollments -H "$LUKAS"
```
```
HTTP/1.1 422 Unprocessable Content
...
{"detail":"key reused"}
HTTP/1.1 404 Not Found
...
{"detail":"course not found"}
```
(Your `curl` output also has the other header lines.)

A key protects only one tap. The real guard against enrolling twice is the unique pair `(student_id, course_id)` in the
database plus `INSERT ... ON CONFLICT DO NOTHING` (see `new_enrollment` in `main.py`): let the database decide, because it
is the one place where every request meets. Prove it with the double tap: Priya's two requests at the same moment, no key.
```bash
(sh enroll3.sh & sh enroll3.sh & wait) | sort
```
```
201
409
```
The database let exactly one win.

Now three more enrollments, so the next steps have something to show (Priya in course 2, Lukas in courses 2 and 3):
```bash
curl -s -X POST $API/courses/2/enrollments -H "$PRIYA"
curl -s -X POST $API/courses/2/enrollments -H "$LUKAS"
curl -s -X POST $API/courses/3/enrollments -H "$LUKAS"
```
```
{"id":5,"course_id":2}{"id":6,"course_id":2}{"id":7,"course_id":3}
```

### 5. Lists: never return everything (keyset pagination)
Always return a page. Two ways to cut pages: `limit` and `offset` (M15-B08) reads and throws away all the skipped rows. Keyset
pagination remembers where the last page ended: every answer carries `next_after`, the id of its last row, and the next
request asks for rows with an id after that. Lukas has three enrollments; ask for a page of two:
```bash
curl -s "$API/me/enrollments?limit=2" -H "$LUKAS"
```
```
{"items":[{"id":1,"course_id":1},{"id":6,"course_id":2}],"next_after":6}
```
Guess what `next_after` says at the end of the next page:
```bash
curl -s "$API/me/enrollments?limit=2&after=6" -H "$LUKAS"
```
```
{"items":[{"id":7,"course_id":3}],"next_after":null}
```
`null` means: this was the end.

### 6. Step 4: who is asking? Three gates
Every request walks through three gates: who are you (token, else 401), may your role do this (403), is this object yours
(else 404) (M17-L03). Passwords are slow salted hashes (Argon2, M17-L01); login gives a short access token and a refresh
token (M17-L02). The rule interviewers love: **the student's number comes from the token, never from the path or the body.**
Otherwise Lukas could write Priya's number. That bug is broken object level authorisation, number one in the OWASP API list.
```bash
curl -si $API/me/enrollments
curl -si $API/enrollments/1/progress -H "$PRIYA"
curl -si $API/enrollments/1/progress -H "$LUKAS"
```
```
HTTP/1.1 401 Unauthorized
...
{"detail":"missing token"}
HTTP/1.1 404 Not Found
...
{"detail":"enrollment not found"}
HTTP/1.1 200 OK
...
{"done":0,"total":3,"percent":0}
```
No token gives 401. Priya asking for Lukas's enrollment gets 404, not 403: a 403 would tell her the enrollment exists. And
Lukas gets his own progress: 0 of 3 lessons. The login itself gets a rate limit in Redis (M18-L04).

### 7. Step 3: the tables, and the index you need
The tables come from the nouns (see `schema.sql`). The database guards a lot by itself: primary keys, the unique pair
on enrollments, foreign keys, a check that the price is above zero (M16-L04). Two requests can pass the same check in
Python at the same moment, but only one can win a unique rule.
- `lesson_progress`: the key is the pair (enrollment, lesson), so marking a lesson done twice is the same row.
- `certificates`: one row per enrollment, with `status` (`pending` or `sent`) and `attempts`. This row is the job.
- `idempotency_keys`: `(student_id, key)` is the primary key, the stored answer sits beside it.

For every question the API asks, ask which index answers it. "My enrollments" (by student): the unique pair starts with
`student_id`, so it is covered. "The next page after this id": the primary key. "The students of a course": the pair starts
with the wrong column, so Postgres would read the whole table. That question needs its own index.

Prove it. Generate 200,000 students and about a million enrollments, then add a small course with just 40 students:
```bash
docker exec -i m23l03-pg psql -U postgres -d allcs -q < bulk_load.sql
docker exec -i m23l03-pg psql -U postgres -d allcs -q < rust_course.sql
docker exec m23l03-pg psql -U postgres -d allcs -c "SELECT (SELECT count(*) FROM students) AS students, (SELECT count(*) FROM courses) AS courses, (SELECT count(*) FROM enrollments) AS enrollments"
```
```
 students | courses | enrollments
----------+---------+-------------
   200003 |      61 |     1000045
(1 row)
```
(The video counted before adding the small course: 60 courses and 1,000,005 enrollments.) The instructor opens the page of
"Rust for Python Programmers": the server counts its students. Without an index on the course:
```bash
docker exec -i m23l03-pg psql -U postgres -d allcs -At <<'SQL'
SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, COSTS OFF) SELECT count(*) FROM enrollments WHERE course_id = 61;
SQL
```
```
SET
Aggregate (actual time=44.488..44.489 rows=1 loops=1)
  ->  Seq Scan on enrollments (actual time=44.473..44.474 rows=40 loops=1)
        Filter: (course_id = 61)
        Rows Removed by Filter: 1000005
Planning Time: 0.833 ms
Execution Time: 44.607 ms
```
A sequential scan: it reads the whole table and throws away a million rows to find forty (the video's machine took
72 ms; yours will differ). Now create the index and ask again:
```bash
docker exec -i m23l03-pg psql -U postgres -d allcs -At <<'SQL'
CREATE INDEX enrollments_course_id_idx ON enrollments (course_id);
VACUUM ANALYZE enrollments;
SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, COSTS OFF) SELECT count(*) FROM enrollments WHERE course_id = 61;
SQL
```
```
CREATE INDEX
SET
Aggregate (actual time=0.102..0.103 rows=1 loops=1)
  ->  Index Only Scan using enrollments_course_id_idx on enrollments (actual time=0.092..0.095 rows=40 loops=1)
        Index Cond: (course_id = 61)
        Heap Fetches: 0
Planning Time: 0.312 ms
Execution Time: 0.165 ms
```
Under a millisecond (the video: 72 ms down to 0.14 ms, about 500 times faster; a popular course with more than 16,000
students went from 96 to 6.6 ms). The lookup by student, which already had the unique pair, takes well under a millisecond.
An index is not free (M16-L01): it takes space and every insert updates it. So add one index for each real question, not one
for each column.

### 8. Offset against keyset, 900,000 rows deep
The same 20 rows, 900,000 rows deep, in a table of a million. Offset first:
```bash
docker exec -i m23l03-pg psql -U postgres -d allcs -At <<'SQL'
SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, COSTS OFF) SELECT id FROM enrollments ORDER BY id LIMIT 20 OFFSET 900000;
EXPLAIN (ANALYZE, COSTS OFF) SELECT id FROM enrollments WHERE id > 900000 ORDER BY id LIMIT 20;
SQL
```
```
SET
Limit (actual time=84.636..84.639 rows=20 loops=1)
  ->  Index Only Scan using enrollments_pkey on enrollments (actual time=0.057..65.516 rows=900020 loops=1)
        Heap Fetches: 0
Planning Time: 0.151 ms
Execution Time: 84.650 ms
Limit (actual time=0.027..0.029 rows=20 loops=1)
  ->  Index Only Scan using enrollments_pkey on enrollments (actual time=0.027..0.028 rows=20 loops=1)
        Index Cond: (id > 900000)
        Heap Fetches: 0
Planning Time: 0.139 ms
Execution Time: 0.036 ms
```
The offset query walked 900,020 rows; the keyset query jumped straight to the place through the index (the video: 152 ms
against 0.05 ms, about 3,000 times faster). Keyset has a price: you cannot jump straight to page 17. For a feed or a list that
can grow that is fine; for a small table offset is simpler. Asha picks keyset for every list that can grow.

### 9. Step 6: the cache
Rule one: do not cache before you measure. The progress page runs two small queries on indexed columns and belongs to one
student: nothing to gain. But the popular courses list is the same for everybody and counts a million rows. That deserves a
cache: cache-aside (M18-L01). Look in Redis first; on a miss ask Postgres and store the answer for 60 seconds. If Redis is
down, load the answer anyway: the cache is optional, never required (see `cache.py`).
```bash
curl -si $API/courses/popular
curl -si $API/courses/popular
docker exec m23l03-redis redis-cli ttl popular
```
```
HTTP/1.1 200 OK
...
x-cache: miss
[{"course_id":19,"students":16668},{"course_id":20,"students":16668},{"course_id":21,"students":16668}]
HTTP/1.1 200 OK
...
x-cache: hit
[{"course_id":19,"students":16668},{"course_id":20,"students":16668},{"course_id":21,"students":16668}]
60
```
(The `ttl` number counts down from 60; it may show 59 or 58.) First a miss, then a hit, then the time to live. Now the
benchmark: 20 requests with the key deleted each time, and 20 with the key kept. Guess how many times faster.
```bash
uv run python bench_cache.py
```
```
without the cache: 51 ms
with the cache:    3 ms
```
Yours will differ (the video: 78 ms against 2 ms, about 40 times faster). Three cautions: never put personal data under a
shared key; when many requests find the key gone at the same moment they all hit Postgres together (the stampede, M18-L01);
and if data must change at once, delete the key when you write.

### 10. Step 5: the certificate job
After the last lesson, the student gets an email. Do you send it inside the request? No: sending takes a second or more and
can fail, and a failed email must never make a finished lesson fail. So the request does two quick things in **one
transaction**: it saves the lesson and a certificate row marked `pending`. Then it puts a job on the queue. A worker takes
the job and sends the email. The row is the promise: if the queue is down at that moment, the row still says pending and
nothing is lost (the outbox idea, M18-L03).

The worker (`worker.py`) retries with backoff: 1 second, 2, 4 (M18-B12). Because a queue delivers at least once, the worker
must be ready to see the same job twice: it first reads the row, and if the status is already `sent`, it stops. It counts
the attempt and commits it, sends the mail, then marks the row `sent`. If sending fails, the row is not marked, so the next
try starts clean.

Real run. Here the mail server is a stand-in that fails while a file called `mail_down` exists. Switch it off, let Priya
finish the last lesson of Git and GitHub (enrollment 5, lessons 4 and 5), and after 4.5 seconds switch it on again. Guess:
how many tries, and how many emails?
```bash
touch mail_down
curl -s -X PUT $API/enrollments/5/lessons/4 -H "$PRIYA"
curl -s -X PUT $API/enrollments/5/lessons/5 -H "$PRIYA"
sleep 4.5; rm mail_down
sleep 6
```
```
{"done":1,"total":2,"percent":50,"certificate":null}
{"done":2,"total":2,"percent":100,"certificate":"queued"}
```
The answer came at once: 200, certificate queued. The worker terminal tells the rest (your times and job ids differ):
```
21:49:38  [7b76c601] received
21:49:38  [7b76c601] retry: Retry in 1s: SendError('mail server not answering')
21:49:38  [7b76c601] received
21:49:39  [7b76c601] retry: Retry in 2s: SendError('mail server not answering')
21:49:39  [7b76c601] received
21:49:41  [7b76c601] retry: Retry in 4s: SendError('mail server not answering')
21:49:41  [7b76c601] received
21:49:45  [7b76c601] succeeded: 'sent'
```
(In the real log each line starts with `[2026-... INFO/MainProcess] Task worker.send_certificate[...]`; the lines above are trimmed.)
The fourth try succeeded. Check the row:
```bash
docker exec m23l03-pg psql -U postgres -d allcs -c "SELECT id, status, attempts FROM certificates"
```
```
 id | status | attempts
----+--------+----------
  1 | sent   |        4
(1 row)
```
Now the queue delivers the same job two more times, as it sometimes does:
```bash
uv run python -c "from worker import send_certificate as s; s.delay(1); s.delay(1)"
sleep 3
cut -d' ' -f1,2 sent_mail.txt
wc -l < sent_mail.txt
```
```
certificate 1
1
```
The worker log shows two more `received` lines that both end with `succeeded: 'already sent'`, and the mail file still has
one line (the second column of `sent_mail.txt` is a time stamp, cut away here). One certificate, one email.

### 11. Step 6, continued: four numbers to watch
Module 20 gave three signals: logs, metrics, traces. Asha names four numbers: for every route the **rate**, the **errors**
and the **duration** (as P95, never only the average); a business number, enrollments per hour; and for the job, how many
certificates are pending and how old is the oldest. The service publishes counters on `/metrics`:
```bash
curl -s $API/metrics | grep -E '^(enrollments_created_total|certificates_queued_total|http_requests_total.*courses/.course_id./enrollments)'
```
```
http_requests_total{route="/courses/{course_id}/enrollments",status="201"} 6.0
http_requests_total{route="/courses/{course_id}/enrollments",status="409"} 2.0
http_requests_total{route="/courses/{course_id}/enrollments",status="422"} 1.0
http_requests_total{route="/courses/{course_id}/enrollments",status="404"} 1.0
enrollments_created_total 5.0
certificates_queued_total 1.0
```
Six answers of 201 on the enroll route, but only five enrollments created: the replay was not counted. One certificate
queued. Counters only go up; the monitoring system turns them into rates. Labels need a few known values (the route and the
status code), never a student number, or the series explode. Alerts watch what a student feels: error rate above 1 percent
for 5 minutes, or a certificate pending for more than 10 minutes. (This only matches if you ran every step above, in order.)

### 12. Step 7: growing, and what breaks
**If it grows 100 times:** phones talk to a load balancer; behind it several copies of the API; they all use one Postgres, one
Redis (cache and queue) and a pool of workers. The API copies hold no state (no sessions in memory, no files on disk): state
lives in Postgres, Redis and the queue. To grow, go in order: more API copies, a connection pool sized as in M16-L05, then a
read replica. Sharding comes last, and it is far away at 9 requests per second.

**What breaks?** An API copy dies: the load balancer stops sending it requests. Postgres is down: the readiness check fails
and nothing is saved wrongly. A worker dies mid-job: the job is delivered again, and the "already sent" check makes that safe.
The mail server is down: retry, then a dead letter list (M18-B12).

Now Redis. Stop it and guess: does the popular list still answer? Does a student's last lesson still finish? And what
happens to the certificate? (Lukas finishes course 3, enrollment 7, lessons 6 and 7.)
```bash
docker stop m23l03-redis
curl -si $API/courses/popular
curl -s -X PUT $API/enrollments/7/lessons/6 -H "$LUKAS"
curl -s -X PUT $API/enrollments/7/lessons/7 -H "$LUKAS"
docker exec m23l03-pg psql -U postgres -d allcs -c "SELECT id, status, attempts FROM certificates ORDER BY id"
```
```
m23l03-redis
HTTP/1.1 200 OK
...
x-cache: down
[{"course_id":19,"students":16668},{"course_id":20,"students":16668},{"course_id":21,"students":16668}]
{"done":1,"total":2,"percent":50,"certificate":null}
{"done":2,"total":2,"percent":100,"certificate":"queued"}
 id | status  | attempts
----+---------+----------
  1 | sent    |        4
  2 | pending |        0
(2 rows)
```
The popular list answers 200 with the cache marked down: slower, but it works. The last lesson finishes with 200. The
certificate row is `pending` with zero attempts, because the job never reached the queue. Start Redis again and run the
sweeper, a small script that queues every row still pending after 2 seconds:
```bash
docker start m23l03-redis
sleep 5
uv run python sweep.py
sleep 3
docker exec m23l03-pg psql -U postgres -d allcs -c "SELECT id, status, attempts FROM certificates ORDER BY id"
```
```
m23l03-redis
queued again: 2
 id | status | attempts
----+--------+----------
  1 | sent   |        4
  2 | sent   |        1
(2 rows)
```
Nothing was lost.

One last habit: protect others from your failures, and yourself from theirs. Time outs on every call that leaves the
service, a rate limit in front of it, and a circuit breaker for services you call (M18-L04).

## The mistakes Rahul sees most
1. Drawing before asking.
2. Reaching for the biggest tools first (microservices, Kafka) at 9 requests per second.
3. Saying no numbers at all.
4. Forgetting the double tap, the dropped connection and the crashed worker.
5. Forgetting who is allowed to see what.
6. Silence. Thinking for two minutes without a word leaves Rahul guessing.

A good answer has a shape: clarify, estimate, draw the simple version first, give a reason for each choice, ask "where does
this break?". When Rahul pushes back, do not defend: say "good point, here is the trade-off."

## Interview question
*Your design uses one database and one queue. Why not microservices?* At about nine requests per second one Postgres and
one worker are enough. Splitting into services adds network calls, more ways to fail and more to deploy. I would split a part
out when it needs a different scale, a different team or a different release speed, and I would measure first.

## Common mistakes
1. Skipping the numbers: without them you cannot say whether one Postgres is enough.
2. Trusting the student number from the path or the body instead of the token.
3. Returning 403 for someone else's object (it leaks that the object exists): return 404.
4. Relying on the idempotency key alone and forgetting the unique pair in the database.
5. Sending the email inside the request, or writing the certificate row and the job in two steps that can disagree.
6. A worker that is not safe to run twice.
7. Caching before measuring, putting personal data under a shared key, or making the cache required.
8. Adding an index for every column instead of one for each real question.
9. Using offset pages on a list that can grow.
10. High-cardinality labels (a student number) on metrics.

## Try it yourself
1. Add a delete endpoint for enrollments, and say which codes it answers.
2. Draw a second job: a reminder for students who stopped learning.
3. Explain in one minute what happens when Postgres is down. Say each answer out loud.

## Clean up
Stop the API and the worker (Ctrl+C in their terminals), then:
```bash
docker rm -f -v m23l03-pg m23l03-redis
rm -f mail_down sent_mail.txt
rm -rf .venv
```

## Next
[M23-L04 · Mock Interview and Roadmap](../m23-l04-mock-interview-and-roadmap/)
