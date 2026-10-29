import httpx
from bs4 import BeautifulSoup

r = httpx.get("http://localhost:22280/courses?page=1")
soup = BeautifulSoup(r.text, "html.parser")

for box in soup.select(".course"):
    link = box.select_one(".title a")
    title = link.get_text(strip=True)
    price = box.select_one(".price").get_text(strip=True)
    print(title, price)

print(link["href"])
