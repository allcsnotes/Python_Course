import pytest

from course import Course


@pytest.fixture
def course():
    print("  setup: the course opens")
    course = Course("Python Basics", 2)
    yield course
    print("  teardown: the course closes")


def test_enroll(course):
    print("  test: enrolling")
    course.enroll("Lukas")
    assert course.seats_left() == 1


def test_broken(course):
    print("  test: broken")
    assert course.seats_left() == 5
