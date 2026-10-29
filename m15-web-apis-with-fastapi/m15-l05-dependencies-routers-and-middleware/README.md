# M15-L05 · Dependencies, Routers and Middleware

> Video: Module 15, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- Dependencies with `Depends`: hand an endpoint what it needs (a store, paging, a course lookup, a login check)
- Helpers with `yield` that clean up after the request, even when the endpoint fails
- Swapping a helper in a test with `app.dependency_overrides`
- Splitting an app into routers and a package layout, with shared helpers in `deps.py`
- Middleware that logs every request with its time, and what CORS really is
- Three traps: a circular import, round brackets after the helper, an override that is never cleared

## Before you start

- Python 3.14 or newer (`python --version`) and `uv`. No Docker is needed.
- A project with `fastapi[standard]` and `pytest`: `uv add "fastapi[standard]"` and `uv add --dev pytest`. (Run below: FastAPI 0.162.0, pytest 9.2.0, uvicorn 0.54.0, Starlette 1.10.0.)
- Follows [M15-L04](../m15-l04-errors-done-right/). Dependency injection as an idea is from Module 14, Lesson 4; tests are from Module 13.
- Run every command from inside this folder unless the step says otherwise. The server demos use port 8155; run the `curl` commands in a second terminal and stop each server with Control C. `uv run python -m uvicorn ...` works the same as `uvicorn ...`.

## Files in this folder

| File | What it is |
|------|------------|
| `store.py` | A small in-memory `Store` class, starting with two courses |
| `hook_app.py`, `test_hook.py` | The problem: one store in the file, two tests that share it |
| `deps_app.py` | Fix: `get_store` and `Depends(get_store)` |
| `annotated_demo.py` | The same dependency written with `Annotated` |
| `deps_more.py` | Four helpers: paging, course-or-404, login key, and the store |
| `yield_demo.py` | A helper with `yield` and `finally` |
| `test_fixed.py` | Tests with a fixture that overrides `get_store` |
| `test_auth.py` | Overriding the login check `require_key` |
| `test_leak.py` | Trap: an override that is never cleared |
| `catalog/app/...` | The router layout: `main.py`, `deps.py`, `store.py`, `routers/courses.py`, `routers/students.py` |
| `mw_app.py` | Logging middleware with a timing header |
| `cors_app.py` | `CORSMiddleware` with one allowed site |
| `bad_brackets.py` | Trap: `Depends(get_store())` |
| `bad_circular/app/...` | Trap: the router imports the helper from `main.py` |
| `pytest.ini` | Hides one harmless library warning from the test client |

## Follow along

### 1. The problem: tests that share a store

`hook_app.py` creates `store = Store()` in the file and both endpoints use it directly. `test_hook.py` adds a Rust course in test one and expects two courses in test two:

```bash
uv run pytest test_hook.py
```

You should see (the first lines and paths will differ):

```
test_hook.py .F                                [100%]

>       assert len(courses) == 2
E       AssertionError: assert 3 == 2
E        +  where 3 = len([{'id': 1, 'title': 'Python Basics', 'price': 499}, {'id': 2, 'title': 'Web APIs', 'price': 799}, {'id': 3, 'title': 'Rust', 'price': 999}])

FAILED test_hook.py::test_list_courses - AssertionE...
============ 1 failed, 1 passed in 0.27s ============
```

Rust is still in the one store that lives in the file. The result depends on which test ran first. Every endpoint also repeats the same lines, and a test can never hand an endpoint a different store.

### 2. Depends (`deps_app.py`)

A dependency is a function that FastAPI calls for you, before your endpoint runs, and whose answer it hands to the endpoint. The endpoint's parameters are the order slip.

```python
def get_store() -> Store:
    return STORE


@app.get("/courses")
def list_courses(store: Store = Depends(get_store)):
    return list(store.courses.values())
```

There are no round brackets after `get_store`: you hand FastAPI the function itself, and it calls it on every request.

```bash
uv run uvicorn deps_app:app --port 8155
```

```bash
curl -s localhost:8155/courses/2
curl -s localhost:8155/courses/9
```

