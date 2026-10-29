import httpx

response = httpx.get("http://localhost:8074/missing")
print(response.status_code)
print(response.json())
