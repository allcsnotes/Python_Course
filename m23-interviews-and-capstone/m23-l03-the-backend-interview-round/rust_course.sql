-- one small course with just 40 students, to show the index on course_id
INSERT INTO courses (id, title, price) VALUES (61, 'Rust for Python Programmers', 999);
INSERT INTO enrollments (student_id, course_id) SELECT id, 61 FROM students WHERE id BETWEEN 1000 AND 1039;
ANALYZE;
