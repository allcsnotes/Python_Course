import time

import httpx

BASE = "http://localhost:8182"


def login(email):
    form = {"username": email, "password": "demo-password-1"}
    token = httpx.post(f"{BASE}/auth/login", data=form).json()
    return {"Authorization": "Bearer " + token["access_token"]}


lukas = login("lukas@example.com")
start = time.perf_counter()
reply = httpx.post(f"{BASE}/courses/1/enrollments", headers=lukas)
took = round(time.perf_counter() - start, 2)
print("enrol:", reply.status_code, "in", took, "seconds")

asha = login("asha@example.com")
job = httpx.post(f"{BASE}/reports/enrollments", headers=asha)
print("report:", job.status_code)
url = BASE + job.json()["status_url"]
print("poll:", job.json()["status_url"])
for _ in range(8):
    body = httpx.get(url, headers=asha).json()
    print("status:", body["status"], body.get("result", ""))
    if body["status"] == "SUCCESS":
        break
    time.sleep(1)
