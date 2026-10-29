from unittest.mock import Mock

import store


def test_everything_mocked(monkeypatch):
    monkeypatch.setattr(
        store,
        "price_with_gst",
        lambda course_id: 590,
    )
    result = store.buy("Priya", "c101", Mock())
    assert result == "Priya bought c101 for Rs 590"
