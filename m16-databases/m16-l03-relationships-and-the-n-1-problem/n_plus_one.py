from sqlalchemy import select
from sqlalchemy.orm import Session

from counting import QueryCounter
from db import engine, show_sql
from models import Course

show_sql()
counter = QueryCounter(engine)
with Session(engine) as session:
    courses = session.scalars(select(Course).limit(2))
    for course in courses:
        print(course.title, len(course.lessons))
print("queries:", counter.count)
