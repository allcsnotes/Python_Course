from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
start = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(start)
