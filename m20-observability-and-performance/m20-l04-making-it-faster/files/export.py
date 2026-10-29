import time

import httpx

BASE = "http://localhost:8204"
client = httpx.Client(base_url=BASE, timeout=60)
reply = client.post(
    "/auth/login",
    data={"username": "meera@example.com", "password": "meera-demo-pass"},
)
headers = {"Authorization": f"Bearer {reply.json()['access_token']}"}

for name, path in (("inline", "/me/export/inline"), ("as a job", "/me/export")):
    start = time.perf_counter()
    reply = client.post(path, headers=headers)
    print(f"{name:<9} {reply.status_code}  {time.perf_counter() - start:.2f} s  {reply.json()}")
