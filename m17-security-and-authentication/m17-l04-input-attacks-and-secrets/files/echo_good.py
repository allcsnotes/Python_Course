import logging

from search_good import search

logging.basicConfig(format="%(message)s")
engine_log = logging.getLogger("sqlalchemy.engine")
engine_log.setLevel(logging.INFO)
search("zzz' OR true --")
