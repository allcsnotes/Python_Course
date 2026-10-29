import asyncio
import time


async def slow_page():
    await asyncio.sleep(5)
    return "page"


async def main():
    start = time.perf_counter()
    try:
        async with asyncio.timeout(1):
            await slow_page()
    except TimeoutError:
        print("gave up")
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
