import json

import httpx

url = "http://localhost:8153/courses"
bad = {"title": "Python Basics", "price": "free"}
r = httpx.post(url, json=bad)
print(r.status_code)
print(json.dumps(r.json(), indent=2))
