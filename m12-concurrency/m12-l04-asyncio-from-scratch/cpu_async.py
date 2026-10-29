import asyncio
import time

N = 100_000_000


async def count(n):
    while n > 0:
        n -= 1


async def main():
    start = time.perf_counter()
    await count(N)
    one = time.perf_counter() - start
    start = time.perf_counter()
    await asyncio.gather(count(N), count(N), count(N))
    three = time.perf_counter() - start
    print(f"one count:    {one:.2f} s")
    print(f"three counts: {three:.2f} s")


asyncio.run(main())
