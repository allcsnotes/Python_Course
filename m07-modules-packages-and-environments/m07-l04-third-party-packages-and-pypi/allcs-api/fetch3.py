import httpx

url = "http://localhost:8074/courses"
response = httpx.get(url)
courses = response.json()
print(type(courses))
for course in courses:
    print(course["title"], course["price"])
