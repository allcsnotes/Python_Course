# Q40 - Structured logs with a request ID
import contextvars
import json
import logging
import sys

request_id = contextvars.ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": request_id.get(),
            "logger": record.name,
        })


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
log = logging.getLogger("api")
log.addHandler(handler)
log.setLevel(logging.INFO)


def handle(rid):
    request_id.set(rid)             # every log line in this request now carries it
    log.info("enrollment started")
    log.warning("slow query, %d ms", 850)

handle("req-7f3a")
handle("req-91bc")
