from pricing import bundle_total, final_price


def test_no_coupon():
    assert final_price(500, "") == 500


def test_half_price():
    assert final_price(500, "HALF") == 250


def test_bundle_of_three():
    assert bundle_total(100, 3) == 270


def test_bundle_of_one():
    assert bundle_total(100, 1) == 100
