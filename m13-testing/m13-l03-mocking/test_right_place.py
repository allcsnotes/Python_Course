import shop


def test_label(monkeypatch):
    monkeypatch.setattr(
        "shop.fetch_price",
        lambda course_id: 123,
    )
    assert shop.label("c101") == "Rs 123"
