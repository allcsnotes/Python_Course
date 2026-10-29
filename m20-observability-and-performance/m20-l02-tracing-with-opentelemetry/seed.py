from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Course, Lesson, Student
from app.security import hash_password

PEOPLE = [("Lukas", "student"), ("Priya", "student"), ("Meera", "instructor")]
COURSES = [("Python Basics", 499, "beginner"), ("SQL in Two Weeks", 599, "beginner")]
with Session(engine) as s:
    s.execute(text("truncate enrollments, lessons, courses, students restart identity cascade"))
    for name, role in PEOPLE:
        low = name.lower()
        s.add(Student(name=name, email=f"{low}@example.com", role=role, password_hash=hash_password(f"{low}-demo-pass")))
    for title, price, level in COURSES:
        c = Course(title=title, price=price, level=level)
        c.lessons = [Lesson(title="Welcome", position=1)]
        s.add(c)
    s.commit()
print("seeded")
