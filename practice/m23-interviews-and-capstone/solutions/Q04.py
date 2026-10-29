# Q04 - Threads, processes or asyncio? And what freezes an event loop
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def wait_io(_):                     # IO-bound: waiting for the network
    time.sleep(0.5)

def burn(n):                        # CPU-bound: calculating
    return sum(i * i for i in range(n))

async def wait_async(_):
    await asyncio.sleep(0.5)

async def many():
    await asyncio.gather(*(wait_async(i) for i in range(10)))

async def blocking_one(_):
    time.sleep(0.3)                 # BAD inside async: nobody else can run

async def thread_one(_):
    await asyncio.to_thread(time.sleep, 0.3)    # fix: hand it to a worker thread

async def five(fn):
    await asyncio.gather(*(fn(i) for i in range(5)))

def timed(label, fn):
    start = time.perf_counter()
    fn()
    print(f"{label:<34}{time.perf_counter() - start:5.2f}s")

if __name__ == "__main__":
    timed("10 waits, one after another", lambda: [wait_io(i) for i in range(10)])
    with ThreadPoolExecutor(10) as pool:
        timed("10 waits, 10 threads", lambda: list(pool.map(wait_io, range(10))))
    timed("10 waits, asyncio.gather", lambda: asyncio.run(many()))
    with ProcessPoolExecutor(4) as pool:
        list(pool.map(burn, [10] * 4))          # warm up the workers first
        timed("4 CPU jobs, 4 processes", lambda: list(pool.map(burn, [3_000_000] * 4)))
    timed("4 CPU jobs, one process", lambda: [burn(3_000_000) for _ in range(4)])
    timed("5 x time.sleep inside async", lambda: asyncio.run(five(blocking_one)))
    timed("5 x asyncio.to_thread", lambda: asyncio.run(five(thread_one)))
