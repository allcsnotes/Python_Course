import time
from concurrent.futures import ThreadPoolExecutor

import httpx

from core import LINKS, OPTIONS, from_response

client = httpx.Client(**OPTIONS)


def check(url):
    start = time.perf_counter()
    response = client.get(url)
    return from_response(url, response, start)


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, LINKS))
print(len(results), "links checked")
