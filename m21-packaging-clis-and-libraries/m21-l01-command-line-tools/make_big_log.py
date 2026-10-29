# Builds big.log (450,000 lines, about 24 MB) by repeating server.log 75 times.
# Used for the progress-bar step. Run: python make_big_log.py
from pathlib import Path

lines = Path("server.log").read_text(encoding="utf-8")
Path("big.log").write_text(lines * 75, encoding="utf-8")
print("big.log written")
