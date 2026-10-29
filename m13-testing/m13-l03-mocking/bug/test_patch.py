import store


def test_gst_added(monkeypatch):
    monkeypatch.setattr(
        store,
        "fetch_price",
        lambda course_id: 500,
    )
    assert store.price_with_gst("c101") == 590
