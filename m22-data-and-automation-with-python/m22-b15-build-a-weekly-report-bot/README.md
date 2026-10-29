# M22-B15 · Build a Weekly Report Bot

> Video: Module 22, Build 15. Watch it first, then follow along here.

Every Monday morning Meera wants the same report. In this build a program does it all by itself: it asks the allcsvideos
backend for last week's numbers, works out the totals with pandas, builds an Excel file and a PDF with a chart, and emails
both to Meera. Then you schedule it with cron, and break it on purpose: the server down, an empty week, a time zone
mistake and a report sent twice.

## What you'll build

- A small admin address on the backend, `/admin/report`, that returns the enrollments made and the refunds paid between two moments
- A bot in the `src` layout from Module 21: ten small files (`settings`, `weeks`, `api`, `analyse`, `excel`, `pdf`, `mail`, `marker`, `job`, `cli`), each with one job; only `cli` knows about Typer
- An Excel report (a summary sheet with a real `SUM` formula, and a sheet with every enrollment) and a one-page PDF with a bar chart
- An email with both files attached, sent to Mailpit (a fake mail server: no real email is ever sent)
- Tests with a fake server, a cron schedule in a container, and four safety nets: retries with a growing pause plus an alert email, a quiet email for an empty week, a week cut in India time, and a "sent" marker so a report is never sent twice

## Before you start

- Python 3.14 or newer (`python --version`), [uv](https://docs.astral.sh/uv/) (Module 7), and Docker Desktop with Docker Compose.
- Give Docker about 2 GB of memory. The stack runs four containers (the API, Postgres, Redis, Mailpit) and, later, a fifth
  with cron.
- Ideas from earlier lessons: the whole of M22 (files, Excel, email, cron, scraping, pandas), the backend from Module 19
  (Compose, pydantic settings), Alembic from Module 16, login tokens from Module 17, tests from Module 13 and Ruff from Module 14.
- All data is generated for this course with a fixed seed. Every password, key and email in this folder is a fake demo value.

## Files in this folder

| Path | What it is |
|------|------------|
| `stack/compose.yml` | The lab: Postgres 17, Redis 8, Mailpit v1.32.0, the API (built from `allcs/`), and the cron container (started with `--profile cron`) |
| `stack/seed.py` | Fills the database with one week of generated data (fixed seed 2026) |
| `allcs/` | The allcsvideos backend from Module 19, with one new route (`app/routers/admin.py`, `GET /admin/report`) and one new Alembic migration (`migrations/versions/a7c3e91d5b20_enrollment_timestamps.py`) |
| `bot/pyproject.toml`, `bot/uv.lock` | The bot project: `fpdf2`, `httpx`, `matplotlib`, `openpyxl`, `pandas`, `pydantic-settings`, `typer`, `tzdata`; dev tools `pytest` and `ruff` (all pinned in `uv.lock`) |
| `bot/src/weekly_report/settings.py` | Settings from the environment; the password is a `SecretStr` |
| `bot/src/weekly_report/weeks.py` | `last_monday`, `week_bounds` (midnight in Asia/Kolkata), `week_label` |
| `bot/src/weekly_report/api.py` | `login`, `fetch_report`, and `fetch_with_tries` (retries, then `ApiDown`) |
| `bot/src/weekly_report/analyse.py` | `to_frame`, `summarise` and the `Summary` object |
| `bot/src/weekly_report/excel.py` | The workbook: `Summary` and `Enrollments` sheets |
| `bot/src/weekly_report/pdf.py` | The bar chart (matplotlib, Agg backend) and the one-page PDF (fpdf2) |
| `bot/src/weekly_report/mail.py` | `make_message` and `send` (standard library) |
| `bot/src/weekly_report/marker.py` | The "this week was sent" file |
| `bot/src/weekly_report/job.py` | `get_summary`, `build_message`, `run_week`, `alert` |
| `bot/src/weekly_report/cli.py` | The `weekly-report run` command (Typer) |
| `bot/demo/d1_weeks.py` ... `d7_utc.py` | Small scripts that the video runs after each step |
| `bot/tests/test_report.py` | Seven tests with a fake server |
| `bot/Dockerfile`, `crontab`, `run.sh`, `entrypoint.sh` | The cron container: Python 3.14, cron, India time zone, user `app` |

## Run it

The quick version, for when you only want to see the bot work. Every step is explained below in "Build it step by step".

```bash
# 1. the lab (run in stack/)
cd stack
docker compose up -d --build
docker compose exec api alembic upgrade head
docker compose exec -w /app api python seed.py

# 2. the bot (run in bot/)
cd ../bot
uv sync
export API_URL=http://localhost:8725
export API_USER=reports@allcsvideos.com
export API_PASSWORD=demo-report-bot-pass
export SMTP_HOST=localhost
export SMTP_PORT=22525
export OUT_DIR=out
uv run weekly-report run --week 2026-10-19
```

Then open <http://localhost:22526> (Mailpit): a message "Weekly report 2026-W43" from `reports@allcsvideos.com` to
`meera@allcsvideos.com`, with the Excel file and the PDF attached. On Windows PowerShell, set the variables with
`$env:API_URL = "http://localhost:8725"` and so on.

## Build it step by step

### 0. The lab (the server)

The backend is the allcsvideos API from Module 19. It had no report yet, so the course added one small thing: an address for
admins, `GET /admin/report?start=...&end=...`, that returns the enrollments made and the refunds paid in that time. For it,
each enrollment got three new columns with one Alembic migration (Module 16): the exact moment (`enrolled_at`), the amount
paid (`amount`) and the moment of a refund (`refunded_at`).

Start the lab in the `stack/` folder, create the tables and fill them with the generated week:

```bash
cd stack
docker compose up -d --build
docker compose exec api alembic upgrade head
docker compose exec -w /app api python seed.py
docker compose ps --format "table {{.Service}}\t{{.Status}}"
```

The seed script prints `seeded`. The first build takes a few minutes. The services:

```
SERVICE    STATUS
api        Up ... (healthy)
mailpit    Up ... (healthy)
postgres   Up ... (healthy)
redis      Up ... (healthy)
```

The API is on <http://localhost:8725> (docs at `/docs`), Postgres on 22551, Redis on 22451, Mailpit's mail port on 22525 and
its web page on <http://localhost:22526>. The seeded data has 36 enrollments in the week of Monday 19 October 2026 (India
time), 14 in the week before, 5 refunds paid in that week, and four enrollments right at the edges of the week, to test the time zone.

