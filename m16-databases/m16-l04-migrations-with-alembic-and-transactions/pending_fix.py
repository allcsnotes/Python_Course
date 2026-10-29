from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import engine
from models import Enrollment

count = select(func.count()).select_from(Enrollment)

with Session(engine) as s, s.begin():
    s.add(Enrollment(student_id=1, course_id=1))

with Session(engine) as s:
    s.add(Enrollment(student_id=1, course_id=1))
    try:
        s.commit()
    except IntegrityError:
        s.rollback()
        print("already enrolled")
    print(s.scalar(count))
