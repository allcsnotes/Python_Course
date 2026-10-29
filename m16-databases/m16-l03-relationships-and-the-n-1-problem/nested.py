from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from counting import QueryCounter
from db import engine
from models import Enrollment, Student

counter = QueryCounter(engine)


def course_lists(stmt):
    counter.count = 0
    with Session(engine) as session:
        for student in session.scalars(stmt):
            [e.course.title for e in student.enrollments]
    return counter.count


chain = selectinload(Student.enrollments).selectinload(
    Enrollment.course
)
print("lazy:", course_lists(select(Student)))
stmt = select(Student).options(chain)
print("selectinload chain:", course_lists(stmt))
