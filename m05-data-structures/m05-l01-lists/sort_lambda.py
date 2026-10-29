hours = [9, 14, 18, 20]
print(sorted(hours, key=lambda hour: abs(hour - 17)))
print(min(hours, key=lambda hour: abs(hour - 17)))
