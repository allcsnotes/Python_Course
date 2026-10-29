# M16-L04 · Migrations with Alembic and Transactions

> Video: Module 16, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- What a migration is, and how to create, apply and undo one with Alembic
- Why adding a required column to a table that has rows needs a default
- Transactions: commit, rollback, `with session.begin()`, and the isolation level
- The "last seat sold twice" race, and two fixes: a row lock (`FOR UPDATE`) and a unique constraint
- Four pitfalls: renames, `PendingRollbackError`, missing metadata, editing a shared migration

## Before you start

- Python 3.14 or newer: `python --version`
- Docker running (pinned image `postgres:17`)
- Lessons M16-L02 and M16-L03 (sessions and models). This folder is self-contained
- A virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Versions in the video: SQLAlchemy 2.1.6, Alembic 1.20.1, psycopg 3.3.6. The database user and password (`allcs` / `secret`) are demo values.

## Files in this folder

| File | What it is |
|------|------------|
| `requirements.txt` | Pinned packages |
| `db.py` | The engine URL (port 15404, database `allcsvideos`) |
| `models_v1.py` | The models before the change: no `seats` column |
| `models.py` | The final models, with `seats` (server default 30) |
| `setup_v1.py` | The `create_all` era: builds the tables and saves 3 courses and 2 students |
| `show.py` | Prints each course and its seats (starts with `create_all`) |
| `alembic.ini`, `migrations/` | Alembic settings and the two migrations as they ended in the video (`create tables`, `add seats`) |
| `seed.py` | Saves 3 courses and 2 students (after the first migration) |
| `commit.py`, `begin.py`, `isolation.py` | Transactions: two sessions, `session.begin()`, isolation levels |
| `race.py`, `repeat_nopause.py`, `race_lock.py` | The double booking, the 200-run test, and the fix with a row lock |
| `twice.py` | Lukas double-clicks: the primary key stops the second enrolment |
| `pending.py`, `pending_fix.py` | `PendingRollbackError` and its fix |
| `_reset.py`, `_reset_data.py`, `sql` | Helper scripts: wipe the schema, reset seats and enrollments, run `psql` in the container |

The migration files in `migrations/versions/` have IDs like `1d0d7e49b5cb`. Yours will be different when you generate your own.
To follow along from scratch, work in a copy of this folder and delete `alembic.ini` and `migrations/` first (step 3).

## Follow along

### 1. Start Postgres

```bash
docker run --name m16l04-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=allcsvideos -p 15404:5432 -d postgres:17
```

### 2. The problem: `create_all` never changes a table

Start with the old models and the old tables:

```bash
cp models_v1.py models.py
python setup_v1.py
```

```text
tables created, 3 courses and 2 students saved
```

Now add one line to the `Course` model, below `level`: `seats: Mapped[int]`. Then:

```bash
python show.py
```

```text
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) column courses.seats does not exist
...
```

`create_all` only builds tables that are missing. The `courses` table exists, so it is left alone. We need migrations: numbered changes, written as small Python files, each with an `upgrade()` and a `downgrade()`. Alembic keeps the id of the last applied one in a one-row table, `alembic_version`.

### 3. Set up Alembic

Reset to the old situation first (wipe the schema, go back to the old models):

```bash
python _reset.py
cp models_v1.py models.py
alembic init migrations
```

`init` creates `alembic.ini` and a `migrations/` folder. Open `migrations/env.py` and replace the line `target_metadata = None` with:

```python
from db import URL
from models import Base

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", URL)
```

(The URL and the models are the two things Alembic must know.)

### 4. The first migration

```bash
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```

You should see lines like:

```text
INFO  [alembic.autogenerate.compare.tables] Detected added table 'courses'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'students'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'enrollments'
Generating .../migrations/versions/1d0d7e49b5cb_create_tables.py ...  done
...
INFO  [alembic.runtime.migration] Running upgrade  -> 1d0d7e49b5cb, create tables
```

Read the generated file: `down_revision = None` (nothing before it), three `op.create_table(...)` in `upgrade()`, and the drops in the opposite order in `downgrade()`. Look inside Postgres:

