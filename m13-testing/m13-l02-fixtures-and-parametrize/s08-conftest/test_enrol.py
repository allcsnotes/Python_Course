import pytest

from course import CourseFullError


def test_enroll_adds_student(course):
    course.enroll("Lukas")
    assert course.students == ["Lukas"]


def test_full_course(course):
    course.enroll("Lukas")
    course.enroll("Priya")
    with pytest.raises(CourseFullError):
        course.enroll("Meera")
