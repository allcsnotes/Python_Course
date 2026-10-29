from collections import Counter, deque
from functools import cache
from itertools import batched, groupby

words = ["go", "sql", "go", "rust", "sql", "go"]
print(Counter(words).most_common(1))
last = deque(words, maxlen=2)
print(list(last))
for key, grp in groupby(sorted(words)):
    print(key, len(list(grp)))
print(list(batched(words, 4)))


@cache
def square(n):
    return n * n


print(square(12))
