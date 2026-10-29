from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import SessionLocal
from models import Course

app = FastAPI()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get("/courses/{course_id}")
async def read_course(course_id: int, session: SessionDep):
    course = await session.get(Course, course_id)
    if course is None:
        raise HTTPException(404, "Course not found")
    return {"id": course.id, "title": course.title,
            "price": course.price}
