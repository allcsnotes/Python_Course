import logging
from datetime import date
from typing import Annotated

import httpx
import typer

from weekly_report import job
from weekly_report.api import ApiDown
from weekly_report.settings import Settings
from weekly_report.weeks import last_monday, week_label

app = typer.Typer(
    help="Make and send the allcsvideos weekly report.",
    add_completion=False,
)


@app.callback()
def main():
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )


@app.command()
def run(
    week: Annotated[
        str | None,
        typer.Option(
            help="Monday of the week, YYYY-MM-DD. Default: last week."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(help="Build the files, send nothing."),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(help="Send even if this week was sent."),
    ] = False,
):
    settings = Settings()
    monday = (
        date.fromisoformat(week)
        if week
        else last_monday(date.today())
    )
    with httpx.Client(
        base_url=settings.api_url, timeout=10
    ) as client:
        try:
            job.run_week(
                settings, monday, client, dry_run, force
            )
        except ApiDown as err:
            if not dry_run:
                job.alert(settings, week_label(monday), err)
            raise typer.Exit(1)
