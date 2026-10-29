from collections import Counter

levels = Counter()
for level in ["INFO", "ERROR", "INFO", "INFO"]:
    levels[level] += 1
print(levels)
print(levels["WARNING"])
