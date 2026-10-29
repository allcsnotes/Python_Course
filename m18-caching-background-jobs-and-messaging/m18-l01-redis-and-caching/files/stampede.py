from concurrent.futures import ThreadPoolExecutor

import httpx
import redis
from client import BASE, LIST

r = redis.Redis(port=18401)
httpx.get(LIST)
httpx.post(f"{BASE}/stats/reset")
r.delete("courses:list:all:50:0")

with ThreadPoolExecutor(20) as pool:
    for _ in range(20):
        pool.submit(httpx.get, LIST)
print(httpx.get(f"{BASE}/stats").json())
