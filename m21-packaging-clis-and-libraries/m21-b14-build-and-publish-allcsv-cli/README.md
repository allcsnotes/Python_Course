# M21-B14 · Build and Publish allcsv-cli

> Video: Module 21, Build 14. Watch it first, then follow along here.

Asha builds the whole `allcsv` tool from an empty folder: a real command, like `git` or `ls`. She plans it, builds it in layers, tests it, packages it, publishes it to a package index on her laptop, installs it like any other tool, and ships a second version.

## What you'll build

- A command-line tool with three jobs: `allcsv courses list`, `allcsv enrollments report --from 2026-09-01` and `allcsv logs analyse server.log`
- Every answer is a table for people, or JSON (`--json`) for other programs; every mistake is one clear line and an exit code, never a traceback
- Built in layers (data, logs, API, show, cli) with Typer, rich and httpx, in a src layout, with tests (`CliRunner`) and ruff
- A wheel and an sdist, published for real to a local index (pypiserver in Docker), installed with `uv tool install`, then upgraded from 0.1.0 to 0.2.0
- A release workflow, shown as text

## Before you start

- Python 3.14 or newer (`python --version`) and `uv` (`uv --version`).
- Docker running (for the local index, image `pypiserver/pypiserver:v2.4.2`).
- Module 21, lessons 1 and 2 (Typer; packages and publishing) and Module 7 (uv projects) are the background. No earlier folder is needed: everything is in this folder.
- Nothing goes to the public PyPI or TestPyPI, and no real token is used.

## Files in this folder

| File | What it is |
|------|------------|
| `v1/` | The whole project as it is when version 0.1.0 is published (with `uv.lock`) |
| `v2/` | The project at the end of the video: version 0.2.0, with `logs analyse --only` (final result) |
| `v1/pyproject.toml` | The label: name, version, MIT licence, dependencies as ranges, the `allcsv` script, `uv_build`, dev group, ruff setting |
| `v1/src/allcsv_cli/__init__.py` | Reads the version back from the installed package |
| `v1/src/allcsv_cli/data.py` | Data layer: `Course`, `Enrollment`, and the CSV readers |
| `v1/src/allcsv_cli/logs.py` | Log layer: counts the levels (0.2.0 adds `lines_of_level`) |
| `v1/src/allcsv_cli/api.py` | API layer: `fetch_courses` with httpx |
| `v1/src/allcsv_cli/show.py` | Output layer: `as_json`, `as_table` |
| `v1/src/allcsv_cli/cli.py` | The only file that knows Typer: connects the typed words to the jobs |
| `v1/tests/test_cli.py` | Six tests (seven in `v2/`) |
| `v1/sample/` | `courses.csv` (5 courses), `enrollments.csv` (10 enrollments), `server.log` (10 lines) |
| `v1/README.md`, `LICENSE`, `CHANGELOG.md` | The front page on the index, the MIT licence, the changelog |
| `v1/.github/workflows/release.yml` | The release workflow (text only, not run) |
| `tools/fake_api.py` | A tiny stand-in for the allcsvideos API on one port (`GET /courses`) |
| `tools/htpasswd`, `tools/demo-login.env` | The login of the local index: user `asha`, with a DEMO password. Not a real account |

`v1/` and `v2/` differ only in: `cli.py` (the `--only` option), `logs.py` (`lines_of_level`), `tests/test_cli.py` (one more test), `CHANGELOG.md` (one more entry) and `pyproject.toml` (version `0.2.0`).

## Run it

To try the finished tool without building it (version 0.2.0):

```bash
cd v2
uv sync --locked
cd sample
uv run allcsv --help
uv run allcsv courses list
uv run allcsv enrollments report --from 2026-09-01
uv run allcsv logs analyse server.log --only ERROR
```

The commands read `courses.csv`, `enrollments.csv` and `server.log` from the folder you run them in, so `cd sample` first. The sections below build the same thing step by step.

## Build it step by step

### 1. Plan: four rules for the tool

