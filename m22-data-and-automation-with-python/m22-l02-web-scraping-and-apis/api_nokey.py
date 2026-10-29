import httpx

r = httpx.get("http://localhost:22281/api/courses")
print(r.status_code, r.json())
