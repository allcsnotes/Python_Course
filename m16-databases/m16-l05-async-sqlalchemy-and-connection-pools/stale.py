import asyncio
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from db import URL
from helpers import close_idle

PING = "--ping" in sys.argv
engine = create_async_engine(URL, pool_pre_ping=PING)
COUNT = text("SELECT count(*) FROM courses")


async def count_courses():
    async with engine.connect() as conn:
        return await conn.scalar(COUNT)


async def main():
    print("first query:", await count_courses())
    await close_idle()
    print("database closed our idle connection")
    print("second query:", await count_courses())


asyncio.run(main())
