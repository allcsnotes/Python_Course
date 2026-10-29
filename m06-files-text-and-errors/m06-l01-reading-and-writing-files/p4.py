from pathlib import Path

path = Path("data") / "notes.txt"
text = "Lukas joined the course"
path.write_text(text, encoding="utf-8")
