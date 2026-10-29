from unittest.mock import patch

import httpx

import store


@patch("store.httpx.get")
def test_service_down(mock_get):
    error = httpx.ConnectError("service is down")
    mock_get.side_effect = error
    assert store.safe_price("c101") is None
