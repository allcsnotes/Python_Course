from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

FORMAT = "%Y-%m-%d %H:%M:%S"
mumbai = ZoneInfo("Asia/Kolkata")
utc_hours = Counter()
mumbai_hours = Counter()
with Path("server.log").open(encoding="utf-8") as f:
    for line in f:
        if " ERROR " in line:
            day, clock, _ = line.split(" ", 2)
            when = datetime.strptime(f"{day} {clock}", FORMAT)
            when = when.replace(tzinfo=timezone.utc)
            utc_hours[when.hour] += 1
            mumbai_hours[when.astimezone(mumbai).hour] += 1
print("UTC:   ", utc_hours.most_common(2))
print("Mumbai:", mumbai_hours.most_common(2))
