from invoice import cart_total


def test_coupon_comes_off_the_whole_cart():
    assert cart_total([1500, 500, 500], 10) == 2250
