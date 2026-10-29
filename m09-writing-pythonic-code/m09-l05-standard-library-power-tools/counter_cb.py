from collections import Counter

monday = Counter(["Python", "SQL", "Python"])
tuesday = Counter(["Python", "Docker"])
print(monday + tuesday)
monday.update(["Go", "Go"])
print(monday)
