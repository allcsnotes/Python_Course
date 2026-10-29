import logging

logging.warning("early call")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
)
logging.debug("can we see this?")
