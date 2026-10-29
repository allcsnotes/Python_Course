import shutil
from pathlib import Path

import typer

KINDS = {".csv": "data", ".xlsx": "sheets", ".pdf": "documents",
         ".txt": "documents", ".jpg": "images", ".png": "images"}


def tidy(name: str) -> str:
    return name.lower().replace(" ", "-")


def unique(target: Path, taken: set[Path]) -> Path:
    new, n = target, 2
    while new in taken or new.exists():
        new = target.with_stem(f"{target.stem}-{n}")
        n += 1
    return new


def main(folder: Path, apply: bool = False):
    taken = set()
    for path in sorted(folder.glob("*")):
        if path.is_dir():
            continue
        kind = KINDS.get(path.suffix.lower(), "other")
        target = unique(folder / kind / tidy(path.name), taken)
        taken.add(target)
        print(f"{path.name} -> {kind}/{target.name}")
        if apply:
            target.parent.mkdir(exist_ok=True)
            shutil.move(path, target)


typer.run(main)
