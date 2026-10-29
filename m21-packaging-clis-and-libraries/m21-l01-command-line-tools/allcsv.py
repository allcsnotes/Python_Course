import json
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import open as progress_open
from rich.table import Table

from logtools import Level, analyse

app = typer.Typer(help="Tools for allcsvideos.com")
logs = typer.Typer(help="Work with server logs")
courses = typer.Typer(help="Work with the course list")
app.add_typer(logs, name="logs")
app.add_typer(courses, name="courses")

console = Console()
problems = Console(stderr=True)


@logs.command("analyse")
def analyse_log(
    logfile: Annotated[
        Path, typer.Argument(exists=True, allow_dash=True)
    ],
    level: Annotated[
        Level, typer.Option(help="Lines to count")
    ] = Level.ERROR,
    top: Annotated[int, typer.Option(help="How many to show")] = 3,
    as_json: Annotated[
        bool, typer.Option("--json", help="Print JSON")
    ] = False,
    max_errors: Annotated[
        int | None, typer.Option(help="Exit 1 above this")
    ] = None,
):
    """Count the lines of a server log, and show the top messages."""
    if str(logfile) == "-":
        result = analyse(sys.stdin, level.value)
    else:
        with progress_open(
            logfile, "rt", description="Reading", console=problems
        ) as f:
            result = analyse(f, level.value)
    count = result["levels"][level.value]
    top_messages = result["kinds"].most_common(top)
    if as_json:
        data = {
            "file": str(logfile),
            "level": level.value,
            "lines": result["total"],
            "matching": count,
            "bad_lines": result["bad"],
            "top": top_messages,
        }
        print(json.dumps(data))
    else:
        table = Table(
            title=f"{level.value} messages in {logfile}",
            caption=f"{count} of {result['total']} lines",
        )
        table.add_column("Count", justify="right", style="bold red")
        table.add_column("Message", style="cyan")
        for message, number in top_messages:
            table.add_row(str(number), message)
        console.print(table)
    if max_errors is not None and count > max_errors:
        problems.print(f"[bold red]Too many {level.value} lines[/]")
        raise typer.Exit(code=1)


@courses.command("list")
def list_courses(
    level: Annotated[
        str | None, typer.Option(help="beginner, intermediate...")
    ] = None,
):
    """Show the courses from courses.json."""
    items = json.loads(Path("courses.json").read_text(encoding="utf-8"))
    if level:
        items = [c for c in items if c["level"] == level]
    table = Table(title="Courses")
    table.add_column("Id", justify="right")
    table.add_column("Title", style="cyan")
    table.add_column("Level")
    table.add_column("Price", justify="right")
    for c in items:
        price = f"Rs {c['price']}"
        table.add_row(str(c["id"]), c["title"], c["level"], price)
    console.print(table)


if __name__ == "__main__":
    app()