Open a second terminal for the bot, in the `bot/` folder:

```bash
cd bot
uv sync
```

and set the settings (the names are the fields of the `Settings` class, in capitals):

```bash
export API_URL=http://localhost:8725
export API_USER=reports@allcsvideos.com
export API_PASSWORD=demo-report-bot-pass
export SMTP_HOST=localhost
export SMTP_PORT=22525
export OUT_DIR=out
```

### 1. The plan on paper

Meera asks four questions every Monday: how many new enrollments, how much money for each course, which course is on top,
how many refunds. She wants one email, with an Excel file for the details and a PDF for a quick look, every Monday at 8:00,
India time. Five steps, each one small file so each can be tested alone:

1. fetch last week's rows from the server;
2. analyse them with pandas;
3. build the Excel file and the PDF;
4. send the email;
5. let a schedule start the whole thing, with nobody watching.

### 2. Settings (`settings.py`)

A class from pydantic-settings. The API address, user and password come from the environment. The password is a `SecretStr`,
so it never shows up in a log or a print. The mail addresses, the time zone (`Asia/Kolkata`), the number of tries (3) and the
pause (2 seconds) have defaults. Nothing secret is written in the code.

### 3. The week (`weeks.py`, demo `d1_weeks.py`)

`last_monday(today)` goes back to this Monday, then seven more days. `week_bounds(monday, tz)` makes midnight on that Monday in
`Asia/Kolkata` and, seven days later, the end. No hours are ever added by hand.

```bash
uv run python demo/d1_weeks.py
```

