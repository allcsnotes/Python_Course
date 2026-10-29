from sqlalchemy.orm import Session

from db import engine
from models import Course

with Session(engine) as session:
    course = Course(
        title="Go Basics",
        price=499,
        level="beginner",
    )
    session.add(course)
    session.commit()

print(course.title)
