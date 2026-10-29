import httpx
from client import BASE, login

PEOPLE = [
    ("lukas", "student"),
    ("meera", "instructor"),
    ("asha", "admin"),
]

for name, role in PEOPLE:
    headers = login(f"{name}@example.com", f"{name}-demo-pass")
    course = {"title": f"A course by {name}", "price": 499}
    r = httpx.post(f"{BASE}/courses", json=course, headers=headers)
    print(name, role, r.status_code)
