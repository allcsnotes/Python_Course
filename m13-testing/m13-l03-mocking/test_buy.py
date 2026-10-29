from unittest.mock import Mock

import store


def test_buy_charges_once(monkeypatch):
    monkeypatch.setattr(
        store,
        "fetch_price",
        lambda course_id: 500,
    )
    gateway = Mock()
    result = store.buy("Priya", "c101", gateway)
    assert result == "Priya bought c101 for Rs 590"
    gateway.charge.assert_called_once_with("Priya", 590)
