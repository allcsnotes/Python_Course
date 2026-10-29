# M16-B09 · Build allcsvideos Backend v1

> Video: Module 16, Build 9. Watch it first, then follow along here.

## What you'll learn

- How to put all of Module 16 into one project: FastAPI, SQLAlchemy, Postgres and Alembic
- Four tables (courses, lessons, students, enrollments) with rules the database itself guards: unique, check and primary key
- Turning a database refusal into a clean 404 / 409 / 422 answer in one error shape
- Fixing the N+1 problem with `selectinload` and keeping it fixed with a test
- Tests against their own database, rolled back after every test, and a test that counts queries
- Why two workers always agree: they share one Postgres

## Before you start

- Python 3.14 or newer: `python --version`
- `uv` (as in Module 7): `uv --version`
- Docker running (pinned image `postgres:17`)
- Build 8 (the in-memory catalog) and lessons M16-L01 to M16-L05
- Every user name, password and email here (`allcs` / `allcs`, `lukas@example.com`) is a demo value for a throw-away container. Real settings come in Modules 17 and 19.

## Files in this folder

This whole folder is the project, as it stands at the end of the video.

| File | What it is |
|------|------------|
| `pyproject.toml`, `uv.lock` | Project settings and the exact package versions (FastAPI 0.162.0, SQLAlchemy 2.1.6, psycopg 3.3.6, Alembic 1.20.1, pytest 9.1.1). `pythonpath = ["."]` lets the tests find `app/` |
| `app/db.py` | Engine, `Base`, `get_session`, `get_or_404`, `save` and the table of conflict rules |
| `app/models.py` | `Course`, `Lesson`, `Student`, `Enrollment` |
| `app/schemas.py` | The shapes of data going in and out (Pydantic) |
| `app/domain.py`, `app/errors.py` | `NotFound` and `Conflict`, and the handlers that make the JSON error shape |
| `app/routers/courses.py`, `students.py`, `enrollments.py` | The nine routes |
| `app/main.py` | Creates the app, includes the routers, registers the handlers |
| `alembic.ini`, `migrations/` | Alembic settings and two migrations (`courses and lessons`, `students and enrollments`) |
| `try_tables.py` | Prints the SQL that SQLAlchemy would send for `courses` |
| `seed.py`, `seed_students.py` | Post six courses with three lessons each, and two students, through the API |
| `race.py` | Five enrol requests at the same moment |
| `queries.py` | Counts the statements that one list request sends |
| `tests/conftest.py`, `tests/test_api.py` | Fixtures (own database, rollback per test, query counter) and the 12 tests |

## Run it

If you only want to see the finished backend working:

```bash
docker run -d --name m16b09-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs \
  -e POSTGRES_DB=allcs -v m16b09-data:/var/lib/postgresql/data -p 15409:5432 postgres:17
uv sync
uv run alembic upgrade head
uv run fastapi dev app/main.py --port 8659
```

Then, in a second terminal: `uv run python seed.py`, and open `http://localhost:8659/docs`.
(Wait a few seconds after `docker run` before `alembic upgrade head`, until Postgres has started.)

## Build it step by step

The video builds it in six steps. The files in this folder are the end result, so to build from nothing, create an empty folder and add the files as each step says.

### Setup

```bash
uv init --bare allcs
cd allcs
uv add "fastapi[standard]" sqlalchemy "psycopg[binary]" alembic
uv add --dev pytest
```

Then add this to `pyproject.toml` so the tests can find the `app` folder:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

(Our `pyproject.toml` is exactly this: five packages and pytest.) Start the database:

```bash
docker run -d --name m16b09-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs \
  -e POSTGRES_DB=allcs -v m16b09-data:/var/lib/postgresql/data -p 15409:5432 postgres:17
docker ps
```

The port 15409 is used so it never clashes with anything else. `docker ps` should list `m16b09-pg` with `0.0.0.0:15409->5432/tcp`.

The plan on paper: a course has a title, a price (whole rupees) and a level; a lesson has a title and a position and belongs to one course; a student has a name and a unique email; an enrollment says "this student joined this course on this date". Rules the database guards: title unique, price above zero, email unique, and the pair (student, course) only once. Nine routes: five for courses, one to add a lesson, two for students, one to enrol.

### Step 1: the models

Create `app/__init__.py` (empty), `app/db.py` and `app/models.py`. In this step `models.py` has only `Course` and `Lesson`. `db.py` has the engine, `Base` and `get_session` (the helper with `yield`); the error helpers come in step 3. Then check what SQLAlchemy would send:

```bash
uv run python try_tables.py
```

```text
CREATE TABLE courses (
	id SERIAL NOT NULL, 
	title VARCHAR(60) NOT NULL, 
	price INTEGER NOT NULL, 
	level VARCHAR(12) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT price_positive CHECK (price > 0), 
	UNIQUE (title)
)
```

