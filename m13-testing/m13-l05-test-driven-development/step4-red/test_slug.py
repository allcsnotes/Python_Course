from slug import slugify


def test_lowercase():
    assert slugify("Python") == "python"


def test_spaces_become_dashes():
    assert slugify("Learn Go") == "learn-go"


def test_punctuation_is_dropped():
    assert slugify("C++ Basics!") == "c-basics"


def test_extra_spaces_collapse():
    assert slugify(" Learn  Go ") == "learn-go"
