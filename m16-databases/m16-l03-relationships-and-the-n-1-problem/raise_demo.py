from sqlalchemy import select
from sqlalchemy.orm import Session, raiseload

from db import engine
from models import Course

with Session(engine) as session:
    stmt = (
        select(Course)
        .options(raiseload(Course.lessons))
    )
    course = session.scalars(stmt).first()
    print(course.title)
    print(len(course.lessons))