```
start 2026-10-19T00:00:00+05:30
  in UTC 2026-10-18T18:30:00+00:00
end   2026-10-26T00:00:00+05:30
```

The start is midnight, plus five thirty. In UTC (the time the server uses) the same moment is 18:30 on the 18th. Remember that: it
comes back in the pitfalls.

### 4. The API (`api.py`, demo `d2_fetch.py`)

`login` posts the user and password as a form and gets a token back (Module 17); the secret string is opened only here, at
the last moment. `fetch_report` sends the start and end as timestamps, with the token in a header (like lesson 2), and
`raise_for_status` turns a failure into an error. The client is a parameter, so a test can hand in a fake one.

```bash
uv run python demo/d2_fetch.py
```

```
36 enrollments
5 refunds
{'amount': 499,
 'course': 'Python Basics',
 'course_id': 1,
 'enrolled_at': '2026-10-18T18:50:00+00:00',
 'refunded_at': None,
 'student_id': 55}
```

Look at the first row: its time ends in `+00:00`. The server speaks UTC. The report must speak India time.

### 5. Analyse (`analyse.py`, demo `d3_analyse.py`)

`to_frame` turns the list of dictionaries into a DataFrame and converts both time columns: read them as UTC, then move them to
India time. `summarise` keeps the enrollments of the week (at or after the start, before the end), counts the rows from before
the start (last week), and takes the refunds paid inside this week, even when the student joined earlier. Then the `groupby`
from lesson 3: for each course, count the enrollments and add up the amounts. `Summary.net` is a property: money in, minus money paid back.

```bash
uv run python demo/d3_analyse.py
```

```
36 enrollments, last week 14
gross 21164 refunded 3295 net 17869
                        enrollments  revenue
course                                      
SQL in Two Weeks                 11     6589
Docker for Python Apps            7     6293
Python Basics                    11     5489
Git for Teams                     7     2793
```

### 6. Tests, with a fake server (`tests/test_report.py`)

The fake client uses `httpx.MockTransport`: a small function plays the server. For the login it answers with a token. For
the report it can fail on purpose the first few times, then answer with the data. The fake data has a row made at 18:45 UTC
on the 18th, which is quarter past midnight in India, so it belongs to the week; one row from the week before; and one refund.

```bash
uv run pytest -v
uv run ruff check
uv run ruff format --check
```

```
tests/test_report.py::test_week_starts_at_midnight_in_india PASSED
tests/test_report.py::test_last_monday PASSED
tests/test_report.py::test_summary_numbers PASSED
tests/test_report.py::test_empty_week_is_quiet PASSED
tests/test_report.py::test_retry_then_success PASSED
tests/test_report.py::test_gives_up_after_three_tries PASSED
tests/test_report.py::test_second_run_sends_nothing PASSED
7 passed in 12.24s
All checks passed!
19 files already formatted
```

(The test time and the header lines of pytest will differ on your machine.) The last test, a second run sends nothing,
is the marker at work (step 10).

### 7. The Excel file (`excel.py`, demo `d4_excel.py`)

The `Summary` sheet gets a title, four numbers and a table with a blue header. Under it a `Total` row with a real formula,
`=SUM(...)`, and a number format `"Rs "#,##0` on the revenue cells. The second sheet, `Enrollments`, lists every enrollment;
Excel has no time zones, so each time is first turned into a plain local time, and `freeze_panes = "A2"` keeps the header
in view.

```bash
uv run python demo/d4_excel.py
```

```
['Summary', 'Enrollments']
('Course', 'Enrollments', 'Revenue')
('SQL in Two Weeks', 11, 6589)
('Docker for Python Apps', 7, 6293)
('Python Basics', 11, 5489)
('Git for Teams', 7, 2793)
('Total', '=SUM(B8:B11)', '=SUM(C8:C11)')
A2
```

Two sheets, and the totals are formulas, not numbers: Excel adds them up when it opens the file (openpyxl never calculates).
The file is saved in `out/2026-W43.xlsx`; open it in Excel or LibreOffice to look.

