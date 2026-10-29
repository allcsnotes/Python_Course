from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Course


def describe(course: Course) -> str:
    return f"{course.title}: {len(course.lessons)} lessons"


def course_lines_slow(session: Session) -> list[str]:
    courses = session.scalars(select(Course))
    return [describe(c) for c in courses]


def course_lines(session: Session) -> list[str]:
    stmt = select(Course).options(selectinload(Course.lessons))
    return [describe(c) for c in session.scalars(stmt)]
