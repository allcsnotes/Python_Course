import pytest

from course import Course


@pytest.fixture
def course():
    print("making a course")
    return Course("Python Basics", 2)


def test_first(course):
    course.enroll("Lukas")
    print(course.students)


def test_second(course):
    print(course.students)
