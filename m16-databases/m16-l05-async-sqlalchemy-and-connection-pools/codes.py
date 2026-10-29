import asyncio
import time
from collections import Counter

import httpx


async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8165",
                                 timeout=60) as client:
        start = time.perf_counter()
        calls = [client.get("/courses/1/welcome")
                 for _ in range(3)]
        replies = await asyncio.gather(*calls)
        seconds = time.perf_counter() - start
    print(dict(Counter(r.status_code for r in replies)))
    print(f"all three answered after {seconds:.1f} seconds")


asyncio.run(main())
