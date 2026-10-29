from typer.testing import CliRunner

from allcsv_cli import __version__
from allcsv_cli.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == f"allcsv {__version__}"


def test_courses_list_json():
    result = runner.invoke(app, ["courses", "list", "--json"])
    assert result.exit_code == 0
    assert '"Python Basics"' in result.stdout
