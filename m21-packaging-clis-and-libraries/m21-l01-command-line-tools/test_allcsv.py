import json

from typer.testing import CliRunner

from allcsv import app

runner = CliRunner()

LINES = [
    "2026-03-12 10:00:00 ERROR Database connection timeout",
    "2026-03-12 10:00:05 ERROR Database connection timeout",
    "2026-03-12 10:01:00 INFO GET /courses 200 12ms",
    "this is not a log line",
]


def test_json_output(tmp_path):
    log = tmp_path / "test.log"
    log.write_text("\n".join(LINES))
    result = runner.invoke(app, ["logs", "analyse", str(log), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["matching"] == 2
    assert data["bad_lines"] == 1


def test_missing_file():
    result = runner.invoke(app, ["logs", "analyse", "nope.log"])
    assert result.exit_code == 2


def test_too_many_errors(tmp_path):
    log = tmp_path / "test.log"
    log.write_text("\n".join(LINES))
    result = runner.invoke(app, ["logs", "analyse", str(log), "--max-errors", "1"])
    assert result.exit_code == 1