### 8. The PDF (`pdf.py`, demo `d5_pdf.py`)

The bar chart (revenue per course) is drawn with matplotlib and saved as a picture. One detail: `matplotlib.use("Agg")`, the
backend that draws without a window, because a scheduled job has no screen. Then `fpdf2` makes one page: a title, three lines
of numbers and the chart.

```bash
uv run python demo/d5_pdf.py
```

```
['2026-W43.pdf', '2026-W43.png', '2026-W43.xlsx']
```

Open `out/2026-W43.pdf`: one page, the numbers first, then the chart. Meera can read it on her phone.

### 9. The email (`mail.py`, demo `d6_mail.py`)

A message from the standard library (like lesson 1): from, to, subject, a plain-text body, and one attachment for each file
with its type. `send` opens a connection to the mail host and port from the settings. Mailpit accepts plain text, so there is
no login here; a real mail server also wants encryption and a login, and those would come from the environment, like the API password.

```bash
uv run python demo/d6_mail.py
```

```
sent to meera@allcsvideos.com
```

Open <http://localhost:22526>: a message from `reports@allcsvideos.com` to `meera@allcsvideos.com`, subject
`Weekly report 2026-W43`, with two attachments (the Excel file and the PDF). Nothing leaves your laptop.

### 10. The marker (`marker.py`)

After a report is sent, `mark_sent` writes a tiny file `out/sent/<week>.json`, with the receiver and the time. Before
starting, the bot looks for that file: if it is there, that week was already sent. The pitfalls below show why.

### 11. The job (`job.py`)

`get_summary` works out the start and end, asks the server for two weeks (this one and the one before), with tries
(step 14), and summarises. `build_message` makes the files, but only when the week had enrollments, and builds a message with a
subject, a body and the files as attachments. `run_week` joins it all: if the marker says the week was sent, stop; otherwise get
the summary and build the message; a dry run stops there and only logs; otherwise send, write the marker and log. `send` is a
parameter, so a test can hand in a fake sender. `alert` sends a failure email to Asha (not to Meera).

### 12. The command (`cli.py`)

Typer (Module 21). The `run` command has three options: `--week` (text, default last week), `--dry-run` and `--force`. In its
body: read the settings, work out the Monday, open one client, and run the week. If the server stays down, the job raises `ApiDown`,
and the command sends an alert email and exits with code 1.

The help page is made for free from the code:

```bash
uv run weekly-report --help
uv run weekly-report run --help
```

```
 Usage: weekly-report [OPTIONS] COMMAND [ARGS]...

 Make and send the allcsvideos weekly report.

╭─ Options ────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────╮
│ run                                                          │
╰──────────────────────────────────────────────────────────────╯
```

and `run --help` shows the three options with the text written in the code:

```
 Usage: weekly-report run [OPTIONS]

╭─ Options ────────────────────────────────────────────────────╮
│ --week                       <str>  Monday of the week,      │
│                                     YYYY-MM-DD. Default:     │
│                                     last week.               │
│ --dry-run    --no-dry-run           Build the files, send    │
│                                     nothing.                 │
│                                     [default: no-dry-run]    │
│ --force      --no-force             Send even if this week   │
│                                     was sent.                │
│                                     [default: no-force]      │
│ --help                              Show this message and    │
│                                     exit.                    │
╰──────────────────────────────────────────────────────────────╯
```

(The box widths depend on your terminal width.)

### 13. Run it: a dry run, then for real

First empty the output folder (and the Mailpit inbox, with `curl -s -X DELETE localhost:22526/api/v1/messages`), so you
see everything from scratch. Then a dry run for Monday the 19th:

```bash
rm -rf out
uv run weekly-report run --week 2026-10-19 --dry-run
ls out
```

```
21:58:16 INFO week 2026-10-19 to 2026-10-26
21:58:17 INFO 36 enrollments, 5 refunds
21:58:18 INFO dry run: nothing sent
2026-W43.pdf
2026-W43.png
2026-W43.xlsx
```

(Your clock times will differ.) It built the files and sent nothing. Now the same line without `--dry-run`:

