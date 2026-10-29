import httpx

URL = "http://localhost:8156/courses/7/thumbnail"

for name in ["thumb.png", "notes.txt"]:
    with open(name, "rb") as file:
        reply = httpx.post(URL, files={"file": file})
    print(name, reply.status_code)
    print(reply.json())
