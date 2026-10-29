import logging

from sqlalchemy import create_engine

URL = "postgresql+psycopg://postgres:devpass@localhost:15403/allcs"
engine = create_engine(URL)


def show_sql():
    logging.basicConfig(format="%(message)s")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
