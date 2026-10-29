import logging

logger = logging.getLogger(__name__)


def charge(student, rupees):
    logger.info("charging %s Rs %d", student, rupees)
    if rupees <= 0:
        logger.warning("nothing to charge for %s", student)
        return False
    logger.debug("payment accepted")
    return True
