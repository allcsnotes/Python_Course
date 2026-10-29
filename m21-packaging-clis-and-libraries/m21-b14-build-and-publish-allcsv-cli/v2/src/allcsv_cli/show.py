"""Print results as a table or as JSON."""

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def as_json(rows: list[Any]) -> None:
    items = [asdict(r) if is_dataclass(r) else r for r in rows]
    print(json.dumps(items, default=str, indent=2))


def as_table(
    title: str, columns: list[str], rows: list[tuple]
) -> None:
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    console.print(table)
