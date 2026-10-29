import requests

response = requests.get("http://localhost:8074/courses")
print(response.status_code)
print(response.json()[0])
