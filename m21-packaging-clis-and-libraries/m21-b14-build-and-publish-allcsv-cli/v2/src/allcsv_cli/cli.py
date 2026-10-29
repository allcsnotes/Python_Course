"""The allcsv command."""

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Annotated

import httpx
import typer

from allcsv_cli import __version__, api, data, logs, show

app = typer.Typer(help="Look at allcsvideos data.")
courses = typer.Typer(help="Courses.", no_args_is_help=True)
enrollments = typer.Typer(help="Enrollments.")
log_app = typer.Typer(help="Log files.")
app.add_typer(courses, name="courses")
app.add_typer(enrollments, name="enrollments")
app.add_typer(log_app, name="logs")

JsonFlag = Annotated[bool, typer.Option("--json")]


def show_version(value: bool) -> None:
    if value:
        print(f"allcsv {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", callback=show_version),
    ] = False,
) -> None:
    """Look at allcsvideos data."""


@courses.command("list")
def list_courses(
    file: Path = Path("courses.csv"),
    api_url: Annotated[
        str | None, typer.Option("--api")
    ] = None,
    level: str | None = None,
    as_json: JsonFlag = False,
) -> None:
    """List courses, from a file or from the API."""
    try:
        if api_url:
            found = api.fetch_courses(api_url)
        else:
            found = data.read_courses(file)
    except FileNotFoundError:
        show.console.print(f"[red]No such file:[/red] {file}")
        raise typer.Exit(1)
    except httpx.HTTPError as error:
        show.console.print(f"[red]API problem:[/red] {error}")
        raise typer.Exit(1)
    if level:
        found = [c for c in found if c.level == level]
    if as_json:
        show.as_json(found)
        return
    rows = [(c.id, c.title, c.level, c.price) for c in found]
    show.as_table(
        "Courses", ["Id", "Title", "Level", "Rs"], rows
    )


@enrollments.command("report")
def report(
    from_: Annotated[
        datetime,
        typer.Option("--from", formats=["%Y-%m-%d"]),
    ],
    file: Path = Path("enrollments.csv"),
    as_json: JsonFlag = False,
) -> None:
    """Count enrollments per course since a day."""
    rows = data.read_enrollments(file)
    since = [e for e in rows if e.day >= from_.date()]
    counts = Counter(e.course_id for e in since)
    if as_json:
        show.as_json(
            [
                {"course_id": c, "enrollments": n}
                for c, n in counts.most_common()
            ]
        )
        return
    show.as_table(
        "Enrollments",
        ["Course", "Enrollments"],
        counts.most_common(),
    )


@log_app.command("analyse")
def analyse(
    file: Path,
    only: Annotated[str | None, typer.Option("--only")] = None,
) -> None:
    """Count the lines of each level in a log file."""
    if only:
        for line in logs.lines_of_level(file, only.upper()):
            print(line)
        return
    for level, n in logs.count_levels(file).most_common():
        print(f"{level:8} {n}")
