# M16-L03 · Relationships and the N+1 Problem

> Video: Module 16, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- One-to-many and many-to-many links between tables, as Python attributes (`relationship`, `back_populates`)
- Lazy loading, and how reading an attribute can quietly ask the database
- The N+1 problem, shown with real counted queries
- Two fixes: `selectinload` (for lists) and `joinedload` (for one object), and why `.unique()` is needed
- How to keep it fixed: `raiseload` and a test that asserts the number of queries

## Before you start

- Python 3.14 or newer: `python --version`
- Docker running (pinned image `postgres:17`)
- The `Course` model idea from M16-L02 (SQLAlchemy Core Ideas). This folder is self-contained
- A virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Versions in the video: SQLAlchemy 2.1.6, psycopg 3.3.6, pytest 9.1.1. The password `devpass` is a demo value.

## Files in this folder

| File | What it is |
|------|------------|
| `requirements.txt` | Pinned packages |
| `db.py` | The engine (port 15403) and `show_sql()` |
| `models.py` | `Course`, `Lesson`, `Student`, `Enrollment` with relationships |
| `seed.py` | Resets the tables and fills them: 10 courses, lessons, 3 students, 6 enrollments (`python seed.py 200` makes 200 courses) |
| `counting.py` | `QueryCounter`: counts queries sent to the database (Priya's helper) |
| `hook.py` | The courses page loop: how many queries? |
| `first_look.py` | Use the relationship in both directions |
| `add_lesson.py` | Append a lesson to a course |
| `students_courses.py` | Many-to-many through `Enrollment` |
| `lazy_echo.py` | Lazy loading with the SQL echoed |
| `n_plus_one.py` | N+1 with the SQL echoed |
| `selectin.py` | Fix 1: `selectinload` |
| `joined_bad.py`, `joined.py` | Fix 2: `joinedload`, first without and then with `.unique()` |
| `compare.py`, `compare_one.py` | Measure lazy / selectinload / joinedload |
| `nested.py` | Chained loaders: student, enrollment, course |
| `detached.py`, `raise_demo.py` | Pitfalls: closed session, `raiseload` |
| `service.py`, `test_queries.py` | A function with a hidden N+1, and a test that catches it |

## Follow along

### 1. Start Postgres and fill the tables

```bash
docker run --name m16l03-pg -e POSTGRES_PASSWORD=devpass -p 15403:5432 -d postgres:17
docker exec m16l03-pg psql -U postgres -c "CREATE DATABASE allcs"
python seed.py 10
```

`seed.py` prints nothing. (Lesson count: 3, 4 or 5 lessons per course, 39 in total.)

### 2. The hook: how many queries?

```bash
python hook.py
```

```text
Python Basics 3
SQL in Two Weeks 4
Git and GitHub 5
Linux Essentials 3
Async Python 4
Python Performance 5
Docker Basics 3
Web APIs 4
Testing with pytest 5
Kotlin Basics 3
queries: 11
```

Eleven: one for the course list and one lesson query for each of the ten courses. With 200 courses it would be 201.

### 3. Relationships: a link in Python

A foreign key column (`lessons.course_id`) holds the number. `relationship(back_populates=...)` is the Python attribute that follows it, in both directions. Read `models.py`: `Lesson.course_id` is a real column, `Lesson.course` and `Course.lessons` are not columns.

```bash
python first_look.py
```

```text
Python Basics
  1. Welcome
  2. The idea
  3. Try it
Python Basics
```

Both sides stay in step in Python, right away:

```bash
python add_lesson.py
```

```text
Python Basics None
1
```

Before the commit the lesson already knows its course, but `course_id` is `None`. After the commit it is 1. Run `python seed.py 10` again afterwards to reset the data.

### 4. Many-to-many: the sign-up sheet

`Enrollment` has two foreign keys that are both part of the primary key, plus its own column `enrolled_on`.

```bash
python students_courses.py
```

```text
Lukas -> Python Basics 2026-09-01
Lukas -> SQL in Two Weeks 2026-09-02
['Lukas', 'Priya', 'Ben']
```

### 5. Lazy loading

```bash
python lazy_echo.py
```

The query log (after the three start-up lines) shows the lessons are only asked for when `course.lessons` is touched:

```text
BEGIN (implicit)
SELECT courses.id, courses.title, courses.price, courses.level, courses.description 
FROM courses 
WHERE courses.id = %(pk_1)s::INTEGER
[generated in 0.00011s] {'pk_1': 1}
-- got the course
SELECT lessons.id, lessons.title, lessons.course_id 
FROM lessons 
WHERE %(param_1)s::INTEGER = lessons.course_id
[generated in 0.00009s] {'param_1': 1}
-- asked for the lessons
3
ROLLBACK
```

(SQL goes to stderr and the markers to stdout, so they may be mixed differently in your terminal.)

### 6. The N+1 problem, seen

```bash
python n_plus_one.py
```

The log shows the same lessons query twice, once with 1 and once with 2:

```text
SELECT courses.id, ... FROM courses  LIMIT 2
SELECT lessons.id, lessons.title, lessons.course_id FROM lessons WHERE 1 = lessons.course_id
Python Basics 3
SELECT lessons.id, lessons.title, lessons.course_id FROM lessons WHERE 2 = lessons.course_id
SQL in Two Weeks 4
queries: 3
```

(Shortened here: the real log prints each statement over several lines with `%(param_1)s::INTEGER` placeholders.)

### 7. Fix 1: selectinload

```bash
python selectin.py
```

```text
SELECT courses.id, courses.title, courses.price, courses.level, courses.description 
FROM courses 
 LIMIT %(param_1)s::INTEGER
SELECT lessons.course_id, lessons.id, lessons.title 
FROM lessons 
WHERE lessons.course_id IN (%(primary_keys_1)s::INTEGER, %(primary_keys_2)s::INTEGER)
Python Basics 3
SQL in Two Weeks 4
queries: 2
```

Two queries, whether it is two courses or two hundred.

### 8. Fix 2: joinedload (and `.unique()`)

```bash
python joined_bad.py
```

```text
sqlalchemy.exc.InvalidRequestError: The unique() method must be invoked on this Result, as it contains results that include joined eager loads against collections
```

(A traceback comes before this line.) A join repeats a course once per lesson, so SQLAlchemy asks you to say `.unique()`.

```bash
python joined.py
```

```text
SELECT courses.id, courses.title, courses.price, courses.level, courses.description, lessons_1.id AS id_1, lessons_1.title AS title_1, lessons_1.course_id 
FROM courses LEFT OUTER JOIN lessons AS lessons_1 ON courses.id = lessons_1.course_id 
WHERE courses.id <= %(id_2)s::INTEGER
Python Basics 3
SQL in Two Weeks 4
queries: 1
```

### 9. Measure

```bash
python compare.py
python seed.py 200
python compare.py
python seed.py 10
```

```text
lazy         queries:  11    25 ms
selectinload queries:   2     5 ms
joinedload   queries:   1    10 ms
lazy         queries: 201   382 ms
selectinload queries:   2    10 ms
joinedload   queries:   1     9 ms
```

The query counts are exact; the milliseconds depend on your computer. Rule of thumb: `selectinload` for lists (lessons of a course), `joinedload` for a single object on the other side (the course of a lesson).

```bash
python compare_one.py
python nested.py
```

```text
lazy: 11
joinedload: 1
```

```text
lazy: 8
selectinload chain: 3
```

Lazy shows 11, not 39, because SQLAlchemy remembers a course it already loaded in the session. Chain loaders for longer links: `selectinload(Student.enrollments).selectinload(Enrollment.course)`.

### 10. Pitfalls and keeping it fixed

```bash
python detached.py
python raise_demo.py
```

```text
Python Basics
...
sqlalchemy.orm.exc.DetachedInstanceError: Parent instance <Course at 0x1085823c0> is not bound to a Session; lazy load operation of attribute 'lessons' cannot proceed (Background on this error at: https://sqlalche.me/e/21/bhk3)
```

```text
Python Basics
...
sqlalchemy.exc.InvalidRequestError: 'Course.lessons' is not available due to lazy='raise'
```

(Tracebacks are in the `...`; the memory address differs for you.) `raiseload` turns a hidden N+1 into a loud error while you develop.

Last, a test that nobody can silently break:

```bash
python -m pytest test_queries.py -v
```

```text
test_queries.py::test_list_is_two_queries PASSED                         [ 50%]
test_queries.py::test_slow_list_is_two_queries FAILED                    [100%]
...
E       assert 11 <= 2
...
FAILED test_queries.py::test_slow_list_is_two_queries
1 failed, 1 passed
```

The second test fails on purpose: `course_lines_slow` touches `course.lessons` in a loop. Change it to call `course_lines` and it passes.

## Common mistakes

- Looping over a relationship without eager loading: one extra query per row (N+1).
- Using a lazy relationship after the session closed: `DetachedInstanceError`. Load what you need first.
- Forgetting `.unique()` with `joinedload` on a list.
- Using `joinedload` for lists with many children: repeated rows. Prefer `selectinload`.
- Not measuring. Count the queries (`QueryCounter`) and turn them into a test.

## Clean up

```bash
docker rm -f -v m16l03-pg
deactivate
rm -rf .venv
```

## Next

[M16-L04 · Migrations with Alembic and Transactions](../m16-l04-migrations-with-alembic-and-transactions/)
