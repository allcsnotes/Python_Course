# a second log, from the day before, with fewer lines (made the same way as make_log.py from module 6)
import random
from datetime import datetime, timedelta
from pathlib import Path

rng = random.Random(2025)
DAY = datetime(2026, 3, 11)
BUSY = [1, 1, 1, 1, 1, 2, 3, 5, 8, 10, 10, 9, 8, 9, 10, 9, 8, 8, 9, 10, 9, 6, 3, 2]
MESSAGES = {"INFO": ["GET /courses 200 {ms}ms", "Student {n} enrolled in course {c}"],
            "WARNING": ["Slow query on lessons table ({ms}ms)", "Video {n} is buffering"],
            "ERROR": ["Database connection timeout", "Payment failed for order {n}", "Video {n} file not found", "Upload failed for lesson {n}"]}
lines = []
for _ in range(2500):
    hour = rng.choices(range(24), weights=BUSY)[0]
    when = DAY + timedelta(hours=hour, seconds=rng.randint(0, 3599))
    level = "ERROR" if rng.random() < 0.05 else ("WARNING" if rng.random() < 0.08 else "INFO")
    message = rng.choice(MESSAGES[level]).format(ms=rng.randint(8, 900), n=rng.randint(100, 999), c=rng.randint(1, 40))
    lines.append((when, f"{when:%Y-%m-%d %H:%M:%S} {level} {message}"))
lines.sort()
Path("yesterday.log").write_text("\n".join(l for _, l in lines) + "\n")
