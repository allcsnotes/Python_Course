import asyncio
import time

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from db import URL

engine = create_async_engine(
    URL, pool_size=2, max_overflow=0, pool_timeout=1
)
start = time.perf_counter()


async def visit(name):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT pg_sleep(2)"))
        result = "done"
    except Exception as error:
        result = type(error).__name__
    seconds = time.perf_counter() - start
    print(f"{name}: {result} after {seconds:.1f} s")


async def main():
    await asyncio.gather(*(visit(name) for name in "ABCD"))


asyncio.run(main())
