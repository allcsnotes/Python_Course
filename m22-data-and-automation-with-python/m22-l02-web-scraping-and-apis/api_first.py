import os

import httpx

TOKEN = os.environ["ALLCS_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
url = "http://localhost:22281/api/courses?limit=10"
courses = []

while url:
    r = httpx.get(url, headers=HEADERS, timeout=5)
    r.raise_for_status()
    data = r.json()
    courses.extend(data["results"])
    print(r.status_code, len(courses), "so far")
    url = data["next"]

print(len(courses), "courses")
print(courses[0])
