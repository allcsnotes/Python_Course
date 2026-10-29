import asyncio
import time

import httpx

URL = "http://localhost:8156"


async def burst(web, path):
    start = time.perf_counter()
    await asyncio.gather(*[web.get(path) for _ in range(10)])
    took = time.perf_counter() - start
    print(f"{path}: ten requests took {took:.1f} seconds")


async def main():
    async with httpx.AsyncClient(base_url=URL, timeout=30) as web:
        for path in ["/rating/plain", "/rating/async"]:
            await burst(web, path)


asyncio.run(main())
