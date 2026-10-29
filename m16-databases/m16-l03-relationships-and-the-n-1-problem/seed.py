import sys
from datetime import date

from sqlalchemy.orm import Session

from db import engine
from models import Base, Course, Enrollment, Lesson, Student

TITLES = ["Python Basics", "SQL in Two Weeks", "Git and GitHub", "Linux Essentials", "Async Python",
          "Python Performance", "Docker Basics", "Web APIs", "Testing with pytest", "Kotlin Basics"]
PRICES = [449, 399, 299, 349, 499, 549, 399, 449, 349, 299]
LESSONS = ["Welcome", "The idea", "Try it", "Mistakes", "Recap"]


ENROL = [(1, 1, 1), (1, 2, 2), (2, 2, 2), (2, 3, 3), (2, 5, 4), (3, 2, 5)]


def seed(n_courses=10, n_students=3):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(n_courses):
            title = TITLES[i] if i < len(TITLES) else f"Course {i + 1}"
            course = Course(title=title, price=PRICES[i % 10], level="beginner")
            course.lessons = [Lesson(title=f"{k + 1}. {name}") for k, name in enumerate(LESSONS[: 3 + i % 3])]
            session.add(course)
        students = [Student(name=n) for n in ["Lukas", "Priya", "Ben"][:n_students]]
        session.add_all(students)
        session.flush()
        for s_id, c_id, day in ENROL:
            session.add(Enrollment(student_id=s_id, course_id=c_id, enrolled_on=date(2026, 9, day)))
        session.commit()


if __name__ == "__main__":
    seed(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
