from datetime import datetime


def read_day(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return None


print(read_day("2026-11-02"))
print(read_day("02/11/2026"))
