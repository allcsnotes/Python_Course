import asyncio
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
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


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get("/courses/{course_id}/welcome")
async def welcome(course_id: int, session: SessionDep):
    course = await session.get(Course, course_id)
    await asyncio.sleep(2)  # pretend: a slow email service
    return {"sent": course.title}
