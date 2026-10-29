names = ["Lukas", "Priya", "Asha"]
pts = [82, 95, 82]
for i, (n, p) in enumerate(zip(names, pts), start=1):
    print(i, n, p)
print(names[::-1])
print(names[:2], names[-1])
print("level" == "level"[::-1])
