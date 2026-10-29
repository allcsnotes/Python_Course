import sys
from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session

sys.path.insert(0, "allcs")
from app.db import engine  # noqa: E402
from app.models import Course, Enrollment, Lesson, Student  # noqa: E402
from app.security import hash_password  # noqa: E402

PEOPLE = [("Lukas", "student"), ("Priya", "student"), ("Meera", "instructor"), ("Asha", "admin")]
with Session(engine) as s:
    s.execute(text("truncate refresh_tokens, enrollments, lessons, courses, students restart identity cascade"))
    for name, role in PEOPLE:
        low = name.lower()
        s.add(Student(name=name, email=f"{low}@example.com", role=role, password_hash=hash_password(f"{low}-demo-pass")))
    s.flush()
    titles = ["Python Basics", "SQL in Two Weeks", "Git and GitHub", "Docker for Developers"]
    for i in range(300):
        title = titles[i] if i < 4 else f"Course {i + 1}"
        c = Course(title=title, price=[499, 599, 299, 899][i] if i < 4 else 299 + (i % 7) * 100, level=["beginner", "intermediate", "advanced"][i % 3], owner_id=3)
        c.lessons = [Lesson(title=f"Lesson {p}", position=p) for p in range(1, 31)]
        s.add(c)
    s.flush()
    s.add(Enrollment(student_id=1, course_id=1, enrolled_on=date(2026, 9, 1)))
    s.commit()
print("seeded")
