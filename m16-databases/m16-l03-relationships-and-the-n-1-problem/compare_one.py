from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from counting import QueryCounter
from db import engine
from models import Lesson

counter = QueryCounter(engine)


def course_titles(stmt):
    counter.count = 0
    with Session(engine) as session:
        for lesson in session.scalars(stmt):
            lesson.course.title
    return counter.count


print("lazy:", course_titles(select(Lesson)))
stmt = select(Lesson).options(joinedload(Lesson.course))
print("joinedload:", course_titles(stmt))
