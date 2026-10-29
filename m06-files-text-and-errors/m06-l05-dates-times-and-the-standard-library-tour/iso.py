from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
text = start.isoformat()
print(text)
print(datetime.fromisoformat(text) == start)
