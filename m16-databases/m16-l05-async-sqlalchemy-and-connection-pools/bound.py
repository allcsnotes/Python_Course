import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from db import URL

engine = create_async_engine(URL, echo=True)
QUERY = text("""\
SELECT id, amount FROM payments
WHERE student_id = :student AND amount > :limit
ORDER BY id LIMIT 3""")


async def main():
    async with engine.connect() as conn:
        values = {"student": 2, "limit": 800}
        result = await conn.execute(QUERY, values)
        for row in result:
            print(row.id, row.amount)


asyncio.run(main())
