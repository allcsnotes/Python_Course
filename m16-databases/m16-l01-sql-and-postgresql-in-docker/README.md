# M16-L01 · SQL and PostgreSQL in Docker

> Video: Module 16, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why a database keeps the data safe and shared, where a Python list cannot
- How to start PostgreSQL 17 in Docker with a name, a password, a volume and a port
- Tables, columns and types: `CREATE TABLE`, `INSERT`, `SELECT` with `WHERE`, `ORDER BY`, `LIMIT`, `OFFSET`, `UPDATE`, `DELETE`
- Primary keys, foreign keys and `JOIN`, using Asha's courses, students and enrollments
- What an index is and how `EXPLAIN ANALYZE` shows it making a search faster

## Before you start

- Python is not needed in this lesson. If you want to check your tools anyway: `python --version` should say Python 3.14 or newer.
- Docker Desktop (or Docker Engine) running: `docker --version`. We use the pinned image `postgres:17`.
- No earlier lesson folder is needed. (The eight courses are the same ones as the catalog in Module 15.)
- Every password here (`devpass`) and every email is a demo value. Never reuse them anywhere real.

## Files in this folder

| File | What it is |
|------|------------|
| `lesson.sql` | Every statement of the video, in order. You can type them by hand (best) or run the whole file at the end |

## Follow along

### 1. Start Postgres in a Docker box

```bash
docker run --name m16l01-pg \
  -e POSTGRES_PASSWORD=devpass \
  -v m16l01-data:/var/lib/postgresql/data \
  -p 15401:5432 -d postgres:17
docker ps --filter name=m16l01-pg --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

`docker run` prints a long container ID. The first time, Docker also downloads the image (about a minute). Then you should see:

```text
NAMES       STATUS                  PORTS
m16l01-pg   Up Less than a second   0.0.0.0:15401->5432/tcp, [::]:15401->5432/tcp
```

- `-e` sets the password of the database user `postgres`.
- `-v` gives the box a named shelf (a volume) outside itself, so the data survives. Remember this for step 10.
- `-p 15401:5432` opens port 15401 on your computer and sends it to Postgres's own port 5432 inside the box.
- `-d` runs it in the background.

### 2. Open psql, make a database

`psql` is the small program that comes with Postgres, for typing SQL.

```bash
docker exec -it m16l01-pg psql -U postgres
```

You land at a `postgres=#` prompt. Everything below is typed there. Every SQL statement ends with a semicolon. Lines starting with a backslash are psql commands and need no semicolon.

```sql
CREATE DATABASE allcs;
\c allcs
SHOW server_version;
```

```text
CREATE DATABASE
You are now connected to database "allcs" as user "postgres".
         server_version
---------------------------------
 17.11 (Debian 17.11-1.pgdg13+2)
(1 row)
```

(The last digits of the version may be newer for you.)

### 3. Create the courses table

```sql
CREATE TABLE courses (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title text NOT NULL,
  price integer NOT NULL,
  level text NOT NULL
);
\d courses
```

`id` is numbered by Postgres itself (1, 2, 3 ...) and is the primary key: no two rows may share it. `NOT NULL` means the value cannot be left empty. `price` is a whole number of rupees.

```text
CREATE TABLE
                         Table "public.courses"
 Column |  Type   | Collation | Nullable |           Default
--------+---------+-----------+----------+------------------------------
 id     | integer |           | not null | generated always as identity
 title  | text    |           | not null |
 price  | integer |           | not null |
 level  | text    |           | not null |
Indexes:
    "courses_pkey" PRIMARY KEY, btree (id)
```

The index `courses_pkey` was built for the primary key automatically.

### 4. Insert rows

```sql
INSERT INTO courses (title, price, level)
VALUES ('Python Basics', 499, 'beginner');
INSERT INTO courses (title, price, level) VALUES
  ('SQL in Two Weeks', 399, 'beginner'),
  ('Git and GitHub', 299, 'beginner'),
  ('Docker for Developers', 599, 'intermediate'),
  ('FastAPI in Practice', 699, 'intermediate'),
  ('Async Python', 799, 'advanced'),
  ('Python Performance', 899, 'advanced'),
  ('Linux Essentials', 349, 'beginner');
```

```text
INSERT 0 1
INSERT 0 7
```

Text goes in single quotes, numbers do not. In `INSERT 0 1` the 0 is a leftover from old times; the last number is the rows added.

### 5. Read rows with SELECT

```sql
SELECT * FROM courses;
```

