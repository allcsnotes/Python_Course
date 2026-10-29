import pytest

from pricing import final_price


@pytest.mark.parametrize(
    "price, percent, expected",
    [
        pytest.param(1000, 10, 900, id="ten percent"),
        pytest.param(1000, 0, 1000, id="no discount"),
        pytest.param(1000, 100, 0, id="free"),
        pytest.param(999, 15, 850, id="rounds down"),
    ],
)
def test_final_price(price, percent, expected):
    assert final_price(price, percent) == expected


@pytest.mark.parametrize("percent", [-1, 101, 250])
def test_bad_percent(percent):
    with pytest.raises(ValueError):
        final_price(1000, percent)