1. It reads the files we already have, and it can ask the server.
2. Every answer is a table for people, or JSON for other programs.
3. A mistake gives one clear line and an exit code, never a traceback.
4. One command installs it, and one command updates it.

The folder is the src layout from lesson 2: the code sits in `src/allcsv_cli`, the tests next to it, with the README, the licence and the changelog. Inside the package every file has one job. Only `cli.py` knows about Typer, so tests can call the other files directly.

The road for today: write the code and test it, build the package, publish it, install it, and ship a second version.

### 2. The project

Make the folder and add the packages. (`--author-from none` keeps your own name and email out of the file; `--vcs none` skips the git setup.)

```bash
uv init --package --vcs none --author-from none allcsv-cli
cd allcsv-cli
find . -type f
uv add typer rich httpx
uv add --dev pytest ruff
```

```
Initialized project `allcsv-cli` at `/.../allcsv-cli`
./.python-version
./README.md
./pyproject.toml
./src/allcsv_cli/__init__.py
```

`uv add` writes the three packages into `dependencies` and installs 15 packages (Typer, rich, httpx and their helpers); the second command adds a `dev` group with pytest and ruff, which stay out of the package. (Version numbers move on: the video had pytest 9.1.1, and today `uv add` may pick a newer one. Our `v1/uv.lock` pins 9.1.1.)

We read every line of `pyproject.toml` in lesson 2, so only the choices are new. Replace the generated file with `v1/pyproject.toml`:

```toml
[project]
name = "allcsv-cli"
version = "0.1.0"
description = "Look at allcsvideos courses, enrollments and logs."
readme = "README.md"
license = "MIT"
license-files = ["LICENSE"]
authors = [{ name = "Asha", email = "asha@example.com" }]
requires-python = ">=3.14"
dependencies = [
    "httpx>=0.28.1",
    "rich>=15.0.0",
    "typer>=0.27.3",
]

[project.scripts]
allcsv = "allcsv_cli.cli:app"

[build-system]
requires = ["uv_build>=0.13.6,<0.14.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "pytest>=9.1.1",
    "ruff>=0.17.3",
]

[tool.ruff]
line-length = 64
```

The choices: the name `allcsv-cli`, the MIT licence in its own file (`LICENSE`), a minimum version for each dependency, the scripts table that gives the command its name (`allcsv` = the object `app` in the module `allcsv_cli.cli`), `uv_build` as the build system, and the `dev` group. The author email is a demo value (`example.com` is reserved for examples).

### 3. The data layer: `data.py`

A course and an enrollment are small frozen data classes (Module 8): nobody can change one by mistake. The day is a real date, not text. A CSV file holds only text, so the id and the price become numbers once, at the door. After this point every other file gets real types.

```python
"""Read allcsvideos data from CSV files."""

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Course:
    id: int
    title: str
    level: str
    price: int


@dataclass(frozen=True)
class Enrollment:
    student: str
    course_id: int
    day: date


def read_courses(path: Path) -> list[Course]:
    with path.open(newline="") as f:
        return [
            Course(
                int(r["id"]),
                r["title"],
                r["level"],
                int(r["price"]),
            )
            for r in csv.DictReader(f)
        ]


def read_enrollments(path: Path) -> list[Enrollment]:
    with path.open(newline="") as f:
        return [
            Enrollment(
                r["student"],
                int(r["course_id"]),
                date.fromisoformat(r["day"]),
            )
            for r in csv.DictReader(f)
        ]
```

### 4. Logs: `logs.py`

The promise from Module 6, now one small function. For each line, split into four parts (date, time, level, message). The third part is the level, and a `Counter` (Module 9) counts them. A line with fewer than four parts is skipped, so a broken line cannot crash the count.

```python
"""Count the levels in a server log."""

from collections import Counter
from pathlib import Path


def count_levels(path: Path) -> Counter[str]:
    levels: Counter[str] = Counter()
    for line in path.read_text().splitlines():
        parts = line.split(maxsplit=3)
        if len(parts) == 4:
            levels[parts[2]] += 1
    return levels
```

### 5. The server: `api.py`

