import time

import toolkit


def test_cache_expires_slow():
    calls = []

    @toolkit.cache_for(1)
    def price(code):
        calls.append(code)
        return 500

    price("c101")
    price("c101")
    assert len(calls) == 1
    time.sleep(1.1)
    price("c101")
    assert len(calls) == 2
