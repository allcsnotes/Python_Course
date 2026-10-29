import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from db import URL

engine = create_async_engine(URL)
watcher = create_async_engine(URL)
COUNT = """SELECT count(*) FROM pg_stat_activity
         WHERE datname = 'allcs' AND pid <> pg_backend_pid()"""


async def visit():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT pg_sleep(2)"))


async def watch():
    await asyncio.sleep(1)
    async with watcher.connect() as conn:
        limit = await conn.scalar(text("SHOW max_connections"))
        busy = await conn.scalar(text(COUNT))
    print(f"Postgres allows {limit}, this program uses {busy}")


async def main():
    await asyncio.gather(watch(), *(visit() for _ in range(40)))


asyncio.run(main())
