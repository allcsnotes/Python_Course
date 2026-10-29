"""Task 5 - a sliding-window rate limiter with an injectable clock."""
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, limit: int, window: float, clock=time.monotonic):
        if limit < 1 or window <= 0:
            raise ValueError("limit must be >= 1 and window > 0")
        self.limit, self.window, self.clock = limit, window, clock
        self._calls: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = self.clock()
        calls = self._calls[key]
        while calls and calls[0] <= now - self.window:   # forget calls outside the window
            calls.popleft()
        if len(calls) >= self.limit:
            return False
        calls.append(now)
        return True

    def retry_after(self, key: str) -> float:
        """Seconds until the next call would be allowed (0 if allowed now)."""
        calls = self._calls[key]
        if len(calls) < self.limit:
            return 0.0
        return max(0.0, calls[0] + self.window - self.clock())