```text
 id |         title         | price |    level
----+-----------------------+-------+--------------
  1 | Python Basics         |   499 | beginner
  2 | SQL in Two Weeks      |   399 | beginner
  3 | Git and GitHub        |   299 | beginner
  4 | Docker for Developers |   599 | intermediate
  5 | FastAPI in Practice   |   699 | intermediate
  6 | Async Python          |   799 | advanced
  7 | Python Performance    |   899 | advanced
  8 | Linux Essentials      |   349 | beginner
(8 rows)
```

Pick columns, and filter with `WHERE` (one `=`, not two: SQL is not Python):

```sql
SELECT title, price FROM courses;
SELECT title, price FROM courses WHERE level = 'beginner';
```

```text
      title       | price
------------------+-------
 Python Basics    |   499
 SQL in Two Weeks |   399
 Git and GitHub   |   299
 Linux Essentials |   349
(4 rows)
```

(The first query prints the eight titles and prices, with no filter.)

Guess first: which beginner courses cost under 400, and in what order?

```sql
SELECT title, price FROM courses
WHERE level = 'beginner' AND price < 400
ORDER BY price DESC;
```

```text
      title       | price
------------------+-------
 SQL in Two Weeks |   399
 Linux Essentials |   349
 Git and GitHub   |   299
(3 rows)
```

Paging, as in the catalog of Module 15 (`LIMIT` = how many rows, `OFFSET` = how many to skip), and counting:

```sql
SELECT id, title FROM courses WHERE level = 'beginner'
ORDER BY id LIMIT 2 OFFSET 2;
SELECT count(*) FROM courses WHERE level = 'beginner';
```

```text
 id |      title
----+------------------
  3 | Git and GitHub
  8 | Linux Essentials
(2 rows)

 count
-------
     4
(1 row)
```

Always add `ORDER BY` when the order matters. Without it Postgres may return rows in any order.

### 6. Change and delete rows

```sql
UPDATE courses SET price = 449 WHERE title = 'Python Basics';
SELECT id, title, price FROM courses WHERE id = 1;
INSERT INTO courses (title, price, level) VALUES ('Test Course', 1, 'beginner');
DELETE FROM courses WHERE title = 'Test Course';
```

```text
UPDATE 1
 id |     title     | price
----+---------------+-------
  1 | Python Basics |   449
(1 row)

INSERT 0 1
DELETE 1
```

The most dangerous mistake: forgetting `WHERE`. We try it inside a trial (`BEGIN` ... `ROLLBACK`, explained in lesson 4 of this module). Guess how many rows change:

```sql
BEGIN;
UPDATE courses SET price = 1;
SELECT id, title, price FROM courses ORDER BY id;
ROLLBACK;
SELECT id, title, price FROM courses ORDER BY id;
```

```text
BEGIN
UPDATE 8
(all eight courses now show price 1)
ROLLBACK
(all eight courses show their real prices again, Python Basics at 449)
```

SQL did exactly what you typed and never asked "are you sure?". Write the `WHERE` first, or run a `SELECT` with the same `WHERE` before an update or delete.

### 7. Keys: students and enrollments

```sql
CREATE TABLE students (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL,
  email text NOT NULL UNIQUE
);
INSERT INTO students (name, email) VALUES
  ('Lukas', 'lukas@example.com'),
  ('Priya', 'priya@example.com'),
  ('Ben', 'ben@example.com');
CREATE TABLE enrollments (
  student_id integer NOT NULL REFERENCES students (id),
  course_id integer NOT NULL REFERENCES courses (id),
  enrolled_on date NOT NULL,
  PRIMARY KEY (student_id, course_id)
);
INSERT INTO enrollments VALUES
  (1, 1, '2026-10-01'), (1, 2, '2026-10-03'),
  (2, 2, '2026-10-02'), (2, 3, '2026-10-04'),
  (2, 5, '2026-10-09'), (3, 2, '2026-10-07');
```

`REFERENCES` makes a foreign key: a column that points into another table. The primary key here is the pair of columns, so one student can enrol in one course only once. (`@example.com` is a reserved demo domain.) Now try to break the rules; each of these must fail:

```sql
INSERT INTO enrollments VALUES (1, 2, '2026-10-12');
INSERT INTO enrollments VALUES (99, 1, '2026-10-12');
DELETE FROM courses WHERE id = 2;
```

```text
ERROR:  duplicate key value violates unique constraint "enrollments_pkey"
DETAIL:  Key (student_id, course_id)=(1, 2) already exists.
ERROR:  insert or update on table "enrollments" violates foreign key constraint "enrollments_student_id_fkey"
DETAIL:  Key (student_id)=(99) is not present in table "students".
ERROR:  update or delete on table "courses" violates foreign key constraint "enrollments_course_id_fkey" on table "enrollments"
DETAIL:  Key (id)=(2) is still referenced from table "enrollments".
```

