import asyncio

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from db import URL
from models import Course

engine = create_async_engine(
    URL, pool_size=2, max_overflow=0, pool_timeout=1
)
SessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)
app = FastAPI()


@app.get("/courses/{course_id}/welcome")
async def welcome(course_id: int):
    async with SessionLocal() as session:
        course = await session.get(Course, course_id)
    await asyncio.sleep(2)  # pretend: a slow email service
    return {"sent": course.title}
