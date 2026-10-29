from pathlib import Path

odd = Path("odd.log")
odd.write_bytes(b"2026-03-12 10:00:00 INFO caf\xe9 order\n")
with odd.open(encoding="utf-8", errors="replace") as f:
    print(f.readline().rstrip())
