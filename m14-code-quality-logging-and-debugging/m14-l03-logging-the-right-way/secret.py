import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("login")

email = "lukas@example.com"
password = "hunter2"

logger.info("login: %s %s", email, password)
logger.info("login: %s", email)
