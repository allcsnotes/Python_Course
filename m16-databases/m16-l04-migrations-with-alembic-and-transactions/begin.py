from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import engine
from models import Enrollment


def enrol(crash):
    with Session(engine) as s, s.begin():
        s.add(Enrollment(student_id=2, course_id=2))
        if crash:
            raise RuntimeError("card declined")


def total():
    with Session(engine) as s:
        return s.scalar(select(func.count()).select_from(Enrollment))


enrol(crash=False)
print("saved:", total())
try:
    enrol(crash=True)
except RuntimeError as error:
    print("error:", error)
print("saved:", total())
