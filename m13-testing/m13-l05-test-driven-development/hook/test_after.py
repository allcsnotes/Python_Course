from slug import slugify


def test_slug_of_a_c_course():
    assert slugify("C++ Basics!") == "c---basics-"
