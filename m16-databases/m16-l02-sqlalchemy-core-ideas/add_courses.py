from sqlalchemy.orm import Session

from db import engine, show_sql
from models import Course

show_sql()
with Session(engine) as session:
    course = Course(
        title="Python Basics",
        price=449,
        level="beginner",
    )
    print("id before:", course.id)
    session.add(course)
    print("waiting:", session.new)
    session.commit()
    print("id after:", course.id)
