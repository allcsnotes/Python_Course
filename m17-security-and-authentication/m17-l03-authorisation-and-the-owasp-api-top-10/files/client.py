import httpx

BASE = "http://localhost:8173"


def login(email, password):
    form = {"username": email, "password": password}
    reply = httpx.post(f"{BASE}/auth/login", data=form)
    token = reply.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
