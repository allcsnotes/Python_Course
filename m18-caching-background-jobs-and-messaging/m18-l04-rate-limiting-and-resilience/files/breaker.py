import time


class CircuitOpen(Exception):
    pass


class Breaker:
    def __init__(self, limit=3, pause=2.0):
        self.limit, self.pause = limit, pause
        self.fails, self.opened_at = 0, None

    def state(self):
        if self.opened_at is None:
            return "closed"
        if time.monotonic() - self.opened_at >= self.pause:
            return "half-open"
        return "open"

    def call(self, func):
        if self.state() == "open":
            raise CircuitOpen("skipped")
        try:
            result = func()
        except Exception:
            self.fails += 1
            if self.fails >= self.limit:
                self.opened_at = time.monotonic()
            raise
        self.fails, self.opened_at = 0, None
        return result
