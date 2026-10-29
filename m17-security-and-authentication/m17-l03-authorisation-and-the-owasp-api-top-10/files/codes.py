import httpx
from client import BASE, login

lukas = login("lukas@example.com", "lukas-demo-pass")
course = {"title": "My course", "price": 499}


def show(label, r):
    body = r.json()
    message = body.get("detail") or body["error"]["message"]
    print(r.status_code, label, message)


show("no token", httpx.get(f"{BASE}/students/1/enrollments"))
r = httpx.post(f"{BASE}/courses", json=course, headers=lukas)
show("new course", r)
url = f"{BASE}/students/2/enrollments"
show("Priya's list", httpx.get(url, headers=lukas))
