import asyncio

from db import SessionLocal
from models import Course


async def main():
    async with SessionLocal() as session:
        course = await session.get(Course, 1)
        print(course.title)
        print(len(course.lessons), "lessons")


asyncio.run(main())
