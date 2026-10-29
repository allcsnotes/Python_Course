import json
from collections import Counter

levels = Counter()
with open("app.jsonl") as f:
    for line in f:
        record = json.loads(line)
        levels[record["level"]] += 1

print(levels)
