from pathlib import Path

folder = Path("data")
folder.mkdir(exist_ok=True)
path = folder / "notes.txt"
text = "Lukas joined the course"
path.write_text(text, encoding="utf-8")
print(path.exists())
print(path.read_text(encoding="utf-8"))
