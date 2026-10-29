from sqlalchemy.orm import Session

from db import engine
from models import Course, Lesson

with Session(engine) as session:
    course = session.get(Course, 1)
    bonus = Lesson(title="6. Bonus")
    course.lessons.append(bonus)
    print(bonus.course.title, bonus.course_id)
    session.commit()
    print(bonus.course_id)
