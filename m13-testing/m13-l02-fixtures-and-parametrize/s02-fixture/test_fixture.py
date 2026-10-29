import pytest

from course import Course, CourseFullError


@pytest.fixture
def course():
    return Course("Python Basics", 2)


def test_enroll_adds_student(course):
    course.enroll("Lukas")
    assert course.students == ["Lukas"]


def test_seats_left(course):
    course.enroll("Lukas")
    assert course.seats_left() == 1


def test_full_course(course):
    course.enroll("Lukas")
    course.enroll("Priya")
    with pytest.raises(CourseFullError):
        course.enroll("Meera")
