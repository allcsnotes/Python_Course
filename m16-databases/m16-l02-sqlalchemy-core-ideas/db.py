import logging

from sqlalchemy import create_engine

URL = "postgresql+psycopg://postgres:devpass@localhost:15402/allcs"
engine = create_engine(URL)


def show_sql():
    logging.basicConfig(format="%(message)s")
    log = logging.getLogger("sqlalchemy.engine")
    log.setLevel(logging.INFO)
