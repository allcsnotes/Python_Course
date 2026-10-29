import logging


def setup():
    logger = logging.getLogger("dup")
    logger.addHandler(logging.StreamHandler())
    return logger


setup()
logger = setup()
logger.warning("payment failed")
