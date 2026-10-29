-- demo data for the lesson: 200,000 students and about one million enrollments (all fake)
INSERT INTO courses (title, price) SELECT 'Course ' || g, 100 + g FROM generate_series(4, 60) g;
INSERT INTO students (email, password_hash) SELECT 'user' || g || '@example.com', 'x' FROM generate_series(1, 200000) g;
INSERT INTO enrollments (student_id, course_id) SELECT s.id, 1 + ((s.id + k * 7) % 60) FROM students s, generate_series(0, 4) k WHERE s.id > 3;
ANALYZE;
