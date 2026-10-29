from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from counting import QueryCounter
from db import engine, show_sql
from models import Course

show_sql()
counter = QueryCounter(engine)
with Session(engine) as session:
    stmt = (
        select(Course)
        .options(joinedload(Course.lessons))
        .where(Course.id <= 2)
    )
    for course in session.scalars(stmt).unique():
        print(course.title, len(course.lessons))
print("queries:", counter.count)
