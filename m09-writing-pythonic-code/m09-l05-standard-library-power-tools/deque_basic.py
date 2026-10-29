from collections import deque

line = deque(["Lukas", "Priya"])
line.append("Asha")
line.appendleft("Meera")
print(line)
print(line.popleft())
print(line)
