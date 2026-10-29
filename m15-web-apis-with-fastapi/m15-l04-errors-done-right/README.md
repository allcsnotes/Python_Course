# M15-L04 · Errors Done Right

> Video: Module 15, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Why `200` with an empty body is a quiet failure, and how to answer with the right status code instead
- `HTTPException`, your own error classes in a `domain.py` that knows nothing about the web, and exception handlers
- One shape for every error: `{"error": {"code": ..., "message": ...}}`, even for FastAPI's own 404 and 422 errors
- A crash handler that logs the traceback with an error id and never leaks details to the caller
- Testing the error contract with pytest and `TestClient`

## Before you start

- Python 3.14 or newer (`python --version`) and `uv`. No Docker is needed.
- A project with `fastapi[standard]` and `pytest`: `uv add "fastapi[standard]"` and `uv add --dev pytest`. (Run below: FastAPI 0.162.0, pytest 9.x.)
- Follows [M15-L03](../m15-l03-pydantic-models/). Logging basics are from Module 14, Lesson 3.
- Copy this folder's `.py` files into one project folder: the files import each other. Each demo is one app module, started with `uv run python -m uvicorn <module>:app --port 8154`. Run the `curl` commands in a second terminal, and stop the server with Control C between demos.

In every output below the `date:` line is shown as `...` and the `server:` and `content-length:` headers are left out. `content-type` is shown only when it is not JSON.

## Files in this folder

| File | What it is |
|------|------------|
| `store.py` | The two courses (ids 1 and 2) as a dictionary |
| `hook.py` | The problem: `courses.get(...)` returns `None`, answered with `200` |
| `http_exc.py` | Fix 1: `raise HTTPException(404, ...)` |
| `domain.py` | Business rules with no web code: `CourseNotFound`, `AlreadyEnrolled`, `find_course`, `enrol` |
| `d_app.py` | Handlers that turn the domain errors into 404 and 409 |
| `api.py` | The consistent error shape: helper `error(...)`, handlers for domain errors and `HTTPException` |
| `api_f0.py` | Adds `GET /courses?limit=` and shows the default 422 body |
| `api_f.py` | Adds a handler for `RequestValidationError` |
| `db.py` | A stand-in for a database that is down (raises `RuntimeError`) |
| `g0.py` | A crash with no handler: plain `500` |
| `g_bad.py` | The bad crash handler that leaks the message |
| `g_good.py` | The good crash handler: error id, log, calm message |
| `test_api.py` | Three tests for the error contract |
| `p_return.py` | Pitfall: `return HTTPException(...)` |
| `p_status.py` | Pitfall: a handler with no status code |

## Follow along

### 1. The quiet failure (`hook.py`)

```bash
uv run python -m uvicorn hook:app --port 8154
```

```bash
curl -i localhost:8154/courses/1
curl -i localhost:8154/courses/99
```

```
HTTP/1.1 200 OK
...
{"id":1,"title":"Python","price":499}

HTTP/1.1 200 OK
...
null
```

Course 99 does not exist, but the server says success with a body of `null`. Lukas's page shows a blank. The cure: say clearly what went wrong, with the right status code.

Status codes come in families by their first digit. `2xx`: it worked. `4xx`: the caller made a mistake. `5xx`: we made a mistake. The ones you will use most: `400` bad request, `404` not found, `409` conflict (clashes with something that exists, like enrolling twice), `422` wrong shape, `500` our own bug. (`401` and `403` come in the security module.)

### 2. HTTPException (`http_exc.py`)

```python
from fastapi import FastAPI, HTTPException

from store import courses

app = FastAPI()


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    course = courses.get(course_id)
    if course is None:
        raise HTTPException(
            status_code=404,
            detail=f"Course {course_id} not found",
        )
    return course
```

```bash
uv run python -m uvicorn http_exc:app --port 8154
curl -i localhost:8154/courses/99
curl -i localhost:8154/courses/1
```

