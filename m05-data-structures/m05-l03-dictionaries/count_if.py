orders = ["Python", "SQL", "Python", "Docker", "Python", "SQL"]
counts = {}
for course in orders:
    if course in counts:
        counts[course] += 1
    else:
        counts[course] = 1
print(counts)
