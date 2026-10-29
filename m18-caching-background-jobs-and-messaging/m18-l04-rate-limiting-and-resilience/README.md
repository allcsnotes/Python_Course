# M18-L04 · Rate Limiting and Resilience

> Video: Module 18, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Calls going out: a time out on every call, retries with exponential backoff and jitter (only for safe, temporary errors), a circuit breaker and a bulkhead
- Why a retry must only repeat what is safe to repeat (idempotency keys)
- Calls coming in: a fixed window rate limit and the token bucket idea, kept in Redis so every worker shares it
- A login limit for the allcsvideos backend: `429 Too Many Requests` with `Retry-After`
- A fallback (graceful degradation): serving the last good copy, clearly labelled, when Postgres is down

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- This lesson continues the backend from lessons 1 to 3 (`../m18-l01-redis-and-caching/`). The folder `allcs/` is the secure backend, with the cache from lesson 1, plus `app/ratelimit.py` and `app/lastgood.py`.
- Two containers: Redis 8 on port 18404 and Postgres 17 on port 18504 (demo passwords). The "practice service" in `files/rates.py` is a tiny local server, so no real service is called.

```bash
docker run -d --name pyrepo-m18-l04-redis -p 18404:6379 redis:8
docker run -d --name pyrepo-m18-l04-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 18504:5432 postgres:17.11
docker exec pyrepo-m18-l04-pg psql -U allcs -c "create database allcs_test"

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 httpx==0.28.1 pytest==9.1.1
export SECRET_KEY=demo-only-not-a-real-secret-4f2a
(cd allcs && alembic upgrade head)
python seed.py
```

```
INFO  [alembic.runtime.migration] Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens
seeded
```

(The video uses `uv add redis` and `uv run`; `pip` works the same.)

## Files in this folder

| File | What it is |
|------|------------|
| `files/rates.py` | The practice service on port 8284: `python rates.py slow\|nap\|flaky\|outage\|down\|charge` |
| `files/slow.py` | A call with no time out against one with a 1 second time out |
| `files/backoff.py`, `files/retry_demo.py` | `retry()` with exponential backoff, jitter and `temporary()` |
| `files/herd.py` | 50 callers retrying with and without jitter |
| `files/charge.py` | A retried payment, without and with an `Idempotency-Key` |
| `files/breaker.py`, `files/breaker_demo.py` | A hand-built circuit breaker and a run against an outage |
| `files/bulkhead.py` | A semaphore with two places for the rate service |
| `files/fixed.py` | A fixed window counter in Redis, and its edge effect |
| `files/attack.py` | Eight wrong passwords and then the right one against `/auth/login` |
| `files/degrade.py` | Asks for the course list and for course 1 |
| `allcs/app/ratelimit.py` | The login limit: key `login:<ip>:<email>`, limit 5, window 60 s |
| `allcs/app/lastgood.py` | Saves and loads the last good copy of a list answer |
| `allcs/app/routers/auth.py`, `courses.py`, `errors.py`, `main.py`, `db.py` | Login uses the limiter; the list route falls back to the last good copy; a 503 handler for database errors |
| `allcs/tests/test_limits.py` | Seven tests for the limit (including "Redis is down, login still works") |
| `variants/old-app/` | The same five app files as they were BEFORE this lesson (no limit, in-memory failure counter), for the "9 lines" demo |
| `seed.py` | Resets the database to Lukas, Priya, Meera, Asha (demo password `<name>-demo-pass`) and four courses |

## Follow along

### 1. The problem: nobody stops the guessing

Run the old server. Copy the project to a scratch folder and swap in the old files:

```bash
cp -r allcs /tmp/allcs_old
cp variants/old-app/db.py variants/old-app/errors.py variants/old-app/main.py /tmp/allcs_old/app/
cp variants/old-app/routers/*.py /tmp/allcs_old/app/routers/
cd /tmp/allcs_old && uvicorn app.main:app --port 8184
```

From this lesson's `files/` folder, in another terminal:

```bash
python attack.py
```

```
try 1: 401  retry-after: -
...
try 8: 401  retry-after: -
the right password: 200
```

Eight wrong guesses (all `401`), then the right password gets in. Stop the server (Ctrl+C).

