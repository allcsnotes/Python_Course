from collections import Counter

orders = ["Python", "SQL", "Python", "Docker", "Python", "SQL"]
counts = Counter(orders)
print(counts)
print(counts.most_common(2))
print(counts["Python"], counts["Rust"])
