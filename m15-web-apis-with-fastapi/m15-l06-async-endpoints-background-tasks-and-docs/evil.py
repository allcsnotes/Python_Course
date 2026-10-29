import httpx

URL = "http://localhost:8156/courses/7/thumbnail"

with open("thumb.png", "rb") as file:
    sent = ("../../evil.png", file, "image/png")
    reply = httpx.post(URL, files={"file": sent})
print(reply.json())
