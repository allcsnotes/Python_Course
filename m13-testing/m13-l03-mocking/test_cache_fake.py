import toolkit


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def monotonic(self):
        return self.now


def test_cache_expires(monkeypatch):
    clock = FakeClock()
    monkeypatch.setattr(toolkit, "time", clock)
    calls = []

    @toolkit.cache_for(60)
    def price(code):
        calls.append(code)
        return 500

    price("c101")
    price("c101")
    assert len(calls) == 1
    clock.now += 61
    price("c101")
    assert len(calls) == 2