```
HTTP/1.1 404 Not Found
...
{"detail":"Course 99 not found"}

HTTP/1.1 200 OK
...
{"id":1,"title":"Python","price":499}
```

FastAPI catches the raised exception and builds the answer. But now the function that finds a course knows about `404`, a web idea. A nightly script that reuses it would not want that.

### 3. Your own errors and handlers (`domain.py`, `d_app.py`)

`domain.py` holds the rules of the school and no web code at all:

```python
class CourseNotFound(Exception):
    pass


class AlreadyEnrolled(Exception):
    pass


def find_course(course_id):
    if course_id not in courses:
        raise CourseNotFound(course_id)
    return courses[course_id]
```

(`enrol` calls `find_course`, then raises `AlreadyEnrolled` if the pair is already in the `enrolled` set. Lukas is enrolled in course 1 from the start.) `d_app.py` translates each class with `@app.exception_handler(...)`, and the endpoints become one line each:

```python
@app.exception_handler(domain.CourseNotFound)
def not_found(request, exc):
    body = {"detail": f"Course {exc} not found"}
    return JSONResponse(body, status_code=404)
```

```bash
uv run python -m uvicorn d_app:app --port 8154
curl -i localhost:8154/courses/99
curl -i -X POST localhost:8154/enrol/Priya/1
curl -i -X POST localhost:8154/enrol/Lukas/1
```

```
HTTP/1.1 404 Not Found
...
{"detail":"Course 99 not found"}

HTTP/1.1 200 OK
...
{"student":"Priya","course":1}

HTTP/1.1 409 Conflict
...
{"detail":"Lukas is already enrolled"}
```

`HTTPException` is quick for a one-off check. Your own classes keep the rules free of the web, work in scripts too, and one handler serves every endpoint that can raise that error.

### 4. One shape for every error (`api.py`)

Priya's page should need one branch, not three. The shape: `{"error": {"code": "...", "message": "..."}}`. Machines read the code, people read the message, and the status code is still the first line. A helper builds it:

```python
def error(status, code, message, **more):
    body = {"code": code, "message": message, **more}
    return JSONResponse({"error": body}, status_code=status)
```

FastAPI's own 404 for an unknown path is an `HTTPException` from the library underneath (Starlette), so `api.py` handles that class too.

```bash
uv run python -m uvicorn api:app --port 8154
curl -i localhost:8154/nothing
curl -i localhost:8154/courses/99
curl -i -X POST localhost:8154/enrol/Lukas/1
```

```
HTTP/1.1 404 Not Found
...
{"error":{"code":"http_error","message":"Not Found"}}

HTTP/1.1 404 Not Found
...
{"error":{"code":"course_not_found","message":"Course 99 not found"}}

HTTP/1.1 409 Conflict
...
{"error":{"code":"already_enrolled","message":"Lukas is already enrolled"}}
```

### 5. Reshape the validation error (`api_f0.py`, `api_f.py`)

`api_f0.py` adds `GET /courses` with `limit: int = 10`. A bad limit gives FastAPI's own `422`, with a noisy list:

```bash
uv run python -m uvicorn api_f0:app --port 8154
curl -i "localhost:8154/courses?limit=abc"
```

```
HTTP/1.1 422 Unprocessable Content
...
{"detail":[{"type":"int_parsing","loc":["query","limit"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

`api_f.py` adds a handler for `RequestValidationError` that keeps only the field name (the last part of `loc`) and the message:

```bash
uv run python -m uvicorn api_f:app --port 8154
curl -i "localhost:8154/courses?limit=abc"
curl -i "localhost:8154/courses?limit=1"
```

```
HTTP/1.1 422 Unprocessable Content
...
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"limit","problem":"Input should be a valid integer, unable to parse string as an integer"}]}}

