import asyncio

from sqlalchemy import select

from db import SessionLocal
from models import Course


async def main():
    async with SessionLocal() as session:
        result = session.execute(select(Course))
        print(result.scalars().all())


asyncio.run(main())
