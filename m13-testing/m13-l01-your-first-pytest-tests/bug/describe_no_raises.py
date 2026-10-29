from linkrules import describe


def test_describe_404():
    assert describe(404) == "broken"


def test_describe_200():
    assert describe(200) == "fine"


def test_describe_999():
    describe(999)
