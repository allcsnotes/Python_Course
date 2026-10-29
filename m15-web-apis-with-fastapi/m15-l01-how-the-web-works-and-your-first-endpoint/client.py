import httpx

response = httpx.get("http://localhost:8151/courses")
print(response.status_code)
print(response.headers["content-type"])
for course in response.json():
    print(course["title"], course["price"])
