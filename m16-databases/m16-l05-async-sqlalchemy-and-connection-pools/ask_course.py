import httpx

for course_id in (2, 99):
    url = f"http://localhost:8165/courses/{course_id}"
    reply = httpx.get(url)
    print(reply.status_code, reply.json())
