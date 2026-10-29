from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import engine
from models import Enrollment


def count(s):
    return s.scalar(select(func.count()).select_from(Enrollment))


with Session(engine) as a, Session(engine) as b:
    a.add(Enrollment(student_id=1, course_id=1))
    print("a sees:", count(a), " b sees:", count(b))
    a.commit()
    print("after commit, b sees:", count(b))
    a.add(Enrollment(student_id=2, course_id=1))
    a.rollback()
    print("after rollback, a sees:", count(a))
