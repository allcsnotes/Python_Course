import httpx

BASE = "http://localhost:8659"
PEOPLE = [
    ("Lukas", "lukas@example.com"),
    ("Priya", "priya@example.com"),
]
for name, email in PEOPLE:
    body = {"name": name, "email": email}
    r = httpx.post(f"{BASE}/students", json=body)
    print(r.status_code, r.json()["name"])
