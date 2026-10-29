import time

import httpx

URL = "http://localhost:8284/rate"


def ask(limit):
    start = time.perf_counter()
    try:
        r = httpx.get(URL, timeout=limit)
        result = f"rate {r.json()['inr_per_eur']}"
    except httpx.TimeoutException:
        result = "gave up"
    took = time.perf_counter() - start
    print(f"timeout {limit}: {result} after {took:.1f} s")


ask(None)
ask(1.0)