`fetch_courses` asks the API for `/courses` with httpx (Module 7, lesson 4). `raise_for_status` turns a 400 or 500 answer into an error. The JSON answer becomes the same `Course` objects as the file, so the rest of the program does not care where a course came from. The client is a parameter, so a test can hand in a fake one.

```python
"""Ask the allcsvideos API for courses."""

import httpx

from allcsv_cli.data import Course


def fetch_courses(
    url: str, client: httpx.Client | None = None
) -> list[Course]:
    client = client or httpx.Client(timeout=5)
    response = client.get(f"{url}/courses")
    response.raise_for_status()
    return [Course(**item) for item in response.json()]
```

### 6. Show: `show.py`

Two small functions. `as_json` turns data classes into dictionaries with `asdict` and prints them. `as_table` builds a rich table: the columns first, then one row per item. All output is in one file, so every command can offer both, and the look can change in one place.

```python
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
```

### 7. The version: `__init__.py`

The version lives in one place only, `pyproject.toml`. This file asks the installed package, so `allcsv --version` always tells the truth.

```python
"""allcsv: look at allcsvideos data from the command line."""

from importlib.metadata import version

__version__ = version("allcsv-cli")
```

### 8. The cli: `cli.py`

One Typer app for the whole tool, and one small app for each group of jobs: courses, enrollments, logs. `add_typer` attaches each group under its name, and that name is the sub-command (lesson 1). The `--json` flag is defined once (`JsonFlag`), so every command can use it. `show_version` prints the version and exits.

`courses list`: the parameters become options. `file` has a default, `level` filters the courses, `--api` asks the server instead of reading a file, and the last parameter is the JSON flag. A missing file prints one red line and exits with code 1, no traceback; a server that cannot be reached does the same.

`enrollments report`: the option is called `--from`, but `from` is a Python keyword, so the parameter is named `from_` and Typer is told the real option name. The day is typed as a `datetime` with the format `%Y-%m-%d`, and arrives as a date object. The report keeps the enrollments on or after that day and counts them per course with a `Counter`, most popular first.

`logs analyse`: for each level, it prints how many lines it has.

```python
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
def analyse(file: Path) -> None:
    """Count the lines of each level in a log file."""
    for level, n in logs.count_levels(file).most_common():
        print(f"{level:8} {n}")
```

That is the whole tool: six small files.

### 9. Run it, from the sample data

Install everything, then run from the folder with the sample data. (If you copy `v1/` to work on it: `cp -R v1 allcsv-work && cd allcsv-work && uv sync`.)

```bash
cd v1
uv sync --locked
cd sample
uv run allcsv --help
uv run allcsv courses list
```

```
                                                                
 Usage: allcsv [OPTIONS] COMMAND [ARGS]...                      
                                                                
 Look at allcsvideos data.                                      
                                                                
╭─ Options ────────────────────────────────────────────────────╮
│ --version                                                    │
│ --install-completion          Install completion for the     │
│                               current shell.                 │
│ --show-completion             Show completion for the        │
│                               current shell, to copy it or   │
│                               customize the installation.    │
│ --help                        Show this message and exit.    │
╰──────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────╮
│ courses      Courses.                                        │
│ enrollments  Enrollments.                                    │
│ logs         Log files.                                      │
╰──────────────────────────────────────────────────────────────╯
```

```
                       Courses                       
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━┓
┃ Id ┃ Title                  ┃ Level        ┃ Rs   ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━┩
│ 1  │ Python for Beginners   │ beginner     │ 999  │
│ 2  │ FastAPI in a Weekend   │ intermediate │ 1499 │
│ 3  │ SQL and Postgres       │ beginner     │ 1299 │
│ 4  │ Docker for Python Apps │ intermediate │ 1799 │
│ 5  │ Async Python           │ advanced     │ 1999 │
└────┴────────────────────────┴──────────────┴──────┘
```

(The box widths follow your terminal; the video used 64 columns.) The help page is made by Typer from our code. The data comes from `courses.csv`, the default.

The same data for another program, only the beginner level, as JSON:

```bash
uv run allcsv courses list --level beginner --json
```

