import httpx
from client import BASE, login

headers = login("lukas@example.com", "lukas-demo-pass")

for number in (1, 2):
    url = f"{BASE}/students/{number}/enrollments"
    r = httpx.get(url, headers=headers)
    titles = [e["title"] for e in r.json()]
    print(number, r.status_code, titles)
