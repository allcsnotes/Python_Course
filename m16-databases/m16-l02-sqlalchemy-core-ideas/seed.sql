-- Hidden setup from the video: recreates what lesson 1 left in the database (all demo data).
DROP TABLE IF EXISTS courses CASCADE;
CREATE TABLE courses (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title text NOT NULL,
  price integer NOT NULL,
  level text NOT NULL
);
INSERT INTO courses (title, price, level) VALUES
  ('Python Basics', 449, 'beginner'),
  ('SQL in Two Weeks', 399, 'beginner'),
  ('Git and GitHub', 299, 'beginner'),
  ('Docker for Developers', 599, 'intermediate'),
  ('FastAPI in Practice', 699, 'intermediate'),
  ('Async Python', 799, 'advanced'),
  ('Python Performance', 899, 'advanced'),
  ('Linux Essentials', 349, 'beginner');
