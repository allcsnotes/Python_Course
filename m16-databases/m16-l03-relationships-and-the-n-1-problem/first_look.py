from sqlalchemy.orm import Session

from db import engine
from models import Course

with Session(engine) as session:
    course = session.get(Course, 1)
    print(course.title)
    for lesson in course.lessons:
        print(" ", lesson.title)
    print(course.lessons[0].course.title)
