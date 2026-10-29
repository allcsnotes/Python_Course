from itertools import groupby

levels = ["INFO", "ERROR", "INFO", "ERROR", "INFO"]
for level, group in groupby(sorted(levels)):
    print(level, len(list(group)))