The rules from the class (unique title, check on price) are in the SQL.

### Step 2: migrations

```bash
uv run alembic init migrations
```

In `migrations/env.py`, add these lines (see our `env.py`): import the models and the URL, set the URL, and set the metadata:

```python
from app import models  # noqa: F401
from app.db import URL, Base

config.set_main_option("sqlalchemy.url", URL)
target_metadata = Base.metadata
```

Then draft the first migration and apply it:

```bash
uv run alembic revision --autogenerate -m "courses and lessons"
uv run alembic upgrade head
docker exec m16b09-pg psql -U allcs -c '\dt'
docker exec m16b09-pg psql -U allcs -c '\d courses'
```

```text
INFO  [alembic.runtime.migration] Running upgrade  -> cb9aa85a3921, courses and lessons
```

(Your revision ID will differ; the file in `migrations/versions/` here has `cb9aa85a3921`.) At this step `\dt` shows three tables: `courses`, `lessons` and `alembic_version`. `\d courses` shows the unique title, the check `price_positive`, and the foreign key from `lessons`.

### Step 3: the courses routes and their errors

Create `app/schemas.py` (course and lesson parts), `app/routers/__init__.py` (empty), `app/routers/courses.py` and `app/main.py`. All routes are plain `def` with the plain session. Start the server and seed it:

```bash
uv run fastapi dev app/main.py --port 8659
```

In a second terminal:

```bash
uv run python seed.py
curl -s "localhost:8659/courses?limit=2"
```

```text
1 Python Basics
2 SQL in Two Weeks
3 Git and GitHub
4 Docker for Developers
5 FastAPI in Practice
6 Async Python
```

```text
{"items":[{"title":"Python Basics","price":499,"level":"beginner","id":1,"lessons":[{"title":"Welcome","position":1,"id":1},{"title":"Setup","position":2,"id":2},{"title":"First steps","position":3,"id":3}]},{"title":"SQL in Two Weeks","price":599,"level":"beginner","id":2,"lessons":[{"title":"Welcome","position":1,"id":4},{"title":"Setup","position":2,"id":5},{"title":"First steps","position":3,"id":6}]}],"total":6,"limit":2,"offset":0}
```

A mistake on purpose: post a course whose title exists. At first the answer is `500 Internal Server Error` in plain text (the server window shows `IntegrityError` wrapping `duplicate key value violates unique constraint "courses_title_key"`). To fix it, add `app/domain.py` with `NotFound` and `Conflict`, the `CONFLICTS` table plus `get_or_404` and `save` to `app/db.py`, and `app/errors.py`; register the three handlers in `main.py`; and use `get_or_404` and `save` in the routes. The server reloads by itself. Now:

```bash
curl -s -i --json '{"title": "Python Basics", "price": 499}' localhost:8659/courses
curl -s -i localhost:8659/courses/99
curl -s -i --json '{"title": "Go", "price": 0, "level": "expert"}' localhost:8659/courses
curl -s "localhost:8659/courses?level=beginner&limit=2&offset=2"
```

```text
HTTP/1.1 409 Conflict
{"error":{"code":"duplicate_title","message":"Title already used"}}

HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"Course 99 not found"}}

HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"title","problem":"String should have at least 3 characters"},{"field":"price","problem":"Input should be greater than 0"},{"field":"level","problem":"Input should be 'beginner', 'intermediate' or 'advanced'"}]}}
```

(Headers such as `date` are left out here.) The last request returns one course, "Git and GitHub", with `"total":3`: the database cuts the page and the total counts all beginner courses. Because the 409 comes from the database, even two requests at the same moment cannot fool it.

### Step 4: students and enrollments

Add `Student` and `Enrollment` to `app/models.py`, the student and enrollment schemas to `schemas.py`, and `app/routers/students.py` and `app/routers/enrollments.py`; include both routers in `main.py`. The models changed, so you need a second migration:

```bash
uv run alembic revision --autogenerate -m "students and enrollments"
uv run alembic upgrade head
docker exec m16b09-pg psql -U allcs -c '\d enrollments'
```

```text
INFO  [alembic.runtime.migration] Running upgrade cb9aa85a3921 -> 6d1d3956ce21, students and enrollments
```

`\d enrollments` shows the primary key on `(student_id, course_id)`. Only the new revision ran: Alembic knows from its notebook that the first one is done. Now create students and enrol:

```bash
uv run python seed_students.py
curl -s -i -X POST localhost:8659/courses/2/enrollments --json '{"student_id": 1}'
curl -s -i -X POST localhost:8659/courses/2/enrollments --json '{"student_id": 1}'
```

```text
201 Lukas
201 Priya
HTTP/1.1 201 Created
{"student_id":1,"course_id":2,"enrolled_on":"2026-10-29"}
HTTP/1.1 409 Conflict
{"error":{"code":"already_enrolled","message":"Already enrolled in this course"}}
```

