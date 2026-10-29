import pytest
from linkrules import describe


def test_describe_404_raises():
    with pytest.raises(ValueError):
        describe(404)
