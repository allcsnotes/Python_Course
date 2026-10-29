INSERT INTO students (email, password_hash, role) VALUES
 ('lukas@example.com', 'x', 'student'),
 ('priya@example.com', 'x', 'student'),
 ('meera@example.com', 'x', 'instructor');
INSERT INTO courses (title, price) VALUES
 ('Python Basics', 499), ('Git and GitHub', 299), ('SQL in Two Weeks', 399);
INSERT INTO lessons (course_id, position, title) VALUES
 (1, 1, 'Variables'), (1, 2, 'Loops'), (1, 3, 'Functions'),
 (2, 1, 'Commits'), (2, 2, 'Branches'),
 (3, 1, 'SELECT'), (3, 2, 'JOIN');
