# M15-L02 · Parameters, Bodies and Responses

> Video: Module 15, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Path parameters (`/courses/2`) and how type hints convert and check them
- Query parameters (`?level=beginner&max_price=450`) with defaults
- The request body, and the methods POST, PUT and DELETE
- Status codes that answer them: 201 created, 204 no content, 404 not found, 422 wrong shape
- Response models: decide what leaves your server, so an internal field never leaks

## Before you start

- Python 3.14 or newer (`python --version`) and `uv`. No Docker is needed.
- The project from [M15-L01](../m15-l01-how-the-web-works-and-your-first-endpoint/): a folder with `fastapi[standard]` added (`uv add "fastapi[standard]"`).
- `curl`. Newer versions (8.x) have the `--json` shortcut used below.
- Open a second terminal for the `curl` commands; the first one runs the server.

## Files in this folder

| File | What it is |
|------|------------|
| `main.py` | The final app of the lesson: all routes and the response model |
| `stages/01_start.py` | Start: home page and `GET /courses`, as at the end of Lesson 1 |
| `stages/02_path_param.py` | Adds `GET /courses/{course_id}` (returns `null` when missing) |
| `stages/03_path_param_404.py` | The same route raising `HTTPException(404)` |
| `stages/04_query_params.py` | `GET /courses` with `level`, `max_price`, `limit` |
| `stages/05_post_dict.py` | `POST /courses` with a `dict` body (answers 200) |
| `stages/06_post_201.py` | The same, answering 201 |
| `stages/07_put_delete.py` | `find_index` helper, `PUT` and `DELETE` |
| `stages/08_cost_leak.py` | Courses get a secret `cost` field that leaks |
| `stages/pitfall_str_hint.py` | Pitfall: `course_id: str` instead of `int` |
| `stages/pitfall_route_order_wrong.py` | Pitfall: `/courses/featured` below `/courses/{course_id}` |
| `stages/pitfall_route_order_fixed.py` | The fixed order |

Each stage is a complete `main.py`. To try a stage: `cp stages/<file> main.py` in your project and start the server:

```bash
uv run fastapi dev main.py --port 8152
```

The server stays in the foreground. Stop it with Control C before you start the next stage. In every output below, `date:` and `server:` header lines are left out, and the `...` stands for them.

## Follow along

### 1. Three people, three failures (stage `01_start.py`)

Lukas wants course 2, Priya wants the beginner courses, Meera wants to add a course. Try all three on the Lesson 1 server (`cp stages/01_start.py main.py`, start it on port 8152):

```bash
curl -s -i localhost:8152/courses/2
curl -s -i "localhost:8152/courses?level=beginner"
curl -s -i -X POST localhost:8152/courses
```

You should see:

```
HTTP/1.1 404 Not Found
...
{"detail":"Not Found"}

HTTP/1.1 200 OK
...
[{"id":1,"title":"Python","price":499,"level":"beginner"},{"id":2,"title":"SQL","price":399,"level":"beginner"},{"id":3,"title":"Docker","price":449,"level":"intermediate"}]

HTTP/1.1 405 Method Not Allowed
allow: GET
...
{"detail":"Method Not Allowed"}
```

No route for `/courses/2`; the `?level=` part is silently ignored (Docker is not a beginner course); and the route only knows GET. The server can answer one fixed question only.

The three ways to send data, with a library picture: a number on a shelf is a path parameter (part of the address), a note on the side is a query parameter (after `?`), and a parcel is the request body (JSON, never in the address).

### 2. A path parameter (stage `02_path_param.py`)

```python
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for course in COURSES:
        if course["id"] == course_id:
            return course
```

The name in the curly brackets must match the function parameter. Save, then ask for course 2, course 99 and course `abc`:

```bash
curl -s -i localhost:8152/courses/2
curl -s -i localhost:8152/courses/99
curl -s -i localhost:8152/courses/abc
```

```
HTTP/1.1 200 OK
...
{"id":2,"title":"SQL","price":399,"level":"beginner"}

HTTP/1.1 200 OK
...
null

HTTP/1.1 422 Unprocessable Content
...
{"detail":[{"type":"int_parsing","loc":["path","course_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

Course 99 gives `200` and `null`: the loop found nothing and the function returned `None`. That is a lie, because the course does not exist. For `abc`, FastAPI tried to turn the text into an `int`, failed, and refused the request before your function ran. In the error: `type` is the kind of problem, `loc` is where (the path, the part named `course_id`), `msg` is a plain sentence, `input` is what you sent.

### 3. Fix the lie with a 404 (stage `03_path_param_404.py`)

```python
from fastapi import FastAPI, HTTPException
...
    raise HTTPException(
        status_code=404,
        detail="Course not found",
    )
