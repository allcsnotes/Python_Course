from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from app.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL, pool_size=20, max_overflow=20
)


class Base(DeclarativeBase):
    pass


def get_session():
    with Session(engine) as session:
        yield session
