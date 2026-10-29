from pricing import final_price


def test_ten_percent():
    assert final_price(1000, 10) == 900


def test_no_discount():
    assert final_price(1000, 0) == 1000


def test_free():
    assert final_price(1000, 100) == 0


def test_rounding():
    assert final_price(999, 15) == 850