```

(The `raise` sits after the loop.) Ask for course 99 again:

```
HTTP/1.1 404 Not Found
...
{"detail":"Course not found"}
```

Errors get a whole lesson later (M15-L04).

### 4. The hint decides what your code receives (`pitfall_str_hint.py`)

Change `course_id: int` to `course_id: str`. Now `curl -s -i localhost:8152/courses/2` gives:

```
HTTP/1.1 404 Not Found
...
{"detail":"Course not found"}
```

The course exists, but the id from the address is now the text `"2"`, and text never equals the number `2`. Go back to `int`.

### 5. Query parameters (stage `04_query_params.py`)

A function parameter whose name is not in the address is a query parameter. A default makes it optional; `None` means "not given". With no default it would be required.

```python
@app.get("/courses")
def list_courses(
    level: str | None = None,
    max_price: int | None = None,
    limit: int = 10,
):
    result = COURSES
    if level is not None:
        result = [c for c in result if c["level"] == level]
    if max_price is not None:
        result = [c for c in result if c["price"] <= max_price]
    return result[:limit]
```

Put quotes around addresses that contain `&`, or the shell treats it as a command of its own:

```bash
curl -s -i "localhost:8152/courses?level=beginner"
curl -s -i "localhost:8152/courses?level=beginner&max_price=450"
curl -s -i "localhost:8152/courses?max_price=cheap"
curl -s -i "localhost:8152/courses?limit=1"
```

```
HTTP/1.1 200 OK
...
[{"id":1,"title":"Python","price":499,"level":"beginner"},{"id":2,"title":"SQL","price":399,"level":"beginner"}]

HTTP/1.1 200 OK
...
[{"id":2,"title":"SQL","price":399,"level":"beginner"}]

HTTP/1.1 422 Unprocessable Content
...
{"detail":[{"type":"int_parsing","loc":["query","max_price"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"cheap"}]}

HTTP/1.1 200 OK
...
[{"id":1,"title":"Python","price":499,"level":"beginner"}]
```

Filters combine: a course must pass all of them. Same checking machinery as before, but `loc` now says `query`.

### 6. A body with POST (stages `05_post_dict.py`, `06_post_201.py`)

A parameter with the hint `dict` is read from the body:

```python
@app.post("/courses")
def create_course(course: dict):
    course["id"] = max(c["id"] for c in COURSES) + 1
    COURSES.append(course)
    return course
```

The `max(... for ...)` is a generator expression (Module 9). A real database would choose the id (Module 16). `-X POST` picks the method, `-H` adds a header, `-d` is the body:

```bash
curl -s -i -X POST localhost:8152/courses -H "Content-Type: application/json" -d '{"title": "Git", "price": 299, "level": "beginner"}'
```

```
HTTP/1.1 200 OK
...
{"title":"Git","price":299,"level":"beginner","id":4}
```

Creating has a more exact code. Use stage `06_post_201.py` (`@app.post("/courses", status_code=201)`) and use the `--json` shortcut, which sets the method and the header for you (restart the server, because the course list is in memory and `id` 4 was already used):

```bash
curl -s -i localhost:8152/courses --json '{"title": "Git", "price": 299, "level": "beginner"}'
curl -s -i localhost:8152/courses/4
```

```
HTTP/1.1 201 Created
...
{"title":"Git","price":299,"level":"beginner","id":4}

HTTP/1.1 200 OK
...
{"title":"Git","price":299,"level":"beginner","id":4}
```

### 7. The honest problem: a dict checks nothing

```bash
curl -s -i localhost:8152/courses --json '{"name": "oops"}'
curl -s -i "localhost:8152/courses?level=beginner"
```

```
HTTP/1.1 201 Created
...
{"name":"oops","id":5}

HTTP/1.1 500 Internal Server Error
...
Internal Server Error
```

The junk was stored with `201`, and then the filter hit a course with no `level` and raised `KeyError`. One bad post broke the list for everybody. Lesson 3 (Pydantic models) fixes this.

### 8. PUT and DELETE (stage `07_put_delete.py`)

Both work on one existing course, so the search moves into a helper:

```python
def find_index(course_id: int) -> int:
    for index, course in enumerate(COURSES):
        if course["id"] == course_id:
            return index
    raise HTTPException(
        status_code=404,
        detail="Course not found",
    )


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return COURSES[find_index(course_id)]
```

`PUT` replaces a course and `DELETE` removes it, answering `204` (no body, on purpose):

```python
@app.put("/courses/{course_id}")
def replace_course(course_id: int, course: dict):
    index = find_index(course_id)
    course["id"] = course_id
    COURSES[index] = course
    return course


@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int):
    del COURSES[find_index(course_id)]
