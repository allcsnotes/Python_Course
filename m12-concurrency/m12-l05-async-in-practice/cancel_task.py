import asyncio
import time

import httpx

SLOW = "http://localhost:8125/slow"


async def main():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        task = asyncio.create_task(client.get(SLOW))
        await asyncio.sleep(1)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("cancelled:", task.cancelled())
    print(f"stopped after {time.perf_counter() - start:.1f} seconds")


asyncio.run(main())
