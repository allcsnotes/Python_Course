from bs4 import BeautifulSoup

BASE = "http://localhost:22280"


def read_page(html):
    soup = BeautifulSoup(html, "html.parser")
    boxes = soup.select(".course, .card")
    if not boxes:
        raise ValueError("no courses found: did the page change?")
    rows = []
    for box in boxes:
        link = box.select_one(".title a, .card-title a")
        price = box.select_one(".price, .card-price")
        if link is None or price is None:
            raise ValueError("a course box has changed")
        rows.append({
            "title": link.get_text(strip=True),
            "price": price.get_text(strip=True),
            "url": BASE + link["href"],
        })
    nxt = soup.select_one("a.next, a[rel=next]")
    return rows, (BASE + nxt["href"] if nxt else None)
