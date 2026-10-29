import time

import httpx

from breaker import Breaker, CircuitOpen

breaker = Breaker(limit=3, pause=2.0)


def get_rate():
    r = httpx.get("http://localhost:8284/rate", timeout=1.0)
    r.raise_for_status()
    return r.json()["inr_per_eur"]


start = time.perf_counter()
for n in range(1, 11):
    before = breaker.state()
    try:
        result = f"rate {breaker.call(get_rate)}"
    except CircuitOpen:
        result = "skipped"
    except httpx.HTTPError:
        result = "failed"
    now = time.perf_counter() - start
    print(f"{now:4.1f} s  {before:9}  {result}")
    time.sleep(0.5)
