from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import get_settings

engine = create_engine(
    str(get_settings().database_url), pool_pre_ping=True
)


def get_session():
    with Session(engine) as session:
        yield session
