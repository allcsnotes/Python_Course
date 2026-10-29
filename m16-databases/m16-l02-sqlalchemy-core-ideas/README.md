# M16-L02 · SQLAlchemy Core Ideas

> Video: Module 16, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Why a raw driver (psycopg) is not enough, and what SQLAlchemy adds
- The engine, the connection and the session, and the "shopping basket" idea
- Models: a Python class that describes a table, and `create_all`
- Add, find, change and delete courses, and how to watch the real SQL
- The session as a FastAPI dependency (`yield`), and three common traps

## Before you start

- Python 3.14 or newer: `python --version`
- Docker running. We use the pinned image `postgres:17`
- Lesson M16-L01 (SQL and PostgreSQL in Docker) gives you the database idea. This lesson starts its own fresh container
- A virtual environment with the pinned packages:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Versions used in the video: SQLAlchemy 2.1.6, psycopg 3.3.6, FastAPI 0.162.0, uvicorn 0.54.0, Pydantic 2.14.1.
The password `devpass` is a demo value for a throw-away container.

## Files in this folder

| File | What it is |
|------|------------|
| `requirements.txt` | The pinned packages |
| `seed.sql` | Hidden setup: the 8 courses that lesson 1 left in the database |
| `hook_raw.py` | A plain psycopg driver query: rows are anonymous tuples |
| `db.py` | The engine (one URL) and `show_sql()` to print the SQL |
| `connect.py` | Core level: engine, connection, `text()` with a bound `:limit` |
| `models.py` | `Base` and the `Course` model |
| `create_tables.py` | `drop_all` then `create_all`, with the SQL shown |
| `add_courses.py` | Add one course with a session |
| `add_more.py` | `add_all` with the other seven courses |
| `find_courses.py` | `select(Course).where(...).order_by(...)` and `scalars` |
| `find_more.py` | `get`, `execute` and `scalars` compared |
| `change_course.py` | Update by changing an attribute, then delete |
| `api_app.py` | FastAPI app with `get_session` as a dependency |
| `p_nocommit.py`, `p_detached.py`, `p_notnull.py` | The three traps |

## Follow along

### 1. Start Postgres and load the starting data

```bash
docker run --name m16l02-pg -e POSTGRES_PASSWORD=devpass -p 15402:5432 -d postgres:17
docker exec m16l02-pg psql -U postgres -c "CREATE DATABASE allcs"
docker exec -i m16l02-pg psql -U postgres -d allcs -q < seed.sql
```

The first command prints the container ID, the second prints `CREATE DATABASE`. The third prints a harmless
`NOTICE: table "courses" does not exist, skipping` the first time.

### 2. The raw driver

```bash
python hook_raw.py
```

```text
[(1, 'Python Basics', 449), (2, 'SQL in Two Weeks', 399), (3, 'Git and GitHub', 299)]
Python Basics
```

Python sees plain tuples. You must remember that the title sits at position 1. The SQL is only text, and the connection is closed by hand.

### 3. Engine, connection and `text()`

`db.py` holds the engine. `create_engine` does not connect yet; it connects the first time someone needs a connection.

```bash
python connect.py
```

```text
SQL in Two Weeks 399
Git and GitHub 299
Linux Essentials 349
```

The value 400 travels separately (`{"limit": 400}`) and is never glued into the SQL text. A row has names, so `row.title` works.

### 4. Models and `create_all`

Read `models.py`. `Mapped[str]` is a required column (NOT NULL), `Mapped[str | None]` is optional. Then:

```bash
python create_tables.py
```

The output is SQLAlchemy's own log. The important part is the table it creates from the class:

```text
DROP TABLE courses
...
CREATE TABLE courses (
	id SERIAL NOT NULL, 
	title VARCHAR NOT NULL, 
	price INTEGER NOT NULL, 
	level VARCHAR NOT NULL, 
	description VARCHAR, 
	PRIMARY KEY (id)
)
```

`create_all` only creates tables that do not exist. It never changes an existing table. For that you need migrations (lesson 4).

### 5. Add courses

```bash
python add_courses.py
```

```text
BEGIN (implicit)
INSERT INTO courses (title, price, level, description) VALUES (%(title)s::VARCHAR, %(price)s::INTEGER, %(level)s::VARCHAR, %(description)s::VARCHAR) RETURNING courses.id
[generated in 0.00007s] {'title': 'Python Basics', 'price': 449, 'level': 'beginner', 'description': None}
COMMIT
BEGIN (implicit)
SELECT courses.id, courses.title, courses.price, courses.level, courses.description 
FROM courses 
WHERE courses.id = %(pk_1)s::INTEGER
[generated in 0.00013s] {'pk_1': 1}
ROLLBACK
id before: None
waiting: IdentitySet([Course(None, 'Python Basics', 449)])
id after: 1
```

