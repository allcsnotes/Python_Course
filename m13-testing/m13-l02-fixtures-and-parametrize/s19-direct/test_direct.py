import pytest

from course import Course


@pytest.fixture
def course():
    return Course("Python Basics", 2)


def test_seats():
    c = course()
    assert c.seats_left() == 2