```bash
./sql '\dt'
./sql 'SELECT * FROM alembic_version'
python seed.py
```

(`sql` is a tiny script that runs `psql` in the container.)

```text
            List of relations
 Schema |      Name       | Type  | Owner 
--------+-----------------+-------+-------
 public | alembic_version | table | allcs
 public | courses         | table | allcs
 public | enrollments     | table | allcs
 public | students        | table | allcs
(4 rows)

 version_num  
--------------
 1d0d7e49b5cb
(1 row)

3 courses and 2 students saved
```

### 5. A second migration: add `seats`

Add `seats: Mapped[int]` to `Course` in `models.py` again, then:

```bash
alembic revision --autogenerate -m "add seats"
```

It reports `Detected added column 'courses.seats'` and writes a file whose `upgrade()` is:

```python
op.add_column('courses', sa.Column(
    'seats', sa.Integer(), nullable=False))
```

(The video wraps the line like this so it fits on screen.) The table already holds three rows. Guess what `alembic upgrade head` does.

```text
sqlalchemy.exc.IntegrityError: (psycopg.errors.NotNullViolation) column "seats" of relation "courses" contains null values
[SQL: ALTER TABLE courses ADD COLUMN seats INTEGER NOT NULL]
```

```bash
alembic current
```

```text
1d0d7e49b5cb
```

It failed, and nothing is half done: we are still at the old id. The fix is a server default, in two places that must agree. In the migration file:

```python
op.add_column('courses', sa.Column(
    'seats', sa.Integer(), nullable=False, server_default='30'))
```

and in the model:

```python
seats: Mapped[int] = mapped_column(server_default="30")
```

```bash
alembic upgrade head
./sql "SELECT * FROM courses"
alembic check
```

```text
INFO  [alembic.runtime.migration] Running upgrade 1d0d7e49b5cb -> a2ed3c4e42fe, add seats
 id |        title        | price |  level   | seats 
----+---------------------+-------+----------+-------
  1 | Python Basics       |   499 | beginner |    30
  2 | SQL in Docker       |   799 | beginner |    30
  3 | FastAPI Live Cohort |  1499 | advanced |    30
(3 rows)

No new upgrade operations detected.
```

`alembic check` compares the models with the database. Now the way back:

```bash
alembic downgrade -1
./sql "SELECT * FROM courses"
alembic upgrade head
alembic history
alembic current
```

```text
INFO  [alembic.runtime.migration] Running downgrade a2ed3c4e42fe -> 1d0d7e49b5cb, add seats
 id |        title        | price |  level   
----+---------------------+-------+----------
  1 | Python Basics       |   499 | beginner
  2 | SQL in Docker       |   799 | beginner
  3 | FastAPI Live Cohort |  1499 | advanced
(3 rows)

INFO  [alembic.runtime.migration] Running upgrade 1d0d7e49b5cb -> a2ed3c4e42fe, add seats
1d0d7e49b5cb -> a2ed3c4e42fe (head), add seats
<base> -> 1d0d7e49b5cb, create tables
a2ed3c4e42fe (head)
```

A downgrade deleted the `seats` column and its values. In production, a downgrade can delete data. The loop: change the model, autogenerate, read the file, upgrade.

### 6. Transactions: all or nothing

(From here the files `models.py` and the database are at the final state.)

```bash
python _reset_data.py 30
python commit.py
```

```text
a sees: 1  b sees: 0
after commit, b sees: 1
after rollback, a sees: 1
```

Session A's work is invisible to B until A commits. `rollback` throws away the second enrolment.

```bash
python _reset_data.py 30
python begin.py
```

```text
saved: 1
error: card declined
saved: 1
```

`with Session(engine) as s, s.begin():` commits when the block ends normally and rolls back when an error leaves it.

### 7. Isolation levels

```bash
python _reset_data.py 30
python isolation.py
```

```text
READ COMMITTED: 0 then 1
REPEATABLE READ: 1 then 1
```

