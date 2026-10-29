import sys
from sqlalchemy import text
from sqlalchemy.orm import Session

sys.path.insert(0, "allcs")
from app.db import engine
from app.models import Course, Enrollment, Student
from app.security import hash_password

PASSWORD = "demo-password-1"
with Session(engine) as s:
    s.execute(text('truncate enrollments, courses, refresh_tokens, students restart identity cascade'))
    people = [Student(name=n, email=f"{n.lower()}@example.com", role=r, password_hash=hash_password(PASSWORD))
              for n, r in (("Lukas", "student"), ("Priya", "student"), ("Asha", "admin"))]
    s.add_all(people)
    s.add_all([Course(title="Python Basics", price=999, level="beginner"), Course(title="Async Python", price=1499, level="advanced")])
    s.flush()
    c = s.query(Course).order_by(Course.id).all()
    s.add_all([Enrollment(student_id=people[1].id, course_id=c[0].id), Enrollment(student_id=people[1].id, course_id=c[1].id)])
    s.commit()
    print("courses", [x.id for x in c], "students", [x.id for x in people])
