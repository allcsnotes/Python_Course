from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import Base, Course

Base.metadata.create_all(engine)

with Session(engine) as s:
    for course in s.scalars(select(Course)):
        print(course.title, course.seats)
