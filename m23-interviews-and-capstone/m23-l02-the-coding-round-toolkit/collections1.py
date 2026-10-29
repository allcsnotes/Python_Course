from collections import Counter, defaultdict

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
groups = defaultdict(list)
for w in words:
    groups["".join(sorted(w))].append(w)
print(dict(groups))
print(Counter("eat") == Counter("tea"))
print(Counter("hello").most_common(1))
