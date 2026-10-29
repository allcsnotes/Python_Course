orders = ["Python", "SQL", "Python", "Docker", "Python", "SQL"]
counts = {}
for course in orders:
    counts[course] = counts.get(course, 0) + 1
print(counts)
