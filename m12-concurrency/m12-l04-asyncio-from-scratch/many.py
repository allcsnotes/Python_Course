import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    pages = [f"page {n}" for n in range(100)]
    start = time.perf_counter()
    results = await asyncio.gather(*[fetch(p) for p in pages])
    print(len(results), "pages")
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
