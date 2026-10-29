import httpx

response = httpx.get("http://localhost:8074/missing")
response.raise_for_status()
print(response.json())
