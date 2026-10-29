# M15-B08 · Build a Course Catalog API

> Video: Module 15, Build 8. Watch it first, then follow along here.

In this build Asha writes a real service for allcsvideos.com: a course catalog API. Priya's course page and Meera (an instructor) can add, read, replace and remove courses by sending requests to it. It uses everything from M15-L01 to M15-L06: routes, parameters, Pydantic models, consistent errors, dependencies, a router, tests and the docs page. The courses live in memory; a real database comes in Module 16.

## What you'll build

Five routes, all under `/courses`:

- `POST /courses` adds a course (answers `201`)
- `GET /courses` lists a page of courses, with an optional filter by `level`
- `GET /courses/{course_id}` reads one
- `PUT /courses/{course_id}` replaces one
- `DELETE /courses/{course_id}` removes one (answers `204`)

And three kinds of errors, all with the same shape `{"error": {"code": ..., "message": ...}}`: `404` (no such course), `409` (a course with that title already exists), `422` (the data does not fit the rules).

## Before you start

- Python 3.14 or newer (`python --version`) and `uv` (Module 7). No Docker is needed.
- Follows [M15-L06](../m15-l06-async-endpoints-background-tasks-and-docs/). Run below: FastAPI 0.162.0, pytest 9.2.0.
- `curl` 8.x (for the `--json` flag).

## Files in this folder

This is the whole project as it is at the end of the video.

| File | What it is |
|------|------------|
| `pyproject.toml` | Dependencies (`fastapi[standard]`, dev: `pytest`) and `pythonpath = ["."]` so tests find `app` |
| `uv.lock` | The exact versions `uv` resolved |
| `app/models.py` | `Level` enum, `CourseIn` (what a client sends), `Course` (with an id), `CoursePage` |
| `app/domain.py` | Our own errors: `CourseNotFound`, `DuplicateTitle` (no web code) |
| `app/store.py` | `CourseStore`: the courses in a dictionary plus a next-id counter |
| `app/deps.py` | One store, and `get_store()` that hands it out |
| `app/errors.py` | The `error(...)` helper and the three handlers |
| `app/routers/courses.py` | The five routes |
| `app/main.py` | The front desk: creates the app, includes the router, registers the handlers |
| `try_models.py` | A quick check of the models, no server |
| `try_store.py` | A quick check of the store, no server |
| `seed.py` | Posts eight courses to your own running server (port 8658) |
| `tests/conftest.py` | The `client` and `python_course` fixtures |
| `tests/test_courses.py` | Twelve checks |

## Run it

From this folder:

```bash
uv sync
uv run fastapi dev app/main.py --port 8658
```

`uv sync` creates the environment from `uv.lock`. The server prints where it listens (`http://127.0.0.1:8658`) and where the docs live (`/docs`). The prompt does not come back: leave this terminal alone. In a second terminal:

```bash
uv run python seed.py
curl -s "localhost:8658/courses?level=beginner&limit=2&offset=2"
```

```
201 Python Basics
201 SQL in Two Weeks
201 Git and GitHub
201 Docker for Developers
201 FastAPI in Practice
201 Async Python
201 Python Performance
201 Linux Essentials
{"items":[{"title":"Git and GitHub","price":299,"level":"beginner","id":3},{"title":"Linux Essentials","price":349,"level":"beginner","id":8}],"total":4,"limit":2,"offset":2}
```

The second beginner page: two courses, and a total of 4 beginner courses in all. Run the tests (no server needed):

```bash
uv run pytest -v
```

