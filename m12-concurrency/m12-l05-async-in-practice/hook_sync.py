import time

import httpx

URL = "http://localhost:8125/page/{}"

start = time.perf_counter()
with httpx.Client() as client:
    for n in range(1, 21):
        client.get(URL.format(n))
seconds = time.perf_counter() - start
print(f"20 pages, one by one: {seconds:.1f} seconds")