### 2. A time out on every call that leaves your program

```bash
python rates.py slow &            # the practice service answers after 4 seconds
python slow.py
```

```
timeout None: rate 90.5 after 4.1 s
timeout 1.0: gave up after 1.0 s
```

(Timings differ a little.) With no limit you wait the full 4 seconds. A time out is an error: catch it and decide what to do. Stop the service (`kill %1`). Pick the number a little above the normal slow answer and far below what a user will wait. The backend has three: the HTTPX call, the Postgres connect time out, and the Redis time outs.

### 3. Retries: backoff, jitter, only temporary errors

`backoff.py` waits `random.uniform(0, base * 2 ** (attempt - 1))` between tries (exponential backoff with jitter), retries only errors that can go away (`500` and above, time outs, lost connections) and gives up after a few tries. The practice service answers `503` to its first three calls:

```bash
python rates.py flaky &
python retry_demo.py
```

```
attempt 1 failed, waiting 0.25 s
attempt 2 failed, waiting 0.62 s
attempt 3 failed, waiting 0.78 s
rate: 90.5
```

The waits are random, so yours will differ (they still tend to grow). Stop the service. Why jitter? Fifty callers that failed together would all return at the same moment:

```bash
python herd.py
```

```
no jitter: busiest 0.1 s had 50 retries
jitter   : busiest 0.1 s had 16 retries
```

(The second number differs a little from run to run.) Spread out, instead of one wall of calls.

### 4. Only repeat what is safe to repeat

A `GET` that reads a rate is safe. A `POST` that charges a card is not: the first request may have arrived, just slowly.

```bash
python rates.py charge &
python charge.py
```

```
no answer, asking again
charges so far: 2
no answer, asking again
charges so far: 3
```

The first payment (no key) was charged twice (`2`). The second payment sends `Idempotency-Key: order-17`, so the service recognises the retry and only one more charge is made (`3`). Stop the service.

### 5. Circuit breaker

`breaker.py` has three states: closed (calls go through), open (calls are skipped at once after 3 failures in a row) and half-open (after a 2 second pause one call is tried).

```bash
python rates.py outage &          # down for its first 2.8 seconds
python breaker_demo.py
```

```
 0.0 s  closed     failed
 0.5 s  closed     failed
 1.1 s  closed     failed
 1.6 s  open       skipped
 2.1 s  open       skipped
 2.6 s  open       skipped
 3.1 s  half-open  rate 90.5
 3.6 s  closed     rate 90.5
 4.1 s  closed     rate 90.5
 4.6 s  closed     rate 90.5
```

(Times differ by a tenth of a second.) The breaker saves your workers and lets you answer at once with a fallback. The limit and the pause need tuning for your service. Stop the service.

### 6. Bulkhead

A wall inside a ship: one limit on parallel calls for each outside service, here an `asyncio.Semaphore(2)`.

```bash
python rates.py nap &             # each call takes 1 second
python bulkhead.py
```

```
0.0 s call 1 starts
0.0 s call 2 starts
1.1 s call 1 done
1.1 s call 3 starts
1.1 s call 2 done
1.1 s call 4 starts
2.1 s call 4 done
2.1 s call 5 starts
2.1 s call 3 done
2.1 s call 6 starts
3.1 s call 5 done
3.1 s call 6 done
```

Two at a time, three rounds, about 3 seconds. Stop the service.

### 7. Rate limiting: the fixed window

```bash
python fixed.py
```

```
request  1  at 1.81 s  yes
request  2  at 1.85 s  yes
request  3  at 1.90 s  yes
request  4  at 1.94 s  yes
request  5  at 1.99 s  yes
request  6  at 0.03 s  yes
request  7  at 0.08 s  yes
request  8  at 0.13 s  yes
request  9  at 0.17 s  yes
request 10  at 0.22 s  yes
request 11  at 0.26 s  no
request 12  at 0.30 s  no
```

The limit is 5 per 2 second window, but the script sends 12 requests just across a window edge, so 10 get a "yes" in about 0.4 seconds. The exact times differ. The fixed window is the simplest (`INCR` and `EXPIRE`) and fine for a login limit. The token bucket (a bucket of 10 tokens refilled at a steady speed) handles bursts better.