```
tests/test_courses.py::test_create_returns_201_and_an_id PASSED
tests/test_courses.py::test_read_one_course PASSED
tests/test_courses.py::test_missing_course_is_a_404 PASSED
tests/test_courses.py::test_duplicate_title_is_a_409 PASSED
tests/test_courses.py::test_bad_input_is_a_422[bad0] PASSED
tests/test_courses.py::test_bad_input_is_a_422[bad1] PASSED
tests/test_courses.py::test_bad_input_is_a_422[bad2] PASSED
tests/test_courses.py::test_update_replaces_the_course PASSED
tests/test_courses.py::test_delete_then_gone PASSED
tests/test_courses.py::test_filter_by_level PASSED
tests/test_courses.py::test_pagination_pages_and_total PASSED
tests/test_courses.py::test_limit_above_fifty_is_a_422 PASSED

12 passed in 0.09s
```

(The header lines are left out, the percentages and the time will differ.)

## Build it step by step

The video builds the project in five steps. The folder holds the finished files, so for each step below, only use the part of each file that the step mentions, and add the rest as you reach the later steps. Each file is short, so you can type them one by one.

### Step 0. Set up the project

```bash
uv init --bare catalog
cd catalog
uv add "fastapi[standard]"
uv add --dev pytest
```

Add one extra setting to `pyproject.toml` so the tests can find the `app` folder (step 5):

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

Make the folders `app/` and `app/routers/`, each with an empty `__init__.py`.

### Step 1. The models (`app/models.py`)

A course has an id (the server chooses it), a title, a price in whole rupees and a level. Two models, two shapes: `CourseIn` is what a client may send (no id), and `Course` is `CourseIn` plus an id.

```python
class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100_000)
    level: Level = Level.BEGINNER


class Course(CourseIn):
    id: int
```

(`CoursePage` is added in step 4.) Check it before any server:

```bash
uv run python try_models.py
```

```
title='Python Basics' price=499 level=<Level.BEGINNER: 'beginner'>
3 problems
```

The good course gets the default level. The bad one (`title="Py", price=-5, level="expert"`) has three problems, all found at once, and you wrote no checking code.

### Step 2. The store and the routes

`app/store.py` is a cupboard with numbered drawers: a dictionary from id to course, and a counter for the next id. At first it has only `find_all`, `get`, `create`, `replace` and `delete`, with no checks (the title check and the errors come in step 3). `app/deps.py` makes one store and hands it out:

```python
STORE = CourseStore()


def get_store() -> CourseStore:
    return STORE
```

Try the store on its own, as plain Python:

```bash
uv run python try_store.py
```

```
2
SQL in Two Weeks
```

`app/routers/courses.py` has `APIRouter(prefix="/courses", tags=["courses"])` and the five routes. Each asks for the store with `Depends(get_store)`. At this step `list_courses` has no parameters yet and returns `store.find_all()`. A `POST` route reads its body as `data: CourseIn`, so FastAPI checks it before your function starts. All five are plain `def`, because nothing waits (L06). `app/main.py` only creates the app and includes the router:

```python
app = FastAPI(title="allcsvideos catalog")
app.include_router(courses.router)
```

Start the server, seed it, and ask:

```bash
uv run fastapi dev app/main.py --port 8658
```

```bash
uv run python seed.py
curl -s localhost:8658/courses/2
curl -s localhost:8658/courses/99 -i
```

You should see the eight `201` lines from `seed.py`, then:

```
{"title":"SQL in Two Weeks","price":399,"level":"beginner","id":2}
HTTP/1.1 500 Internal Server Error
date: Thu, 29 Oct 2026 16:20:15 GMT
server: uvicorn
content-length: 21
content-type: text/plain; charset=utf-8

Internal Server Error
```

(The date will differ.) A missing course should be a `404`, but the store has no rule for it, so Python's own `KeyError: 99` came out and the server turned it into a plain `500`. The traceback is in the server window.

### Step 3. Errors

