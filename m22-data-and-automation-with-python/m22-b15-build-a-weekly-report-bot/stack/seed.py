"""Seeds a week of data for the report bot demo (generated for the course, fixed seed)."""
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Course, Enrollment, Lesson, Student
from app.security import hash_password

IST = timezone(timedelta(hours=5, minutes=30))
rng = random.Random(2026)
COURSES = [("Python Basics", 499, "beginner"), ("SQL in Two Weeks", 599, "beginner"),
           ("Async Python", 1999, "advanced"), ("Git for Teams", 399, "beginner"), ("Docker for Python Apps", 899, "intermediate")]
WEIGHTS = [8, 5, 2, 3, 4]


def at(day, hour, minute):  # a moment in India time
    return datetime(2026, 10, day, hour, minute, tzinfo=IST)


with Session(engine) as s:
    s.execute(text("truncate enrollments, lessons, courses, students restart identity cascade"))
    s.add(Student(name="Report Bot", email="reports@allcsvideos.com", role="admin", password_hash=hash_password("demo-report-bot-pass")))
    s.add(Student(name="Meera", email="meera@allcsvideos.com", role="instructor", password_hash=hash_password("meera-demo-pass")))
    for i in range(1, 61):
        s.add(Student(name=f"Student {i:02d}", email=f"student{i:02d}@example.com", role="student"))
    for title, price, level in COURSES:
        c = Course(title=title, price=price, level=level)
        c.lessons = [Lesson(title="Welcome", position=1)]
        s.add(c)
    s.flush()
    students = list(range(3, 63))
    rng.shuffle(students)
    pool = {c: [] for c in range(1, 6)}
    moments = []
    # last week before the report week (12-18 Oct): 14 enrollments
    for _ in range(14):
        moments.append(at(rng.randint(12, 18), rng.randint(7, 22), rng.randint(0, 59)))
    # the report week (19-25 Oct, India time): 32 spread over the days, more on weekdays
    for _ in range(32):
        day = rng.choices(range(19, 26), [6, 6, 5, 5, 4, 2, 2])[0]
        moments.append(at(day, rng.randint(7, 22), rng.randint(0, 59)))
    # the boundary cases: two just after Monday midnight, two just before Sunday midnight, India time
    moments += [at(19, 0, 20), at(19, 0, 45), at(25, 23, 15), at(25, 23, 50)]
    # two just after the end of the report week (Monday 26 Oct, India time), and a few later this week
    moments += [at(26, 0, 40), at(26, 1, 10), at(26, 3, 20), at(26, 9, 5), at(27, 11, 30), at(27, 16, 42), at(28, 8, 15)]
    k = 0
    for m in sorted(moments):
        course = rng.choices(range(1, 6), WEIGHTS)[0]
        student = students[k]; k += 1
        s.add(Enrollment(student_id=student, course_id=course, enrolled_at=m, enrolled_on=m.astimezone(IST).date(),
                         amount=COURSES[course - 1][1]))
    s.flush()
    # refunds paid in the report week: two from last week's enrollments, three from this week's
    rows = s.query(Enrollment).order_by(Enrollment.enrolled_at).all()
    def pick(lo, hi, n):
        return [e for e in rows if lo <= e.enrolled_at < hi][:n]
    for e, when in zip(pick(at(12, 0, 0), at(19, 0, 0), 2), [at(20, 11, 0), at(22, 15, 30)]):
        e.refunded_at = when
    for e, when in zip(pick(at(19, 6, 0), at(23, 0, 0), 3), [at(21, 10, 5), at(23, 9, 40), at(24, 17, 25)]):
        e.refunded_at = when
    s.commit()
print("seeded")
