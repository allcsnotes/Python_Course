import pytest

from pricing import final_price


@pytest.mark.parametrize(
    "price, percent, expected",
    [
        (1000, 10, 900),
        (1000, 0, 1000),
        (1000, 100, 0),
        (999, 15, 850),
    ],
)
def test_final_price(price, percent, expected):
    assert final_price(price, percent) == expected
