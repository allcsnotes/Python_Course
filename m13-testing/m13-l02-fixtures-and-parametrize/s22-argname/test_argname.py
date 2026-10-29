import pytest


@pytest.mark.parametrize(
    "price, percent", [(1000, 10)]
)
def test_x(price):
    assert price == 1000
