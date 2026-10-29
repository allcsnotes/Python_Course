from itertools import groupby

levels = ["INFO", "ERROR", "INFO", "ERROR", "INFO"]
for level, group in groupby(levels):
    print(level, len(list(group)))
