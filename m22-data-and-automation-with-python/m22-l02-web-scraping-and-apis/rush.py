from pathlib import Path

import polite
from read_page import read_page

polite.DELAY = 0.1
polite.CACHE = Path("cache_rush")
polite.CACHE.mkdir(exist_ok=True)

url = polite.BASE + "/courses?page=1"
while url:
    rows, url = read_page(polite.get(url))
    print(len(rows), "rows")
