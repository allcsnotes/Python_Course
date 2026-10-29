import pytest
from sqlalchemy.orm import Session

from counting import QueryCounter
from db import engine
from service import course_lines, course_lines_slow


@pytest.fixture
def counted():
    with Session(engine) as session:
        yield session, QueryCounter(engine)


def test_list_is_two_queries(counted):
    session, counter = counted
    assert len(course_lines(session)) == 10
    assert counter.count <= 2


def test_slow_list_is_two_queries(counted):
    session, counter = counted
    assert len(course_lines_slow(session)) == 10
    assert counter.count <= 2
