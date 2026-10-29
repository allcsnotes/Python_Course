import json

import httpx
import pytest
from typer.testing import CliRunner

from allcsv_cli import __version__
from allcsv_cli.api import fetch_courses
from allcsv_cli.cli import app

runner = CliRunner()


@pytest.fixture
def courses_csv(tmp_path):
    path = tmp_path / "courses.csv"
    path.write_text(
        "id,title,level,price\n"
        "1,Python for Beginners,beginner,999\n"
        "2,Async Python,advanced,1999\n"
    )
    return path


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() == f"allcsv {__version__}"


def test_level_filter_as_json(courses_csv):
    args = ["courses", "list", "--file", str(courses_csv)]
    result = runner.invoke(
        app, [*args, "--level", "advanced", "--json"]
    )
    assert result.exit_code == 0
    assert [c["title"] for c in json.loads(result.output)] == [
        "Async Python"
    ]


def test_missing_file_exits_with_1(tmp_path):
    args = [
        "courses",
        "list",
        "--file",
        str(tmp_path / "x.csv"),
    ]
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert "No such file" in result.output


def test_report_counts_since_a_day(tmp_path):
    path = tmp_path / "enrollments.csv"
    path.write_text(
        "student,course_id,day\n"
        "Lukas,1,2026-08-30\n"
        "Priya,1,2026-09-02\n"
        "Meera,2,2026-09-03\n"
    )
    args = ["enrollments", "report", "--from", "2026-09-01"]
    result = runner.invoke(
        app, [*args, "--file", str(path), "--json"]
    )
    assert json.loads(result.output) == [
        {"course_id": 1, "enrollments": 1},
        {"course_id": 2, "enrollments": 1},
    ]


def test_logs_analyse_counts_levels(tmp_path):
    path = tmp_path / "server.log"
    path.write_text(
        "2026-09-01 08:00:01 INFO GET /courses 200 104ms\n"
        "2026-09-01 08:03:31 ERROR Payment failed for order 8097\n"
        "2026-09-01 08:08:55 INFO Student 31 enrolled in course 1\n"
    )
    result = runner.invoke(app, ["logs", "analyse", str(path)])
    assert result.output.split() == [
        "INFO",
        "2",
        "ERROR",
        "1",
    ]


def test_api_courses_with_a_fake_server():
    def handler(request):
        assert request.url.path == "/courses"
        item = {
            "id": 1,
            "title": "Async Python",
            "level": "advanced",
            "price": 1999,
        }
        return httpx.Response(200, json=[item])

    client = httpx.Client(
        transport=httpx.MockTransport(handler)
    )
    courses = fetch_courses("http://fake", client)
    assert [c.title for c in courses] == ["Async Python"]
