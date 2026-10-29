import logging


def setup():
    logger = logging.getLogger("dup")
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
    return logger


setup()
logger = setup()
logger.warning("payment failed")
