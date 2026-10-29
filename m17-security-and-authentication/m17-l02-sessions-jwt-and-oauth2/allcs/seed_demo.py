from sqlalchemy import text

from app.db import engine
from app.models import Course, Enrollment, Student
from app.security import hash_password
from sqlalchemy.orm import Session

with Session(engine) as s:
    s.execute(text("TRUNCATE refresh_tokens, enrollments, lessons, courses, students RESTART IDENTITY CASCADE"))
    s.add_all([
        Course(title="Python Basics", price=499, level="beginner"),
        Course(title="SQL in Two Weeks", price=599, level="beginner"),
    ])
    s.add_all([
        Student(name="Lukas", email="lukas@example.com", password_hash=hash_password("lukas-demo-password")),
        Student(name="Priya", email="priya@example.com", password_hash=hash_password("priya-demo-password")),
    ])
    s.flush()
    s.add(Enrollment(student_id=1, course_id=1))
    s.commit()
print("seeded")
