import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "audit.log", maxBytes=100, backupCount=2
)
logger = logging.getLogger("audit")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

for number in range(20):
    logger.info("line number %d", number)
