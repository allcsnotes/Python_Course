import logging

logging.warning("early call")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
    force=True,
)
logging.debug("can we see this?")
