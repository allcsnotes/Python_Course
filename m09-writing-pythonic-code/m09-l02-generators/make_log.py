# makes a log like the M06-B03 one, with N lines: python mk_log.py N out
import random, sys
from datetime import datetime, timedelta
n = int(sys.argv[1]); out = sys.argv[2]
rng = random.Random(2026)
DAY = datetime(2026, 3, 12)
BUSY = [1, 1, 1, 1, 1, 2, 3, 5, 8, 10, 10, 9, 8, 9, 10, 9, 8, 8, 9, 10, 9, 6, 3, 2]
MESSAGES = {"INFO": ["GET /courses 200 {ms}ms", "Student {n} enrolled in course {c}"],
            "WARNING": ["Slow query on lessons table ({ms}ms)", "Video {n} is buffering"],
            "ERROR": ["Database connection timeout", "Payment failed for order {n}", "Video {n} file not found", "Upload failed for lesson {n}"]}
hours = rng.choices(range(24), weights=BUSY, k=n)
with open(out, "w") as f:
    rows = []
    for hour in hours:
        offset = rng.randint(0, 3599)
        when = DAY + timedelta(hours=hour, seconds=offset)
        if rng.random() < (0.22 if hour == 14 else 0.02): level = "ERROR"
        else: level = "WARNING" if rng.random() < 0.08 else "INFO"
        msg = rng.choice(MESSAGES[level]).format(ms=rng.randint(8, 900), n=rng.randint(100, 999), c=rng.randint(1, 40))
        rows.append(f"{when:%Y-%m-%d %H:%M:%S} {level} {msg}")
    rows.sort()
    f.write("\n".join(rows) + "\n")
print("wrote", n, "lines to", out)
