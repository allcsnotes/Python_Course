# M23-B16 · Capstone: Course Copilot-lite

> Video: Module 23, Build 16. Watch it first, then follow along here.

The last build of the course: a small but complete backend service, built from an empty folder in fifteen steps.
A student types a question in plain words ("how do I wait for the network") and gets the best matching lessons with a
short snippet. Students can save notes and mark lessons done. Admins can edit a lesson. A background worker keeps the
search index fresh and sends a weekly progress email.

"Lite" is honest: there is no AI model and no outside API. Search is the keyword search that is built into Postgres,
over lesson notes that this project generates with a fixed seed. Everything runs on your laptop.

## What you'll learn
- How to plan a service on paper (goal, rules, picture, tables, addresses, steps) and then build it in small steps
- How Postgres full-text search turns text into word roots (`tsvector`) and ranks matches
- How the pieces from the whole course fit together: FastAPI, SQLAlchemy and Alembic, Argon2 and JWT, a Redis cache
  and rate limit, Celery jobs, logs with a request ID, health and metrics, tests with a coverage gate, a non-root
  container and a CI pipeline
- What breaks (a stopped worker means stale search) and the honest limits of the design
- How to talk about a project like this in an interview

## Before you start
- Python 3.14 or newer. Check with `python --version` (use `python3 --version` if `python` is not found).
- [uv](https://docs.astral.sh/uv/) (module 7, lesson 3). The video used uv 0.13.x.
- Docker Desktop, running. Compose starts Postgres 17, Redis 8 and mailpit (a mail catcher: nothing is sent to the
  internet, mails stay in a web inbox on your laptop).
- `curl` and `jq` for the shell commands.
- Optional, only for step 15: [act](https://github.com/nektos/act) (module 19, lesson 3) and git.
- Free ports: 8736 (the API), 23536 (Postgres), 23436 (Redis), 23525 (mail), 23526 (mailpit inbox).
- Earlier lessons help, and each step below names the lesson it comes from.

Work on a **copy**, not in the repo, so that `git pull` keeps working:

```bash
cp -R m23-interviews-and-capstone/m23-b16-capstone-course-copilot-lite ~/copilot
cd ~/copilot
```

(Run that from the repo root. Everything below happens in `~/copilot`.)

## What we are building

**The goal, in four lines**
1. Log in with a password, and a role: student or admin.
2. Search the lesson notes in plain words and get the best lessons with a snippet.
3. Save notes and mark lessons done.
4. When an admin edits a lesson, a background worker updates the search index. Once a week every student gets a
   progress email.

**Rules for production.** Popular searches come from a Redis cache, and the cache is cleared when a lesson changes. A
student can search 20 times a minute, no more. Every log line is one JSON line with a request ID. There are health and
metrics addresses, tests that must cover 90 percent, and a pipeline that checks it all. All containers run as a normal
user, not root.

**The picture.** The client talks to the FastAPI server. The server reads and writes Postgres, which also does the
searching. Redis holds three things: the search cache, the rate-limit counters and the queue of jobs. A Celery worker
takes jobs from the queue, updates the index in Postgres and sends the weekly email to mailpit.

```
client --> FastAPI api --> Postgres (data + search)
              |
              +--> Redis (cache, rate limit, job queue) <-- Celery worker --> Postgres, mailpit
```

**Four tables**
- `users`: email (unique), name, password hash, role (default `student`)
- `lessons`: code like `M18-L01`, title, notes, and `search_vector`, the column Postgres searches, with a GIN index
- `notes`: owned by a user, attached to a lesson
- `progress`: one row per user and finished lesson, both ids together as the key

**Thirteen addresses**

| Who | Addresses |
|---|---|
| Accounts | `POST /auth/register`, `POST /auth/login`, `GET /me` |
| Students | `GET /search`, `POST /notes`, `POST /progress/{lesson_id}` (and `GET /progress`) |
| Admins | `PUT /admin/lessons/{lesson_id}`, `POST /admin/weekly-emails` |
| Operators | `GET /health/live`, `GET /health/ready`, `GET /metrics` |

## Files in this folder

```
.
├── README.md
├── pyproject.toml           project and tool settings (ruff, pyright, pytest, coverage)
├── uv.lock                  exact package versions
├── .env.example             demo settings; copy to .env
├── .gitignore  .dockerignore
├── alembic.ini
├── Dockerfile               multi-stage, runs as user "app"
├── compose.yml              postgres, redis, mailpit + migrate, api, worker
├── .github/workflows/ci.yml lint, typecheck, test, image
├── app/
│   ├── settings.py          pydantic-settings class
│   ├── db.py  models.py     engine, session, the four tables
│   ├── seed.py              40 made-up lessons + 3 demo users, and the index function
│   ├── search.py            the one SQL search statement
│   ├── security.py          Argon2 hashing, JWT
│   ├── deps.py              current_user, require_admin
│   ├── schemas.py           request and response models
│   ├── cache.py             Redis cache with a generation number
│   ├── ratelimit.py         20 searches a minute
│   ├── logs.py              JSON log formatter with request_id
│   ├── metrics.py  health.py
│   ├── mailer.py            sends to mailpit
│   ├── worker.py            Celery app, beat schedule, three tasks
│   ├── main.py              app, middleware, routers
│   └── routers/             auth.py  search.py  learn.py  admin.py
├── migrations/              Alembic (env.py edited, 0001_create_tables.py generated)
├── tests/                   29 tests
└── versions/                the small versions shown on screen: main_v1..v5.py, search_v1..v3.py,
                             compose_step2_infra.yml
```

| File | What it is |
|---|---|
| `.env.example` | Demo values only: database address, Redis address, a fake secret key, mail port. Copy it to `.env` |
| `compose.yml` | The final Compose file (step 14). The services are pinned: `postgres:17`, `redis:8`, `axllent/mailpit:v1.32.0` (the video used the `latest` tag of mailpit, which was v1.32.0) |
| `versions/compose_step2_infra.yml` | The step 2 Compose file with only the three services |
| `versions/main_v1.py` ... `main_v5.py` | `app/main.py` as it grows: auth only, then search, learn, middleware and health, and finally admin |
| `versions/search_v1.py` ... `search_v3.py` | `app/routers/search.py` as it grows: plain search, then with the cache, then with the rate limit |
| `tests/` | `conftest.py` plus six test files, 29 tests in all |

Every password, key and email in these files is fake (the demo users have the password `demo-password-23`, and the
secret key says `dev-only-secret-change-me-in-prod`). Do not reuse any of them anywhere real.

## Run it

If you only want to see the finished system working, do this. It starts everything from the containers.

```bash
cd ~/copilot
docker compose up -d --build
```

Wait about 20 seconds, then check:

```bash
docker compose ps --format "table {{.Service}}\t{{.Status}}"
```
```
SERVICE    STATUS
api        Up 12 seconds (healthy)
mailpit    Up 20 seconds (healthy)
postgres   Up 20 seconds (healthy)
redis      Up 20 seconds (healthy)
worker     Up 12 seconds
```

The `migrate` service ran once (migrations plus the seed), and exited. That is normal.

Log in as Lukas (a seeded student), search, and ask again:

```bash
API=localhost:8736
curl -s $API/health/ready | jq -c
TOKEN=$(curl -s $API/auth/login -d "username=lukas@allcsvideos.com&password=demo-password-23" | jq -r .access_token)
ask() { curl -s -G $API/search -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$1"; }
ask "how do I wait for the network" | jq -c '{cache, found: [.results[] | [.code, .rank]]}'
ask "how do I wait for the network" | jq -c '{cache, found: [.results[] | [.code, .rank]]}'
```
```
{"status":"ready","postgres":"ok","redis":"ok"}
{"cache":"miss","found":[["M12-L02",0.8],["M12-L04",0.4]]}
{"cache":"hit","found":[["M12-L02",0.8],["M12-L04",0.4]]}
```

The first answer came from Postgres (miss), the second from Redis (hit).

Meera is the seeded admin. Ask for the weekly emails:

```bash
MEERA=$(curl -s $API/auth/login -d "username=meera@allcsvideos.com&password=demo-password-23" | jq -r .access_token)
curl -s -X POST $API/admin/weekly-emails -H "Authorization: Bearer $MEERA" | jq -c
sleep 4
docker compose logs --no-log-prefix worker | grep "progress email" | sed -E 's/^[^{]*//' | jq -c '{message, to}'
```
```
{"status":"queued"}
{"message":"progress email sent","to":"priya@allcsvideos.com"}
{"message":"progress email sent","to":"lukas@allcsvideos.com"}
```

Only Lukas and Priya get a mail here because Asha does not exist yet (you register her in step 6; with all three
students you get three mails). Open the mail catcher inbox at <http://localhost:23526> to read the emails.

Stop everything when you are done (see [Clean up](#clean-up)).

## Build it step by step

Now build it yourself from an empty folder, the way the video does. The finished files are in this folder, so each
step says which files to copy in. Set a shortcut to this folder first (use the real path of your clone):

```bash
SRC=~/Python_Course/m23-interviews-and-capstone/m23-b16-capstone-course-copilot-lite
mkdir ~/copilot-build && cd ~/copilot-build
ls -la
```
```
total 0
drwxr-xr-x@  2 asha  staff   64 Oct 28 12:21 .
drwxr-xr-x@ 25 asha  staff  800 Oct 28 12:21 ..
```

Dates, owner and sizes will differ on your computer. The video plans first (the goal, rules, picture, tables and
addresses above) and then builds in these fifteen steps.

### Step 1: the project (module 7, lesson 3)

```bash
uv init --bare --name copilot
cat pyproject.toml
```
```
Initialized project `copilot`

[project]
name = "copilot"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = []
```

Add the packages. The first command is for the service, the second adds tools only you use, in the `dev` group so they
stay out of the container later:

```bash
uv add fastapi python-multipart uvicorn-worker gunicorn sqlalchemy "psycopg[binary]" alembic pydantic-settings argon2-cffi pyjwt redis "celery[redis]" prometheus-client
uv add --dev pytest pytest-cov httpx2 ruff pyright celery-types
```

uv resolves 48 packages and installs 47 (versions such as `fastapi==0.162.0`, `sqlalchemy==2.1.6`,
`celery==5.6.3`), then 13 more for the dev group (`pytest==9.2.0`, `ruff==0.17.3`, `pyright==1.1.414`). The exact
versions are pinned in `uv.lock` in this folder. If you want exactly the video's versions, copy `uv.lock` over yours
and run `uv sync`.

### Step 2: the services (module 19)

Copy the step 2 Compose file. It has only Postgres, Redis and mailpit, on ports of our own, and every service has a
`user:` line so it runs as a normal user:

```bash
cp $SRC/versions/compose_step2_infra.yml compose.yml
docker compose up -d
docker compose ps --format "table {{.Service}}\t{{.Status}}"
docker inspect -f '{{.Name}} {{.Config.User}}' $(docker compose ps -q)
```
```
SERVICE    STATUS
mailpit    Up 8 seconds (healthy)
postgres   Up 8 seconds
redis      Up 8 seconds
```
```
/m23b16-mailpit-1 1000:1000
/m23b16-postgres-1 postgres
/m23b16-redis-1 redis
```

None of them is root. (The compose project is called `m23b16`, so the names start with that.)

### Step 3: settings (module 19, lesson 2)

```bash
mkdir app && touch app/__init__.py
cp $SRC/app/settings.py app/
cp $SRC/.env.example .env
cp $SRC/.gitignore .
cat .env
uv run python -c "from app.settings import get_settings as g; s = g(); print(s.secret_key, s.search_limit)"
```
```
DATABASE_URL=postgresql+psycopg://copilot:copilot@localhost:23536/copilot
REDIS_URL=redis://localhost:23436/0
SECRET_KEY=dev-only-secret-change-me-in-prod
SMTP_PORT=23525
```
```
********** 20
```

(`.env` also starts with a comment line in the file you copied.) The database address, Redis address and secret key
have no default, so they must be given; the rest have safe defaults (a search limit of 20 a minute, a cache time of
300 seconds). Now hide the `.env` and run it again:

```bash
mv .env .env.off
uv run python -c "from app.settings import get_settings as g; g()" 2>&1 | tail -14
mv .env.off .env
```
```
pydantic_core._pydantic_core.ValidationError: 3 validation errors for Settings
database_url
  Field required [type=missing, input_value={}, input_type=dict]
redis_url
  Field required [type=missing, input_value={}, input_type=dict]
secret_key
  Field required [type=missing, input_value={}, input_type=dict]
```

(Each error also prints a "For further information" line.) The service refuses to start, at the start, not at 3 in the
morning.

### Step 4: the database (module 16)

```bash
cp $SRC/app/db.py $SRC/app/models.py app/
uv run alembic init migrations
cp $SRC/migrations/env.py migrations/
```

`alembic init` makes the folder. The copied `migrations/env.py` is changed in two ways: it reads the database address
from our settings, and it gets the metadata of our models. Now make and apply the first migration:

```bash
uv run alembic revision --autogenerate --rev-id 0001 -m "create tables"
uv run alembic upgrade head
docker compose exec postgres psql -U copilot -c "\d lessons"
```
```
INFO  [alembic.autogenerate.compare.tables] Detected added table 'lessons'
INFO  [alembic.autogenerate.compare.constraints] Detected added index 'ix_lessons_search' on '('search_vector',)'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'users'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'notes'
INFO  [alembic.autogenerate.compare.constraints] Detected added index 'ix_notes_user_id' on '('user_id',)'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'progress'
Generating .../copilot-build/migrations/versions/0001_create_tables.py ...  done
INFO  [alembic.runtime.migration] Running upgrade  -> 0001, create tables
                                       Table "public.lessons"
    Column     |           Type           | Collation | Nullable |               Default
---------------+--------------------------+-----------+----------+-------------------------------------
 id            | integer                  |           | not null | nextval('lessons_id_seq'::regclass)
 code          | character varying        |           | not null |
 title         | character varying        |           | not null |
 notes         | text                     |           | not null |
 search_vector | tsvector                 |           |          |
 updated_at    | timestamp with time zone |           | not null | now()
Indexes:
    "lessons_pkey" PRIMARY KEY, btree (id)
    "ix_lessons_search" gin (search_vector)
    "lessons_code_key" UNIQUE CONSTRAINT, btree (code)
Referenced by:
    TABLE "notes" CONSTRAINT "notes_lesson_id_fkey" FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    TABLE "progress" CONSTRAINT "progress_lesson_id_fkey" FOREIGN KEY (lesson_id) REFERENCES lessons(id)
```

(Some `INFO` lines about the autogenerate plugins are left out above.) `search_vector` has the type `tsvector`, and
`ix_lessons_search` is a GIN index: the kind of index built for searching inside text.

### Step 5: the lesson notes, and how Postgres searches text

`seed.py` generates 40 lessons with real titles from this course and six keywords each. It shuffles the keywords with
`random.Random(23)`, so you get the same text as the video every time. It also creates three demo users (Meera the
admin, Lukas and Priya students) and fills the search column.

```bash
cp $SRC/app/seed.py $SRC/app/security.py $SRC/app/search.py app/
uv run python -m app.seed
pq() { docker compose exec -T postgres psql -U copilot -At -c "$1"; }
pq "select count(*) from lessons"
pq "select title, notes from lessons where code = 'M18-L01'"
```
```
40
Redis and Caching|This lesson is about Redis and stale. Remember that expiry and invalidate always go together. Practise cache until it feels boring, then add hit.
```

How does Postgres search? It does not look for your exact words. It first turns text into a `tsvector`, a list of word
roots with their places:

```bash
pq "select to_tsvector('english', 'Redis keeps the cached answers')"
pq "select plainto_tsquery('english', 'how do I cache answers')"
pq "select to_tsvector('english', 'Redis keeps the cached answers') @@ plainto_tsquery('english', 'cache answer')"
pq "select replace(plainto_tsquery('english', 'cache expiry stale')::text, '&', '|')"
pq "select code, left(search_vector::text, 60) from lessons where code = 'M18-L01'"
```
```
'answer':5 'cach':4 'keep':2 'redi':1
'cach' & 'answer'
t
'cach' | 'expiri' | 'stale'
M18-L01|'add':26B 'alway':16B 'bore':24B 'cach':3A,20B 'expiri':13B
```

The little word "the" is gone, "cached" became `cach`, "keeps" became `keep`. The question gets the same treatment, and
`@@` asks "does this vector match this query?" That is keyword search: it matches roots, not meaning. `plainto_tsquery`
joins words with `&` (all must match), which is too strict for students, so the search swaps `&` for `|` (any word can
match; more matches rank higher). The title gets weight A and the notes weight B (the `A` and `B` after the numbers
above), so `cache` in a title ranks above `cache` in the notes. Open `app/search.py` to read the one SQL statement:
`ts_rank_cd` for the rank, `ts_headline` for the snippet with `[square brackets]`, order by rank, best five.

### Step 6: passwords and login (module 17)

`security.py` has `hash_password`, `check_password` (false, not an error, on a mismatch) and the JWT functions
(`make_token`: user id, role and a 30 minute expiry; `read_token`). `deps.py` has the guards `current_user` (bad token
is 401) and `require_admin` (any other role is 403). The auth router has register (409 on a second account with the
same email, only the hash is stored) and login (checks a dummy hash even for an unknown email, so both mistakes take
the same time and give the same answer).

```bash
cp $SRC/app/schemas.py $SRC/app/deps.py app/
mkdir app/routers && cp $SRC/app/routers/__init__.py $SRC/app/routers/auth.py app/routers/
cp $SRC/versions/main_v1.py app/main.py
uv run uvicorn app.main:app --port 8736 --no-access-log
```

Leave the server running and open a **second terminal** in `~/copilot-build` for the commands below. (After each new
step, stop the server with Ctrl+C and start it again, or add `--reload`.)

```bash
API=localhost:8736
post() { curl -s -w " %{http_code}\n" -X POST "$API$1" -H "Authorization: Bearer $TOKEN" -H "content-type: application/json" -d "$2"; }
login() { curl -s $API/auth/login -d "username=$1@allcsvideos.com&password=$2" "${@:3}"; }
post /auth/register '{"email": "asha@allcsvideos.com", "name": "Asha", "password": "correct-horse-staple"}'
login asha correct-horse-staple | jq -c '.access_token |= (.[:24] + "...")'
login asha wrong -w " %{http_code}"; echo
curl -s $API/me -w " %{http_code}"; echo
```
```
{"id":4,"email":"asha@allcsvideos.com","name":"Asha","role":"student"} 201
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5...","token_type":"bearer"}
{"detail":"wrong email or password"} 401
{"detail":"Not authenticated"} 401
```

No password anywhere in the answer. Is it safe in the database, and what is inside a token?

```bash
pq "select email, left(password_hash, 40) from users where email like 'asha%'"
tok() { login $1 demo-password-23 | jq -r .access_token; }
TOKEN=$(tok lukas)
echo ${#TOKEN} characters
curl -s $API/me -H "Authorization: Bearer $TOKEN" | jq -c
uv run python -c "import jwt, sys; print(jwt.decode(sys.argv[1], options={'verify_signature': False}))" $TOKEN
```
```
asha@allcsvideos.com|$argon2id$v=19$m=65536,t=3,p=4$ouZMg2vrZ
164 characters
{"id":2,"email":"lukas@allcsvideos.com","name":"Lukas","role":"student"}
{'sub': '2', 'role': 'student', 'iat': 1793170310, 'exp': 1793172110}
```

The column holds an Argon2 hash with its settings in front, never the password. A JWT is signed, not secret: anyone can
read the user id, role and times. Only the signature needs the secret key. (Salt, token digits and times will differ.)

### Step 7: the search address (module 15)

```bash
cp $SRC/versions/search_v1.py app/routers/search.py
cp $SRC/versions/main_v2.py app/main.py
```

Restart the server. `q` must have 2 to 100 characters (FastAPI answers 422 otherwise). Two shell helpers, then ask.
Before each answer, guess: which lessons come back, and in which order?

```bash
ask() { curl -s -G $API/search -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$1"; }
ask "how do I wait for the network" | jq -c '.results[] | [.code, .rank, .snippet]'
ask "background job retry" | jq -c '.results[] | [.code, .rank]'
ask "make my site faster" | jq -c '.results[] | [.code, .title]'
ask "speed up my code" | jq -c '.results[] | [.code, .title]'
curl -s -G $API/search -H "Authorization: Bearer $TOKEN" --data-urlencode "q=a" -w " %{http_code}"; echo
```
```
["M12-L02",0.8,"data, then change [network]. Next time, check [waiting] before you touch thread."]
["M12-L04",0.4,"[waiting]. Try a small example with event loop, then change tasks. Practise"]
["M18-L02",2.8]
["M09-L03",0.4]
["M18-L04",0.4]
["M20-L04","Making It Faster"]
["M03-L01","Making Decisions with if"]
["M11-L04","Measuring and Improving Speed"]
["M11-L04","Measuring and Improving Speed"]
["M15-L01","How the Web Works and Your First Endpoint"]
["M20-L04","Making It Faster"]
{"detail":[{"type":"string_too_short","loc":["query","q"],"msg":"String should have at least 2 characters","input":"a","ctx":{"min_length":2}}]} 422
```

Now the honest part. "make my site faster" finds the right lesson first, but second is "Making Decisions with if",
because "make" and "making" share a root. Postgres matched the word, not the meaning. "speed up my code" finds the right
lesson first, but the web lesson is second, because of the word "code". That is what "lite" means. The next step would
be embeddings with pgvector.

### Step 8: the cache (module 18, lesson 1)

`cache.py` keeps answers in Redis. The key comes from the search text (lower case, tidied spaces, hashed) plus a
**generation** number. `put` saves with a 300 second expiry. `invalidate` adds 1 to the generation, so every old key is
unreachable at once and expires by itself. The router asks the cache first and sets an `X-Cache` header.

```bash
cp $SRC/app/cache.py app/
cp $SRC/versions/search_v2.py app/routers/search.py
```

Restart the server, then:

```bash
hd() { curl -s -D - -o /dev/null "$@" | grep -iE "^HTTP|x-cache|x-request-id|retry-after"; }
askh() { hd -G $API/search -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$1"; }
rc() { docker compose exec -T redis redis-cli "$@"; }
askh "cache expiry stale"
askh "cache expiry stale"
rc --scan --pattern "search:*"
rc ttl $(rc --scan --pattern "search:*" | head -1)
secs() { curl -s -o /dev/null -w "%{time_total}s\n" -G $API/search -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$1"; }
secs "network waiting"
secs "network waiting"
```
```
HTTP/1.1 200 OK
x-cache: MISS
HTTP/1.1 200 OK
x-cache: HIT
search:0:0ee61092673f
299
0.010552s
0.002189s
```

The key is `search:<generation>:<hash>`; the time to live counts down from 300. The timings (yours will differ) show a
small gain because the table is tiny; with a big table the miss gets slower and the hit does not.

### Step 9: the rate limit (module 18, lesson 4)

`ratelimit.py` counts searches in Redis with a key for the user and the current minute and `INCR`. The first count sets a
60 second expiry. Above 20, the answer is 429 with a `Retry-After` header.

```bash
cp $SRC/app/ratelimit.py app/
cp $SRC/versions/search_v3.py app/routers/search.py
```

Restart the server. Guess first: 22 searches in one minute, limit 20, how many are 429? Start early in a clock minute
(the counter resets at the minute change):

```bash
status() { curl -s -o /dev/null -w "%{http_code} " -G $API/search -H "Authorization: Bearer $TOKEN" --data-urlencode "q=$1"; }
for i in {1..22}; do status cache; done; echo
askh cache
```
```
200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 429 429
HTTP/1.1 429 Too Many Requests
retry-after: 59
```

Twenty times 200, then two times 429. `retry-after` is the seconds until the minute ends, so yours will differ. If a
`429` shows up earlier, you used some of this minute's searches already: wait for the next minute.

### Step 10: notes and progress (module 15)

`learn.py` has notes and progress. "Mark done" inserts a row with `ON CONFLICT DO NOTHING`, so marking twice is
harmless (the word for that is **idempotent**). Progress counts the done rows and the number of lessons.

```bash
cp $SRC/app/routers/learn.py app/routers/
cp $SRC/versions/main_v3.py app/main.py
```

Restart the server (wait for a new minute if you hit the limit), then:

```bash
post /notes '{"lesson_id": 30, "body": "TTL means time to live"}'
post /progress/30
post /progress/30
post /progress/12
post /progress/999
```
```
{"id":1,"lesson_id":30,"body":"TTL means time to live"} 201
{"done":1,"total":40,"percent":2} 200
{"done":1,"total":40,"percent":2} 200
{"done":2,"total":40,"percent":5} 200
{"detail":"no such lesson"} 404
```

Marking lesson 30 twice still gives 1 of 40.

### Step 11: logs and metrics (module 14 lesson 3, module 20 lesson 1)

`logs.py` is the JSON formatter from module 14, with one extra field on every line: the `request_id`, kept in a context
variable so each request has its own. `main.py` now has a middleware that gives each request an ID (from the
`X-Request-ID` header, or a new random one), times it, counts it for Prometheus, puts the ID in the response and writes
one log line. `health.py` has `/health/live` and `/health/ready` (503 if Postgres or Redis is down). Metric labels use
the route pattern, never the raw address, so there are only a few time series.

```bash
cp $SRC/app/logs.py $SRC/app/metrics.py $SRC/app/health.py app/
cp $SRC/app/routers/search.py app/routers/
cp $SRC/versions/main_v4.py app/main.py
```

Restart the server **with its output going to a file**, so you can grep it (stop the old one first):

```bash
uv run uvicorn app.main:app --port 8736 --no-access-log > api.log 2>&1 &
```

```bash
hd $API/health/live
curl -s $API/health/ready | jq -c
askh "docker root"
```
```
HTTP/1.1 200 OK
x-request-id: ab3cf97101e9
{"status":"ready","postgres":"ok","redis":"ok"}
HTTP/1.1 200 OK
x-cache: MISS
x-request-id: 57ee9cf7c1b8
```

Use the request ID you got (yours will differ) to find the log line:

```bash
grep 57ee9cf7c1b8 api.log | jq -c
curl -s $API/metrics | grep -E "^copilot_(requests|searches)_total"
```
```
{"level":"INFO","logger":"copilot.api","request_id":"57ee9cf7c1b8","message":"request","method":"GET","path":"/search","status":200,"ms":14.0}
copilot_requests_total{method="GET",route="/health/live",status="200"} 2.0
copilot_requests_total{method="POST",route="/auth/login",status="200"} 6.0
copilot_requests_total{method="GET",route="/health/ready",status="200"} 1.0
copilot_requests_total{method="GET",route="/search",status="200"} 1.0
copilot_searches_total{cache="miss"} 1.0
```

The counts depend on what you already did. The line has the method, path, status and milliseconds.

### Step 12: the worker (module 18, lesson 2, and module 22)

Two jobs that are slow or can fail, so they run outside the request, in a Celery worker with Redis as the broker.
- `reindex_lesson`: rebuilds the search index for one lesson (the same index function as the seed), commits, then
  invalidates the cache.
- `weekly_progress_all`: finds the students and queues one `send_progress_email` for each. A beat schedule says "every
  Monday at 8, India time" (cron in Python). `send_progress_email` is idempotent: a key for the user and the week is set
  with `NX`; if it already exists the email was sent and the task stops. If sending fails, the task deletes the key and
  raises, so the automatic retries can try again.
- Both tasks take an extra `rid` argument (request ID). The admin address passes it, and the task puts it into the same
  context variable, so the worker's log lines carry the same ID as the request that started the job.

```bash
cp $SRC/app/mailer.py $SRC/app/worker.py app/
cp $SRC/app/routers/admin.py app/routers/
cp $SRC/versions/main_v5.py app/main.py
```

Restart the API, then start the worker in a **third terminal**, logging to a file:

```bash
uv run celery -A app.worker worker --pool=threads -c 2 -l INFO > worker.log 2>&1 &
sleep 8; grep -A3 "\[tasks\]" worker.log
```
```
[tasks]
  . app.worker.reindex_lesson
  . app.worker.send_progress_email
  . app.worker.weekly_progress_all
```

The worker lists the three tasks and says `ready`. Now the edit flow. A student is refused, the admin is accepted, and
the search finds the new word:

```bash
MEERA=$(tok meera)
edit() { curl -s -D - -X PUT $API/admin/lessons/$1 -H "Authorization: Bearer $2" -H "content-type: application/json" -d "{\"notes\": \"$3\"}" | grep -iE "^HTTP|x-request-id|^\{"; }
ask "aside" | jq -c '{cache, found: [.results[].code]}'
edit 30 $TOKEN "Anything"
edit 30 $MEERA "Cache aside: read the cache first. After a price change, delete the key."
sleep 3
ask "aside" | jq -c '{cache, found: [.results[].code], snippet: .results[0].snippet}'
```
```
{"cache":"miss","found":[]}
HTTP/1.1 403 Forbidden
x-request-id: 55964d2b51e3
{"detail":"admins only"}
HTTP/1.1 202 Accepted
x-request-id: e473efc143e5
{"status":"saved, search index updating"}
{"cache":"miss","found":["M18-L01"],"snippet":"[aside]: read the cache first. After a price change, delete the key."}
```

(Run these in a different clock minute from step 9, or the rate limit answers first.) The second search is a miss
because the cache was cleared, and it finds the lesson with its new text. The worker log holds the same request ID:

```bash
grep e473efc143e5 worker.log | jq -c '{request_id, message, lesson_id, generation}'
```
```
{"request_id":"e473efc143e5","message":"lesson reindexed","lesson_id":30,"generation":1}
```

Now the weekly email. Ask twice with a request ID of your choice:

```bash
curl -s -X POST $API/admin/weekly-emails -H "Authorization: Bearer $MEERA" -H "x-request-id: weekly-1"; echo
sleep 4
curl -s localhost:23526/api/v1/messages | jq -r '.total, (.messages[] | .To[0].Address + ": " + .Subject)'
curl -s -X POST $API/admin/weekly-emails -H "Authorization: Bearer $MEERA" -H "x-request-id: weekly-2"; echo
sleep 4
curl -s localhost:23526/api/v1/messages | jq -r .total
grep -E 'weekly-[12]' worker.log | grep copilot.worker | jq -c '[.request_id, .message, (.to // .user_id)]'
```
```
{"status":"queued"}
3
asha@allcsvideos.com: Your week: 0 of 40 lessons
priya@allcsvideos.com: Your week: 0 of 40 lessons
lukas@allcsvideos.com: Your week: 2 of 40 lessons
{"status":"queued"}
3
["weekly-1","weekly emails queued",null]
["weekly-1","progress email sent","lukas@allcsvideos.com"]
["weekly-1","progress email sent","priya@allcsvideos.com"]
["weekly-1","progress email sent","asha@allcsvideos.com"]
["weekly-2","weekly emails queued",null]
["weekly-2","already sent",2]
["weekly-2","already sent",3]
["weekly-2","already sent",4]
```

Three mails (one per student), and after the second call nothing new arrives: one email per student per week, even when
the job runs twice. Open <http://localhost:23526> to read Lukas's mail ("2 of 40 lessons"). The order of the lines in the
log can differ, because two tasks run at once. Stop the API and the worker with Ctrl+C in their terminals (or `pkill -f uvicorn; pkill -f celery` if you started them in the background).

### Step 13: tests and checks (module 13)

The tests run against a real test database and Redis database 15. No mocks for these, because the search is SQL and the
cache is Redis. `conftest.py` creates the `copilot_test` database if it is missing, runs the migrations, and empties
the tables after every test. Celery runs in eager mode, so a job runs at once inside the test. The tool settings
(line length 60, rule sets, pyright for Python 3.14, where coverage looks) are in the `[tool.*]` sections at the end of
`pyproject.toml`; copy the whole file when you reach this step, and copy the tests:

```bash
cp $SRC/pyproject.toml .
cp -R $SRC/tests .
uv sync
uv run pytest -q
```
```
.............................                                                                [100%]
29 passed in 3.22s
```

Twenty-nine tests: login and roles, search and cache, the rate limit, notes and progress, the jobs, health, metrics and
the log format. One test edits a lesson as an admin and checks that the old word finds nothing and the new word finds
the lesson: it covers the worker, the index and the cache clearing together. Add `-v` to see all the names.

Now the coverage gate. Ask for 99 percent: it fails even though every test passed. Ask for 90, which the pipeline will
require:

```bash
uv run pytest -q --cov --cov-fail-under=99 --cov-report=
uv run pytest -q --cov --cov-fail-under=90 --cov-report=term-missing:skip-covered
```
```
ERROR: Coverage failure: total of 97 is less than fail-under=99
FAIL Required test coverage of 99% not reached. Total coverage: 96.88%
29 passed in 2.44s
```
```
Name            Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------
app/deps.py        21      1      4      1    92%   23
app/health.py      30      2      2      0    94%   26-27
app/logs.py        19      1      6      1    92%   26
app/mailer.py      15      3      0      0    80%   25-29
app/seed.py        44      5     12      1    89%   118-121, 125
app/worker.py      57      1      6      0    98%   35
-----------------------------------------------------------
TOTAL                468     13     44      3    97%

16 files skipped due to complete coverage.
Required test coverage of 90% reached. Total coverage: 96.88%
29 passed in 2.92s
```

The table lists the lines no test visits. Then the other two checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
```
```
All checks passed!
30 files already formatted
0 errors, 0 warnings, 0 informations
```

(`30 files` is for the project as built in the video. If you also copied the `versions/` folder it says more.) Pyright
needs two small casts for the Redis answers, which is honest: the library cannot tell the type from here.

### Step 14: the container (module 19, lessons 1 and 4)

A multi-stage `Dockerfile`: the build stage has uv and installs the locked packages (`uv sync --locked --no-dev`); the
runtime stage copies only the virtual environment and the code, creates a user called `app`, switches to it, and starts
gunicorn with the Uvicorn worker. Then the final `compose.yml` runs this image in three roles: `migrate` (alembic
upgrade plus the seed, once, when Postgres is healthy), `api` (waits for the migration and Redis, health check on the
`ready` address) and `worker` (the same image with a `celery` command). An anchor (`x-app`) shares the image and
settings between the three.

```bash
docker compose down
cp $SRC/Dockerfile $SRC/.dockerignore .
cp $SRC/compose.yml .
docker build -t m23b16-copilot:1 .
docker images m23b16-copilot:1 --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
docker run --rm m23b16-copilot:1 id
```
```
REPOSITORY       TAG       SIZE
m23b16-copilot   1         351MB
uid=1000(app) gid=1000(app) groups=1000(app)
```

The image is about 351 MB (the full `python:3.14` image is 1.64 GB), and `id` says it runs as `app`, not root. Sizes
depend on your platform. Start everything:

```bash
docker compose up -d
sleep 10
docker compose ps --format "table {{.Service}}\t{{.Status}}"
docker inspect -f '{{.Name}} {{.Config.User}}' $(docker compose ps -q)
```
```
SERVICE    STATUS
api        Up 10 seconds (healthy)
mailpit    Up 23 seconds (healthy)
postgres   Up 23 seconds (healthy)
redis      Up 23 seconds (healthy)
worker     Up 10 seconds
```
```
/m23b16-api-1 app
/m23b16-mailpit-1 1000:1000
/m23b16-postgres-1 postgres
/m23b16-redis-1 redis
/m23b16-worker-1 app
```

`migrate` ran and exited, then `api` and `worker` started. All of them are normal users. The API is on
<http://localhost:8736>, so the commands from the [Run it](#run-it) section work now.

### Step 15: the pipeline (module 19, lesson 3)

`.github/workflows/ci.yml` has four jobs. `lint` runs ruff, `typecheck` runs pyright; each installs uv at a fixed
version (0.13.6) with Python 3.14 and syncs with `--locked` (the lock file must be up to date). `test` starts Postgres
and Redis as services on ports of their own (23538 and 23438), points the tests at them with two variables
(`TEST_DATABASE_URL`, `TEST_REDIS_URL`) and runs pytest with the coverage gate of 90. `image` needs the other three jobs
and then builds the container. On GitHub it would push the image; here it only builds.

Keep the project in a local git repository. Nothing is pushed anywhere:

```bash
mkdir -p .github/workflows && cp $SRC/.github/workflows/ci.yml .github/workflows/
git init -b main
git add .
git commit -m "Course Copilot-lite"
```

Then run the very same workflow on your laptop, in containers, with act (the first run pulls a big runner image):

```bash
act push -P ubuntu-latest=catthehacker/ubuntu:act-latest --container-architecture linux/arm64 --pull=false --concurrent-jobs 1
```

(On an Intel machine leave out `--container-architecture`. Run `act` from the folder that holds `.github`, with the
Compose stack from step 14 stopped if you get a "port is already allocated" error.) The last lines of each job in the
video:

```
[ci/lint     ]   | All checks passed!
[ci/lint     ]   | 30 files already formatted
[ci/lint     ] Job succeeded
[ci/typecheck]   | 0 errors, 0 warnings, 0 informations
[ci/typecheck] Job succeeded
[ci/test     ]   | Required test coverage of 90% reached. Total coverage: 96.88%
[ci/test     ]   | 29 passed in 2.05s
[ci/test     ] Job succeeded
[ci/image    ]   Success - Main docker build -t copilot:ci .
[ci/image    ] Job succeeded
```

Every job succeeded: the pipeline is green. (The act output is shown as in the video; the pipeline checks themselves are
the same commands you ran in step 13 and 14.)

## What breaks, and the honest limits

**The worker is down.** Stop it, edit lesson 25 as Meera, and search for the new word:

```bash
docker compose stop worker
curl -s -o /dev/null -w "%{http_code}\n" -X PUT $API/admin/lessons/25 -H "Authorization: Bearer $MEERA" -H "content-type: application/json" -d '{"notes": "Prefetch loads related rows at once. Use selectinload to stop the N plus one problem."}'
ask "selectinload" | jq -c '{cache, found: [.results[].code]}'
docker compose exec redis redis-cli llen celery
docker compose start worker
sleep 6
ask "selectinload" | jq -c '{cache, found: [.results[].code]}'
```
```
202
{"cache":"miss","found":[]}
1
{"cache":"miss","found":["M16-L03"]}
```

Saving still answers 202, because saving does not need the worker, but the search finds nothing: the index is stale and
one job waits in Redis (`llen celery` is 1). Start the worker and it picks up the job; a few seconds later the lesson is
found. Nothing was lost, because the queue kept the job, but for a while search was out of date and nobody was told. In
production you **alert on the length of the queue**.

**Four honest limits**
1. Keyword search matches words, not meaning, so a student has to guess the words. Next step: embeddings with pgvector.
2. Any edit clears the whole search cache: simple, but wasteful on a busy site.
3. The limit counts in fixed windows, so 20 at the end of one minute and 20 at the start of the next can both pass.
4. The secret key in this Compose file is for the demo only. A real deployment reads it from a secret store.

## Common mistakes
- **Starting the tests without Postgres and Redis.** The tests need the step 2 services (or the full Compose stack)
  running on ports 23536 and 23436.
- **Forgetting to restart the server after copying a file.** Without `--reload`, uvicorn keeps the old code.
- **Running the rate-limit demo late in the minute.** The counter resets at the minute change, so the 429s come at a
  different count. Start early in a minute.
- **Searching for the new word before the worker has finished.** Editing returns 202 at once. The index changes a moment
  later, in the worker. Wait a second or two.
- **Having no worker running.** Edits and weekly emails queue up in Redis and nothing happens until it starts.
- **Putting the real `.env` in git or in the image.** `.env` is in `.gitignore` and `.dockerignore`. Only `.env.example`
  with fake demo values belongs in the repo.
- **Port already in use.** Another service on 8736, 23536, 23436, 23525 or 23526 stops Compose or uvicorn from starting.
  Stop the other service, or run one lab at a time.
- **Trusting the JWT to be secret.** Anyone can read what is inside it; only the signature needs the secret key.

## Extensions to try
- Refresh tokens (module 17).
- pgvector, to compare word search with meaning search.
- An OpenTelemetry trace across the API and the worker (module 20).
- A Locust load test of the search address (module 20).
- A real server, with the steps of module 19, lesson 4.

## Interview tip

Rahul asks: "Tell me about a project you built."

> I built a study helper for a video course. Search uses Postgres full-text search, with a Redis cache that I clear by
> changing a generation number. A Celery worker rebuilds the index after an edit. And something broke: while the worker
> was down, search was stale. So now I watch the length of the queue.

Three points to take away:
1. Plan on paper, then build in small steps, with small files that each do one job: settings, models, search, security,
   cache, limit and worker.
2. Production is more than endpoints: a cache with a way to clear it, a limit, logs with a request ID, health and
   metrics, tests with a coverage gate, a container that is not root, and a pipeline.
3. Know what your tool really does. Keyword search matches word roots, not meaning, and a background job can lag behind.
   Say that out loud, and measure it.

**Your turn** (pause the video and try): add a delete-note address with a test. Add a popular-searches address with a
Redis sorted set. Change the rate limit to 10, and watch the pipeline turn red until you update the test.

## Clean up

Stop and remove everything this lesson created: the containers, their network and the database and cache data, and the
image.

```bash
cd ~/copilot            # or ~/copilot-build, whichever you used
docker compose down -v --remove-orphans
docker rmi m23b16-copilot:1
```

If you built step by step with the step 2 Compose file and the later one, run `docker compose down -v` in the same
folder once for each. If you ran act, remove its leftovers: `docker ps -a --format '{{.Names}}' | grep '^act-'` lists
the containers (remove them with `docker rm -f`). Then delete the folders (`rm -r ~/copilot ~/copilot-build`) when you
no longer need them. The `.venv` inside them is plain files; nothing was installed globally.

## Next

This was the last build of the course. Keep going with the [Final Practice Sheet](../../practice/m23-interviews-and-capstone/):
fifty interview questions with model answers, and ten build-it-yourself tasks.
