import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lazy")


class Report:
    def __str__(self):
        print("building the text...")
        return "big report"


logger.debug("lazy: %s", Report())
logger.debug(f"f-string: {Report()}")
logger.info("info: %s", Report())
