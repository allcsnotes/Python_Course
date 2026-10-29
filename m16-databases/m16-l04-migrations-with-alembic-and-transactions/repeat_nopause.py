import threading, time
import psycopg
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from db import engine
from models import Course, Enrollment
def one():
    with psycopg.connect("postgresql://allcs:secret@localhost:15404/allcsvideos", autocommit=True) as c:
        c.execute("DELETE FROM enrollments"); c.execute("UPDATE courses SET seats=1 WHERE id=3")
    def book(sid):
        with Session(engine) as s:
            course = s.get(Course, 3)
            left = course.seats - s.scalar(select(func.count()).where(Enrollment.course_id == 3))
            if left > 0:
                s.add(Enrollment(student_id=sid, course_id=3)); s.commit()
    th = [threading.Thread(target=book, args=(i,)) for i in (1, 2)]
    for t in th: t.start()
    for t in th: t.join()
    with Session(engine) as s:
        return s.scalar(select(func.count()).where(Enrollment.course_id == 3))
r = [one() for _ in range(200)]
print(sum(1 for x in r if x > 1), "of", len(r))
