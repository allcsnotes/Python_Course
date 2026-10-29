import httpx

BASE = "http://localhost:8184"

for path in ("/courses?limit=3", "/courses/1"):
    r = httpx.get(BASE + path)
    where = r.headers.get("x-served-from", "-")
    print(f"{path:17} {r.status_code}  {where}")
