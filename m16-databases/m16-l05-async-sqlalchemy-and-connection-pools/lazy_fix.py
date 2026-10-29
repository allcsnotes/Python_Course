import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import SessionLocal
from models import Course


async def main():
    async with SessionLocal() as session:
        query = select(Course).where(Course.id == 1).options(
            selectinload(Course.lessons))
        course = (await session.execute(query)).scalar_one()
        print(course.title)
        print(len(course.lessons), "lessons")


asyncio.run(main())
