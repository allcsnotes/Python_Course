from sqlalchemy.orm import Session

from db import engine, show_sql
from models import Course

show_sql()
with Session(engine) as session:
    course = session.get(Course, 1)
    course.price = 399
    print("changed:", session.dirty)
    session.commit()

    session.delete(course)
    session.commit()
