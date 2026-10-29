import store


def test_price_with_gst():
    assert store.price_with_gst("c101") == 590
