import httpx

BASE = "http://localhost:8192"
form = {
    "username": "priya@example.com",
    "password": "demo-password-1",
}
login = httpx.post(f"{BASE}/auth/login", data=form)
print("login:", login.status_code)
token = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
me = httpx.get(f"{BASE}/me", headers=headers)
print("me:", me.status_code, me.json())
