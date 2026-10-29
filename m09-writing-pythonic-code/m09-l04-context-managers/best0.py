from pathlib import Path

best = 0
try:
    best = int(Path("best.txt").read_text())
except FileNotFoundError:
    pass
print("best so far:", best)
