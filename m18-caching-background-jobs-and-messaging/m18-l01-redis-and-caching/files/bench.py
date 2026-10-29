import time

import httpx
from client import BASE, LIST

httpx.get(f"{BASE}/courses?limit=1")
httpx.post(f"{BASE}/stats/reset")


def timed(label):
    start = time.perf_counter()
    httpx.get(LIST)
    ms = (time.perf_counter() - start) * 1000
    print(f"{label:<8}{ms:6.1f} ms")


for label in ("first", "second", "third"):
    timed(label)
print(httpx.get(f"{BASE}/stats").json())
