import httpx

URL = "http://localhost:8156/enrolments"
body = {"email": "lukas@example.com", "course_id": 7}

reply = httpx.post(URL, json=body)
print(reply.status_code, reply.json())
