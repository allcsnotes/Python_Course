import threading
import time

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import engine
from models import Course, Enrollment

COURSE = 3
T0 = time.perf_counter()


def log(message):
    print(f"{time.perf_counter() - T0:3.1f}s  {message}")


def taken(s):
    return s.scalar(select(func.count()).where(
        Enrollment.course_id == COURSE))


def book(name, sid):
    with Session(engine) as s:
        course = s.get(Course, COURSE)
        left = course.seats - taken(s)
        log(f"{name} sees seats left: {left}")
        if left > 0:
            time.sleep(0.5)  # the payment, the email: real work
            s.add(Enrollment(student_id=sid, course_id=COURSE))
            s.commit()
            log(f"{name} booked it")
        else:
            log(f"{name}: sold out")


people = [("Lukas", 1), ("Priya", 2)]
threads = [threading.Thread(target=book, args=p) for p in people]
for t in threads:
    t.start()
for t in threads:
    t.join()
with Session(engine) as s:
    log(f"seats: {s.get(Course, COURSE).seats}, booked: {taken(s)}")
