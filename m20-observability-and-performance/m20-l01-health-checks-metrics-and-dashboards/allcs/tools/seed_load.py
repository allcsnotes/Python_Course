# runs inside the api container: 200 students, 40 courses, long-lived tokens
import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Course, Lesson, Student
from app.tokens import make_access_token

with Session(engine) as s:
    s.execute(text("truncate enrollments, lessons, courses, students restart identity cascade"))
    students = [Student(name=f"Student {i}", email=f"s{i}@example.com", role="student") for i in range(1, 201)]
    s.add_all(students)
    for i in range(1, 41):
        c = Course(title=f"Course {i}", price=499, level="beginner")
        c.lessons = [Lesson(title="Welcome", position=1)]
        s.add(c)
    s.commit()
    print(json.dumps([make_access_token(st.id) for st in students]))
