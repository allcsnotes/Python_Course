import shop


def test_label(monkeypatch):
    monkeypatch.setattr(
        "store.fetch_price",
        lambda course_id: 123,
    )
    assert shop.label("c101") == "Rs 123"
