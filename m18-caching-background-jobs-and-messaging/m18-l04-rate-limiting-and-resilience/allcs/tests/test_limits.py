import time

import pytest

from app import ratelimit
from app.cache import r


def test_the_sixth_wrong_password_is_429(make_user, login):
    lukas = make_user("Lukas")
    for _ in range(5):
        assert login(lukas, "wrong-password").status_code == 401
    r6 = login(lukas, "wrong-password")
    assert r6.status_code == 429
    assert 1 <= int(r6.headers["Retry-After"]) <= 60


def test_the_right_password_is_refused_while_locked(make_user, login):
    lukas = make_user("Lukas")
    for _ in range(5):
        login(lukas, "wrong-password")
    assert login(lukas).status_code == 429


def test_a_good_login_resets_the_count(make_user, login):
    lukas = make_user("Lukas")
    for _ in range(4):
        login(lukas, "wrong-password")
    assert login(lukas).status_code == 200
    for _ in range(5):
        assert login(lukas, "wrong-password").status_code == 401


def test_another_student_is_not_blocked(make_user, login):
    lukas, priya = make_user("Lukas"), make_user("Priya")
    for _ in range(6):
        login(lukas, "wrong-password")
    assert login(priya).status_code == 200


def test_the_window_ends(make_user, login, monkeypatch):
    monkeypatch.setattr(ratelimit, "WINDOW", 1)
    lukas = make_user("Lukas")
    for _ in range(5):
        login(lukas, "wrong-password")
    assert login(lukas).status_code == 429
    time.sleep(1.2)
    assert login(lukas).status_code == 200


def test_the_counter_expires_by_itself(make_user, login):
    lukas = make_user("Lukas")
    login(lukas, "wrong-password")
    key = ratelimit.login_key("testclient", lukas.email)
    assert 0 < r.ttl(key) <= ratelimit.WINDOW


def test_if_redis_is_down_login_still_works(
    make_user, login, monkeypatch
):
    class Broken:
        def __getattr__(self, name):
            def fail(*args, **kwargs):
                raise ratelimit.redis.ConnectionError("down")

            return fail

    monkeypatch.setattr(ratelimit, "r", Broken())
    assert login(make_user("Lukas")).status_code == 200
