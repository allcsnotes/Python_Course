import httpx
from client import BASE, login

headers = login("lukas@example.com", "lukas-demo-pass")

for number in (1, 2, 999):
    url = f"{BASE}/students/{number}/enrollments"
    r = httpx.get(url, headers=headers)
    if r.is_success:
        titles = [e["title"] for e in r.json()]
        print(number, r.status_code, titles)
    else:
        message = r.json()["error"]["message"]
        print(number, r.status_code, message)
