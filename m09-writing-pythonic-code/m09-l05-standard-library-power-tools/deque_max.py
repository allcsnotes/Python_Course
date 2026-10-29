from collections import deque

recent = deque(maxlen=3)
for number in range(1, 6):
    recent.append(f"line {number}")
    print(list(recent))
