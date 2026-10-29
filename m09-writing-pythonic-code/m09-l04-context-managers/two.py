from pathlib import Path

with open("in.txt") as src, open("out.txt", "w") as dst:
    for line in src:
        dst.write(line.upper())
print(Path("out.txt").read_text().split())
