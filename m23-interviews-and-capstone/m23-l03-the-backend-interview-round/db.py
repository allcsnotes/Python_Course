import atexit
import os

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DSN = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:demo@localhost:23503/allcs",
)
pool = ConnectionPool(
    DSN, min_size=1, max_size=5, kwargs={"row_factory": dict_row}
)


atexit.register(pool.close)
