from datetime import UTC, date

from weekly_report.weeks import week_bounds

start, end = week_bounds(date(2026, 10, 19), "Asia/Kolkata")
print("start", start.isoformat())
print("  in UTC", start.astimezone(UTC).isoformat())
print("end  ", end.isoformat())
