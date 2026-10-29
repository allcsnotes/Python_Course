import time
from collections import deque

items = list(range(100000))
start = time.perf_counter()
while items:
    items.pop(0)
list_time = time.perf_counter() - start

line = deque(range(100000))
start = time.perf_counter()
while line:
    line.popleft()
deque_time = time.perf_counter() - start

print(f"list pop(0): {list_time * 1000:.1f} ms")
print(f"deque popleft: {deque_time * 1000:.1f} ms")
