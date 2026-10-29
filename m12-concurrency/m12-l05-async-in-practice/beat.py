import asyncio
import time


async def heartbeat():
    last = time.perf_counter()
    worst = 0
    for _ in range(30):
        await asyncio.sleep(0.1)
        now = time.perf_counter()
        worst = max(worst, now - last)
        last = now
    print(f"worst gap between beats: {worst:.1f} seconds")
