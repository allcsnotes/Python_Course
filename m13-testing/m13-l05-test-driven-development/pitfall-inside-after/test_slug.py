import slug
from slug import slugify


def test_fix_helper():
    assert slug._fix("C++ Go") == "c   go"


def test_slug():
    assert slugify("C++ Go") == "c-go"
