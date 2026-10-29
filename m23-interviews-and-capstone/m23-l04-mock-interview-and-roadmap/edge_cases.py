from streak_v2 import longest_streak

cases = {
    "empty": [],
    "one day": [5],
    "duplicates": [4, 4, 5, 5],
    "negative": [-2, -1, 0, 1],
    "gaps": [1, 2, 3, 10, 11],
}
for name, days in cases.items():
    print(name, "->", longest_streak(days))
