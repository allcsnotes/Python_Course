"""The allcsv command."""

import json
from importlib.resources import files
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from allcsv_cli import __version__

app = typer.Typer(help="Tools for allcsvideos.com")
courses = typer.Typer(help="Work with the course list")
app.add_typer(courses, name="courses")

console = Console()


def show_version(value: bool) -> None:
    if value:
        print(f"allcsv {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool, typer.Option("--version", callback=show_version)
    ] = False,
) -> None:
    """Tools for allcsvideos.com"""


def load_courses() -> list[dict]:
    folder = files("allcsv_cli")
    text = folder.joinpath("courses.json").read_text()
    return json.loads(text)


@courses.command("list")
def list_courses(
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Show the courses."""
    items = load_courses()
    if as_json:
        print(json.dumps(items, indent=2))
        return
    table = Table(title="Courses")
    table.add_column("Id", justify="right")
    table.add_column("Title", style="cyan")
    table.add_column("Level")
    table.add_column("Price", justify="right")
    for c in items:
        price = f"Rs {c['price']}"
        table.add_row(str(c["id"]), c["title"], c["level"], price)
    console.print(table)
