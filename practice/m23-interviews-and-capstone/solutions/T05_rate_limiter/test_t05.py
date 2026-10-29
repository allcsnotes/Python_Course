import pytest

from limiter import RateLimiter


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_allows_up_to_limit_then_blocks():
    rl = RateLimiter(3, 60, FakeClock())
    assert [rl.allow("asha") for _ in range(5)] == [True, True, True, False, False]


def test_keys_are_independent():
    rl = RateLimiter(1, 60, FakeClock())
    assert rl.allow("asha") and rl.allow("lukas")
    assert not rl.allow("asha")


def test_window_slides():
    clock = FakeClock()
    rl = RateLimiter(2, 10, clock)
    assert rl.allow("k")            # t=0
    clock.now = 6
    assert rl.allow("k")            # t=6
    clock.now = 9
    assert not rl.allow("k")        # both still inside the window
    clock.now = 10.5                # the call at t=0 has slid out
    assert rl.allow("k")
    assert not rl.allow("k")


def test_retry_after():
    clock = FakeClock()
    rl = RateLimiter(1, 10, clock)
    assert rl.retry_after("k") == 0
    rl.allow("k")
    clock.now = 4
    assert rl.retry_after("k") == 6
    clock.now = 10
    assert rl.retry_after("k") == 0 and rl.allow("k")


def test_rejects_bad_settings():
    with pytest.raises(ValueError):
        RateLimiter(0, 10)
    with pytest.raises(ValueError):
        RateLimiter(1, 0)
