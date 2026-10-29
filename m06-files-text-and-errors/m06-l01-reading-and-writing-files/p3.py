from pathlib import Path

path = Path("data") / "notes.txt"
with open(path, "a", encoding="utf-8") as file:
    file.write("\nPriya joined the course")
print(path.read_text(encoding="utf-8"))
