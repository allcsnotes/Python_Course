import asyncio
import time

import httpx

BASE = "http://localhost:8125"


async def check(client, path):
    try:
        response = await client.get(BASE + path)
        response.raise_for_status()
    except httpx.HTTPError as error:
        return f"{path}: failed ({type(error).__name__})"
    return f"{path}: ok"


async def main():
    paths = ["/page/1", "/missing", "/slow", "/page/2"]
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=2) as client:
        jobs = [check(client, p) for p in paths]
        results = await asyncio.gather(*jobs)
    print("\n".join(results))
    print(f"{time.perf_counter() - start:.1f} seconds")


asyncio.run(main())
