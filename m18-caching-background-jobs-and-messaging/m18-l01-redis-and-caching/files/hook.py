import httpx
from client import BASE, LIST

httpx.post(f"{BASE}/stats/reset")
for _ in range(5):
    httpx.get(LIST)
print(httpx.get(f"{BASE}/stats").json())
