-- M16-L01: every statement from the video, in order.
-- Run: docker exec -i m16l01-pg psql -U postgres < lesson.sql   (the video types these by hand)
-- Demo data only: all names and emails are made up.

CREATE DATABASE allcs;
\c allcs
SHOW server_version;
CREATE TABLE courses (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title text NOT NULL,
  price integer NOT NULL,
  level text NOT NULL
);
\d courses
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
SELECT * FROM courses;
SELECT title, price FROM courses;
SELECT title, price FROM courses WHERE level = 'beginner';
-- guess first: which courses, in what order?
SELECT title, price FROM courses
WHERE level = 'beginner' AND price < 400
ORDER BY price DESC;
SELECT id, title FROM courses WHERE level = 'beginner'
ORDER BY id LIMIT 2 OFFSET 2;
SELECT count(*) FROM courses WHERE level = 'beginner';
UPDATE courses SET price = 449 WHERE title = 'Python Basics';
SELECT id, title, price FROM courses WHERE id = 1;
INSERT INTO courses (title, price, level) VALUES ('Test Course', 1, 'beginner');
DELETE FROM courses WHERE title = 'Test Course';
BEGIN;
UPDATE courses SET price = 1;
SELECT id, title, price FROM courses ORDER BY id;
ROLLBACK;
SELECT id, title, price FROM courses ORDER BY id;
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
-- the next three fail on purpose
INSERT INTO enrollments VALUES (1, 2, '2026-10-12');
INSERT INTO enrollments VALUES (99, 1, '2026-10-12');
DELETE FROM courses WHERE id = 2;
SELECT students.name, enrollments.course_id
FROM enrollments
JOIN students ON students.id = enrollments.student_id;
SELECT s.name, c.title
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id
ORDER BY s.name, c.title;
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
SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM page_views WHERE student_id = 4242;
CREATE INDEX page_views_student_idx
ON page_views (student_id);
EXPLAIN (ANALYZE, COSTS OFF)
SELECT * FROM page_views WHERE student_id = 4242;
SELECT pg_size_pretty(pg_relation_size('page_views')) AS table_size,
pg_size_pretty(pg_relation_size('page_views_student_idx')) AS index_size;
-- pitfall: wrong quotes (this one fails on purpose)
SELECT * FROM courses WHERE level = "beginner";
SELECT count(*) FROM courses;
