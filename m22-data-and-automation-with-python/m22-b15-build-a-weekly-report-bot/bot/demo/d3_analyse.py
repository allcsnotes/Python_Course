from datetime import date, timedelta

import httpx

from weekly_report.analyse import summarise
from weekly_report.api import fetch_report
from weekly_report.settings import Settings
from weekly_report.weeks import week_bounds

settings = Settings()
tz = settings.timezone
start, end = week_bounds(date(2026, 10, 19), tz)
with httpx.Client(base_url=settings.api_url) as client:
    data = fetch_report(
        client, settings, start - timedelta(days=7), end
    )
s = summarise(data, start, end, tz)
print(s.enrollments, "enrollments, last week", s.before)
print("gross", s.gross, "refunded", s.refunded, "net", s.net)
print(s.per_course)
