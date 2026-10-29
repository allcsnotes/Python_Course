# Exercise 05 - Top marks, zeros removed
def best_marks(marks, n=3):
    valid = []
    for mark in marks:
        if mark > 0:
            valid.append(mark)
    valid.sort(reverse=True)
    return valid[:n]


raw = [0, 72, 95, 0, 88, 61, 95]
print("Raw:", raw)
print("Top 3:", best_marks(raw))
print("Top 2:", best_marks(raw, 2))
print("Top 10:", best_marks(raw, 10))
print("Raw after:", raw)

while 0 in raw:
    raw.remove(0)
print("Cleaned in place:", raw)
