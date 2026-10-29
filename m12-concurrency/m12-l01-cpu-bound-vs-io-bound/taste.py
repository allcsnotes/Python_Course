import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def check_page(n):
    time.sleep(0.5)


def build_report(n):
    total = 0
    for i in range(35_000_000):
        total += i


async def check_page_async(n):
    await asyncio.sleep(0.5)


async def many(count):
    await asyncio.gather(*(check_page_async(n) for n in range(count)))


def timed(label, fn):
    start = time.perf_counter()
    fn()
    print(f"{label}: {time.perf_counter() - start:.2f} s")


if __name__ == "__main__":
    pages = range(10)
    jobs = range(4)
    timed("10 pages, one by one", lambda: [check_page(n) for n in pages])
    with ThreadPoolExecutor(10) as pool:
        timed("10 pages, threads", lambda: list(pool.map(check_page, pages)))
    timed("4 reports, one by one", lambda: [build_report(n) for n in jobs])
    with ThreadPoolExecutor(4) as pool:
        timed("4 reports, threads", lambda: list(pool.map(build_report, jobs)))
    with ProcessPoolExecutor(4) as pool:
        timed("4 reports, processes", lambda: list(pool.map(build_report, jobs)))
    timed("1000 pages, asyncio", lambda: asyncio.run(many(1000)))
