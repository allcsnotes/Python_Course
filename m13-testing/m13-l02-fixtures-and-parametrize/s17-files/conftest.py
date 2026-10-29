import pytest

from course import Course


@pytest.fixture
def course():
    return Course("Python Basics", 2)
