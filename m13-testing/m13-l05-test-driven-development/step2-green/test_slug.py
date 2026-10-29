from slug import slugify


def test_lowercase():
    assert slugify("Python") == "python"


def test_spaces_become_dashes():
    assert slugify("Learn Go") == "learn-go"
