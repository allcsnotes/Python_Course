import pytest

from pricing import final_price


def test_flat_100():
    final_price(500, "FLAT100")


def test_unknown_coupon():
    with pytest.raises(ValueError):
        final_price(500, "FREE")
