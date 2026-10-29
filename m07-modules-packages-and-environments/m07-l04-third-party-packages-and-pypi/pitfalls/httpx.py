import httpx

response = httpx.get("http://localhost:8074/courses")
print(response.status_code)
