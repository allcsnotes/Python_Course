from sqlalchemy.orm import Session

from db import engine
from models import Course

with Session(engine) as session:
    course = session.get(Course, 1)

print(course.title)
print(course.lessons)
