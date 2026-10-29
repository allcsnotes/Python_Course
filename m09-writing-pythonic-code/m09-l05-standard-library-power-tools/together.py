from collections import Counter, deque

lines = [
    "10:01 INFO login",
    "10:02 ERROR payment failed",
    "10:03 INFO login",
    "10:04 ERROR video missing",
    "10:05 INFO logout",
    "10:06 ERROR payment failed",
]
counts = Counter()
last = deque(maxlen=2)
for line in lines:
    level = line.split()[1]
    counts[level] += 1
    if level == "ERROR":
        last.append(line)
print(counts)
print(list(last))
