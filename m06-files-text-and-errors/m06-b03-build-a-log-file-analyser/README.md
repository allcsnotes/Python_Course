# M06-B03 · Build a Log File Analyser

> Video: Module 6, Build 3. Watch it first, then follow along here.

## What you'll build
Meera, an instructor on allcsvideos.com, tells Asha the videos felt slow and broken around the middle of the day. Asha opens the server log: 6,000 lines, one for everything the server did. Nobody can read that, so Asha writes a small tool. It reads the log one line at a time, skips (and counts) the broken lines, counts the errors in each hour, and writes three reports: a text report for a person, a CSV file for a spreadsheet and a JSON file for other programs. The answer: hour 14 had 96 errors, every other hour 13 or fewer.

It uses only what module 6 taught: `pathlib`, dates and times, `Counter`, `try` and `except`, CSV and JSON.

## What you'll learn
- Read a big file one line at a time with `with path.open(...)` and a `for` loop.
- Take a line apart with `split` and turn the text into a `datetime` with `strptime`.
- Let a function raise `ValueError` for a bad line, and let the loop catch it, skip the line and count it.
- Count with `Counter` and group error messages with `re.sub`.
- Write text, CSV and JSON reports, with one function for each job.

## Before you start
- Python 3.14 or newer. Check with `python --version`.
- No packages and no Docker. Everything is in the standard library.
- Helpful: M06-L01 (files), M06-L02 (CSV and JSON), M06-L04 (raising errors) and M06-L05 (dates, `Counter`, `re`).
- Run every command from this folder (the project root).

## Files in this folder
| File | What it is |
| --- | --- |
| `make_log.py` | makes the fake `server.log` (6,000 lines, fixed seed, 6 damaged lines) |
| `analyser.py` | the finished analyser (113 lines) |
| `steps/step1-the-log/peek.py` | step 1: read four lines |
| `steps/step2-one-line/parse.py`, `crash.py` | step 2: take one line apart, and a line that crashes it |
| `steps/step3-bad-lines/parse.py` | step 3: skip and count bad lines |
| `steps/step4-counting/analyse.py` | step 4: count with `Counter` |
| `steps/extras/` | the small demos from the "what breaks" section (`counter.py`, `kinds.py`, `tz.py`, `oddbytes.py`, `oddfix.py`) |
| `expected-report/` | the report files you should get (`report.txt`, `errors_per_hour.csv`, `summary.json`) |

`server.log` and the `report/` folder do not exist yet: you create them when you run the programs.

## Run it
The quick way, with the finished project:
```bash
python analyser.py
```
You should see (the log does not exist yet, so the guard answers with a message, not a traceback):
```
server.log not found: run make_log.py
```
Make the log, then run the analyser again:
```bash
python make_log.py
python analyser.py
ls report
```
You should see:
```
Wrote 6000 lines to server.log
Read 6000 lines.
Skipped 6 bad lines.
Reports are in the report folder.
errors_per_hour.csv
report.txt
summary.json
```
On Windows, use `dir report` instead of `ls report`, and `type` instead of `cat`.

## The plan
A log is like the diary a ship's captain keeps: one new line each time something happens. Here are four lines from the server log. Each has four parts: the date, the time, the level (`INFO` normal, `WARNING` something odd, `ERROR` something failed) and the message (free text with spaces inside).

Requirements:
1. Read the log file, line by line.
2. Take each line apart into a time, a level and a message.
3. Skip broken lines, but count them.
4. Count the errors in each hour of the day.
5. Write a report as text, CSV and JSON.
6. Every job lives in its own function.

Why line by line? A log of 10 GB would fill the computer's memory if read all at once. A `for` loop over an open file hands over one line at a time, however big the file is.

The jobs as functions: `parse_line` (one line in, three facts out, or an error), `analyse` (reads the whole file), `write_report`, `write_csv` and `write_json` (one file each), and `main` (the boss that calls them in order).

## Build it step by step

### Step 1: the log
Asha's real log is private, so `make_log.py` makes a realistic fake. The trick that matters is a fixed seed: `random.Random(2026)` gives the same numbers every time, so your log file and the video's have the same lines. Errors are rare (2 in 100 lines), except in hour 14 where they are common (22 in 100). That is the problem the analyser should find. Six lines are damaged on purpose: an empty line, a cut-off line, a clock saying 25:61, a marker with no timestamp, a typo in the level and a leftover error trace. You do not need to study this program; its only job is to make test data.
```bash
python make_log.py
```
You should see:
```
Wrote 6000 lines to server.log
```
Now look inside with `steps/step1-the-log/peek.py`:
```python
from pathlib import Path

log = Path("server.log")
print(log.exists())
with log.open(encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip())
        if number == 4:
            break
```
```bash
python steps/step1-the-log/peek.py
```
You should see:
```
True
1 2026-03-12 00:00:28 INFO Student 996 enrolled in course 28
2 2026-03-12 00:01:02 INFO GET /courses 200 591ms
3 2026-03-12 00:04:34 INFO GET /courses 200 17ms
4 2026-03-12 00:06:56 INFO GET /courses 200 131ms
```
A `Path` object stands for the file and `exists()` says whether it is really there. `log.open()` works like `open(path)`, and `with` closes the file for us. `enumerate(f, start=1)` adds the line number. Every line from a file ends with a hidden newline and `print` adds another, so `rstrip()` cuts the extra one off.

