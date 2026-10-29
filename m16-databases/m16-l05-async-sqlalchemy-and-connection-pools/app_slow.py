from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import Session

from db import URL

engine = create_engine(URL)
async_engine = create_async_engine(URL)
app = FastAPI()


@app.get("/report/blocked")
async def report_blocked():
    with Session(engine) as session:
        session.execute(text("SELECT pg_sleep(1)"))
    return {"report": "ready"}


@app.get("/report/def")
def report_def():
    with Session(engine) as session:
        session.execute(text("SELECT pg_sleep(1)"))
    return {"report": "ready"}


@app.get("/report/async")
async def report_async():
    async with AsyncSession(async_engine) as session:
        await session.execute(text("SELECT pg_sleep(1)"))
    return {"report": "ready"}
