# M21-L01 · Command-Line Tools

> Video: Module 21, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why a program that has its file name written inside the code is a problem, and how the words typed after a program's name fix it
- Reading the command line with `sys.argv`, then with `argparse` (built into Python), then with Typer (built from type hints)
- Sub-commands, options with defaults, choices, and the `--help` page you get for free
- Colours, tables and a progress bar with `rich`
- Standard output versus standard error, pipes (`|`) and a dash that means "read standard input"
- Exit codes (0, 1, 2), and testing a command-line tool with Typer's `CliRunner`

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv`, the tool from Module 7 (`uv --version`). It installs Typer, rich and pytest for you from `uv.lock`.
- No Docker needed.
- This lesson pays off the promise of Module 6, build 3 (the log analyser): "take the log file name from the command line". The analyser code is in the `problem/` folder here, so you do not need the old folder.

## Files in this folder

| File | What it is |
|------|------------|
| `server.log` | The sample server log from Module 6: 6,000 lines (made-up traffic for allcsvideos.com) |
| `gen_yesterday.py` | Makes `yesterday.log`, the second log (2,500 lines) that Meera sends to Priya |
| `make_big_log.py` | Makes `big.log` (450,000 lines, 24 MB) for the progress bar. Created on your machine, not stored here |
| `problem/analyser.py` | The Module 6 analyser, with `server.log` written inside the code (the problem of this lesson) |
| `logtools.py` | The analysing code from Module 6, now in its own file: `Level`, `read_line`, `analyse` |
| `analyse_v1.py` | The analyser with `sys.argv` |
| `analyse_v2.py` | The analyser with `argparse` |
| `analyse_v3.py` | The analyser with Typer, one function |
| `allcsv.py` | The real tool: Typer sub-commands, rich table and progress bar, `--json`, `--max-errors` |
| `courses.json` | The five courses that `allcsv courses list` shows |
| `noisy.py`, `quiet.py` | The pipe mistake and its fix |
| `test_allcsv.py` | Three tests with `CliRunner` |
| `pyproject.toml`, `uv.lock`, `.python-version` | The uv project: Typer 0.27.3, rich 15.0.0, pytest 9.1.1 (dev) |

## Follow along

Run every command from this folder, unless a step says otherwise. Set up the project once:

```bash
uv sync
```

This creates a `.venv` here and installs the pinned versions from `uv.lock`. (The video ran `uv add typer` and `uv add rich`; `uv sync` gives you the same result.)

### 1. The problem: the file name is inside the code

Priya has a second log, `yesterday.log`. Make it, and try the old analyser on it:

```bash
python gen_yesterday.py
cd problem
cp ../server.log ../yesterday.log .
wc -l server.log yesterday.log
python analyser.py yesterday.log
cd ..
```

```
    6000 server.log
    2500 yesterday.log
    8500 total
Read 6000 lines.
Skipped 6 bad lines.
Reports are in the report folder.
```

It read 6,000 lines: `server.log`. The words `yesterday.log` were never looked at, because the name is written on line 8 of `analyser.py`. You can delete the `problem/report` folder it made.

### 2. `sys.argv`: the list of typed words

`analyse_v1.py` reads element 1 of `sys.argv` (element 0 is the program's own name):

```python
path = Path(sys.argv[1])
```

```bash
uv run analyse_v1.py server.log
uv run analyse_v1.py
```

```
server.log: 204 errors in 6000 lines
Traceback (most recent call last):
  File ".../analyse_v1.py", line 6, in <module>
    path = Path(sys.argv[1])
                ~~~~~~~~^^^
IndexError: list index out of range
```

The promise is kept: any file works. But a forgotten file name gives a traceback, and `sys.argv` knows nothing about options, defaults, choices or a help page. (The path in the traceback is yours.)

### 3. `argparse`: describe the words, let Python read them

Open `analyse_v2.py`. A word without dashes (`logfile`) is a positional argument. A name that starts with two dashes (`--level`, `--top`) is an option. `choices` lists the allowed words, `default` says what to use when nobody types it.

```bash
uv run analyse_v2.py --help
```

```
usage: analyse_v2.py [-h] [--level {INFO,WARNING,ERROR}] [--top TOP]
                     logfile

