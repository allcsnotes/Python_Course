import asyncio
import random

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from db import SessionLocal, engine
from models import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int]
    amount: Mapped[int]


async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Payment.__table__.drop, checkfirst=True)
        await conn.run_sync(Payment.__table__.create)
    random.seed(7)
    rows = [{"student_id": random.randint(1, 6),
             "amount": random.choice([499, 599, 699, 799, 899])}
            for _ in range(50_000)]
    async with SessionLocal() as session:
        await session.execute(Payment.__table__.insert(), rows)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(setup())
