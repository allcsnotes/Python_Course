import logging
from jsonlog import JsonFormatter

handler = logging.FileHandler("app.jsonl", mode="w")
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("enrol")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

for name in ("Lukas", "Priya", "Meera"):
    logger.info("enrolled", extra={"student": name})
logger.warning("almost full", extra={"course": "c101"})
logger.error("payment failed", extra={"student": "Lukas"})
