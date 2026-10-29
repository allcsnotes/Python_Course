import httpx

URL = "http://localhost:8184/auth/login"
EMAIL = "lukas@example.com"

for n in range(1, 9):
    form = {"username": EMAIL, "password": f"guess-{n}"}
    r = httpx.post(URL, data=form)
    wait = r.headers.get("retry-after", "-")
    print(f"try {n}: {r.status_code}  retry-after: {wait}")

form = {"username": EMAIL, "password": "lukas-demo-pass"}
r = httpx.post(URL, data=form)
print("the right password:", r.status_code)
