from datetime import datetime

text = "2026-11-02 18:00"
when = datetime.strptime(text, "%Y-%m-%d %H:%M")
print(when)
print(type(when))
