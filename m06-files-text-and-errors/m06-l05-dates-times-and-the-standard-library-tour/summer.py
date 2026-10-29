from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
berlin = ZoneInfo("Europe/Berlin")
winter = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
summer = datetime(2027, 7, 1, 18, 0, tzinfo=kolkata)
print(winter.astimezone(berlin))
print(summer.astimezone(berlin))
