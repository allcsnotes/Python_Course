import asyncio
import sys
import time

import httpx


async def main(path, count):
    async with httpx.AsyncClient(base_url="http://localhost:8165",
                                 timeout=120) as client:
        start = time.perf_counter()
        calls = [client.get(path) for _ in range(count)]
        await asyncio.gather(*calls)
        seconds = time.perf_counter() - start
    print(f"{path}: {count} requests, {seconds:.1f} seconds")


asyncio.run(main(sys.argv[1], int(sys.argv[2])))
