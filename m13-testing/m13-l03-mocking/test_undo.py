import store


def test_with_stand_in(monkeypatch):
    monkeypatch.setattr(
        store,
        "fetch_price",
        lambda course_id: 500,
    )
    assert store.price_with_gst("c101") == 590


def test_without_it():
    assert store.price_with_gst("c101") == 590
