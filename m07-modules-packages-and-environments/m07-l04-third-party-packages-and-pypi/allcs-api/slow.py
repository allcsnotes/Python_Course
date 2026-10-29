import httpx

url = "http://localhost:8074/slow"
response = httpx.get(url, timeout=1)
print(response.status_code)
