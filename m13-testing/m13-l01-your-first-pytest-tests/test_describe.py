import pytest
from linkrules import describe


def test_describe_404():
    assert describe(404) == "broken"


def test_describe_200():
    assert describe(200) == "fine"


def test_describe_999_names_the_status():
    with pytest.raises(ValueError, match="999"):
        describe(999)
