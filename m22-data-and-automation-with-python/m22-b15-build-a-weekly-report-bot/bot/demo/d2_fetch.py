from datetime import date
from pprint import pprint

import httpx

from weekly_report.api import fetch_report
from weekly_report.settings import Settings
from weekly_report.weeks import week_bounds

settings = Settings()
start, end = week_bounds(date(2026, 10, 19), settings.timezone)
with httpx.Client(base_url=settings.api_url) as client:
    data = fetch_report(client, settings, start, end)
print(len(data["enrollments"]), "enrollments")
print(len(data["refunds"]), "refunds")
pprint(data["enrollments"][0])
