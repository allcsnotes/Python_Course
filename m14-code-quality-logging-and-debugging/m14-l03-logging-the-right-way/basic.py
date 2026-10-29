import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.debug("cart has two items")
logging.info("charging Lukas")
logging.warning("card expires soon")
logging.error("payment failed")
