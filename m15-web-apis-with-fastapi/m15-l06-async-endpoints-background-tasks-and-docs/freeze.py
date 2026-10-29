import asyncio
import time

import httpx

URL = "http://localhost:8156"


async def probe(web, path):
    busy = []
    for _ in range(3):
        busy.append(asyncio.create_task(web.get(path)))
    await asyncio.sleep(0.2)
    start = time.perf_counter()
    await web.get("/health")
    waited = time.perf_counter() - start
    print(f"{path}: health took {waited:.1f} seconds")
    await asyncio.gather(*busy)


async def main():
    async with httpx.AsyncClient(base_url=URL, timeout=30) as web:
        for path in ["/rating/blocked", "/rating/thread"]:
            await probe(web, path)


asyncio.run(main())
