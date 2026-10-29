import asyncio

from sqlalchemy import select

from db import SessionLocal
from models import Course


async def main():
    async with SessionLocal() as session:
        query = select(Course).limit(3)
        result = await session.execute(query)
        for course in result.scalars():
            print(course.id, course.title, course.price)


asyncio.run(main())
