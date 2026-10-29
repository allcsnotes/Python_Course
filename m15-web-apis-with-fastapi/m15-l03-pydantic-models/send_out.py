import httpx

url = "http://localhost:8153/students"
body = {"name": "Lukas", "email": "lukas@example.com", "password": "s3cret-demo"}
r = httpx.post(url, json=body)
print(r.status_code, r.json())
