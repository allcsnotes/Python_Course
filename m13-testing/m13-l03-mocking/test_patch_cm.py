from unittest.mock import patch

import store


def test_with_block():
    with patch("store.fetch_price") as fake_price:
        fake_price.return_value = 500
        assert store.price_with_gst("c101") == 590
    fake_price.assert_called_once_with("c101")
