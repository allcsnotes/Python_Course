from collections import Counter
from datetime import datetime

times = ["18:05:10", "18:40:02", "19:01:55", "18:59:59"]
hours = []
for t in times:
    when = datetime.strptime(t, "%H:%M:%S")
    hours.append(when.hour)
print(Counter(hours))
