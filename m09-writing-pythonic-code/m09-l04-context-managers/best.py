from contextlib import suppress
from pathlib import Path

best = 0
with suppress(FileNotFoundError):
    best = int(Path("best.txt").read_text())
print("best so far:", best)
