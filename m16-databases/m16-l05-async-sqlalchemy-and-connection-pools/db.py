from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

URL = (
    "postgresql+psycopg://postgres:secret"
    "@localhost:15405/allcs"
)

engine = create_async_engine(URL)
SessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)
