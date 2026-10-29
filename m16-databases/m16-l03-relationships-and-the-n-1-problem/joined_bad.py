from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from db import engine
from models import Course

with Session(engine) as session:
    stmt = (
        select(Course)
        .options(joinedload(Course.lessons))
    )
    courses = session.scalars(stmt).all()
    print(len(courses))
