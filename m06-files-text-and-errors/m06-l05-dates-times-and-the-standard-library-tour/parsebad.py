from datetime import datetime

text = "02/11/2026"
when = datetime.strptime(text, "%Y-%m-%d")
print(when)
