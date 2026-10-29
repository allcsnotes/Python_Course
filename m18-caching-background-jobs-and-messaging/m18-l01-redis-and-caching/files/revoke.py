import httpx
import redis
from client import BASE, login

r = redis.Redis(port=18401, decode_responses=True)
headers = login("lukas@example.com", "lukas-demo-pass")


def me():
    return httpx.get(f"{BASE}/me", headers=headers).status_code


print("me before:", me())
httpx.post(f"{BASE}/auth/revoke", headers=headers)
print("me after: ", me())
key = r.keys("blocked:*")[0]
print(key[:16] + "...", "expires in", r.ttl(key), "seconds")
