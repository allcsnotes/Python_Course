from pathlib import Path

import typer

from logtools import Level, analyse


def main(logfile: Path, level: Level = Level.ERROR, top: int = 3):
    """Analyse a server log."""
    with logfile.open(encoding="utf-8") as f:
        result = analyse(f, level.value)
    count = result["levels"][level.value]
    print(f"{logfile}: {count} lines with level {level.value}")
    for message, number in result["kinds"].most_common(top):
        print(f"{number:>5}  {message}")


typer.run(main)
