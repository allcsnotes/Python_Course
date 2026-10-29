from unittest.mock import Mock

import pytest

import store


def test_bank_down(monkeypatch):
    monkeypatch.setattr(
        store,
        "fetch_price",
        lambda course_id: 500,
    )
    gateway = Mock()
    error = ConnectionError("bank is down")
    gateway.charge.side_effect = error
    with pytest.raises(ConnectionError):
        store.buy("Priya", "c101", gateway)
