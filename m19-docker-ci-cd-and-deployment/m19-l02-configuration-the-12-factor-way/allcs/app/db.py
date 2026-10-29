from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session

from app.domain import Conflict, NotFound
from app.settings import get_settings

URL = str(get_settings().database_url)
engine = create_engine(URL)

CONFLICTS = {
    "courses_title_key": ("duplicate_title", "Title already used"),
    "students_email_key": ("duplicate_email", "Email already used"),
    "enrollments_pkey": (
        "already_enrolled",
        "Already enrolled in this course",
    ),
    "enrollments_course_id_fkey": (
        "course_has_students",
        "Course still has students",
    ),
}


class Base(DeclarativeBase):
    pass


def get_session():
    with Session(engine) as session:
        yield session


def get_or_404(session, model, item_id):
    item = session.get(model, item_id)
    if item is None:
        raise NotFound(model.__name__, item_id)
    return item


def save(session):
    try:
        session.commit()
    except IntegrityError as err:
        session.rollback()
        rule = err.orig.diag.constraint_name
        code, message = CONFLICTS[rule]
        raise Conflict(code, message) from err
