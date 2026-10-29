import httpx

url = "http://localhost:8074/courses"
response = httpx.get(url)
print(response.status_code)
print(response.text)
