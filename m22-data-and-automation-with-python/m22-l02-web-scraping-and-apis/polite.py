import time
from pathlib import Path
from urllib.parse import quote
from urllib.robotparser import RobotFileParser

import httpx

BASE = "http://localhost:22280"
UA = "allcsv-bot/1.0 (asha@allcsvideos.com)"
CACHE = Path("cache")
CACHE.mkdir(exist_ok=True)

rp = RobotFileParser(BASE + "/robots.txt")
rp.read()
DELAY = rp.crawl_delay(UA) or 1


def get(url):
    if not rp.can_fetch(UA, url):
        raise PermissionError(f"robots.txt says no: {url}")
    file = CACHE / quote(url, safe="")
    if file.exists():
        return file.read_text()
    while True:
        time.sleep(DELAY)
        r = httpx.get(url, headers={"User-Agent": UA}, timeout=10)
        if r.status_code != 429:
            break
        wait = int(r.headers["Retry-After"])
        print("429: waiting", wait, "seconds")
        time.sleep(wait)
    r.raise_for_status()
    file.write_text(r.text)
    return r.text
