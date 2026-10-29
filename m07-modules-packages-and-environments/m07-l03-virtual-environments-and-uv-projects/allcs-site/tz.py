from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
berlin = ZoneInfo("Europe/Berlin")
start = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(start)
print(start.astimezone(berlin))
print(start == start.astimezone(berlin))
