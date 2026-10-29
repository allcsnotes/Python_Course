import httpx

for n in range(1, 7):
    r = httpx.get("http://localhost:22280/courses?page=1")
    print(n, r.status_code, r.headers.get("retry-after"))
