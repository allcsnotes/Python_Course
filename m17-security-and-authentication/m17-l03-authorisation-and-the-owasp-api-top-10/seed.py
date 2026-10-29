import sys
from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session

sys.path.insert(0, "allcs")
from app.auth import hasher  # noqa: E402
from app.db import engine  # noqa: E402
from app.models import Course, Enrollment, Lesson, Student  # noqa: E402

PEOPLE = [
    ("Lukas", "student"),
    ("Priya", "student"),
    ("Meera", "instructor"),
    ("Asha", "admin"),
]
COURSES = [
    ("Python Basics", 499, "beginner"),
    ("SQL in Two Weeks", 599, "beginner"),
    ("Git and GitHub", 299, "beginner"),
    ("Docker for Developers", 899, "intermediate"),
]
ENROLL = [
    (1, 1, date(2026, 9, 1)),
    (1, 2, date(2026, 9, 2)),
    (2, 2, date(2026, 9, 3)),
    (2, 4, date(2026, 9, 4)),
]
with Session(engine) as s:
    s.execute(text("truncate enrollments, lessons, courses, students restart identity cascade"))
    for name, role in PEOPLE:
        low = name.lower()
        s.add(Student(name=name, email=f"{low}@example.com", role=role, password_hash=hasher.hash(f"{low}-demo-pass")))
    for title, price, level in COURSES:
        c = Course(title=title, price=price, level=level)
        c.lessons = [Lesson(title=t, position=i) for i, t in enumerate(["Welcome", "Setup"], 1)]
        s.add(c)
    s.flush()
    for st, co, d in ENROLL:
        s.add(Enrollment(student_id=st, course_id=co, enrolled_on=d))
    s.commit()
print("seeded")
