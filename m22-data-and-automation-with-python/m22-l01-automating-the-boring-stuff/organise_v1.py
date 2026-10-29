from pathlib import Path

import typer

KINDS = {".csv": "data", ".xlsx": "sheets", ".pdf": "documents",
         ".txt": "documents", ".jpg": "images", ".png": "images"}


def tidy(name: str) -> str:
    return name.lower().replace(" ", "-")


def main(folder: Path):
    for path in sorted(folder.glob("*")):
        kind = KINDS.get(path.suffix.lower(), "other")
        print(f"{path.name} -> {kind}/{tidy(path.name)}")


typer.run(main)