The database itself blocks a double enrolment, whatever Python code runs on top. The build project at the end of the module relies on this.

### 8. Join tables

```sql
SELECT students.name, enrollments.course_id
FROM enrollments
JOIN students ON students.id = enrollments.student_id;

SELECT s.name, c.title
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id
ORDER BY s.name, c.title;
```

```text
 name  |        title
-------+---------------------
 Ben   | SQL in Two Weeks
 Lukas | Python Basics
 Lukas | SQL in Two Weeks
 Priya | FastAPI in Practice
 Priya | Git and GitHub
 Priya | SQL in Two Weeks
(6 rows)
```

(The first query prints six rows with the student name and a course number.) A course title is stored once, so nothing can disagree.

### 9. Indexes: make a search fast

Make half a million fake page views:

```sql
CREATE TABLE page_views (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  student_id integer NOT NULL,
  course_id integer NOT NULL
);
INSERT INTO page_views (student_id, course_id)
SELECT random() * 49999 + 1, random() * 7 + 1
FROM generate_series(1, 500000);
SELECT count(*) FROM page_views;
SELECT count(*) FROM page_views WHERE student_id = 4242;
```

`count(*)` prints `500000`. The data is random, so the second count (13 in our run, 6 in the video) will differ for you. Switch off parallel workers so the plan stays short, then ask for the plan:

```sql
SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM page_views WHERE student_id = 4242;
```

```text
                             QUERY PLAN
--------------------------------------------------------------------
 Seq Scan on page_views (actual time=1.050..16.524 rows=13 loops=1)
   Filter: (student_id = 4242)
   Rows Removed by Filter: 499987
 Planning Time: 0.038 ms
 Execution Time: 16.537 ms
```

A sequential scan: Postgres read all half a million rows to find a handful. Now add an index (a sorted list of values with the place of their rows, like the index of a book) and ask again:

```sql
CREATE INDEX page_views_student_idx
ON page_views (student_id);
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM page_views WHERE student_id = 4242;
SELECT pg_size_pretty(pg_relation_size('page_views')) AS table_size,
pg_size_pretty(pg_relation_size('page_views_student_idx')) AS index_size;
```

```text
 Bitmap Heap Scan on page_views (actual time=0.020..0.033 rows=13 loops=1)
   Recheck Cond: (student_id = 4242)
   Heap Blocks: exact=13
   ->  Bitmap Index Scan on page_views_student_idx (actual time=0.016..0.016 rows=13 loops=1)
         Index Cond: (student_id = 4242)
 Planning Time: 0.096 ms
 Execution Time: 0.041 ms

 table_size | index_size
------------+------------
 21 MB      | 4552 kB
(1 row)
```

Yours will differ in times and in the row count, but the plan changes the same way (video: 23.48 ms down to 0.056 ms). An index costs space and slows writes, so index what you search and join on, not every column.

### 10. Data that survives

Leave psql with `\q`. Destroy the box and start a new one with the same name and the same volume:

```bash
docker rm -f m16l01-pg
docker run --name m16l01-pg \
  -e POSTGRES_PASSWORD=devpass \
  -v m16l01-data:/var/lib/postgresql/data \
  -p 15401:5432 -d postgres:17
docker exec m16l01-pg psql -U postgres -d allcs -c "SELECT count(*) FROM courses"
```

```text
 count
-------
     8
(1 row)
```

The box is new, but the volume kept the data. Without a named volume the next box starts empty. Any number of programs can connect to this one Postgres through port 15401 and see the same courses.

### Run it all at once (optional)

With the container from step 1 running and an empty Postgres:

```bash
docker exec -i m16l01-pg psql -U postgres < lesson.sql
```

## Common mistakes

- Missing semicolon: type `SELECT count(*) FROM courses` and Enter, and the prompt changes to `-`. psql is waiting for more. Type `;` and it runs.
- Wrong quotes: `WHERE level = "beginner"` fails with `column "beginner" does not exist`. Single quotes are for text values, double quotes are for names of columns and tables.
- `UPDATE` or `DELETE` without `WHERE` changes every row.
- Never glue text from a user into a SQL statement yourself. Lesson 2 shows the safe way, Module 17 the attack it prevents.
- Starting Postgres without `-v` and a name: the data disappears with the box.

## Clean up

```bash
docker rm -f -v m16l01-pg
docker volume rm m16l01-data
```

## Next

[M16-L02 · SQLAlchemy Core Ideas](../m16-l02-sqlalchemy-core-ideas/)
