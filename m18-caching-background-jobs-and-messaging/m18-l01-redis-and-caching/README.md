# M18-L01 · Redis and Caching

> Video: Module 18, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What a cache is (hit, miss, TTL) and what Redis is: a big dictionary in memory, shared over the network
- Redis from the terminal (`redis-cli`): strings, `INCR`, `EXPIRE`/`TTL`, hashes and lists
- Redis from Python (`redis-py`), and how to store a Pydantic model as JSON text
- The cache-aside pattern on the course list, and how to forget a copy when the truth changes (and why a TTL stays as a safety net)
- A revoked-token blocklist with a TTL, `lru_cache` against Redis with two workers, and three traps: stampede, personal data under a shared key, and full memory

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- This lesson continues the secure backend from build 10 (`../../m17-security-and-authentication/m17-b10-build-secure-allcsvideos/`). The folder `allcs/` here is that project plus the cache.
- Two containers: Redis 8 on port 18401 and Postgres 17 on port 18501. Passwords are demo values.

```bash
docker run -d --name pyrepo-m18-l01-redis -p 18401:6379 redis:8
docker run -d --name pyrepo-m18-l01-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 18501:5432 postgres:17.11
docker exec pyrepo-m18-l01-pg psql -U allcs -c "create database allcs_test"

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 httpx==0.28.1 pytest==9.1.1
export SECRET_KEY=demo-only-not-a-real-secret-4f2a
export DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:18501/allcs
export REDIS_PORT=18401
```

