import logging

import payments

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("app started")
payments.charge("Lukas", 499)
payments.charge("Priya", 0)