HTTP/1.1 200 OK
...
[{"id":1,"title":"Python","price":499}]
```

### 6. The worst case: a bug nobody planned for (`g0.py`)

`g0.py` calls `db.connect()`, which raises `RuntimeError("cannot connect to db:5432 as asha")` (a made-up message). With no handler:

```bash
uv run python -m uvicorn g0:app --port 8154
curl -i localhost:8154/courses/1/students
```

```
HTTP/1.1 500 Internal Server Error
...
content-type: text/plain; charset=utf-8
Internal Server Error
```

Three plain words: Lukas learns nothing, which is good. The server log has the traceback (the middle lines are cut here):

```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
...
  File "g0.py", line 7, in students
    db.connect()
  File "db.py", line 3, in connect
    raise RuntimeError("cannot connect to db:5432 as asha")
RuntimeError: cannot connect to db:5432 as asha
```

### 7. The helpful handler that leaks (`g_bad.py`)

```python
@app.exception_handler(Exception)
def crash(request, exc):
    return error(500, "server_error", str(exc))
```

```
HTTP/1.1 500 Internal Server Error
...
{"error":{"code":"server_error","message":"cannot connect to db:5432 as asha"}}
```

Now a stranger knows the database server name, its port and a user name. A raw message or a traceback is for the logs, never for the response.

### 8. The right crash handler (`g_good.py`)

```python
@app.exception_handler(Exception)
def crash(request, exc):
    error_id = uuid.uuid4().hex[:8]
    log.error("error %s", error_id, exc_info=exc)
    return error(500, "server_error", "Something went wrong",
                 error_id=error_id)
```

```bash
uv run python -m uvicorn g_good:app --port 8154
curl -i localhost:8154/courses/1/students
```

```
HTTP/1.1 500 Internal Server Error
...
{"error":{"code":"server_error","message":"Something went wrong","error_id":"7f09e7ae"}}
```

The `error_id` is random: yours will differ. In the server terminal the same id appears with the full traceback:

```
error 7f09e7ae
Traceback (most recent call last):
...
  File "g_good.py", line 12, in students
    db.connect()
  File "db.py", line 3, in connect
    raise RuntimeError("cannot connect to db:5432 as asha")
RuntimeError: cannot connect to db:5432 as asha
```

Lukas sends support the id, support searches the log, and finds everything.

### 9. Test the contract (`test_api.py`)

`TestClient` calls the app in memory, with no server. `raise_server_exceptions=False` makes it return the `500` a real client would receive, instead of re-raising the crash.

```bash
uv run pytest -v
```

```
test_api.py::test_missing_course PASSED              [ 33%]
test_api.py::test_double_enrol PASSED                [ 66%]
test_api.py::test_crash_hides_details PASSED         [100%]

==================== 3 passed in 0.63s =====================
```

(The header lines with platform and versions are left out, and the library prints one warning about the test client, which is also left out. The time will differ.) A test now fails if anybody leaks `db:5432` again.

## Common mistakes

1. `return HTTPException(...)` instead of `raise`. With `p_return.py`:

   ```bash
   uv run python -m uvicorn p_return:app --port 8154
   curl -i localhost:8154/courses/99
   ```

   ```
   HTTP/1.1 200 OK
   ...
   {"status_code":404,"detail":"Not found","headers":null}
   ```

   The exception was returned like any value, so the real status is `200`. An error must be raised, never returned.
2. A handler with no status code. With `p_status.py` the body says `{"error":"Course 99 not found"}` but the status line is `HTTP/1.1 200 OK`: `JSONResponse` uses `200` by default. Browsers, monitoring and retry libraries believe the status, so always pass it.
3. The wrong family. A bad course id is the caller's mistake: use `4xx`. Answering `500` turns monitoring red and wakes Asha for nothing. Hiding a real crash behind a `4xx` makes outages invisible.
4. Returning `str(exc)` or a traceback in the response. Log it with an error id; send only the id.

## Clean up

Stop the server with Control C. Nothing else was created.

## Next

[M15-L05 · Dependencies, Routers and Middleware](../m15-l05-dependencies-routers-and-middleware/)
