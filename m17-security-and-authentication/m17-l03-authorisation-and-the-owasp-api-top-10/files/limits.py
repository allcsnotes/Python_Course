import httpx
from client import BASE

r = httpx.get(f"{BASE}/courses?limit=1000")
error = r.json()["error"]
print(r.status_code, error["fields"][0]["problem"])
