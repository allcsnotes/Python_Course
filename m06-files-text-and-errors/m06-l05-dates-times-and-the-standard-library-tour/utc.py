from datetime import datetime, timezone
from zoneinfo import ZoneInfo

saved = datetime(2026, 11, 2, 12, 30, tzinfo=timezone.utc)
print(saved)
print(saved.astimezone(ZoneInfo("Asia/Kolkata")))
print(saved.astimezone(ZoneInfo("Europe/Berlin")))
