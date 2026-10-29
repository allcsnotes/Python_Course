from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
print(start.strftime("%d/%m/%Y"))
print(start.strftime("%H:%M"))
print(start.strftime("%A, %d %B %Y"))
print(f"Class: {start:%d %B, %H:%M}")