```bash
uv run weekly-report run --week 2026-10-19
ls out out/sent
uv run weekly-report run --week 2026-10-19
```

```
21:58:33 INFO week 2026-10-19 to 2026-10-26
21:58:33 INFO 36 enrollments, 5 refunds
21:58:34 INFO sent 2026-W43 to meera@allcsvideos.com
out:
2026-W43.pdf
2026-W43.png
2026-W43.xlsx
sent

out/sent:
2026-W43.json
21:58:49 INFO week 2026-W43 already sent, skipping
```

Mailpit has the new message from the bot to Meera, with its attachments. The second run sent nothing, because of the marker.

### 14. The schedule, with cron in a container

Cron (lesson 1) reads a table: five fields, then the command. The real schedule is `0 8 * * 1`: minute 0 of hour 8, any day,
any month, on weekday 1, which is Monday. It is commented out in `bot/crontab` because a demo cannot wait a week. The demo line
has five stars, every minute, and runs the bot as the user `app` (never root), writing everything to a log file:

```
* * * * *  app  /app/run.sh >> /data/report.log 2>&1
```

Cron runs inside a container, not on your computer. `bot/Dockerfile` installs cron and the time zone data, sets the time zone to
India, creates the user `app`, and starts cron in the foreground. Cron starts a job with an almost empty environment (the trap
from lesson 1), so `entrypoint.sh` saves the container's settings to `/etc/weekly-report.env`, readable only by the job's
user, and `run.sh` loads that file before it runs the bot. The password lives in the container's environment, not in the image.

Empty Mailpit, then start the cron container (from `stack/`):

```bash
curl -s -X DELETE localhost:22526/api/v1/messages
cd ../stack
docker compose --profile cron up -d cron
```

Wait a minute and do not type anything. Then:

```bash
docker exec m22b15-cron cat /data/report.log
```

```
22:00:04 INFO week 2026-10-19 to 2026-10-26
22:00:04 INFO 36 enrollments, 5 refunds
22:00:04 INFO sent 2026-W43 to meera@allcsvideos.com
```

A new message is in Mailpit, sent by the bot, with the same two attachments, and nobody typed anything. Wait one more
minute and look again:

```bash
docker exec m22b15-cron cat /data/report.log
docker exec m22b15-cron ls /data /data/sent
```

```
22:00:04 INFO week 2026-10-19 to 2026-10-26
22:00:04 INFO 36 enrollments, 5 refunds
22:00:04 INFO sent 2026-W43 to meera@allcsvideos.com
22:01:04 INFO week 2026-W43 already sent, skipping
/data:
2026-W43.pdf
2026-W43.png
2026-W43.xlsx
report.log
sent

/data/sent:
2026-W43.json
```

The demo ran every minute on whatever day it is, so that you can see it. The real line fires only on Monday at 8:00 India
time. With no `--week`, the bot reports "last week" of the day it runs (on a Thursday in late October 2026 that is week 43;
on another date the log shows another week). The code and the container are the same. To use the real schedule, comment the
five-star line in `bot/crontab` and uncomment the `0 8 * * 1` line.

## Break it on purpose (the four pitfalls)

### Pitfall 1: the server goes down

A report that fails silently is the worst kind. `fetch_with_tries` tries again with a pause that grows: 2 seconds, then 4. Only
errors that can heal are tried again: no answer, a 500 error, or a 429 (too many requests, lesson 2). Each failed try logs a
warning. On the last try, or on an error that will not get better (like a wrong password), it stops and raises `ApiDown`.

Stop the API and run the bot for the week before (run these in `bot/`):

```bash
docker stop m22b15-api
uv run weekly-report run --week 2026-10-12; echo "exit code $?"
```

```
21:59:10 INFO week 2026-10-12 to 2026-10-19
21:59:10 WARNING try 1/3 failed: [Errno 61] Connection refused
21:59:12 WARNING try 2/3 failed: [Errno 61] Connection refused
21:59:16 WARNING try 3/3 failed: [Errno 61] Connection refused
21:59:16 ERROR alert sent to asha@allcsvideos.com
exit code 1
```

