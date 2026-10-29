import sys
from pathlib import Path


def show(folder: Path, prefix: str = "") -> None:
    items = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, p in enumerate(items):
        last = i == len(items) - 1
        print(prefix + ("└── " if last else "├── ") + p.name + ("/" if p.is_dir() else ""))
        if p.is_dir():
            show(p, prefix + ("    " if last else "│   "))


print(sys.argv[1] + "/")
show(Path(sys.argv[1]))