```
{"id":2,"title":"Web APIs","price":799}
{"detail":"Course not found"}
```

Newer FastAPI docs write the same thing with `Annotated[Store, Depends(get_store)]`. `uv run python annotated_demo.py` prints `200`: same behaviour.

### 3. More helpers (`deps_more.py`)

- `paging(limit=10, offset=0)` declares query parameters and returns them in a dictionary.
- `get_course_or_404(course_id, store=Depends(get_store))` is a helper with a helper of its own: FastAPI builds the chain (store, then this helper, then the endpoint).
- `require_key(x_api_key=Header(default=None))` reads the header `x-api-key` (underscores become dashes) and raises `401` unless it is the demo key `secret-key`.
- `delete_course` lists the check in the decorator as `dependencies=[Depends(require_key)]`: it needs the check to run first, not its answer.

```bash
uv run uvicorn deps_more:app --port 8155
```

```bash
curl -s "localhost:8155/courses?limit=1"
curl -si -X DELETE localhost:8155/courses/1 | head -1
curl -si -X DELETE -H "x-api-key: secret-key" localhost:8155/courses/1 | head -1
curl -s localhost:8155/courses/1
```

```
[{"id":1,"title":"Python Basics","price":499}]
HTTP/1.1 401 Unauthorized
HTTP/1.1 204 No Content
{"detail":"Course not found"}
```

### 4. Helpers that clean up (`yield_demo.py`)

Everything before `yield` is the set-up, the value is handed to the endpoint, and everything after is the clean-up. `finally` makes sure it runs even if the endpoint fails.

```bash
uv run python yield_demo.py
```

```
open session
handling with SESSION
close session
200
open session
about to fail
close session
500
```

The error did not skip the clean-up. In Module 16 the `yield` will hand over a database session; the shape stays the same.

### 5. Swap a helper in a test (`test_fixed.py`)

```python
@pytest.fixture
def client():
    app.dependency_overrides[get_store] = lambda: Store()
    yield TestClient(app)
    app.dependency_overrides.clear()
```

```bash
uv run pytest test_fixed.py -v
```

```
test_fixed.py::test_add_course PASSED          [ 33%]
test_fixed.py::test_list_courses PASSED        [ 66%]
test_fixed.py::test_empty_store PASSED         [100%]

================= 3 passed in 0.22s ==================
```

Every test gets a fresh store, so the order no longer matters, and the endpoint code did not change. The same trick switches off a login check (`test_auth.py`):

```bash
uv run pytest test_auth.py -v
```

```
test_auth.py::test_delete_needs_a_key PASSED   [ 50%]
test_auth.py::test_delete_with_key_switched_off PASSED [100%]

================= 2 passed in 0.25s ==================
```

(The header lines with platform and paths are left out; times will differ.)

### 6. Routers and a project layout (`catalog/`)

```bash
cd catalog
find app -name '*.py' | sort
```

```
app/__init__.py
app/deps.py
app/main.py
app/routers/__init__.py
app/routers/courses.py
app/routers/students.py
app/store.py
```

Shared helpers live in `deps.py`. `routers/courses.py` is a small app with `APIRouter(prefix="/courses", tags=["courses"])`, so its list endpoint uses the empty path `""` and the get-one endpoint `"/{course_id}"`. `main.py` is the front desk:

```python
app = FastAPI(title="allcsvideos catalog")
app.include_router(courses.router)
app.include_router(students.router)


@app.get("/health")
def health():
    return {"status": "ok"}
```

A new topic is one new file and one `include_router` line. Run it from the folder that contains `app`:

```bash
uv run uvicorn app.main:app --port 8155
```

```bash
curl -s localhost:8155/courses/1
curl -s localhost:8155/students
curl -s localhost:8155/health
```

```
{"id":1,"title":"Python Basics","price":499}
["Lukas","Priya"]
{"status":"ok"}
```

### 7. Middleware (`mw_app.py`)

A dependency belongs to one endpoint and hands it a value. Middleware wraps every request, sees it on the way in and the response on the way out, and fills in no parameters. This one logs method, path, status and time, and adds an `X-Process-Time` header:

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time"] = f"{ms:.0f}ms"
    ...
    return response
