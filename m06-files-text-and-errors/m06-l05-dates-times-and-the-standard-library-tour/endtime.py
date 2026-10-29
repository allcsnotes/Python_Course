from datetime import datetime, timedelta

start = datetime(2026, 11, 2, 18, 0)
length = timedelta(hours=1, minutes=30)
end = start + length
print(end)
print(length)
print(end > start)
