def longest_streak(days):
    best = 0
    for day in days:
        n = 1
        while day + n in days:
            n += 1
        best = max(best, n)
    return best