```
[
  {
    "id": 1,
    "title": "Python for Beginners",
    "level": "beginner",
    "price": 999
  },
  {
    "id": 3,
    "title": "SQL and Postgres",
    "level": "beginner",
    "price": 1299
  }
]
```

Now the report. The enrollments file has ten enrollments, from the end of August to 10 September. Ask for the ones from 1 September. Guess first: which course has the most?

```bash
uv run allcsv enrollments report --from 2026-09-01
```

```
      Enrollments       
┏━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Course ┃ Enrollments ┃
┡━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1      │ 3           │
│ 3      │ 2           │
│ 4      │ 1           │
│ 2      │ 1           │
│ 5      │ 1           │
└────────┴─────────────┘
```

Course 1 (Python for Beginners) has three, course 3 has two, and courses 2, 4 and 5 have one each. The enrollment from August is not counted. The log command, on a sample log of ten lines, and the version:

```bash
uv run allcsv logs analyse server.log
uv run allcsv --version
```

```
INFO     6
WARNING  2
ERROR    2
allcsv 0.1.0
```

### 10. The mistakes

A typo in an option: Typer says "no such option" and lists the possible ones; exit code 2. A missing required option: also code 2. A file that does not exist: our own red line and exit code 1. Never a traceback.

```bash
uv run allcsv courses list --lvel beginner; echo "exit code $?"
uv run allcsv enrollments report; echo "exit code $?"
uv run allcsv courses list --file nope.csv; echo "exit code $?"
```

```
Usage: allcsv courses list [OPTIONS]
Try 'allcsv courses list --help' for help.
╭─ Error ──────────────────────────────────────────────────────╮
│ No such option: --lvel (Possible options: --file, --help,    │
│ --level)                                                     │
╰──────────────────────────────────────────────────────────────╯
exit code 2
Usage: allcsv enrollments report [OPTIONS]
Try 'allcsv enrollments report --help' for help.
╭─ Error ──────────────────────────────────────────────────────╮
│ Missing option '--from'.                                     │
╰──────────────────────────────────────────────────────────────╯
exit code 2
No such file: nope.csv
exit code 1
```

### 11. The server (a stand-in)

`tools/fake_api.py` is a tiny stand-in for the allcsvideos API, serving the same courses on one port. In a second terminal, from `v1/sample`:

```bash
python ../../tools/fake_api.py 8724 courses.csv
```

Back in the first terminal, ask it with `--api`, for the advanced level. Then stop the stand-in (Ctrl+C in the second terminal) and run again:

```bash
uv run allcsv courses list --api http://127.0.0.1:8724 --level advanced
```

```
                Courses                
┏━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ Id ┃ Title        ┃ Level    ┃ Rs   ┃
┡━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 5  │ Async Python │ advanced │ 1999 │
└────┴──────────────┴──────────┴──────┘
```

```bash
uv run allcsv courses list --api http://127.0.0.1:8724; echo "exit code $?"
```

```
API problem: [Errno 61] Connection refused
exit code 1
```