(The video uses `uv add redis` and `uv run`; `pip` works the same.)

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/` | The backend with the cache: `app/cache.py` (connection, TTL, key builder, `forget_course_lists`, `blocked_key`), `routers/courses.py` (cache-aside and delete on write), `routers/auth.py` (`/auth/revoke`), `/stats` in `main.py`, `tests/test_cache.py` |
| `variants/no-cache/` | The two files (`main.py`, `routers/courses.py`) of the server BEFORE the cache, for the "15 queries" demo |
| `variants/stale/courses.py` | `courses.py` that caches but forgets to delete the copy on a change, for the stale-data demo |
| `seed.py` | Resets the database: four people, 300 courses with 30 lessons each, one enrollment |
| `files/client.py` | `BASE`, `LIST` and a `login()` helper |
| `files/basics.py`, `ser.py`, `bad.py` | redis-py basics, a model as JSON, and the "invalid input" error |
| `files/hook.py`, `bench.py` | Five requests without a cache, and three requests with it |
| `files/stale.py`, `stampede.py`, `revoke.py` | The stale-data demo, the stampede, the token block |
| `files/lru_app.py`, `lru_client.py` | A tiny app with `lru_cache` and a Redis counter, run with two workers |
| `files/mem.py` | Redis with a memory limit: `noeviction` against `allkeys-lru` |

## Follow along

### 1. Create the tables and the demo data

```bash
cd allcs
alembic upgrade head
cd ..
python seed.py
```

```
INFO  [alembic.runtime.migration] Running upgrade f149f9b699de -> d1a467cf69aa, refresh tokens
seeded
```

### 2. The problem: the same answer, five times

Run the server WITHOUT the cache. Copy the project to a scratch folder and swap in the two old files (or just read `variants/no-cache/` to see what is missing):

```bash
cp -r allcs /tmp/allcs_nocache
cp variants/no-cache/main.py /tmp/allcs_nocache/app/main.py
cp variants/no-cache/routers/courses.py /tmp/allcs_nocache/app/routers/courses.py
cd /tmp/allcs_nocache && uvicorn app.main:app --port 8181
```

In another terminal, from this lesson's `files/` folder:

```bash
python hook.py
```

```
{'db_queries': 15}
```

Five requests for the same list, three queries each (count, page, lessons): 15. Stop the server (Ctrl+C).

### 3. Redis in the terminal

```bash
docker exec -it pyrepo-m18-l01-redis redis-cli
```

At the `127.0.0.1:6379>` prompt:

```
PING                       ->  PONG
SET greeting "hello"       ->  OK
GET greeting               ->  "hello"
INCR visits                ->  (integer) 1
INCR visits                ->  (integer) 2
INCR visits                ->  (integer) 3
EXISTS greeting            ->  (integer) 1
DEL greeting               ->  (integer) 1
GET greeting               ->  (nil)
```

A missing key counts as zero, and `INCR` happens inside Redis in one step, so a hundred servers counting at once never lose a count. Now forgetting:

```
SET session:abc "lukas" EX 5   ->  OK
TTL session:abc                ->  (integer) 5
GET session:abc                ->  "lukas"
(wait 6 seconds)
GET session:abc                ->  (nil)
SET answer 42                  ->  OK
TTL answer                     ->  (integer) -1
EXPIRE answer 60               ->  (integer) 1
TTL answer                     ->  (integer) 60
```

(The `TTL` after `SET ... EX 5` may show 4 or 5.) Redis threw the session away by itself: that is the TTL, the safety net of every cache. A key with no time lives forever (`-1`). A hash and a list:

```
HSET course:1 title "Python Basics" price 499 level beginner   ->  (integer) 3
HGET course:1 price                                             ->  "499"
HGETALL course:1                                                ->  title, Python Basics, price, 499, level, beginner
RPUSH jobs "email-1" "email-2"                                  ->  (integer) 2
LRANGE jobs 0 -1                                                ->  "email-1", "email-2"
LPOP jobs                                                       ->  "email-1"
```

Notice the price comes back as text. Type `exit` to leave `redis-cli`.

### 4. Redis from Python

```bash
cd files
python basics.py
python ser.py
python bad.py
```

```
hello
1 2
lukas 30
{'title': 'Python Basics', 'price': '499'}
None
{"id":1,"title":"Python Basics","price":499}
id=1 title='Python Basics' price=499
redis.exceptions.DataError: Invalid input of type: 'Course'. Convert to a bytes, string, int or float first.
```

(The last command prints a long traceback first; the last line is shown.) `decode_responses=True` gives text instead of bytes. A hash field comes back as a string (`'499'`), so convert it yourself. A missing key gives `None`. Redis accepts only text, bytes and numbers: use `model_dump_json()` to save and `model_validate_json()` to load a model. (`bad.py` gives `set` the model directly, on purpose.)

Clear Redis between demos with `docker exec pyrepo-m18-l01-redis redis-cli FLUSHALL`.

### 5. Cache-aside on the course list

Read `allcs/app/cache.py` (one connection, a TTL of 60 seconds, a key built from everything that changes the answer: `courses:list:<level>:<limit>:<offset>`) and `allcs/app/routers/courses.py`: look in Redis first (a hit returns the stored text), on a miss run the queries, build the page, store the JSON with `ex=cache.TTL`.

Start the final server (from `allcs/`) and time three requests:

```bash
cd ../allcs
uvicorn app.main:app --port 8181
```

```bash
cd ../files
python bench.py
```

```
first     18.4 ms
second     5.6 ms
third      4.5 ms
{'db_queries': 3, 'hits': 2, 'misses': 1}
```

The milliseconds depend on your computer, yours will differ. The pattern stays: the first is a miss (slower), the next two are hits, and only 3 queries for 3 requests (without the cache, the same three would need 9). Look inside Redis:

```bash
docker exec pyrepo-m18-l01-redis redis-cli --no-raw KEYS '*'
docker exec pyrepo-m18-l01-redis redis-cli --no-raw TTL courses:list:all:50:0
```

```
1) "courses:list:all:50:0"
2) "stats:hits"
3) "stats:misses"
4) "courses:list:all:1:0"
(integer) 60
```

The order of keys differs. The TTL counts down from 60; at zero the key vanishes and the next request is a miss that fills it again.

### 6. Stale data, and the fix

Meera lowers the price of Python Basics from 499 to 399. Run the server that forgets to delete the copy (TTL 3 seconds to keep the demo short). Stop the server from step 5 first, reset the data, and use the stale variant:

```bash
docker exec pyrepo-m18-l01-redis redis-cli FLUSHALL
cd .. && python seed.py
cp -r allcs /tmp/allcs_stale
cp variants/stale/courses.py /tmp/allcs_stale/app/routers/courses.py
cd /tmp/allcs_stale && CACHE_TTL=3 uvicorn app.main:app --port 8181
```

```bash
cd <lesson folder>/files
python stale.py
```

```
before  Python Basics 499
update  200
after   Python Basics 499
4s late Python Basics 399
```

The update returned 200 but the list still showed the old price: stale data. Four seconds later the copy had expired. Fix: delete on write. After every create, update, delete or new lesson, the route calls `cache.forget_course_lists()`, which finds the keys that start with `courses:list:` and deletes them. The TTL stays as a safety net (wrong for at most 60 seconds, not forever). Stop the server, reset (`FLUSHALL`, `python seed.py`), start the final server from `allcs/` and run `python stale.py` again:

```
before  Python Basics 499
update  200
after   Python Basics 399
4s late Python Basics 399
```

The new price shows at once. The tests (step 9) turn this rule into a test that can fail.

### 7. Revoking an access token

An access token cannot be taken back, but a blocklist in Redis can refuse it. `POST /auth/revoke` stores a hash of the token under `blocked:<hash>` with the token's remaining seconds as the TTL, and `get_current_user` refuses blocked tokens. With the final server running:

```bash
python revoke.py
```

```
me before: 200
me after:  401
blocked:05301943... expires in 900 seconds
```

(The hash differs for you.) The block lives exactly as long as the token has left, then Redis forgets it. Nothing to clean up.

### 8. Why not just `lru_cache`? Two workers

```bash
cd files
uvicorn lru_app:app --port 8181 --workers 2
```

In another terminal:

```bash
python lru_client.py
```

```
31635 1 1
31635 0 2
31636 0 3
31636 1 4
31636 2 5
31636 3 6
31635 2 7
31635 3 8
```

Columns: process number, that worker's local `lru_cache` hits, the shared Redis counter. The process numbers and the local counts differ for you. The shared counter goes from 1 to 8 with no gap, while each worker only sees its own local hits. `lru_cache` is great for one process; for anything the whole server must agree on, use Redis.

### 9. Pitfalls and tests

Stampede: delete the key, then send 20 requests at once (server from `allcs/` running):

```bash
docker exec pyrepo-m18-l01-redis redis-cli FLUSHALL
python stampede.py
```

```
{'db_queries': 45, 'hits': 5, 'misses': 15}
```

These numbers depend on timing, yours will differ (we saw between 3 and 15 misses): every request that arrives before the first one has stored the copy rebuilds the same list. On a busy site this can knock the database over. Cures: let one request rebuild while the others wait, or refresh the key before it expires.

Memory: Redis is finite. With the default `noeviction` policy a full Redis refuses writes, and for a cache the right policy is `allkeys-lru`:

```bash
python mem.py
```

```
stopped at 1859 -> command not allowed when used memory > 'maxmemory'.
keys kept: 1854 of 10000
evicted: 8172
```

(The numbers differ slightly each run.) Personal data under a shared key is the third trap: a `my courses` key shared by everyone would give the next student the first student's list. Put the student id in the key, or do not cache it.

Tests (the tests need Redis and Postgres running, and the server may be stopped):

```bash
cd ../allcs
pytest tests/test_cache.py -v
pytest -q
```

```
tests/test_cache.py::test_the_second_list_comes_from_redis PASSED
tests/test_cache.py::test_changing_a_course_forgets_the_cached_list PASSED
tests/test_cache.py::test_a_revoked_token_is_refused PASSED
3 passed
...........................
27 passed
```

Against the stale variant the middle test fails (copy the tests next to `/tmp/allcs_stale` and run `pytest tests/test_cache.py -rf`): `1 failed, 2 passed`.

## Common mistakes

- Giving `r.set` a model or dictionary: Redis takes text, bytes and numbers. Convert with `model_dump_json()`.
- Forgetting that hash values come back as text.
- A cache key that leaves out something that changes the answer (level, limit, offset, the user).
- Forgetting to delete the copy when the data changes: stale data. Delete on write and keep the TTL.
- Storing personal data under a shared key.
- A Redis with no memory limit and no eviction policy: set `maxmemory` and `allkeys-lru` for a cache.
- Keeping the only copy of something important in Redis. The truth stays in Postgres.

## Clean up

```bash
docker rm -f -v pyrepo-m18-l01-redis pyrepo-m18-l01-pg
rm -rf /tmp/allcs_nocache /tmp/allcs_stale .venv
```

## Next

[M18-L02 · Background Jobs with Celery](../m18-l02-background-jobs-with-celery/README.md)
