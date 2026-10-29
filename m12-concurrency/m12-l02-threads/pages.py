import httpx

BASE = "http://localhost:8122"


def fetch(n):
    response = httpx.get(f"{BASE}/courses/{n}")
    if response.status_code != 200:
        message = f"course {n}: status {response.status_code}"
        raise ValueError(message)
    return response.json()["title"]