(The date is today's date.) The route never asks "is he already enrolled?". It just inserts, and the primary key refuses the second row. To see why that matters, send five requests at the same moment:

```bash
uv run python race.py
```

```text
[(201, 1), (409, 4)]
```

One created, four conflicts, and exactly one row in the table. No lock and no check were needed.

The same idea protects the other side:

```bash
curl -s -i -X DELETE localhost:8659/courses/2
curl -s localhost:8659/students/1
```

```text
HTTP/1.1 409 Conflict
{"error":{"code":"course_has_students","message":"Course still has students"}}
{"name":"Lukas","email":"lukas@example.com","id":1,"courses":[{"id":2,"title":"SQL in Two Weeks"},{"id":1,"title":"Python Basics"}]}
```

(The second command shows Lukas with courses 2 and 1 because `race.py` enrolled him in course 1.)

### Step 5: fast lists

Listing courses with their lessons looks innocent, but reading `course.lessons` asks the database (lesson 3). `queries.py` listens to every statement and calls the list route for six courses. Before the fix, in `app/routers/courses.py` the page query has no loader option, and the result is:

```text
8 queries
```

(One for the total, one for the courses, and one per course for its lessons. In the video it printed the first 58 characters of each statement.) The fix is one line, `query.options(selectinload(Course.lessons))`, and for the student route a chain: `selectinload(Student.enrollments).selectinload(Enrollment.course)`.

```bash
uv run python queries.py
```

```text
3 queries
SELECT count(*) AS count_1 FROM (SELECT courses.id AS id, 
SELECT courses.id, courses.title, courses.price, courses.l
SELECT lessons.course_id, lessons.id, lessons.title, lesso
```

Three queries, whether the page has six courses or fifty. (This file ends in the fixed state, so you see 3.)

### Step 6: tests

Tests must never touch the real courses, so give them their own database in the same box:

```bash
docker exec m16b09-pg psql -U allcs -c "CREATE DATABASE allcs_test"
```

`tests/conftest.py` points the app at `allcs_test` before the app is imported. The `schema` fixture runs `alembic downgrade base` and `upgrade head` once, so every run also proves the migrations work. The `client` fixture swaps `get_session` (as in Module 15). The `make_course` fixture creates a course through the real route. Our `test_api.py` has 12 tests.

If your `session` fixture simply opens a normal session, every test commits for real and tests start to interfere: the video shows 7 passed and 4 failed (for example a `KeyError: 'id'` because the very first test already created "Python Basics"). The fix is in our `conftest.py`: the `session` fixture opens a connection, starts one outer transaction, and the session joins it with `join_transaction_mode="create_savepoint"`. When a route commits, only a savepoint is released; at the end of the test the outer transaction is rolled back, so nothing is left behind.

```bash
uv run pytest -q
```

```text
............                                                             [100%]
12 passed in 0.36s
```

(Timing differs.) The last test, `test_list_needs_few_queries`, counts the statements and asserts at most three. Do the tests catch the problem? Take `selectinload` out of the list route on purpose and run again:

```text
FAILED tests/test_api.py::test_list_needs_few_queries - assert 8 <= 3
1 failed, 11 passed
```

Put the line back and all twelve are green again (`uv run pytest -v` lists them).

### Two workers

Each worker is a separate Python process with its own memory. In Build 8 that meant two different catalogs. Now:

```bash
uv run fastapi run app/main.py --host 127.0.0.1 --port 8659 --workers 2
for i in 1 2 3 4 5 6; do curl -s "localhost:8659/courses?limit=1" | grep -o '"total":[0-9]*'; done
```

```text
"total":6
"total":6
"total":6
"total":6
"total":6
"total":6
```

Every request lands on whichever worker is free, and all of them ask the same Postgres, so the answers agree. Stop the server with Ctrl+C.

What is still missing: nobody checks who is calling (anyone can delete a course, students have no passwords): Module 17. The pool has its default size (lesson 5 showed what happens when it runs out). The database address and password sit in the code: Module 19.

## Common mistakes

- Checking "already enrolled?" in Python before inserting. Two requests at the same moment both pass the check. Let the primary key decide and turn the refusal into a 409.
- Forgetting `session.rollback()` after a failed commit (our `save` does it).
- Looping over `course.lessons` without `selectinload`: N+1 queries.
- Running the tests against the real database. Use `allcs_test`.
- Tests that commit for real, so one test sees another's rows. Roll back an outer transaction.
- Editing a migration that was already applied somewhere else. Write a new one.

## Clean up

Stop the server (Ctrl+C), then:

```bash
docker rm -f -v m16b09-pg
docker volume rm m16b09-data
```

and remove the `.venv` folder that `uv` created, if you like.

## Next

Module 17 (Security and Authentication) starts with "Passwords Done Right", which fixes the missing passwords. Next: [M17-L01 · Passwords Done Right](../../m17-security-and-authentication/m17-l01-passwords-done-right/).
