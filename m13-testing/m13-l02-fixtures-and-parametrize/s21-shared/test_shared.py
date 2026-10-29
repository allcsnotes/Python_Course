import pytest

from course import Course


@pytest.fixture(scope="module")
def course():
    return Course("Python Basics", 2)


def test_enroll(course):
    course.enroll("Lukas")
    assert course.seats_left() == 1


def test_empty_at_start(course):
    assert course.seats_left() == 2
