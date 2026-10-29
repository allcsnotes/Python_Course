import contextvars
import json
import logging
import sys

request_id = contextvars.ContextVar(
    "request_id", default="-"
)
PLAIN = set(logging.makeLogRecord({}).__dict__) | {
    "message"
}


class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "level": record.levelname,
            "logger": record.name,
            "request_id": request_id.get(),
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in PLAIN:
                data[key] = value
        if record.exc_info:
            data["error"] = self.formatException(
                record.exc_info
            )
        return json.dumps(data)


def configure_logging(level="INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=level, handlers=[handler], force=True
    )
