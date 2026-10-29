import time
from concurrent.futures import ThreadPoolExecutor

import httpx

from core import LINKS, OPTIONS, report
from seq import check


def run(links, workers=8):
    with httpx.Client(**OPTIONS) as client:

        def work(url):
            return check(client, url)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(work, links))


if __name__ == "__main__":
    began = time.perf_counter()
    results = run(LINKS)
    report(results, time.perf_counter() - began)
