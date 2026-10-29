from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from db import URL

CLOSE_ALL = """\
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE datname = 'allcs' AND pid <> pg_backend_pid()"""


async def close_idle():
    admin = create_async_engine(URL)
    async with admin.connect() as conn:
        await conn.execute(text(CLOSE_ALL))
    await admin.dispose()
