create extension if not exists pg_stat_statements;
select setseed(0.42);
truncate enrollments, lessons, courses, students restart identity cascade;
-- 3 named people (passwords are set by seed.py), then 20000 students
insert into students (name, email, role) values
  ('Meera', 'meera@example.com', 'instructor'),
  ('Lukas', 'lukas@example.com', 'student'),
  ('Priya', 'priya@example.com', 'instructor');
insert into students (name, email, role)
  select 'Student ' || g, 'student' || g || '@example.com', 'student'
  from generate_series(1, 20000) g;
-- Meera owns 8 courses, other instructors' courses fill the catalogue (108 in all)
insert into courses (title, price, level, owner_id)
  select 'Course ' || g, 400 + (g % 7) * 100,
         (array['beginner','intermediate','advanced'])[1 + g % 3],
         case when g <= 8 then 1 else null end
  from generate_series(1, 108) g;
update courses set title = (array['Python Basics','SQL in Two Weeks','FastAPI Essentials','Testing with pytest','Docker for Beginners','Async Python','Data Structures','Clean Code'])[id] where id <= 8;
insert into lessons (course_id, title, position)
  select c.id, 'Lesson ' || p, p from courses c, generate_series(1, 6) p;
-- the other 100 courses: every student takes 10 random ones, about 200000 enrollments
insert into enrollments (student_id, course_id)
  select distinct s.id, 9 + floor(random() * 100)::int
  from students s, generate_series(1, 10) k;
-- Meera's 8 courses: 250 students each
insert into enrollments (student_id, course_id)
  select s.id, c.id from courses c
  cross join lateral (select id from students where c.id > 0 order by random() limit 250) s
  where c.id <= 8;
-- Priya has one tiny course with 3 students (the "works on my laptop" case)
insert into courses (title, price, level, owner_id) values ('Intro to Git', 299, 'beginner', 3);
insert into enrollments (student_id, course_id) select s, (select max(id) from courses) from unnest(array[2, 100, 200]) s;
analyze;