### Step 2: take one line apart
If we cut at every space, the message (which has spaces) would be cut too. `split(" ", 3)` means: at most 3 cuts, so four pieces: date, time, level and the whole rest as the message. `strptime` turns the date and time text into a real `datetime`, so the hour becomes a plain number we can use as a bucket for counting. `steps/step2-one-line/parse.py`:
```python
from datetime import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_line(line):
    day, clock, level, message = line.rstrip().split(" ", 3)
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


line = "2026-03-12 14:05:09 ERROR Database connection timeout"
when, level, message = parse_line(line)
print(when)
print(when.hour, level)
print(message)
```
```bash
python steps/step2-one-line/parse.py
```
You should see:
```
2026-03-12 14:05:09
14 ERROR
Database connection timeout
```
But this function trusts every line. `steps/step2-one-line/crash.py` is the same function called with a cut-off line:
```bash
python steps/step2-one-line/crash.py
```
You should see:
```
Traceback (most recent call last):
  File "steps/step2-one-line/crash.py", line 12, in <module>
    print(parse_line("2026-03-12 09:30"))
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "steps/step2-one-line/crash.py", line 7, in parse_line
    day, clock, level, message = line.rstrip().split(" ", 3)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 4, got 2)
```
If this happened at line 1,200 of 6,000, the whole analysis would stop. That is step 3.

### Step 3: bad lines
What should happen to a bad line? Crash (no), ignore it quietly (dangerous: nobody knows how much was missing), or skip it and count it, so the report can say "6 lines were skipped". `parse_line` is the cook: it raises `ValueError` with a clear message. The loop is the manager: it catches the error, skips the line and adds one to the count. An impossible time like 25:61 needs no check of ours, because `strptime` already raises `ValueError`. `steps/step3-bad-lines/parse.py`:
```python
from datetime import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"
LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_line(line):
    parts = line.rstrip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"need 4 parts, got {len(parts)}")
    day, clock, level, message = parts
    if level not in LEVELS:
        raise ValueError(f"unknown level {level}")
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


samples = [
    "2026-03-12 14:05:09 ERROR Database connection timeout",
    "",
    "2026-03-12 09:30",
    "2026-03-12 25:61:07 INFO GET /courses 200 31ms",
    "#### log rotated ####",
    "2026-03-12 20:02:37 ERORR Disk full",
]
bad = 0
for line in samples:
    try:
        when, level, message = parse_line(line)
    except ValueError as err:
        bad += 1
        print("skip:", err)
    else:
        print("ok:", when.hour, level)
print(bad, "bad lines")
```
```bash
python steps/step3-bad-lines/parse.py
```
You should see:
```
ok: 14 ERROR
skip: need 4 parts, got 1
skip: need 4 parts, got 2
skip: time data '2026-03-12 25:61:07' does not match format '%Y-%m-%d %H:%M:%S'
skip: unknown level rotated
skip: unknown level ERORR
5 bad lines
```
Five bad lines and not one crash. The `else` part runs only when nothing went wrong.