`app/domain.py` holds two small classes with no web words in them (`CourseNotFound`, `DuplicateTitle`). The store now raises them: `get` raises `CourseNotFound` for an unknown id, and a new `check_title` raises `DuplicateTitle` when another course has the same title (ignoring capital letters), called first in `create` and in `replace` (with the course's own id, so a course may keep its own title).

`app/errors.py` builds the shape from L04 and has three handlers: `404` (`course_not_found`), `409` (`duplicate_title`) and `422` (`invalid_input`, with a `fields` list). `app/main.py` registers them:

```python
app.add_exception_handler(domain.CourseNotFound, errors.not_found)
app.add_exception_handler(domain.DuplicateTitle, errors.duplicate)
app.add_exception_handler(RequestValidationError, errors.bad_input)
```

Save the files. The dev server notices the changes and restarts, and the eight courses are gone, because they lived in memory. Run `uv run python seed.py` again, then:

```bash
curl -s -i localhost:8658/courses/99
curl -s -i --json '{"title": "Python Basics", "price": 499}' localhost:8658/courses
curl -s -i --json '{"title": "Go", "price": 0, "level": "expert"}' localhost:8658/courses
curl -s -X PUT --json '{"title": "SQL Pro", "price": 449, "level": "intermediate"}' localhost:8658/courses/2
curl -s -i -X DELETE localhost:8658/courses/3
curl -s localhost:8658/courses/3
```

```
HTTP/1.1 404 Not Found
...
{"error":{"code":"course_not_found","message":"Course 99 not found"}}

HTTP/1.1 409 Conflict
...
{"error":{"code":"duplicate_title","message":"Python Basics already exists"}}

HTTP/1.1 422 Unprocessable Content
...
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"title","problem":"String should have at least 3 characters"},{"field":"price","problem":"Input should be greater than 0"},{"field":"level","problem":"Input should be 'beginner', 'intermediate' or 'advanced'"}]}}

{"title":"SQL Pro","price":449,"level":"intermediate","id":2}

HTTP/1.1 204 No Content
...

{"error":{"code":"course_not_found","message":"Course 3 not found"}}
```

(`...` stands for the `date`, `server` and other header lines.) Three different errors, one shape. `PUT` and `DELETE` call the same `get`, so they are protected too.

### Step 4. Pages and the filter

Eight courses are fine, eight thousand are not. Add `CoursePage` to `models.py` (`items`, `total`, `limit`, `offset`), let `find_all(level)` keep only the courses with that level, and change the list route to:

```python
@router.get("", response_model=CoursePage)
def list_courses(
    level: Level | None = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    store: CourseStore = Depends(get_store),
):
    found = store.find_all(level)
    page = found[offset : offset + limit]
    return CoursePage(
        items=page, total=len(found), limit=limit, offset=offset
    )
```

The order is: filter first, count the total, then cut the page. The `le=50` cap matters: without it, one request could ask for a million items. After the restart, run `seed.py` again:

```bash
curl -s "localhost:8658/courses?limit=3"
curl -s "localhost:8658/courses?offset=20"
curl -s "localhost:8658/courses?limit=500&level=expert"
curl -s "localhost:8658/courses?level=advanced"
```

```
{"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1},{"title":"SQL in Two Weeks","price":399,"level":"beginner","id":2},{"title":"Git and GitHub","price":299,"level":"beginner","id":3}],"total":8,"limit":3,"offset":0}
{"items":[],"total":8,"limit":10,"offset":20}
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"level","problem":"Input should be 'beginner', 'intermediate' or 'advanced'"},{"field":"limit","problem":"Input should be less than or equal to 50"}]}}
{"items":[{"title":"Async Python","price":799,"level":"advanced","id":6},{"title":"Python Performance","price":899,"level":"advanced","id":7}],"total":2,"limit":10,"offset":0}
```

An offset past the end is not an error: it is an empty page, and the total is still 8. Both problems of the bad request are listed in the same error shape.

### Step 5. Tests and the docs page

Stop the server (Control C). `tests/conftest.py` has a fixture that overrides `get_store` (L05) and a ready-made course. `tests/test_courses.py` has twelve checks, counting the three bad bodies run by `parametrize`.

A first version of the fixture, copied from L05, was `app.dependency_overrides[get_store] = lambda: CourseStore()`. Run with that, six tests fail and six pass: a lambda runs again for every request, so a `POST` went into one store and the `GET` asked a second, empty one. In L05 each test made one request, so it worked there; here tests make several. The fix (the version in this folder) builds the store once in the fixture and lets the lambda return that same store:

```python
@pytest.fixture
def client():
    store = CourseStore()
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()
```

```bash
uv run pytest -q
```

```
............                                                                                 [100%]
12 passed in 0.09s
```

Do the tests catch real bugs? Break the page on purpose: in the list route change the slice to `found[:limit]` (ignore the offset). One test fails and names the problem:

```
>       assert [c["id"] for c in page["items"]] == [3, 4]
E       assert [1, 2] == [3, 4]
...
FAILED tests/test_courses.py::test_pagination_pages_and_total - assert [1, 2] == [3, 4]
1 failed, 11 passed in 0.10s
```

Put the slice back (`found[offset : offset + limit]`). Then start the server and open `http://localhost:8658/docs`: under the tag `courses` are the five routes, and below them the models `Course`, `CourseIn`, `CoursePage` and `Level`. The list route shows the three allowed levels, the default and range of `limit`, and the minimum of `offset`: the rules you wrote in code became the documentation.

## What breaks in production

Everything below uses the final project.

1. Memory is not storage. Seed, ask for one item, touch a file so the server restarts, and ask again:

   ```bash
   uv run python seed.py
   curl -s "localhost:8658/courses?limit=1"
   touch app/main.py
   curl -s "localhost:8658/courses?limit=1"
   ```

   ```
   {"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1}],"total":8,"limit":1,"offset":0}
   {"items":[],"total":0,"limit":1,"offset":0}
   ```

   Every restart, new version or crash wipes the catalog. Data that must survive must live outside the program.
2. Two workers, two catalogs. A real server runs several copies of your program (workers), each a separate process with its own memory. Stop the dev server, then:

   ```bash
   uv run fastapi run app/main.py --host 127.0.0.1 --port 8658 --workers 2
   ```

   In a second terminal, post one course and ask for the list six times:

   ```bash
   curl -s --json '{"title": "Python Basics", "price": 499}' localhost:8658/courses
   for i in 1 2 3 4 5 6; do curl -s "localhost:8658/courses?limit=1"; echo; done
   ```

   ```
   {"title":"Python Basics","price":499,"level":"beginner","id":1}
   {"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1}],"total":1,"limit":1,"offset":0}
   {"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1}],"total":1,"limit":1,"offset":0}
   {"items":[],"total":0,"limit":1,"offset":0}
   {"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1}],"total":1,"limit":1,"offset":0}
   {"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1}],"total":1,"limit":1,"offset":0}
   {"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1}],"total":1,"limit":1,"offset":0}
   ```

   Which requests see the course varies from run to run (each request lands on whichever worker is free), so the exact pattern of empty and full answers will differ. This is how memory works, not a bug in the code. A database is one place every worker can share (Module 16).
3. More limits: nobody checks who is calling, so anyone who finds the address can delete a course (Module 17). A crash you did not plan for still returns the plain `500`: add the catch-all handler from L04, with a logged error id. And the ids count up from 1 in memory; a database will choose and keep them.

## Try it yourself

1. Add a `search` parameter that keeps the courses whose title contains some text.
2. Sort the list by price.
3. Add a minimum price filter, and test it.
4. Add the catch-all handler from L04 with a test that checks the answer holds no secrets.

## Clean up

Stop any server with Control C. If you ran the project, delete the environment: `rm -r .venv`. Nothing else was created (the data was in memory).

## Next

[M16-L01 · SQL and PostgreSQL in Docker](../../m16-databases/m16-l01-sql-and-postgresql-in-docker/)
