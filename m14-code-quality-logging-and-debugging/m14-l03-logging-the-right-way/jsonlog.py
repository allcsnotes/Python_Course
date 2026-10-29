import json
import logging

FIELDS = ("student", "course")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "time": self.formatTime(record, "%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        for key in FIELDS:
            value = getattr(record, key, None)
            if value is not None:
                data[key] = value
        return json.dumps(data)
