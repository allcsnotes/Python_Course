from unittest.mock import patch

import store


@patch("store.httpx.get")
def test_price_over_fake_network(mock_get):
    reply = mock_get.return_value
    reply.json.return_value = {"price": 500}
    assert store.price_with_gst("c101") == 590
    url = mock_get.call_args.args[0]
    assert url.endswith("/courses/c101")
