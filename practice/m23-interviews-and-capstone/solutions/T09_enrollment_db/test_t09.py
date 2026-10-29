"""Needs Postgres:  docker run -d --name m23p04-pg -e POSTGRES_USER=practice \
-e POSTGRES_PASSWORD=practice -e POSTGRES_DB=practice -p 23604:5432 postgres:17"""
import threading

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from enrollments import (AlreadyEnrolled, Base, Course, CourseFull, Enrollment, Student,
                        enroll, titles_for)

URL = "postgresql+psycopg://practice:practice@localhost:23604/practice"


@pytest.fixture
def engine():
    engine = create_engine(URL, pool_size=15)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session, session.begin():
        session.add_all([Student(id=i, name=f"S{i}") for i in range(1, 21)])
        session.add_all([Course(id=1, title="Python", seats=3),
                         Course(id=2, title="SQL", seats=10),
                         Course(id=3, title="Rust", seats=10)])
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_enroll_and_duplicate(engine):
    assert enroll(engine, 1, 2) > 0
    with pytest.raises(AlreadyEnrolled):
        enroll(engine, 1, 2)
    assert enroll(engine, 2, 2) > 0                     # the failed attempt left no mess behind


def test_unknown_course(engine):
    with pytest.raises(NoResultFound):
        enroll(engine, 1, 99)


def test_course_full(engine):
    for student in (1, 2, 3):
        enroll(engine, student, 1)
    with pytest.raises(CourseFull):
        enroll(engine, 4, 1)


def test_ten_people_race_for_three_seats(engine):
    outcomes = []
    gate = threading.Barrier(10)

    def attempt(student_id):
        gate.wait()                                    # everybody starts together
        try:
            enroll(engine, student_id, 1)
            outcomes.append("ok")
        except CourseFull:
            outcomes.append("full")

    threads = [threading.Thread(target=attempt, args=(i,)) for i in range(1, 11)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(outcomes) == ["full"] * 7 + ["ok"] * 3
    with Session(engine) as session:
        assert session.query(Enrollment).filter_by(course_id=1).count() == 3


def test_titles_use_two_queries(engine):
    for course in (1, 2, 3):
        enroll(engine, 1, course)
    statements = []
    event.listen(engine, "before_cursor_execute", lambda c, cur, stmt, *a: statements.append(stmt))
    assert titles_for(engine, 1) == ["Python", "Rust", "SQL"]
    assert len(statements) == 3          # student, enrollments, courses: constant, not 1 + N