(The SQL log goes to stderr, so in your terminal it may be mixed with the three `print` lines in a different order. I removed the three start-up lines `select pg_catalog.version()` ... here; you will see them. Timings differ.)
`id before` is `None` because the database chooses the number. After the commit the object is "expired", so reading `course.id` sends a `SELECT`.

```bash
python add_more.py
```

This prints nothing. It adds seven courses in one transaction, so all are saved or none.

### 6. Find courses

```bash
python find_courses.py
```

```text
SELECT courses.id, courses.title, courses.price, courses.level, courses.description 
FROM courses 
WHERE courses.price < :price_1 ORDER BY courses.title
Course(3, 'Git and GitHub', 299)
Course(8, 'Linux Essentials', 349)
Course(1, 'Python Basics', 449)
Course(2, 'SQL in Two Weeks', 399)
```

`Course.price < 500` is not True or False: SQLAlchemy changed what `<` does on a column, so it builds a piece of a query. Ordered by title, not price.

```bash
python find_more.py
```

```text
Course(2, 'SQL in Two Weeks', 399)
None
[(Course(6, 'Async Python', 799),), (Course(7, 'Python Performance', 899),)]
[Course(6, 'Async Python', 799), Course(7, 'Python Performance', 899)]
```

`get` finds one row by key (`None` when missing). `execute` gives rows (each a tuple holding one course). `scalars` gives the objects directly.

### 7. Change and delete

```bash
python change_course.py
```

The log (after the three start-up lines) shows only the changed column, then the delete:

```text
BEGIN (implicit)
SELECT courses.id, ... WHERE courses.id = %(pk_1)s::INTEGER
UPDATE courses SET price=%(price)s::INTEGER WHERE courses.id = %(courses_id)s::INTEGER
[generated in 0.00014s] {'price': 399, 'courses_id': 1}
COMMIT
...
DELETE FROM courses WHERE courses.id = %(id)s::INTEGER
[generated in 0.00005s] {'id': 1}
COMMIT
changed: IdentitySet([Course(1, 'Python Basics', 399)])
```

The session remembers how each object looked when loaded and sends the smallest update (the "unit of work"). Note: this deletes course 1, as in the video.

### 8. The session in FastAPI

```bash
uvicorn api_app:app --port 8162 --no-access-log
```

In a second terminal:

```bash
curl -s localhost:8162/courses/2
curl -s localhost:8162/courses/99
curl -s -X POST localhost:8162/courses -H 'Content-Type: application/json' -d '{"title": "Rust Basics", "price": 649, "level": "advanced"}'
curl -s localhost:8162/courses | head -c 140
```

```text
{"title":"SQL in Two Weeks","price":399,"level":"beginner","id":2}
{"detail":"Course not found"}
{"title":"Rust Basics","price":649,"level":"advanced","id":9}
[{"title":"SQL in Two Weeks","price":399,"level":"beginner","id":2},{"title":"Git and GitHub","price":299,"level":"beginner","id":3},{"title
```

In the server window, the two reads end with `ROLLBACK` (nothing to save), the POST ends with `COMMIT` and then a `SELECT` (the committed object was expired). Stop the server with Ctrl+C.
`model_config = ConfigDict(from_attributes=True)` lets Pydantic read fields from an object, not only from a dict.

### 9. The three traps

```bash
python p_nocommit.py
python p_detached.py
python p_notnull.py
```

```text
added: IdentitySet([Course(None, 'Kotlin Basics', 649)])
[]
```

```text
sqlalchemy.orm.exc.DetachedInstanceError: Instance <Course at 0x1082bf4d0> is not bound to a Session; attribute refresh operation cannot proceed (Background on this error at: https://sqlalche.me/e/21/bhk3)
```

```text
sqlalchemy.exc.IntegrityError: (psycopg.errors.NotNullViolation) null value in column "title" of relation "courses" violates not-null constraint
DETAIL:  Failing row contains (11, null, 499, beginner, null).
```

(The memory address and the row number in the last two will differ for you.)

## Common mistakes

- No `commit()`: the basket is thrown away and the course never reaches the database.
- Using an object after its session closed: `DetachedInstanceError`. Read what you need inside the `with` block, or turn the object into plain data (as `CourseOut` does).
- Passing `None` for a required column: the database refuses it (`IntegrityError`). Pydantic should catch this earlier with a 422.
- Gluing user text into SQL. Always pass values separately.
- Reading an attribute can quietly send a query. Inside a loop that is the "N+1" problem of the next lesson.

## Clean up

```bash
docker rm -f -v m16l02-pg
deactivate
rm -rf .venv
```

## Next

[M16-L03 · Relationships and the N+1 Problem](../m16-l03-relationships-and-the-n-1-problem/)
