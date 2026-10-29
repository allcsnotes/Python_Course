from datetime import date

today = date(2026, 10, 25)
class_day = date(2026, 11, 2)
gap = class_day - today
print(gap)
print(gap.days)
