import logging

logger = logging.getLogger("allcsvideos")
logger.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

screen = logging.StreamHandler()
screen.setLevel(logging.INFO)
screen.setFormatter(fmt)

disk = logging.FileHandler("app.log")
disk.setLevel(logging.DEBUG)
disk.setFormatter(fmt)

logger.addHandler(screen)
logger.addHandler(disk)

logger.debug("cart has two items")
logger.info("charging Lukas")
logger.error("payment failed")
