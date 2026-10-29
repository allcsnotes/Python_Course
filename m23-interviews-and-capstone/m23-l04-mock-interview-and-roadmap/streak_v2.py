def longest_streak(days):
    seen = set(days)
    best = 0
    for day in seen:
        if day - 1 not in seen:
            n = 1
            while day + n in seen:
                n += 1
            best = max(best, n)
    return best
