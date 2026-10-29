import pytest

from course import Course, CourseFullError


def test_enroll_adds_student():
    course = Course("Python Basics", 2)
    course.enroll("Lukas")
    assert course.students == ["Lukas"]


def test_seats_left():
    course = Course("Python Basics", 2)
    course.enroll("Lukas")
    assert course.seats_left() == 1


def test_full_course():
    course = Course("Python Basics", 3)
    course.enroll("Lukas")
    course.enroll("Priya")
    with pytest.raises(CourseFullError):
        course.enroll("Meera")
