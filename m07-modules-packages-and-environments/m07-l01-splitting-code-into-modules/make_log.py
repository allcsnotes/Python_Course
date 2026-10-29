import random
from datetime import datetime, timedelta
from pathlib import Path

rng = random.Random(2026)
DAY = datetime(2026, 3, 12)
BUSY = [1, 1, 1, 1, 1, 2, 3, 5, 8, 10, 10, 9,
        8, 9, 10, 9, 8, 8, 9, 10, 9, 6, 3, 2]
MESSAGES = {
    "INFO": ["GET /courses 200 {ms}ms",
             "Student {n} enrolled in course {c}"],
    "WARNING": ["Slow query on lessons table ({ms}ms)",
                "Video {n} is buffering"],
    "ERROR": ["Database connection timeout",
              "Payment failed for order {n}",
              "Video {n} file not found",
              "Upload failed for lesson {n}"],
}
FORMAT = "%Y-%m-%d %H:%M:%S"

lines = []
for _ in range(6000):
    hour = rng.choices(range(24), weights=BUSY)[0]
    offset = rng.randint(0, 3599)
    when = DAY + timedelta(hours=hour, seconds=offset)
    if rng.random() < (0.22 if hour == 14 else 0.02):
        level = "ERROR"
    else:
        level = "WARNING" if rng.random() < 0.08 else "INFO"
    message = rng.choice(MESSAGES[level]).format(
        ms=rng.randint(8, 900), n=rng.randint(100, 999),
        c=rng.randint(1, 40))
    stamp = when.strftime(FORMAT)
    lines.append((when, f"{stamp} {level} {message}"))

lines.sort()
text = [line for _, line in lines]
text[41] = ""
text[1200] = "2026-03-12 09:30"
text[2750] = "2026-03-12 25:61:07 INFO GET /courses 200 31ms"
text[4100] = "#### log rotated ####"
text[5200] = "2026-03-12 20:02:37 ERORR Disk full"
text[5900] = "Traceback (most recent call last):"
Path("server.log").write_text("\n".join(text) + "\n")
print(f"Wrote {len(text)} lines to server.log")
