import time

import httpx
from bs4 import BeautifulSoup

start = time.perf_counter()
r = httpx.get("http://localhost:22280/live")
soup = BeautifulSoup(r.text, "html.parser")

print(r.status_code, len(soup.select("li.session")), "sessions")
print(soup.select_one("#sessions"))
print(f"{time.perf_counter() - start:.2f} s")
