import pytest

from course import Course, CourseFullError


@pytest.fixture
def course():
    return Course("Python Basics", 2)


@pytest.fixture
def full_course(course):
    course.enroll("Lukas")
    course.enroll("Priya")
    return course


def test_no_seats_left(full_course):
    assert full_course.seats_left() == 0


def test_full_course_rejects(full_course):
    with pytest.raises(CourseFullError):
        full_course.enroll("Meera")