The default, read committed, lets the second count see a commit that happened in between. Repeatable read keeps a frozen picture.

### 8. The race: the last seat sold twice

`race.py` has Lukas and Priya book a course with one seat left. Each thread reads the free seats, waits half a second (payment, email), then adds an enrolment.

```bash
python _reset_data.py 1
python race.py
```

```text
0.0s  Priya sees seats left: 1
0.0s  Lukas sees seats left: 1
0.5s  Lukas booked it
0.5s  Priya booked it
0.5s  seats: 1, booked: 2
```

Two bookings for one seat and no error. (Who is listed first can differ.) Without the pause it still happens:

```bash
python repeat_nopause.py
```

```text
193 of 200
```

That is the number of double bookings in 200 runs on our machine; the video showed 198. Yours will differ, but it will be almost all of them.

### 9. Fix 1: lock the row

`race_lock.py` selects the course with `.with_for_update()`, which becomes `SELECT ... FOR UPDATE`. The second request waits until the first transaction ends.

```bash
python _reset_data.py 1
python race_lock.py
```

```text
0.0s  Lukas sees seats left: 1
0.5s  Lukas booked it
0.5s  Priya sees seats left: 0
0.5s  Priya: sold out
0.5s  seats: 1, booked: 1
```

Run it again and Priya may win. Either way, the seat is sold once. A lock makes everyone else wait, so keep the locked part short (lock, check, write, commit).

### 10. Fix 2: a constraint

Lukas double-clicks, and two requests try to enrol him in the same course. The Python check ("already enrolled?") is fooled, but the primary key `(student_id, course_id)` of `enrollments` is not.

```bash
python _reset_data.py 30
python twice.py
./sql "SELECT student_id, course_id FROM enrollments"
```

```text
click 2 enrolled Lukas
click 1 too late: the database said no
 student_id | course_id 
------------+-----------
          1 |          1
(1 row)
```

A limit on "how many": lock the row, then check. A rule that something must be unique: let the database enforce it and catch the error.

### 11. Pitfalls

Pitfall 1, a rename. Change `title` to `name` in `Course` and run `alembic revision --autogenerate -m "rename title"`. Alembic cannot know it is a rename: it writes `add_column('name')` and `drop_column('title')`, which would lose every title. Edit the file by hand:

```python
def upgrade() -> None:
    op.alter_column('courses', 'title', new_column_name='name')

def downgrade() -> None:
    op.alter_column('courses', 'name', new_column_name='title')
```

`alembic upgrade head` then shows the same rows with a `name` column, and `alembic downgrade -1` brings `title` back. (Delete this experiment's migration file and undo the model change afterwards; it is not part of the final project.)

Pitfall 2, `PendingRollbackError`:

```bash
python _reset_data.py 30
python pending.py
python _reset_data.py 30
python pending_fix.py
```

```text
sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: (psycopg.errors.UniqueViolation) duplicate key value violates unique constraint "enrollments_pkey"
DETAIL:  Key (student_id, course_id)=(1, 1) already exists.
...
```

```text
already enrolled
1
```

After a failed commit, call `s.rollback()` first in the error handler (that is the only difference in `pending_fix.py`).

Pitfall 3: if `target_metadata = None` in `env.py`, autogenerate fails with `Can't proceed with --autogenerate option; environment script ... does not provide a MetaData object`. Check that line and that the models are imported.

Pitfall 4: once a migration is shared (a teammate or production already ran it), never edit it. Write a new migration instead.

## Common mistakes

- Expecting `create_all` to change an existing table.
- Adding a `nullable=False` column with no default to a table that has rows.
- Trusting autogenerate without reading the file (renames become drop and add).
- "Check, then write" without a lock or a constraint: a race.
- Holding a row lock while doing slow work.
- Forgetting `rollback()` after a failed commit.

## Clean up

```bash
docker rm -f -v m16l04-pg
deactivate
rm -rf .venv
```

## Next

[M16-L05 · Async SQLAlchemy and Connection Pools](../m16-l05-async-sqlalchemy-and-connection-pools/)
