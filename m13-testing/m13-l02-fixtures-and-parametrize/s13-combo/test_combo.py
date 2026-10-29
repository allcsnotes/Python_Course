import pytest

from course import Course


@pytest.mark.parametrize("seats", [1, 2, 3])
@pytest.mark.parametrize("name", ["Lukas", "Priya"])
def test_first_student_fits(name, seats):
    course = Course("Python Basics", seats)
    course.enroll(name)
    assert course.seats_left() == seats - 1
