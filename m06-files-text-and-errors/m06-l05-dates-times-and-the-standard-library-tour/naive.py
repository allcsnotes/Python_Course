from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
naive = datetime(2026, 11, 2, 18, 0)
aware = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(naive.tzinfo)
print(aware.tzinfo)
print(aware - naive)
