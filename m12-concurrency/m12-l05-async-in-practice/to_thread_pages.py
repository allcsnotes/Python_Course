import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(n):
    return await asyncio.to_thread(httpx.get, URL.format(n))


async def main():
    start = time.perf_counter()
    await asyncio.gather(*(fetch(n) for n in range(1, 21)))
    seconds = time.perf_counter() - start
    print(f"20 pages, threads: {seconds:.1f} seconds")


asyncio.run(main())