### Step 4: counting
`Counter` counts while we read. `counts[key] += 1` works even for a key it has never seen, because a new key starts at zero. `steps/extras/counter.py`:
```bash
python steps/extras/counter.py
```
```
Counter({'INFO': 3, 'ERROR': 1})
0
```
Messages are not identical ("Payment failed for order 8841" and "... 1042" are the same kind of problem). `re.sub` replaces every run of digits with `#`. `steps/extras/kinds.py`:
```bash
python steps/extras/kinds.py
```
```
Payment failed for order #
Payment failed for order #
```
Now `steps/step4-counting/analyse.py` puts it together. `analyse` takes a path, keeps a `Counter` for the levels, one for the errors in each hour and one for the kinds of error, plus a list of bad lines and a total. It only calculates and returns one dictionary; it prints nothing, so the numbers can be shown, saved or tested anywhere.
```python
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("server.log")
FORMAT = "%Y-%m-%d %H:%M:%S"
LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_line(line):
    parts = line.rstrip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"need 4 parts, got {len(parts)}")
    day, clock, level, message = parts
    if level not in LEVELS:
        raise ValueError(f"unknown level {level}")
    when = datetime.strptime(f"{day} {clock}", FORMAT)
    return when, level, message


def analyse(path):
    levels = Counter()
    errors_by_hour = Counter()
    kinds = Counter()
    bad = []
    total = 0
    with path.open(encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            total += 1
            try:
                when, level, message = parse_line(line)
            except ValueError as err:
                bad.append((number, str(err)))
                continue
            levels[level] += 1
            if level == "ERROR":
                errors_by_hour[when.hour] += 1
                kind = re.sub(r"\d+", "#", message)
                kinds[kind] += 1
    return {
        "total": total,
        "bad": bad,
        "levels": levels,
        "errors_by_hour": errors_by_hour,
        "kinds": kinds,
    }


result = analyse(LOG_FILE)
print(result["total"], len(result["bad"]))
print(result["levels"])
print(result["errors_by_hour"].most_common(3))
print(result["kinds"].most_common(2))
```
```bash
python steps/step4-counting/analyse.py
```
You should see (run `python make_log.py` first so `server.log` exists):
```
6000 6
Counter({'INFO': 5311, 'WARNING': 479, 'ERROR': 204})
[(14, 96), (18, 13), (15, 10)]
[('Video # file not found', 57), ('Database connection timeout', 50)]
```
Six bad lines (exactly the six we damaged). Hour 14 has 96 errors, more than seven times the next hour. The commonest kinds of error are `Video # file not found` (57) and `Database connection timeout` (50).

### Step 5: the reports
Three readers, three small functions, each in `analyser.py`.

`write_report` builds a list of lines and writes them once at the end. `{hour:02d}` means two places filled with zeros, so 9 prints as `09`. The bar is `"#" * (count // 3)`.
```python
def write_report(result, folder):
    levels = result["levels"]
    errors = result["errors_by_hour"]
    lines = ["allcsvideos server log report", ""]
    lines.append(f"Lines read: {result['total']}")
    lines.append(f"Bad lines:  {len(result['bad'])}")
    for level in ("INFO", "WARNING", "ERROR"):
        lines.append(f"{level:<8} {levels[level]:>5}")
    lines += ["", "Errors per hour", ""]
    for hour in range(24):
        count = errors[hour]
        bar = "#" * (count // 3)
        lines.append(f"{hour:02d}:00 {bar:<32} {count}")
    lines += ["", "Top error messages", ""]
    for kind, count in result["kinds"].most_common(3):
        lines.append(f"{count:>5}  {kind}")
    lines += ["", "Skipped lines", ""]
    for number, why in result["bad"]:
        lines.append(f"line {number}: {why}")
    path = folder / "report.txt"
    path.write_text("\n".join(lines) + "\n")
```
`write_csv` opens the file for writing with `newline=""`, as the CSV lesson said:
```python
def write_csv(result, folder):
    errors = result["errors_by_hour"]
    path = folder / "errors_per_hour.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["hour", "errors"])
        for hour in range(24):
            writer.writerow([hour, errors[hour]])
```
`write_json` collects the facts other programs want. `most_common(1)` gives a list with one pair, and `[0]` takes the pair so we can unpack it. A `Counter` is a dictionary, so JSON accepts it.
```python
def write_json(result, folder):
    hour, count = result["errors_by_hour"].most_common(1)[0]
    summary = {
        "total_lines": result["total"],
        "bad_lines": len(result["bad"]),
        "levels": result["levels"],
        "busiest_hour": hour,
        "errors_in_busiest_hour": count,
    }
    path = folder / "summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n")
```

### Step 6: main, the boss
`main` first guards against a missing log (a friendly message beats a traceback), then calls the jobs in order. `mkdir(exist_ok=True)` means no error if the folder already exists.
```python
def main():
    if not LOG_FILE.exists():
        print(f"{LOG_FILE} not found: run make_log.py")
        return
    result = analyse(LOG_FILE)
    REPORT_DIR.mkdir(exist_ok=True)
    write_report(result, REPORT_DIR)
    write_csv(result, REPORT_DIR)
    write_json(result, REPORT_DIR)
    print(f"Read {result['total']} lines.")
    print(f"Skipped {len(result['bad'])} bad lines.")
    print(f"Reports are in the {REPORT_DIR} folder.")
```
Read it again: it reads like a list of the jobs. That is why we cut programs into functions. The last line of `analyser.py` calls `main()`.

