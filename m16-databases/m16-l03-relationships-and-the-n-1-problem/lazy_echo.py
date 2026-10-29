from sqlalchemy.orm import Session

from db import engine, show_sql
from models import Course

show_sql()
with Session(engine) as session:
    course = session.get(Course, 1)
    print("-- got the course")
    lessons = course.lessons
    print("-- asked for the lessons")
    print(len(lessons))
