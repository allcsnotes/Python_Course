import time

import httpx

URL = "http://localhost:8156"
body = {"email": "lukas@example.com", "course_id": 7}

for path in ["/enrolments/slow", "/enrolments"]:
    start = time.perf_counter()
    reply = httpx.post(URL + path, json=body)
    took = time.perf_counter() - start
    print(f"{path}: {reply.status_code} in {took:.1f} seconds")
