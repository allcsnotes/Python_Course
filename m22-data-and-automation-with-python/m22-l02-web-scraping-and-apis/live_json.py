import time

import httpx

url = "http://localhost:22280/live-sessions.json"
start = time.perf_counter()
sessions = httpx.get(url).json()
for s in sessions:
    print(s["title"], "-", s["when"])
print(f"{time.perf_counter() - start:.2f} s")
