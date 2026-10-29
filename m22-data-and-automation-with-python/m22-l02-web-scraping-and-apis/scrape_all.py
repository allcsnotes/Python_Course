import httpx
from bs4 import BeautifulSoup

BASE = "http://localhost:22280"
url = BASE + "/courses?page=1"
courses = []
while url:
    r = httpx.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for box in soup.select(".course"):
        link = box.select_one(".title a")
        price = box.select_one(".price")
        courses.append({
            "title": link.get_text(strip=True),
            "price": price.get_text(strip=True),
            "url": BASE + link["href"],
        })
    print(r.status_code, url, len(courses))
    nxt = soup.select_one("a.next")
    url = BASE + nxt["href"] if nxt else None
print(len(courses), "courses")
