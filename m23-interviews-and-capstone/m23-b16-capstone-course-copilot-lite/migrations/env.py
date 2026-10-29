from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from app.models import Base
from app.settings import get_settings

url = str(get_settings().database_url)
fileConfig(context.config.config_file_name)


def run_migrations_online():
    engine = create_engine(url)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
