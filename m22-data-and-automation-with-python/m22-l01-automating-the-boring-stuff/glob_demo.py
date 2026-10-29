from pathlib import Path

folder = Path("downloads")
for path in sorted(folder.glob("*.csv")):
    print(path.name)
print(len(list(folder.glob("*"))), "files in all")
