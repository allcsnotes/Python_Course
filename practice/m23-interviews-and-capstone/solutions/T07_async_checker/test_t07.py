import asyncio

import pytest

from checker import Result, check_all


def run(coro):
    return asyncio.run(coro)


def test_results_keep_the_input_order():
    async def fetch(url):
        await asyncio.sleep({"slow": 0.05, "fast": 0.0}[url])
        return 200

    results = run(check_all(["slow", "fast"], fetch))
    assert [r.url for r in results] == ["slow", "fast"]
    assert all(r.ok for r in results)


def test_status_handling():
    codes = {"ok": 200, "gone": 404}

    async def fetch(url):
        return codes[url]

    results = run(check_all(["ok", "gone"], fetch, retries=3))
    assert results == [Result("ok", True, 200, 1), Result("gone", False, 404, 1)]   # 404: no retries


def test_concurrency_is_limited():
    running = peak = 0

    async def fetch(url):
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.01)
        running -= 1
        return 200

    run(check_all([f"u{i}" for i in range(12)], fetch, concurrency=3))
    assert peak == 3


def test_retry_then_success():
    calls = []

    async def fetch(url):
        calls.append(url)
        return 503 if len(calls) < 3 else 200

    (result,) = run(check_all(["u"], fetch, retries=2))
    assert result.ok and result.attempts == 3


def test_gives_up_after_retries():
    async def fetch(url):
        return 500

    (result,) = run(check_all(["u"], fetch, retries=1))
    assert not result.ok and result.attempts == 2 and result.error == "server error 500"


def test_timeout_and_connection_errors():
    async def fetch(url):
        if url == "hang":
            await asyncio.sleep(5)
        raise ConnectionRefusedError

    results = run(check_all(["hang", "down"], fetch, timeout=0.05, retries=0))
    assert [r.error for r in results] == ["timeout", "ConnectionRefusedError"]


def test_concurrency_must_be_positive():
    with pytest.raises(ValueError):
        run(check_all([], None, concurrency=0))
