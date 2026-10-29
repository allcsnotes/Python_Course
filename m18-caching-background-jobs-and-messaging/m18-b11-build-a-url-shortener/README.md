# M18-B11 · Build a URL Shortener

> Video: Module 18, Build 11. Watch it first, then follow along here.

## What you'll build

A link shortener service with FastAPI, Postgres and Redis. Think of a coat check: the long address is the coat, the short code is the ticket.

- `POST /links` makes a short code (seven letters and digits) for any web address
- `GET /<code>` redirects with `307 Temporary Redirect`; unknown code is `404`, expired code is `410`
- `GET /links/<code>/stats` shows the clicks; `GET /cache/stats` shows cache hits and misses
- Redis keeps copies of popular links (cache-aside), counts clicks, and limits how many links one address can make
- 24 tests, and a load test that measures whether the cache is worth it

The seven rules (each one is a test): a code is seven letters and digits and never used twice; only web addresses are accepted; opening a code gives a 307; an unknown code is 404 and an expired one is 410; a second visit does not ask Postgres; clicks are counted without a write per visit; one address cannot create unlimited links.

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- You should have done lesson M18-L01 (Redis and caching) and M18-L04 (rate limiting).
- Two containers: Postgres 17 on port 18511 and Redis 8 on port 18411. Demo passwords only.

## Files in this folder

| File | What it is |
|------|------------|
| `links/app/settings.py` | Reads the addresses, cache time, flush time and limit from environment variables (with defaults for this laptop) |
| `links/app/db.py`, `models.py` | The engine and the `Link` table (id, unique code, url, clicks, created_at, expires_at) |
| `links/app/codes.py` | `encode()` (base 62) and `new_code()` (random code) |
| `links/app/schemas.py` | `LinkIn` (a `HttpUrl`, `extra="forbid"`) and the output models |
| `links/app/errors.py` | Our own error shape (`{"error": {"code", "message"}}`) |
| `links/app/links.py` | `create_link` (retries on a taken code), `find_link` (cache-aside), `is_expired` |
| `links/app/cache.py` | Redis connection (half second time outs), link copies, hit and miss counters, click counter, `flush_clicks` |
| `links/app/limits.py` | The `rate_limit` dependency: 10 new links per minute per address |
| `links/app/main.py` | The routes, the click flusher (a background loop started in `lifespan`) |
| `links/migrations/versions/4025a0c58b15_create_links.py` | The migration for the `links` table |
| `links/collide.py` | How soon do random codes repeat? (the birthday problem) |
| `links/load.py` | The load test: cache on (port 8691) against cache off (port 8791) |
| `links/tests/` | 24 tests in five files |
| `links/pyproject.toml`, `uv.lock` | Dependencies |

## Run it

```bash
docker run -d --name pyrepo-m18-b11-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=links -p 18511:5432 postgres:17.11
docker run -d --name pyrepo-m18-b11-redis -p 18411:6379 redis:8
cd links
uv sync                              # or: python -m venv .venv, activate it, pip install -e . pytest
uv run alembic upgrade head
uv run fastapi dev app/main.py --port 8691
```

(Without uv: `pip install "fastapi[standard]==0.162.0" sqlalchemy==2.1.6 "psycopg[binary]==3.3.6" redis==8.1.0 alembic==1.20.1 pytest==9.1.1`, drop `uv run`, and use `uvicorn app.main:app --port 8691`.)

In another terminal:

```bash
curl -s -i -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com/courses/python-basics"}'
curl -s -i localhost:8691/<the code from the answer>
```

```
HTTP/1.1 201 Created
content-type: application/json

{"code":"XaFsb4E","short_url":"http://localhost:8691/XaFsb4E","url":"https://allcsvideos.com/courses/python-basics","expires_at":null}
HTTP/1.1 307 Temporary Redirect
location: https://allcsvideos.com/courses/python-basics
```

The code is random, so yours will differ. The server never sends the page: it says "go there", and the browser follows. (Extra headers such as `date` and `server` are also printed.)