Three tries, each refused, six seconds in all (the error number is `[Errno 111]` on Linux). Then an alert: an email to Asha, not
to Meera, with the subject `ALERT: report 2026-W42 failed` saying the report failed and why. The exit code is 1, so cron, or any
monitor, sees a failure. Meera never gets a wrong or half-finished report. Start the API again:

```bash
docker start m22b15-api
```

### Pitfall 2: an empty week

This week in August has no enrollments at all. A table with no rows can break an average or a chart. The job checks the count
first and sends a short, honest email: a quiet week, no attachments. (The test `test_empty_week_is_quiet` covers it.)

```bash
uv run weekly-report run --week 2026-08-03
```

```
21:58:57 INFO week 2026-08-03 to 2026-08-10
21:58:57 INFO 0 enrollments, 0 refunds
21:58:57 INFO sent 2026-W32 to meera@allcsvideos.com
```

In Mailpit the message `Weekly report 2026-W32` says "A quiet week: no enrollments in 2026-W32." and has no attachments.

### Pitfall 3: the time zone mistake

`demo/d7_utc.py` makes the same week twice: once cut in UTC, once in India time.

```bash
uv run python demo/d7_utc.py
```

```
UTC           37 enrollments, Rs 23063
Asia/Kolkata  36 enrollments, Rs 21164
```

Why? The UTC week starts at half past five in the morning in India. It misses the two enrollments made in the first hours of
Monday, and it wrongly adds the three made in the first hours of the next Monday. Both numbers look fine, so nobody notices. The fix
is step 3: a week is cut in the business's own time zone.

### Pitfall 4: sending twice

In the demo, cron runs every minute and sent the report in the first minute. In the second minute the log says
`week 2026-W43 already sent, skipping`. That is the marker. The job is idempotent (Module 18): running it twice gives the same
result as running it once. To send again on purpose, use the `--force` option:

```bash
uv run weekly-report run --week 2026-10-19 --force
```

One honest detail: the marker is written after the send. If the send fails, there is no marker and the next run tries again.
If the machine dies between the send and the marker, Meera could get one extra copy. For a report, that is better than none.

## Common mistakes

- Cutting the business week in UTC instead of the business's own time zone: the numbers look fine and are wrong.
- Retrying every error. Retry only the ones that can heal (no answer, 5xx, 429), with a growing pause and a limit, then alert.
- Letting a failed job stay silent: send an alert and exit with a non-zero code so a monitor can see it.
- Treating an empty week as an error, or drawing a chart from an empty table.
- Sending the same report twice because the schedule fired twice: write a marker and check it first.
- Settings missing in cron: it starts jobs with a nearly empty environment. Load them from a file in `run.sh`.
- Putting the password in the code or the image. It lives in the container's environment.
- Forgetting the Agg backend for matplotlib in a job that has no screen.

Five habits for a script that runs alone, all in this bot: a dry run first; full paths; settings from the environment; a log
file with times; and a marker, to be safe to run twice.

## Ways to grow it (your turn)

- Add the best day of the week to the Excel summary, with a test.
- Take the receivers from a list in the settings.
- Run the dry run for another week (`--week 2026-10-12 --dry-run`).
- Move the schedule to Friday at six in the evening: `0 18 * * 5`.
- Bigger ideas: a trend chart over many weeks; Celery beat (Module 18) instead of cron; a real mail server with encryption and a
  login from the environment; save the summaries in Postgres; a monitor that raises an alarm if no report arrives by nine.

## Clean up

In `stack/`:

```bash
docker compose --profile cron down -v
docker rmi m22b15-api:1 m22b15-bot:1
```

This removes the containers, the network and the volumes (including `m22b15-data` with the logs and the files the cron
container made). In `bot/`, delete the local output and the environment if you like:

```bash
rm -rf out .venv
```

## Next

This was the last build of Module 22. Next: Module 23, lesson 1: [M23-L01 · The Python Gotchas](../../m23-interviews-and-capstone/m23-l01-the-python-gotchas/)
