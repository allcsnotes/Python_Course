from datetime import date, timedelta

import httpx

from weekly_report.analyse import summarise
from weekly_report.api import fetch_report
from weekly_report.settings import Settings
from weekly_report.weeks import week_bounds

settings = Settings()
week = date(2026, 10, 19)
with httpx.Client(base_url=settings.api_url) as client:
    for tz in ["UTC", "Asia/Kolkata"]:
        start, end = week_bounds(week, tz)
        before = start - timedelta(days=7)
        data = fetch_report(client, settings, before, end)
        s = summarise(data, start, end, tz)
        print(
            f"{tz:13}",
            s.enrollments,
            "enrollments, Rs",
            s.gross,
        )