## Build it step by step

The video builds the service in six steps. The files above are the result of the last step.

### Step 1: setup

Start Postgres and Redis (see Run it), then create the project:

```bash
uv init --bare --name links
uv add "fastapi[standard]" sqlalchemy "psycopg[binary]" redis alembic
uv add --dev pytest
```

This installs (among others) `fastapi==0.162.0`, `sqlalchemy==2.1.6`, `psycopg==3.3.6`, `redis==8.1.0`, `alembic==1.20.1` and `pytest==9.1.1`. The table has a **unique** code. Let Alembic write the migration (`uv run alembic revision --autogenerate -m "create links"`, then `upgrade head`):

```
INFO  [alembic.runtime.migration] Running upgrade  -> 4025a0c58b15, create links
```

```bash
docker exec pyrepo-m18-b11-pg psql -U allcs -d links -c "\d links"
```

```
                                       Table "public.links"
   Column   |           Type           | Collation | Nullable |              Default              
------------+--------------------------+-----------+----------+-----------------------------------
 id         | integer                  |           | not null | nextval('links_id_seq'::regclass)
 code       | character varying(12)    |           | not null | 
 url        | character varying(2048)  |           | not null | 
 clicks     | integer                  |           | not null | 0
 created_at | timestamp with time zone |           | not null | now()
 expires_at | timestamp with time zone |           |          | 
Indexes:
    "links_pkey" PRIMARY KEY, btree (id)
    "links_code_key" UNIQUE CONSTRAINT, btree (code)
```

The unique rule made Postgres build an index on `code`, so finding a link by code is fast.

### Step 2: the short code

A code is a number written in base 62 (ten digits, 26 small and 26 capital letters). `encode()` uses `divmod`. In a Python session (`uv run python`):

```python
>>> from app.codes import encode, new_code
>>> encode(61)
'Z'
>>> encode(62)
'10'
>>> encode(125)
'21'
>>> 62 ** 7
3521614606208
>>> new_code()
'nIFlb0I'
```

(`new_code()` is random.) Why random and not the row number? Row numbers would let anyone walk through every link and show how many you have. But random codes can repeat by luck:

```bash
uv run python collide.py
```

```
length 2: 3,844 codes
  first repeat after [130, 64, 60, 65, 48] codes
length 3: 238,328 codes
  first repeat after [352, 563, 1257, 1078, 634] codes
length 4: 14,776,336 codes
  first repeat after [10240, 5673, 6299, 5560, 5297] codes
length 7: 3,521,614,606,208 codes
  a repeat is likely after about 2,351,964 codes
```

The numbers in the "first repeat" lines are random, yours will differ. This is the birthday problem. So never trust luck: the guard is the unique rule in the database.

```bash
docker exec pyrepo-m18-b11-pg psql -U allcs -d links -c "INSERT INTO links (code, url) VALUES ('abc1234', 'https://a.example'), ('abc1234', 'https://b.example')"
```

```
ERROR:  duplicate key value violates unique constraint "links_code_key"
DETAIL:  Key (code)=(abc1234) already exists.
```

(Nothing is inserted, the whole statement is refused.) The app catches this error and tries a new code, up to five times.

### Step 3: create and redirect

