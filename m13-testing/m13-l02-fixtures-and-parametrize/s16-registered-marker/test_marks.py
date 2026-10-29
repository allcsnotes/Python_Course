import sys

import pytest

from pricing import final_price


def test_ten_percent():
    assert final_price(1000, 10) == 900


@pytest.mark.skip(reason="coupons are not built yet")
def test_coupon():
    assert final_price(1000, 10) == 900


@pytest.mark.skipif(
    sys.platform != "linux", reason="Linux only"
)
def test_linux_path():
    assert sys.platform == "linux"


@pytest.mark.xfail(reason="known bug: wrong rounding")
def test_rounding_bug():
    assert final_price(999, 15) == 849
