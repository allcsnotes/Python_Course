import time

import pytest


@pytest.fixture(scope="module")
def catalog():
    print("  loading the catalog (slow)")
    time.sleep(0.5)
    return ["Python Basics", "Git", "SQL"]


def test_has_python(catalog):
    assert "Python Basics" in catalog


def test_has_git(catalog):
    assert "Git" in catalog


def test_size(catalog):
    assert len(catalog) == 3
