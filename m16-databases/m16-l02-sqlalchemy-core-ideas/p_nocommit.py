from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import Course

with Session(engine) as session:
    course = Course(
        title="Kotlin Basics",
        price=649,
        level="advanced",
    )
    session.add(course)
    print("added:", session.new)

with Session(engine) as session:
    stmt = select(Course).where(
        Course.title == "Kotlin Basics"
    )
    print(session.scalars(stmt).all())