(The error text after "API problem:" is your system's wording: on Linux it says `[Errno 111] Connection refused`.)

### 12. Tests and ruff

A tool you cannot test is a tool you are afraid to change (lesson 1). Open `tests/test_cli.py`. A small fixture writes a tiny courses file into `tmp_path` (Module 13). The first test asks for the version: exit code 0 and the printed text equals `allcsv` plus the version of the installed package. The next is a mistake: a missing file gives exit code 1 and the message says "No such file". Exit codes are part of the promise of a tool, so they get a test. The test for the server uses `httpx.MockTransport`: a function that plays the server, checks that the path is `/courses`, and answers with one course. Fake server, real code, and no internet.

```bash
cd ..
uv run pytest
uv run ruff check
uv run ruff format --check
```

```
===================== test session starts ======================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: /.../v1
configfile: pyproject.toml
plugins: anyio-4.15.1
collected 6 items

tests/test_cli.py ......                                 [100%]

====================== 6 passed in 0.23s =======================
All checks passed!
9 files already formatted
```

(`uv run pytest -v` lists the six test names: `test_version`, `test_level_filter_as_json`, `test_missing_file_exits_with_1`, `test_report_counts_since_a_day`, `test_logs_analyse_counts_levels`, `test_api_courses_with_a_fake_server`.) Both tools live in the dev group, with one setting in `pyproject.toml`: lines of at most 64 characters (`[tool.ruff] line-length = 64`). The platform line, paths and times are yours.

### 13. Package it: README, changelog, build

The README is the front page on the index: what the tool does, how to install it, and the licence. The changelog gets its first entry, 0.1.0. Both are in `v1/`. Then build (the tests ran first, so a red test never becomes a package):

```bash
uv build
ls dist
```

```
Building source distribution...
Building wheel from source distribution...
Successfully built dist/allcsv_cli-0.1.0.tar.gz
Successfully built dist/allcsv_cli-0.1.0-py3-none-any.whl
allcsv_cli-0.1.0-py3-none-any.whl
allcsv_cli-0.1.0.tar.gz
```

Open the wheel, as in lesson 2:

```bash
unzip -l dist/allcsv_cli-0.1.0-py3-none-any.whl
unzip -p dist/allcsv_cli-0.1.0-py3-none-any.whl 'allcsv_cli-0.1.0.dist-info/entry_points.txt'
```

```
Archive:  dist/allcsv_cli-0.1.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  01-01-1980 00:00   allcsv_cli/
      139  01-01-1980 00:00   allcsv_cli/__init__.py
      361  01-01-1980 00:00   allcsv_cli/api.py
     2792  01-01-1980 00:00   allcsv_cli/cli.py
      946  01-01-1980 00:00   allcsv_cli/data.py
      349  01-01-1980 00:00   allcsv_cli/logs.py
      634  01-01-1980 00:00   allcsv_cli/show.py
        0  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/licenses/
     1072  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/licenses/LICENSE
        0  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/
       80  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/WHEEL
       47  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/entry_points.txt
      686  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/METADATA
      859  01-01-1980 00:00   allcsv_cli-0.1.0.dist-info/RECORD
---------                     -------
     7965                     14 files
[console_scripts]
allcsv = allcsv_cli.cli:app
```

The wheel holds the code of `allcsv_cli`, the licence and the label. No tests and no `sample` folder: only what the package needs. The entry points file says `allcsv = allcsv_cli.cli:app`: the installer will turn that line into the command.

### 14. Publish to the local index

Go back to this lesson's folder, and run pypiserver in a container of its own on port 21814. The password file holds one user, `asha`, with a demo password that only exists for this lab: logging in is needed to upload, and anyone may download.

```bash
cd ..
mkdir -p pypi-data/packages
cp tools/htpasswd pypi-data/htpasswd
docker run -d --name pyrepo-m21-pypi -p 21814:8080 \
  -v "$PWD/pypi-data:/data" pypiserver/pypiserver:v2.4.2 \
  run -P /data/htpasswd -a update /data/packages
docker ps --filter name=pyrepo-m21-pypi --format 'table {{.Names}}\t{{.Ports}}'
```

```
NAMES             PORTS
pyrepo-m21-pypi   0.0.0.0:21814->8080/tcp, [::]:21814->8080/tcp
```

(The long container id printed by `docker run` is yours.) Now the upload: the address of our index and the two files in `dist`. The user name and password come from environment variables, so they are not on the screen and not in the project:

```bash
source tools/demo-login.env
cd v1
uv publish --publish-url http://localhost:21814/ dist/*
curl -s http://localhost:21814/simple/allcsv-cli/ | grep "<a "
```

```
Publishing 2 files to http://localhost:21814/
Hashing allcsv_cli-0.1.0-py3-none-any.whl (5.6KiB)
Uploading allcsv_cli-0.1.0-py3-none-any.whl (5.6KiB)
Hashing allcsv_cli-0.1.0.tar.gz (3.9KiB)
Uploading allcsv_cli-0.1.0.tar.gz (3.9KiB)
            <a href="/packages/allcsv_cli-0.1.0-py3-none-any.whl#sha256=d8dd65...">allcsv_cli-0.1.0-py3-none-any.whl</a><br>
            <a href="/packages/allcsv_cli-0.1.0.tar.gz#sha256=e9da5f...">allcsv_cli-0.1.0.tar.gz</a><br>
```

Two files go up, and the index lists them, each with its fingerprint (cut short here). Uploading the same version again is refused with `409 Conflict`, as in lesson 2.

### 15. Install it like any other tool

Everything `uv` does here stays inside a scratch folder, so nothing lands in your real `~/.local`:

```bash
export UV_TOOL_DIR="$PWD/../tool-env"
export UV_TOOL_BIN_DIR="$PWD/../tool-bin"
uv tool install allcsv-cli --index http://localhost:21814/simple/
```

```
Resolved 15 packages in 1.03s
Downloading pygments (1.2MiB)
 Downloaded pygments
Prepared 15 packages in 628ms
Installed 15 packages in 15ms
 + allcsv-cli==0.1.0
 + annotated-doc==0.0.5
 + anyio==4.15.1
 + certifi==2026.10.23
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + idna==3.20
 + markdown-it-py==4.2.0
 + mdurl==0.1.2
 + pygments==2.21.0
 + rich==15.0.0
 + shellingham==1.5.4
 + typer==0.27.3
 + typing-extensions==4.16.0
Installed 1 executable: allcsv
warning: `/.../tool-bin` is not on your PATH. To use installed tools, run `export PATH="/.../tool-bin:$PATH"` or `uv tool update-shell`.
```

A tool gets its own private environment, so its libraries never touch yours. Our package came from our index, and the 14 helpers it needs from the public PyPI (reading from it is harmless). At the end: one executable, `allcsv`, and a warning: the folder with the commands is not on the PATH.

Now a fresh shell with only the basic PATH. Type `allcsv`: the shell says "command not found". The shell looks only in the folders of the PATH. The fix is the line `uv` printed: put the tools folder in front of the PATH. (Here `env -i` starts a clean shell for the test; in your own terminal you just run the `export PATH=...` line.)

```bash
env -i PATH=/usr/bin:/bin /bin/bash -c 'allcsv --version; echo "exit code $?"'
env -i PATH="$UV_TOOL_BIN_DIR:/usr/bin:/bin" /bin/bash -c 'allcsv --version; which allcsv; cd sample; allcsv courses list --level advanced'
uv tool list
```

```
/bin/bash: allcsv: command not found
exit code 127
allcsv 0.1.0
/.../tool-bin/allcsv
                Courses                
┏━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ Id ┃ Title        ┃ Level    ┃ Rs   ┃
┡━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 5  │ Async Python │ advanced │ 1999 │
└────┴──────────────┴──────────┴──────┘
allcsv-cli v0.1.0
- allcsv
```

(zsh words the first message as `zsh: command not found: allcsv`. The `cd sample` is there so that `allcsv` finds `courses.csv`; run it from any folder that has that file.)

### 16. Version 0.2: a new option

Priya asks: can I see only the errors of a log? A new option on `analyse`: `--only`. When it is set, we print the lines of that level and stop; otherwise we count as before. The helper `lines_of_level` is three lines in `logs.py`. One more test, and one line in the changelog. The finished files are in `v2/`; the changes are:

```python
# logs.py (added)
def lines_of_level(path: Path, level: str) -> list[str]:
    lines = path.read_text().splitlines()
    return [x for x in lines if f" {level} " in x]
```

```python
# cli.py (the analyse command)
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
    ...
```

To follow along, copy these four files from `v2/` over `v1/`: `src/allcsv_cli/cli.py`, `src/allcsv_cli/logs.py`, `tests/test_cli.py`, `CHANGELOG.md`. Then, in `v1/`:

```bash
uv run ruff format
uv run ruff check
uv run pytest
uv version --bump minor
uv version
```

```
9 files left unchanged
All checks passed!
===================== test session starts ======================
...
collected 7 items

tests/test_cli.py .......                                [100%]

====================== 7 passed in 0.23s =======================
Resolved 21 packages in 5ms
   Building allcsv-cli @ file:///.../v1
      Built allcsv-cli @ file:///.../v1
Prepared 1 package in 4ms
Uninstalled 1 package in 0.78ms
Installed 1 package in 2ms
 - allcsv-cli==0.1.0 (from file:///.../v1)
 + allcsv-cli==0.2.0 (from file:///.../v1)
allcsv-cli 0.1.0 => 0.2.0
allcsv-cli 0.2.0
```

Seven passed. `--bump minor` writes 0.2.0 into `pyproject.toml`: a new feature, old commands still work (a minor change, lesson 2). Now the trap that surprises people. In the project, `uv run` says 0.2.0, but the `allcsv` in your shell, the installed tool, still says 0.1.0: it is a separate copy.

```bash
cd sample
uv run allcsv --version
env -i PATH="$UV_TOOL_BIN_DIR:/usr/bin:/bin" /bin/bash -c 'allcsv --version'
cd ..
```

```
allcsv 0.2.0
allcsv 0.1.0
```

### 17. Build again: old files in `dist`

```bash
uv build
ls dist
```

```
Building source distribution...
Building wheel from source distribution...
Successfully built dist/allcsv_cli-0.2.0.tar.gz
Successfully built dist/allcsv_cli-0.2.0-py3-none-any.whl
allcsv_cli-0.1.0-py3-none-any.whl
allcsv_cli-0.1.0.tar.gz
allcsv_cli-0.2.0-py3-none-any.whl
allcsv_cli-0.2.0.tar.gz
```

`dist` holds four files: the old two and the new two. Guess: what happens when you publish everything in `dist`?

```bash
uv publish --publish-url http://localhost:21814/ dist/*; echo "exit code $?"
```

```
Publishing 4 files to http://localhost:21814/
Hashing allcsv_cli-0.1.0-py3-none-any.whl (5.6KiB)
Uploading allcsv_cli-0.1.0-py3-none-any.whl (5.6KiB)
error: Failed to publish `dist/allcsv_cli-0.1.0-py3-none-any.whl`
       to `http://localhost:21814/`
  cause: Server returned status code 409 Conflict. Server says:
             ...
                     <pre>Package
         &#039;allcsv_cli-0.1.0-py3-none-any.whl&#039; already
         exists!
           You may start server with `--overwrite` option.</pre>
             ...
exit code 2
```

(The HTML page in the middle is shortened.) The index refuses: the first file is the old wheel, 0.1.0, and it is already there. Nothing is wrong with the new version; there are old files in `dist`. The exit code is 2 and nothing new went up. The fix: `uv build --clear`, which empties `dist` first.

```bash
uv build --clear
ls dist
uv publish --publish-url http://localhost:21814/ dist/*
curl -s http://localhost:21814/simple/allcsv-cli/ | grep "<a "
```

```
Building source distribution...
Building wheel from source distribution...
Successfully built dist/allcsv_cli-0.2.0.tar.gz
Successfully built dist/allcsv_cli-0.2.0-py3-none-any.whl
allcsv_cli-0.2.0-py3-none-any.whl
allcsv_cli-0.2.0.tar.gz
Publishing 2 files to http://localhost:21814/
Hashing allcsv_cli-0.2.0-py3-none-any.whl (5.7KiB)
Uploading allcsv_cli-0.2.0-py3-none-any.whl (5.7KiB)
Hashing allcsv_cli-0.2.0.tar.gz (4.0KiB)
Uploading allcsv_cli-0.2.0.tar.gz (4.0KiB)
            <a href="/packages/allcsv_cli-0.1.0-py3-none-any.whl#sha256=d8dd65...">allcsv_cli-0.1.0-py3-none-any.whl</a><br>
            <a href="/packages/allcsv_cli-0.1.0.tar.gz#sha256=e9da5f...">allcsv_cli-0.1.0.tar.gz</a><br>
            <a href="/packages/allcsv_cli-0.2.0-py3-none-any.whl#sha256=42844a...">allcsv_cli-0.2.0-py3-none-any.whl</a><br>
            <a href="/packages/allcsv_cli-0.2.0.tar.gz#sha256=6e3581...">allcsv_cli-0.2.0.tar.gz</a><br>
```

The index has all four files, the wheel and the sdist of each version. Old versions stay, so anyone can still install them.

### 18. Upgrade the installed tool

`uv tool upgrade` remembers the index the tool came from, and moves it from 0.1 to 0.2:

```bash
uv tool upgrade allcsv-cli
env -i PATH="$UV_TOOL_BIN_DIR:/usr/bin:/bin" /bin/bash -c 'cd sample; allcsv --version; allcsv logs analyse server.log --only ERROR'
uv tool list
```

```
Updated allcsv-cli v0.1.0 -> v0.2.0
 - allcsv-cli==0.1.0
 + allcsv-cli==0.2.0
Installed 1 executable: allcsv
warning: `/.../tool-bin` is not on your PATH. To use installed tools, run `export PATH="/.../tool-bin:$PATH"` or `uv tool update-shell`.
allcsv 0.2.0
2026-09-01 08:03:31 ERROR Payment failed for order 8097
2026-09-01 08:07:03 ERROR Database connection timeout
allcsv-cli v0.2.0
- allcsv
```

Now the installed command says 0.2.0, and the new option works.

### 19. The release workflow (text only)

You saw a publish job in lesson 2. Here it has a test job in front (`v1/.github/workflows/release.yml`). When a tag that starts with `v` is pushed, GitHub would run ruff and pytest first. Nothing was pushed to GitHub and no tag was made: this is shown as text.

```yaml
name: release

on:
  push:
    tags: ["v*"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv run ruff check
      - run: uv run pytest

  publish:
    needs: test
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv build
      - run: uv publish
```

The publish job says `needs: test`: if one check fails, nothing is published. It asks for a short pass with `id-token: write`, then builds and publishes with no password at all (trusted publishing, lesson 2). In real life a release is three commands: bump the version, make a tag, and push the tag.

### 20. Three traps, and an interview tip

1. The command not found, because the tools folder was not on the PATH.
2. Old files in `dist`, which made the index refuse the upload (`uv build --clear`).
3. Two copies of `allcsv`, the project and the installed tool, which can show two different versions (`uv tool upgrade`).

Rahul asks: a teammate tells you your command-line tool works on their machine, but not on mine. How do you make sure that other people can install and run it? A good answer: I never trust my own project folder. I run the tests, build the wheel and look inside it. I publish to a test index first, then install the tool from the index, into a fresh environment, and run it from a different folder. Only an installed copy shows what a user gets. Then I bump the version, and each release is a new, tested version, never an overwrite.

### 21. Your turn

Add a command `courses show` that takes a course id, with a test. Bump the patch version and publish it. Upgrade your installed tool. And write the release workflow for your own project.

## Common mistakes

- `allcsv: command not found` after `uv tool install`: the tools folder is not on your PATH. Run the `export PATH=...` line that uv printed, or `uv tool update-shell`.
- Publishing everything in `dist`: old versions are refused with `409 Conflict`. Use `uv build --clear`.
- Thinking the project and the installed tool are the same copy. `uv run allcsv` is the project; `allcsv` in your shell is the installed tool. Update it with `uv tool upgrade`.
- Calling Typer from the data, logs or API files. Only `cli.py` knows Typer, so tests can call the other files directly.
- Reading data files from a path next to the code (see lesson 2): put data inside the package, or pass the file as an option, as `--file` does here.

## Clean up

```bash
docker rm -f -v pyrepo-m21-pypi
rm -rf pypi-data tool-env tool-bin
rm -rf v1/.venv v1/dist v2/.venv v2/dist
```

(The tool environment lives in the folders `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR` pointed to. If you set them to other folders, delete those instead, and remember that `export` only lasts for the terminal session.)

## Next

[M22-L01 · Automating the Boring Stuff](../../m22-data-and-automation-with-python/m22-l01-automating-the-boring-stuff/)
