from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Lesson
from app.seed import TOPICS, seed_lessons, seed_users


def test_seed_is_repeatable_and_fully_indexed():
    for _ in range(2):
        with Session(engine) as session:
            seed_lessons(session)
            seed_users(session)
            session.commit()
    with Session(engine) as session:
        total = session.scalar(
            select(func.count(Lesson.id))
        )
        indexed = session.scalar(
            select(func.count(Lesson.id)).where(
                Lesson.search_vector.is_not(None)
            )
        )
    assert (
        total == indexed == len(TOPICS.strip().splitlines())
    )
