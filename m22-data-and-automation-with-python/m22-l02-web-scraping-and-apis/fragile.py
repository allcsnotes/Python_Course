import httpx
from bs4 import BeautifulSoup

r = httpx.get("http://localhost:22280/new/courses?page=1")
soup = BeautifulSoup(r.text, "html.parser")

boxes = soup.select(".course")
print(r.status_code, len(boxes), "courses")

price = soup.select_one(".price").get_text(strip=True)
print(price)
