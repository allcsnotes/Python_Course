import pytest

from pricing import final_price


def test_flat_100():
    assert final_price(500, "FLAT100") == 400


def test_unknown_coupon():
    with pytest.raises(ValueError):
        final_price(500, "FREE")
