import bisect

hours = [9, 11, 14, 18, 20]
print(bisect.bisect_left(hours, 14))
print(bisect.bisect_left(hours, 15))
bisect.insort(hours, 15)
print(hours)