Analyse a server log.

positional arguments:
  logfile               the log file to read

options:
  -h, --help            show this help message and exit
  --level {INFO,WARNING,ERROR}
  --top TOP             how many
```

(The line breaks follow your terminal width.) A real run, then the two mistakes, then the exit code:

```bash
uv run analyse_v2.py server.log --level WARNING --top 2
uv run analyse_v2.py server.log --level LOUD
uv run analyse_v2.py server.log --top many
echo $?
```

```
server.log: 479 lines with level WARNING
  244  Video # is buffering
  235  Slow query on lessons table (#ms)
usage: analyse_v2.py [-h] [--level {INFO,WARNING,ERROR}] [--top TOP]
                     logfile
analyse_v2.py: error: argument --level: invalid choice: 'LOUD' (choose from 'INFO', 'WARNING', 'ERROR')
usage: analyse_v2.py [-h] [--level {INFO,WARNING,ERROR}] [--top TOP]
                     logfile
analyse_v2.py: error: argument --top: invalid int value: 'many'
2
```

One clear line each, no traceback. `echo $?` shows the exit code of the last command: 2 means "the command line was wrong".

### 4. Typer: the command line from type hints

Typer is a library by the author of FastAPI. It reads the type hints of an ordinary function (Module 10). Open `analyse_v3.py`: the whole tool is one function and the last line, `typer.run(main)`.

Two rules: a parameter without a default is a positional argument; one with a default is an option named after the parameter (`top` becomes `--top`). The `Level` enum (Module 8) becomes the list of choices, and the docstring becomes the description.

```bash
uv run analyse_v3.py --help
uv run analyse_v3.py server.log --top 2
```

```
 Usage: analyse_v3.py [OPTIONS] {logfile}

 Analyse a server log.

╭─ Arguments ────────────────────────────────────────────────────────╮
│ *    logfile      <path>  [required]                               │
╰────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────╮
│ --level        <INFO|WARNING|ERROR>  [default: ERROR]              │
│ --top          <int>                 [default: 3]                  │
│ --help                               Show this message and exit.   │
╰────────────────────────────────────────────────────────────────────╯
server.log: 204 lines with level ERROR
   57  Video # file not found
   50  Database connection timeout
```

Typer helps when you mistype, and checks the enum:

```bash
uv run analyse_v3.py server.log --tpo 2
uv run analyse_v3.py server.log --level LOUD
```

```
Usage: analyse_v3.py [OPTIONS] {logfile}
Try 'analyse_v3.py --help' for help.
╭─ Error ────────────────────────────────────────────────────────────╮
│ No such option: --tpo (Possible options: --top)                    │
╰────────────────────────────────────────────────────────────────────╯
Usage: analyse_v3.py [OPTIONS] {logfile}
Try 'analyse_v3.py --help' for help.
╭─ Error ────────────────────────────────────────────────────────────╮
│ Invalid value for '--level': 'LOUD' is not one of 'INFO',          │
│ 'WARNING', 'ERROR'.                                                │
╰────────────────────────────────────────────────────────────────────╯
```

Both exit with code 2.

One more mistake, a file that does not exist:

```bash
uv run analyse_v3.py nope.log
echo $?
```

```
╭──────────────── Traceback (most recent call last) ─────────────────╮
│ .../analyse_v3.py:10 in main                                       │
│ ...                                                                │
╰────────────────────────────────────────────────────────────────────╯
FileNotFoundError: [Errno 2] No such file or directory: 'nope.log'
1
```

The hint `Path` only converts the text; nothing checks that the file exists. Our own code fails with a traceback and exit code 1, which means "our program crashed". Not what we want for a typing mistake. The next step fixes it.

### 5. The real tool: `allcsv.py` with sub-commands

Open `allcsv.py`. Line 13 makes the main app, lines 14 and 15 make one small app per group of jobs, and `app.add_typer(logs, name="logs")` attaches a group under a name: that name is the sub-command. `@logs.command("analyse")` is a decorator (Module 9) that registers the function as the command `analyse` in the group `logs`. `Annotated` joins a type with extra settings: a help text, the option name, and `exists=True` for the file, so Typer checks the file before your code runs.

```bash
uv run allcsv.py --help
uv run allcsv.py logs analyse --help
uv run allcsv.py logs analyse nope.log
echo $?
```

```
 Usage: allcsv.py [OPTIONS] COMMAND [ARGS]...

 Tools for allcsvideos.com

╭─ Options ──────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current   │
│                               shell.                               │
│ --show-completion             Show completion for the current      │
│                               shell, to copy it or customize the   │
│                               installation.                        │
│ --help                        Show this message and exit.          │
╰────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────╮
│ logs     Work with server logs                                     │
│ courses  Work with the course list                                 │
╰────────────────────────────────────────────────────────────────────╯
```

```
 Usage: allcsv.py logs analyse [OPTIONS] {logfile}

 Count the lines of a server log, and show the top messages.

╭─ Arguments ────────────────────────────────────────────────────────╮
│ *    logfile      <path>  [required]                               │
╰────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────╮
│ --level             <INFO|WARNING|ERROR>  Lines to count           │
│                                           [default: ERROR]         │
│ --top               <int>                 How many to show         │
│                                           [default: 3]             │
│ --json                                    Print JSON               │
│ --max-errors        <int>                 Exit 1 above this        │
│ --help                                    Show this message and    │
│                                           exit.                    │
╰────────────────────────────────────────────────────────────────────╯
```

```
Usage: allcsv.py logs analyse [OPTIONS] {logfile}
Try 'allcsv.py logs analyse --help' for help.
╭─ Error ────────────────────────────────────────────────────────────╮
│ Invalid value for 'logfile': Path 'nope.log' does not exist.       │
╰────────────────────────────────────────────────────────────────────╯
2
```

No traceback, and exit code 2. (The box widths follow your terminal; the video used a narrower one.)

### 6. Colours and a table with rich

`uv run allcsv.py courses list` draws a table with rich (Module 7, lesson 3). The count column is bold red and the message column cyan on a real screen. Here you see plain text, because rich leaves the colours out when output does not go to a screen.

```bash
uv run allcsv.py courses list
uv run allcsv.py logs analyse server.log
```

```
                        Courses
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Id ┃ Title                  ┃ Level        ┃   Price ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━┩
│  1 │ Python Basics          │ beginner     │  Rs 499 │
│  2 │ Object-Oriented Python │ intermediate │  Rs 899 │
│  3 │ FastAPI in Practice    │ intermediate │ Rs 1499 │
│  4 │ Async Python           │ advanced     │ Rs 1299 │
│  5 │ Docker for Python Apps │ intermediate │  Rs 999 │
└────┴────────────────────────┴──────────────┴─────────┘
Reading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 321.6/321.6 kB 0:00:00
     ERROR messages in server.log
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Count ┃ Message                     ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│    57 │ Video # file not found      │
│    50 │ Database connection timeout │
│    50 │ Upload failed for lesson #  │
└───────┴─────────────────────────────┘
           204 of 6000 lines
```

`courses list` reads `courses.json` from the folder you run it in.

### 7. A progress bar on a long run

`server.log` is small. Make the big one (450,000 lines, 24 MB) and analyse it. In `allcsv.py`, `progress_open(...)` from rich takes the place of `open` and draws a bar while the file is read:

```bash
python make_big_log.py
uv run allcsv.py logs analyse big.log
```

```
Reading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 24.1/24.1 MB 0:00:00
       ERROR messages in big.log
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Count ┃ Message                     ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  4275 │ Video # file not found      │
│  3750 │ Database connection timeout │
│  3750 │ Upload failed for lesson #  │
└───────┴─────────────────────────────┘
         15300 of 450000 lines
```

On a screen you watch the bar fill, the megabytes grow and the time left shrink (about 3.5 seconds in the video; yours will differ). Only the last frame is left when the output is captured, as above.

### 8. Three streams, and pipes

A program has three streams: standard input (what flows in), standard output (the answer), and standard error (messages about the run, like the progress bar). On a screen they look the same, but they are different pipes. The `|` connects the output of one program to the input of the next.

The bar in `allcsv.py` is drawn by a console made with `Console(stderr=True)`, so it does not disturb the answer. Use `--json`, which prints one line of JSON for other programs:

```bash
uv run allcsv.py logs analyse server.log --json | python -m json.tool
```

```
Reading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 321.6/321.6 kB 0:00:00
{
    "file": "server.log",
    "level": "ERROR",
    "lines": 6000,
    "matching": 204,
    "bad_lines": 6,
    "top": [
        [
            "Video # file not found",
            57
        ],
        ...
    ]
}
```

(`...` shortens the list here. You see the bar on your screen because it goes to standard error; `json.tool` receives only the JSON.)

A dash in place of the file name means "read standard input". `tail -n 1000` prints the last 1,000 lines of the log:

```bash
tail -n 1000 server.log | uv run allcsv.py logs analyse - --top 1
```

```
       ERROR messages in -
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Count ┃ Message                ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│     6 │ Video # file not found │
└───────┴────────────────────────┘
         20 of 1000 lines
```

The tool does not care whether its lines come from a file or from another program.

### 9. The classic mistake: a friendly `print` before the JSON

`noisy.py` prints a friendly message with a plain `print`, then the JSON. `quiet.py` sends the message to standard error:

```python
print("Reading server.log ...", file=sys.stderr)
```

```bash
uv run noisy.py | python -m json.tool
uv run quiet.py | python -m json.tool
```

```
Expecting value: line 1 column 1 (char 0)
Reading server.log ...
{
    "errors": 204
}
```

With `noisy.py` the first character the helper received was the letter `R` of "Reading", not a bracket. With `quiet.py` the screen shows both lines, but the pipe carries only the JSON.

### 10. Exit codes

Every program ends with a number: 0 means all is well, anything else means a problem. A build server (Module 19, lesson 3) stops when a step returns anything but 0. So far Typer gave us 2 for a wrong command line. In `allcsv.py`, the option `--max-errors` adds our own: if there is a limit and the count is above it, we print a message on standard error and `raise typer.Exit(code=1)`.

`server.log` has 204 errors. Try a limit of 300, then a limit of 100:

```bash
uv run allcsv.py logs analyse server.log --max-errors 300 > /dev/null 2>&1; echo $?
uv run allcsv.py logs analyse server.log --max-errors 100
echo $?
```

```
0
Reading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 321.6/321.6 kB 0:00:00
     ERROR messages in server.log
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Count ┃ Message                     ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│    57 │ Video # file not found      │
│    50 │ Database connection timeout │
│    50 │ Upload failed for lesson #  │
└───────┴─────────────────────────────┘
           204 of 6000 lines
Too many ERROR lines
1
```

Three stories, three numbers: 0 fine, 1 too many errors, 2 a mistyped command.

### 11. Test it with `CliRunner`

Typer's `CliRunner` runs your app inside a test with a list of words, and gives back the exit code and the printed text. `test_allcsv.py` has three tests: a JSON run (exit 0, 2 matches, 1 bad line, using `tmp_path` from Module 13), a missing file (exit 2) and `--max-errors 1` (exit 1).

```bash
uv run pytest -q
```

```
...                                                            [100%]
3 passed in 0.25s
```

(The time will differ.)

### 12. Your turn

1. Add an option `--since` to `logs analyse` that skips the lines before a given hour.
2. Add a sub-command `courses show` that takes a course number.
3. Write a `CliRunner` test for each, and check the exit codes by hand with `echo $?`.

## Common mistakes

- Reading `sys.argv[1]` without checking it: a forgotten word gives an `IndexError` traceback instead of a help message. Let a library read the command line.
- Writing the type and default of every option as text away from the code that uses them (argparse). Typer takes them from the type hints.
- Thinking the `Path` hint checks that the file exists. It only converts the text. Add `exists=True` to get a clean error and exit code 2.
- Printing a friendly message with a plain `print` in a tool whose output is piped. Messages go to standard error (`file=sys.stderr`), answers to standard output.
- Returning 0 even when the run failed. Use `raise typer.Exit(code=1)` so scripts and build servers can tell.

## Clean up

Everything is inside this folder. To remove what the steps made:

```bash
rm -rf .venv big.log yesterday.log problem/server.log problem/yesterday.log problem/report .pytest_cache __pycache__
```

## Next

[M21-L02 · Building and Publishing a Package](../m21-l02-building-and-publishing-a-package/)
