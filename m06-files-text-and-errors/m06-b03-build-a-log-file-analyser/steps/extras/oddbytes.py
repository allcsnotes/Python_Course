from pathlib import Path

odd = Path("odd.log")
odd.write_bytes(b"2026-03-12 10:00:00 INFO caf\xe9 order\n")
print(odd.read_text(encoding="utf-8"))
