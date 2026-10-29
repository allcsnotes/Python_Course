from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def last_monday(today: date) -> date:
    this_monday = today - timedelta(days=today.weekday())
    return this_monday - timedelta(days=7)


def week_bounds(monday: date, tz: str):
    """Midnight Monday to midnight next Monday, in tz."""
    start = datetime.combine(monday, time.min, ZoneInfo(tz))
    return start, start + timedelta(days=7)


def week_label(monday: date) -> str:
    iso = monday.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"
