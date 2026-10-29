import sys
from datetime import date

from sqlalchemy.orm import Session

from sqlalchemy import create_engine

from db import URL
from models import Base, Course, Enrollment, Lesson, Student

TITLES = ["Python Basics", "Functions", "Data Structures", "Databases", "Web APIs",
          "Testing", "Docker", "Security", "Caching", "Deployment"]
LESSONS = ["Welcome", "The idea", "Try it", "Mistakes", "Recap"]


def seed(n_courses=10, n_students=6):
    engine = create_engine(URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(n_courses):
            title = TITLES[i] if i < len(TITLES) else f"Course {i + 1}"
            course = Course(title=title, price=499 + 100 * (i % 5))
            course.lessons = [Lesson(title=f"{k + 1}. {name}") for k, name in enumerate(LESSONS[: 3 + i % 3])]
            session.add(course)
        students = [Student(name=n) for n in ["Lukas", "Priya", "Asha", "Meera", "Ravi", "Anna"][:n_students]]
        session.add_all(students)
        session.flush()
        for s_i, student in enumerate(students):
            for c_i in range(s_i % 3 + 1):
                session.add(Enrollment(student_id=student.id, course_id=c_i + 1, enrolled_on=date(2026, 9, 1 + s_i)))
        session.commit()


if __name__ == "__main__":
    seed(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