`LinkIn` has one field, `url: HttpUrl`, which accepts only `http` and `https` (a `javascript:` link would run a program in the visitor's browser). `create_link` loops up to five times: make a code, add the row, commit, and on a broken unique rule roll back and retry. The redirect route requires the code to match `^[0-9a-zA-Z]{1,12}$`, answers 404 for an unknown code and otherwise `307` (not `301`, which browsers remember forever, so you could never count or change the link).

```bash
curl -s -i localhost:8691/zzzzzzz
curl -s -i -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "javascript:alert(1)"}'
curl -s -i -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com", "code": "mine"}'
curl -s -i localhost:8691/a-b_c
```

```
HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"Unknown link"}}
HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"url","problem":"URL scheme should be 'http' or 'https'"}]}}
HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"code","problem":"Extra inputs are not permitted"}]}}
HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"code","problem":"String should match pattern '^[0-9a-zA-Z]{1,12}$'"}]}}
```

An `ftp://` address gives the same URL scheme error, an address with no scheme gives `Input should be a valid URL, relative URL without a base`.

### Step 4: the cache and the click counter

`find_link` asks Redis first (`link:<code>`), and on a miss asks Postgres and stores a copy with a time to live of one hour. Create a link, then visit it four times and look at the cache:

```bash
curl -s -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com/courses/git-and-github"}'
docker exec pyrepo-m18-b11-redis redis-cli GET link:<code>
for i in 1 2 3 4; do curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" localhost:8691/<code>; done
docker exec pyrepo-m18-b11-redis redis-cli GET link:<code>
docker exec pyrepo-m18-b11-redis redis-cli TTL link:<code>
curl -s localhost:8691/cache/stats
```

```
(nil)
307 0.080744s
307 0.005364s
307 0.003242s
307 0.003679s
"{\"url\": \"https://allcsvideos.com/courses/git-and-github\", \"expires_at\": null}"
(integer) 3600
{"hits":3,"misses":1}
```

(Timings differ for you; the first visit is slower. With a script instead of a terminal, `redis-cli` prints an empty line instead of `(nil)`; the TTL counts down.) One miss and three hits.

Clicks: updating the row on every visit would be a write to Postgres per visit. Instead `count_click` does one `INCR` on `clicks:<code>` in Redis, and a flusher loop (started in `lifespan`, every 5 seconds) moves the numbers to Postgres with `GETDEL` and one `UPDATE`. Five visits, then the stats at once and after 6 seconds:

```bash
for i in 1 2 3 4 5; do curl -s -o /dev/null localhost:8691/<code>; done
curl -s localhost:8691/links/<code>/stats
docker exec pyrepo-m18-b11-redis redis-cli GET clicks:<code>
sleep 6
curl -s localhost:8691/links/<code>/stats
docker exec pyrepo-m18-b11-redis redis-cli GET clicks:<code>
docker exec pyrepo-m18-b11-pg psql -U allcs -d links -c "SELECT code, clicks FROM links WHERE code = '<code>'"
```

```
{"code":"zXaN8e5","url":"https://allcsvideos.com/courses/sql-in-two-weeks","clicks":0,"pending":5}
"5"
{"code":"zXaN8e5","url":"https://allcsvideos.com/courses/sql-in-two-weeks","clicks":5,"pending":0}
(nil)
  code   | clicks 
---------+--------
 zXaN8e5 |      5
```

The server terminal says `flushed 5 clicks`.

### Step 5: expiry and the limit for each address

`POST /links` accepts `expires_in_days`. The redirect route asks `is_expired` and answers `410 Gone` (not 404, because the link did exist). The cache time is the smaller of one hour and the seconds left until expiry. To avoid waiting 7 days, move the time with psql:

```bash
curl -s -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com/courses/redis-basics", "expires_in_days": 7}'
docker exec pyrepo-m18-b11-pg psql -U allcs -d links -c "UPDATE links SET expires_at = now() + interval '8 seconds' WHERE code = '<code>'"
curl -s -i localhost:8691/<code>
docker exec pyrepo-m18-b11-redis redis-cli TTL link:<code>
sleep 9
curl -s -i localhost:8691/<code>
```

```
{"code":"BHASE1R",...,"expires_at":"2026-11-03T10:30:11.1..."}
UPDATE 1
HTTP/1.1 307 Temporary Redirect
(integer) 7
HTTP/1.1 410 Gone
{"error":{"code":"expired","message":"This link has expired"}}
```

The copy lives only as long as the link: the TTL was cut to fit (7 or 8 seconds). The limit: `rate_limit` (a dependency on the create route only) uses a fixed window, 10 new links per minute from one address, key `rate:<address>:<window>`:

```bash
for i in $(seq 1 12); do curl -s -o /dev/null -w "%{http_code} " -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com/courses/git"}'; done; echo
curl -s -i -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com/courses/git"}'
docker exec pyrepo-m18-b11-redis redis-cli --scan --pattern 'rate:*'
```

```
201 201 201 201 201 201 201 201 201 201 429 429 
HTTP/1.1 429 Too Many Requests
retry-after: 40
{"error":{"code":"too_many_requests","message":"Too many links, try again later"}}
rate:127.0.0.1:29884950
```

Ten times 201, then 429. `retry-after` is the seconds left in this window (yours will differ, up to 60), and the window number in the key differs. Redirects are not limited.

### Step 6: tests and a load test

The tests use their own database `links_test` and Redis database number 1. Create the test database and run:

```bash
docker exec pyrepo-m18-b11-pg psql -U allcs -d links -c "CREATE DATABASE links_test"
uv run pytest -q
```

```
........................                                                                     [100%]
24 passed in 1.01s
```

(The time differs.) The 24 tests are `test_cache.py` (second redirect does not ask Postgres, hits and misses are counted, a copy has a time to live, shorter for a link that expires soon), `test_clicks.py` (clicks wait in Redis until the flush, the flush adds to what is stored), `test_codes.py` (base 62, seven characters, different codes), `test_limits.py` (the fourth request is refused when the limit is 3, every address has its own counter, redirects are not limited) and `test_links.py` (create, five bad addresses, extra fields, the 307, the 404, odd characters, the 410, a taken code is retried).

Do the tests really guard the cache? In `app/links.py` comment out the line `cache.put_cached(code, link.url, link.expires_at)` and run `uv run pytest -q --tb=no tests/test_cache.py`: all four cache tests fail (`FFFF`). Put the line back and all 24 are green again.

Is the cache worth it? Start a second copy of the service with the cache switched off and its own Redis database, then run the load test:

```bash
CACHE_ENABLED=0 REDIS_URL=redis://localhost:18411/2 uv run uvicorn app.main:app --port 8791
uv run python load.py
```

```
best of 7 rounds, 3000 requests each
           per second  median  slowest 5%  Postgres
cache on        1065     46 ms      59 ms           1
cache off        588     55 ms     237 ms       21000
```

These numbers depend on your computer and on what else it is doing, so yours will differ (we also measured `789` and `576` requests per second in a second run). The shape stays the same: the cache gives a higher speed and a calmer slow end, and Postgres answers 1 question instead of about 21,000.

## What breaks in production

Stop Redis while the service runs:

```bash
docker stop pyrepo-m18-b11-redis
curl -s -i localhost:8691/<code>
curl -s -i -X POST localhost:8691/links -H 'content-type: application/json' -d '{"url": "https://allcsvideos.com/courses/final-demo-2"}'
docker start pyrepo-m18-b11-redis
```

A redirect still answers `307` (it came from Postgres) and a create still answers `201`; the server terminal shows warnings (`redis is down: reading from postgres`, `link not cached`, `click not counted`, `rate limit not checked`). The half second time outs make this work: without them every request would wait for Redis. The price: while Redis is away, clicks are lost and nobody is limited. Other things that break: a popular link whose copy expires (a stampede), random codes that always miss (keep a short note for "not found"), and the flusher dying (then clicks pile up in Redis).

## Common mistakes

- Using `301` instead of `307` for the redirect: browsers remember it, so you can never count, change or expire the link.
- Trusting random codes to be unique. Keep the unique rule in Postgres and retry.
- Accepting any text as an address. Use `HttpUrl`, which refuses `javascript:` and `ftp:`.
- Writing to Postgres on every visit to count clicks.
- Caching a link longer than it lives.
- A Redis client without time outs: a slow Redis would freeze the service.

## Clean up

```bash
docker rm -f -v pyrepo-m18-b11-pg pyrepo-m18-b11-redis
rm -rf .venv
```

## Next

[M18-B12 · Build an Enrollment Email Worker](../m18-b12-build-an-enrollment-email-worker/README.md)