```

```bash
uv run uvicorn mw_app:app --port 8155 --no-access-log
```

```bash
curl -s localhost:8155/courses
curl -s localhost:8155/slow
curl -si localhost:8155/nope | head -1
curl -si localhost:8155/slow | grep -i process
```

```
[{"id":1,"title":"Python Basics"}]
{"slept":0.3}
HTTP/1.1 404 Not Found
x-process-time: 302ms
```

The server window logs one line per request (the milliseconds will differ; the `/slow` endpoint sleeps 300 ms):

```
INFO catalog: GET /courses -> 200 in 3 ms
INFO catalog: GET /slow -> 200 in 304 ms
INFO catalog: GET /nope -> 404 in 0 ms
INFO catalog: GET /slow -> 200 in 302 ms
```

Even the `404` is logged. With several middleware, the one you add last is the outermost and sees the request first.

### 8. CORS, honestly (`cors_app.py`)

An origin is scheme + host + port. A script on one origin may read an answer from another origin only if that server says it is okay, and the browser enforces this, not your server. `CORSMiddleware` adds the permission headers:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://allcsvideos.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["x-api-key"],
)
```

```bash
uv run uvicorn cors_app:app --port 8155
```

`curl` pretends to be a browser by sending an `Origin` header. The real site, a stranger, and a preflight (the `OPTIONS` question a browser asks before a risky request):

```bash
curl -si -H "Origin: https://allcsvideos.com" localhost:8155/courses | grep -i -e ^http -e ^access
curl -si -H "Origin: https://evil.example" localhost:8155/courses | grep -i -e ^http -e ^access
curl -si -X OPTIONS -H "Origin: https://allcsvideos.com" -H "Access-Control-Request-Method: POST" localhost:8155/courses | grep -i -e ^http -e ^access
```

```
HTTP/1.1 200 OK
access-control-allow-origin: https://allcsvideos.com

HTTP/1.1 200 OK

HTTP/1.1 200 OK
access-control-allow-methods: GET, POST
access-control-max-age: 600
access-control-allow-headers: Accept, Accept-Language, Content-Language, Content-Type, x-api-key
access-control-allow-origin: https://allcsvideos.com
```

(The blank lines separate the three commands; the order of the `access-control-` lines can differ.) The stranger also gets `200` and the data; only the permission header is missing, so a browser refuses to hand the answer to the script. CORS never stops `curl`, a phone app, or an attacker's own program: it is not security. `allow_origins=["*"]` is fine for a public read-only API, but browsers refuse a star together with cookies or logins.

## Common mistakes

1. A circular import. `bad_circular/app/main.py` imports the router, and the router imports `get_store` from `main`:

   ```bash
   cd bad_circular
   python -c "from app.main import app"
   ```

   ```
   ImportError: cannot import name 'get_store' from partially initialized module 'app.main' (most likely due to a circular import) (app/main.py)
   ```

   Put shared helpers in `deps.py`; both `main` and the routers import from there. Dependencies point downwards, never back up to `main`.
2. Round brackets after the helper. `Depends(get_store())` calls it once while the file loads:

   ```bash
   python -c "import bad_brackets"
   ```

   The last line of the traceback (the middle is long, and the address will differ) is:

   ```
   TypeError: <store.Store object at 0x1076538c0> is not a callable object
   ```

   FastAPI needs something it can call on every request. Write `Depends(get_store)`.
3. An override that is never cleared. `test_leak.py` sets an empty store in test one and forgets to clear it:

   ```bash
   uv run pytest test_leak.py
   ```

   ```
   >       assert len(client.get("/courses").json()) == 2
   E       AssertionError: assert 0 == 2
   ```

   Always put back what you swapped: clear the overrides after the `yield` in the fixture.

(`test_hook.py` and `test_leak.py` fail on purpose.)

## Clean up

Stop any running server with Control C. Nothing else was created.

## Next

[M15-L06 · Async Endpoints, Background Tasks and Docs](../m15-l06-async-endpoints-background-tasks-and-docs/)
