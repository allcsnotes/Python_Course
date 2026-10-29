from slug import slugify


def test_slug():
    slugify("Intro to Python") == "intro-to-python"