### 8. The login limit in the backend

Read `allcs/app/ratelimit.py`: `login_key(ip, email)`, `check_login(key)` (answers `429` with `Retry-After` from the key's TTL), `record_failure(key)` (a pipeline: `SET key 0 EX 60 NX` then `INCR`), `forget(key)` after a good login. If Redis is down it logs and lets the login through. Start the server and run the same attack:

```bash
cd ../allcs
uvicorn app.main:app --port 8184
```

```bash
cd ../files
python attack.py
```

```
try 1: 401  retry-after: -
try 2: 401  retry-after: -
try 3: 401  retry-after: -
try 4: 401  retry-after: -
try 5: 401  retry-after: -
try 6: 429  retry-after: 60
try 7: 429  retry-after: 60
try 8: 429  retry-after: 60
the right password: 429
```

Even the right password is refused while locked. The raw answer and what Redis holds:

```bash
curl -si -X POST -d 'username=lukas@example.com&password=x' localhost:8184/auth/login
docker exec pyrepo-m18-l04-redis redis-cli --scan --pattern 'login:*'
docker exec pyrepo-m18-l04-redis redis-cli GET login:127.0.0.1:lukas@example.com
docker exec pyrepo-m18-l04-redis redis-cli TTL login:127.0.0.1:lukas@example.com
```

```
HTTP/1.1 429 Too Many Requests
content-length: 74
content-type: application/json
retry-after: 60

{"error":{"code":"too_many_requests","message":"Too many login attempts"}}
login:127.0.0.1:lukas@example.com
5
59
```

(A `date` and `server` header are also printed. The TTL counts down.) When the TTL reaches zero, Redis forgets the counter. Reset between demos with `docker exec pyrepo-m18-l04-redis redis-cli flushall`.

### 9. Fallback: the last good copy

With the server running, ask for the course list and course 1, then stop Postgres and ask again:

```bash
python degrade.py
docker stop pyrepo-m18-l04-pg
python degrade.py
docker start pyrepo-m18-l04-pg
```

```
/courses?limit=3  200  database
/courses/1        200  -
/courses?limit=3  200  last-good-copy
/courses/1        503  -
```

After a good answer the list route saves a copy (`lastgood:...`) and marks the response `x-served-from: database`. When the query raises an `OperationalError` it serves the copy with `x-served-from: last-good-copy`. Course 1 has no copy, so it gets a clear `503` ("Database is not reachable") with `Retry-After`. Only serve old data when old data is harmless (a course list yes, a bank balance never), and always say so with a header. Stop the server (Ctrl+C).

### 10. Tests

```bash
cd ../allcs
pytest -v tests/test_limits.py
pytest -q
```

```
tests/test_limits.py::test_the_sixth_wrong_password_is_429 PASSED
tests/test_limits.py::test_the_right_password_is_refused_while_locked PASSED
tests/test_limits.py::test_a_good_login_resets_the_count PASSED
tests/test_limits.py::test_another_student_is_not_blocked PASSED
tests/test_limits.py::test_the_window_ends PASSED
tests/test_limits.py::test_the_counter_expires_by_itself PASSED
tests/test_limits.py::test_if_redis_is_down_login_still_works PASSED
7 passed
...............................
31 passed
```

(One test waits for a 1 second window to end, so it takes a few seconds.)

## Common mistakes

- Retries that multiply: a page retries 3 times and the client inside it retries 3 times, so one failure becomes 9 calls. Retry in one place.
- Retrying a call that is not safe to repeat without an idempotency key.
- Limiting by email alone (an attacker can lock Lukas out) or by address alone (a whole school behind one address is blocked). Use both together.
- Believing the limit is enough. It slows an attacker down; strong password hashing (Module 17), long passwords and logs still matter.
- A counter in the memory of one process: with two workers each has its own count. Keep it in Redis.
- No time out on a call that leaves your program.

## Clean up

```bash
docker rm -f -v pyrepo-m18-l04-redis pyrepo-m18-l04-pg
rm -rf /tmp/allcs_old .venv
```

## Next

[M18-B11 · Build a URL Shortener](../m18-b11-build-a-url-shortener/README.md)
