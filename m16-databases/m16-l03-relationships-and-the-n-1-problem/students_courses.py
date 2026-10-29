from sqlalchemy.orm import Session

from db import engine
from models import Course, Student

with Session(engine) as session:
    lukas = session.get(Student, 1)
    for e in lukas.enrollments:
        print(lukas.name, "->", e.course.title, e.enrolled_on)
    sql = session.get(Course, 2)
    print([e.student.name for e in sql.enrollments])
