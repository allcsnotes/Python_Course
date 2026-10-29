from slug import slugify


def test_lowercase():
    assert slugify("Python") == "python"
