import asyncio
import time

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from db import URL


async def run(label, engine):
    start = time.perf_counter()
    for _ in range(50):
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    seconds = time.perf_counter() - start
    print(f"{label:<26}50 queries took {seconds:.2f} seconds")


async def main():
    await run("new connection each time", create_async_engine(
        URL, poolclass=NullPool))
    await run("connections from a pool", create_async_engine(URL))


asyncio.run(main())
