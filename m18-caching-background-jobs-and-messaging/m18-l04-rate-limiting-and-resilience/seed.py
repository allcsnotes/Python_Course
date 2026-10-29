import sys

from sqlalchemy import text
from sqlalchemy.orm import Session

sys.path.insert(0, "allcs")
from app.db import engine  # noqa: E402
from app.models import Course, Lesson, Student  # noqa: E402
from app.security import hash_password  # noqa: E402

PEOPLE = [("Lukas", "student"), ("Priya", "student"), ("Meera", "instructor"), ("Asha", "admin")]
COURSES = [("Python Basics", 499, "beginner"), ("SQL in Two Weeks", 599, "beginner"), ("Git and GitHub", 299, "beginner"), ("Docker for Developers", 899, "intermediate")]
with Session(engine) as s:
    s.execute(text("truncate enrollments, lessons, courses, students restart identity cascade"))
    for name, role in PEOPLE:
        low = name.lower()
        s.add(Student(name=name, email=f"{low}@example.com", role=role, password_hash=hash_password(f"{low}-demo-pass")))
    for title, price, level in COURSES:
        c = Course(title=title, price=price, level=level)
        c.lessons = [Lesson(title=t, position=i) for i, t in enumerate(["Welcome", "Setup"], 1)]
        s.add(c)
    s.commit()
print("seeded")