## The result
`cat report/report.txt` (on Windows: `type report\report.txt`) should show exactly this:
```
allcsvideos server log report

Lines read: 6000
Bad lines:  6
INFO      5311
WARNING    479
ERROR      204

Errors per hour

00:00                                  2
01:00                                  0
02:00                                  1
03:00                                  0
04:00                                  0
05:00                                  2
06:00 #                                3
07:00 ##                               6
08:00 ##                               6
09:00 ##                               6
10:00 #                                4
11:00 ##                               6
12:00 #                                5
13:00 ##                               8
14:00 ################################ 96
15:00 ###                              10
16:00 #                                5
17:00 ##                               8
18:00 ####                             13
19:00 ##                               7
20:00 ###                              10
21:00 #                                4
22:00                                  1
23:00                                  1

Top error messages

   57  Video # file not found
   50  Database connection timeout
   50  Upload failed for lesson #

Skipped lines

line 42: need 4 parts, got 1
line 1201: need 4 parts, got 2
line 2751: time data '2026-03-12 25:61:07' does not match format '%Y-%m-%d %H:%M:%S'
line 4101: unknown level rotated
line 5201: unknown level ERORR
line 5901: unknown level recent
```
`head -5 report/errors_per_hour.csv`:
```
hour,errors
0,2
1,0
2,1
3,0
```
`cat report/summary.json`:
```
{
  "total_lines": 6000,
  "bad_lines": 6,
  "levels": {
    "INFO": 5311,
    "ERROR": 204,
    "WARNING": 479
  },
  "busiest_hour": 14,
  "errors_in_busiest_hour": 96
}
```
Hour 14 has a full row of 32 hashes: 96 errors. Asha can answer Meera now: it was hour 14, by the server's clock. The six skipped lines are listed with their line numbers, so nothing is skipped silently. (`recent` in the last skipped line comes from the leftover trace line, `Traceback (most recent call last):`, whose third word is not a level.)

## What breaks? Four limits of the tool
**1. Size.** Because we read one line at a time, memory stays small even for 60 million lines. It takes longer, but it does not crash.

**2. Time zones.** The server writes UTC, and the rule is: count in UTC. `steps/extras/tz.py` counts the errors twice, once by the server hour and once by the Mumbai hour (the log has no zone, so we first say "these times are UTC" with `replace`, then convert with `astimezone`):
```bash
python steps/extras/tz.py
```
```
UTC:    [(14, 96), (18, 13)]
Mumbai: [(19, 57), (20, 50)]
```
Mumbai is 5 hours 30 minutes ahead, so the half-hour shift cuts the spike into two bars. The data is not wrong; the buckets just do not match. Keep the log in UTC, count in UTC, and convert only the times you show to people.

**3. Bytes that are not text.** `steps/extras/oddbytes.py` writes a line with an old encoding (`cafe` with the accented e stored as the single byte `E9`) and reads it as UTF-8:
```bash
python steps/extras/oddbytes.py
```
You should see (the middle of the traceback is inside Python's own files, so it is trimmed here and the exact lines depend on your Python):
```
Traceback (most recent call last):
  File "steps/extras/oddbytes.py", line 5, in <module>
    print(odd.read_text(encoding="utf-8"))
  ...
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 28: invalid continuation byte
```
The fix is one setting, `errors="replace"`, which puts a replacement mark where the bad byte was. `steps/extras/oddfix.py`:
```bash
python steps/extras/oddfix.py
```
```
2026-03-12 10:00:00 INFO caf� order
```
(the mark is the diamond-shaped replacement character). For a log analyser that is the right choice: one strange letter must not stop the report.

**4. Skipping is only safe while it is rare.** Today 6 of 6,000 lines were skipped. If a new server version changed the format and half the lines were skipped, the report would still look fine and be nonsense. That is why we print the bad count every time and list the reasons. A good next step: stop with an error when more than a few percent of the lines are bad.

## Try these upgrades
1. Take the log file name from the command line (module 21).
2. Write your own `BadLineError` class, like in the raising-errors lesson.
3. Stop when too many lines are bad.
4. Find the slowest requests: the milliseconds are in the message.
5. Send the report automatically every week (a build near the end of the course).

## Common mistakes
- Reading the whole file into memory instead of looping over it line by line.
- Cutting the line at every space, which splits the message. Use `split(" ", 3)`.
- Skipping bad lines quietly without counting them.
- Counting in your local time zone instead of UTC.
- Forgetting `encoding="utf-8"` (and `errors="replace"` for messy logs) in `open`.
- Forgetting the `r` before a regular expression pattern.

## Clean up
These programs create `server.log`, `odd.log` (from `oddbytes.py`) and the `report/` folder in the folder you ran them from. Remove them when you are done:
```bash
rm -rf server.log odd.log report
```
(On Windows: `del server.log odd.log` and `rmdir /s report`.)

## Next
Module 6 is finished. Next is Module 7: [M07-L01 · Splitting Code into Modules](../../m07-modules-packages-and-environments/m07-l01-splitting-code-into-modules/). Our analyser is one file with 113 lines; next you learn to split a program into several files and import them.
