import asyncio
import time

from sqlalchemy import func, select, text

from db import SessionLocal
from payments import Payment

SUM = func.sum(Payment.amount)
ORM_ROWS = select(Payment)
RAW_ROWS = text("SELECT id, student_id, amount FROM payments")
ORM_SUM = select(Payment.student_id, SUM).group_by(
    Payment.student_id
)
RAW_SUM = text("""\
SELECT student_id, sum(amount) FROM payments
GROUP BY student_id""")


async def bench(label, query):
    best = 1e9
    for _ in range(5):
        start = time.perf_counter()
        async with SessionLocal() as session:
            rows = (await session.execute(query)).all()
        best = min(best, time.perf_counter() - start)
    print(f"{label:<16}{len(rows):>6} rows {best * 1000:7.1f} ms")


async def main():
    print("Load every payment")
    await bench("  ORM objects", ORM_ROWS)
    await bench("  text() rows", RAW_ROWS)
    print("Total paid per student")
    await bench("  ORM query", ORM_SUM)
    await bench("  text() query", RAW_SUM)


asyncio.run(main())