```

```bash
curl -s -i -X PUT localhost:8152/courses/2 --json '{"title": "SQL Pro", "price": 449, "level": "advanced"}'
curl -s -i -X PUT localhost:8152/courses/99 --json '{"title": "Go", "price": 299, "level": "beginner"}'
curl -s -i -X DELETE localhost:8152/courses/3
curl -s -i localhost:8152/courses/3
curl -s localhost:8152/courses
```

```
HTTP/1.1 200 OK
...
{"title":"SQL Pro","price":449,"level":"advanced","id":2}

HTTP/1.1 404 Not Found
...
{"detail":"Course not found"}

HTTP/1.1 204 No Content
...

HTTP/1.1 404 Not Found
...
{"detail":"Course not found"}

[{"id":1,"title":"Python","price":499,"level":"beginner"},{"title":"SQL Pro","price":449,"level":"advanced","id":2}]
```

Get reads. Post creates (201). Put replaces. Delete removes (204).

### 9. A response model hides secrets (stage `08_cost_leak.py`, then `main.py`)

Meera's team adds an internal `cost` to every course. In `08_cost_leak.py`:

```bash
curl -s -i localhost:8152/courses/1
```

```
HTTP/1.1 200 OK
...
{"id":1,"title":"Python","price":499,"level":"beginner","cost":120}
```

It leaks. The fix is in the final `main.py`: a `TypedDict` (Module 10) that lists only what may leave, passed as `response_model`:

```python
class CourseOut(TypedDict):
    id: int
    title: str
    price: int
    level: str


@app.get(
    "/courses",
    response_model=list[CourseOut],
)
def list_courses(...): ...


@app.get(
    "/courses/{course_id}",
    response_model=CourseOut,
)
def get_course(course_id: int):
    return COURSES[find_index(course_id)]
```

Run `main.py` and ask again:

```bash
curl -s -i localhost:8152/courses/1
curl -s localhost:8152/courses
```

```
HTTP/1.1 200 OK
...
{"id":1,"title":"Python","price":499,"level":"beginner"}

[{"id":1,"title":"Python","price":499,"level":"beginner"},{"id":2,"title":"SQL","price":399,"level":"beginner"},{"id":3,"title":"Docker","price":449,"level":"intermediate"}]
```

FastAPI checks the answer against the model and drops what is not listed.

## Common mistakes

1. Route order. With `stages/pitfall_route_order_wrong.py`, `curl -s -i localhost:8152/courses/featured` gives:

   ```
   HTTP/1.1 422 Unprocessable Content
   ...
   {"detail":[{"type":"int_parsing","loc":["path","course_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"featured"}]}
   ```

   FastAPI checks routes from the top; `featured` matched `{course_id}` and `int` failed. Put fixed addresses above addresses with parameters (`pitfall_route_order_fixed.py`): the same request gives `200` and the first course.
2. Forgetting the header or the body. These two POSTs (stage `06_post_201.py`) both give 422:

   ```bash
   curl -s -i -X POST localhost:8152/courses -d '{"title": "Git"}'
   curl -s -i -X POST localhost:8152/courses
   ```

   ```
   {"detail":[{"type":"dict_type","loc":["body"],"msg":"Input should be a valid dictionary","input":"{\"title\": \"Git\"}"}]}
   {"detail":[{"type":"missing","loc":["body"],"msg":"Field required","input":null}]}
   ```

   Without `Content-Type: application/json` the server sees plain text, not a dictionary. Always send the header (or use `--json`).
3. Data only in memory. Post a course, list it, then save the file (the server restarts) and list again: the new course is gone. The list lives in the memory of the running program. Keeping data needs a database (Module 16).
4. Treating `200` plus `null` as success for a missing thing. Raise a `404` instead.

## Clean up

Stop the server with Control C. Nothing else was created.

## Next

[M15-L03 · Pydantic Models](../m15-l03-pydantic-models/)
