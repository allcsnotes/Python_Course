from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import Course

with Session(engine) as session:
    print(session.get(Course, 2))
    print(session.get(Course, 99))

    stmt = select(Course).where(Course.level == "advanced")
    rows = session.execute(stmt).all()
    print(rows)

    courses = session.scalars(stmt).all()
    print(courses)
