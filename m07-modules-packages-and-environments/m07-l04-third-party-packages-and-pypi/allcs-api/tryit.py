import httpx

url = "http://localhost:8074/courses"
try:
    response = httpx.get(url, timeout=2)
    response.raise_for_status()
    for course in response.json():
        if course["price"] < 450:
            print(course["title"])
except httpx.HTTPError as error:
    print("Could not load the courses:", error)
