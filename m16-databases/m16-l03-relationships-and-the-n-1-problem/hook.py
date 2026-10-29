from sqlalchemy import select
from sqlalchemy.orm import Session

from counting import QueryCounter
from db import engine
from models import Course

counter = QueryCounter(engine)
with Session(engine) as session:
    for course in session.scalars(select(Course)):
        print(course.title, len(course.lessons))
print("queries:", counter.count)
