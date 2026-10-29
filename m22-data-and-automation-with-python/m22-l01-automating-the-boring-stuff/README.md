# M22-L01 · Automating the Boring Stuff

> Video: Module 22, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Tidy a messy folder with `pathlib` and `shutil`, and always run a dry run first (nothing changes until you say `--apply`)
- Spot name clashes before moving files, so one report can never silently replace another
- Read and write an Excel file with `openpyxl` (formulas, number formats, a frozen header row)
- Send an email with an attachment through SMTP, with the login coming from the environment
- Make cron run the whole job on its own, every minute, for real, and fix the four traps that make a script work in
  your terminal but fail in cron
- Know two other ways to keep time: the `schedule` library and Celery beat

## Before you start

- Python 3.14 or newer (`python --version`) and [uv](https://docs.astral.sh/uv/) (Module 7).
- Docker Desktop running. Docker is used for three things: Mailpit (a fake mail server), a small Linux box with cron,
  and (optional) LibreOffice to draw the Excel file. Nothing is installed in your own computer's scheduler.
- Typer from the last lesson (M21) and `pathlib` from M06-L01. No earlier lesson folder is needed.
- Every email address, user name and password in this folder is a made-up demo value. No real email is sent: it all goes
  to Mailpit on your own laptop.

Work in a copy, not in the repo, so your clone stays clean:

```bash
cp -R m22-l01-automating-the-boring-stuff ~/boring
cd ~/boring
uv sync
```

## Files in this folder

| File | What it is |
|------|------------|
| `pyproject.toml`, `uv.lock` | The project `boring`: openpyxl 3.1.5, schedule 1.2.2, typer 0.27.3 (pinned in the lock file) |
| `setup/gen_data.py` | Course setup (not shown in the video): makes the messy folder and the Excel file. Already run: its output is in `downloads_src/` and `data/` |
| `downloads_src/` | The messy downloads folder: 13 files. Never edit it; the lesson works on a copy called `downloads/` |
| `data/enrollments_week.xlsx` | The file Meera sends: 14 enrollments, 4 columns |
| `tree.py` | Prints a folder as a tree |
| `glob_demo.py` | `Path.glob` on the downloads folder |
| `organise_v1.py` | The sorter, version 1: a dry run only, with a name clash |
| `organise.py` | The sorter, final: `unique()` for clashes, `--apply` to really move |
| `sheets.py` | `summarise()` reads the week, `write_report()` writes the report |
| `read_demo.py`, `write_demo.py`, `check_demo.py` | Run the reader, the writer, and read the written file back |
| `mailer.py` | `send_report()`: the email with the attachment |
| `send_demo.py`, `mailcount.py` | Send one email, and count the messages in Mailpit |
| `job.py` | The whole job: read, write, send, log |
| `demo_schedule.py` | The `schedule` library demo |
| `cron/Dockerfile` | The small Linux box: Python 3.14, openpyxl, cron |
| `cron/crontab.v0` ... `crontab.v4` | The five versions of the crontab, from the broken one to the final one |
| `cron/env.list` | The four mail settings, for running the job by hand in the box |
| `lo/Dockerfile` | LibreOffice (headless), to turn the Excel file into a picture (optional) |

## Follow along

### 1. The messy folder

```bash
cp -R downloads_src downloads
uv run tree.py downloads
```

```
downloads/
├── IMG_2041.JPG
├── IMG_2042.jpg
├── Meera slides.pdf
├── Refunds copy.csv
├── Report Final.xlsx
├── Screenshot 2026-10-20 at 9.14.png
├── archive.zip
├── enrollments 2026-10-19.csv
├── enrollments 2026-10-26.csv
├── invoice oct.pdf
├── notes.txt
├── report-final.xlsx
└── setup.exe
```

Thirteen files with capital letters, spaces and a copy.

### 2. Try glob

`glob_demo.py` lists the files that match `*.csv`, then counts everything with `*`:

```bash
uv run glob_demo.py
```

```
Refunds copy.csv
enrollments 2026-10-19.csv
enrollments 2026-10-26.csv
13 files in all
```

### 3. The sorter, version 1 (a dry run)

`organise_v1.py` has a `KINDS` dictionary (ending to folder), `tidy()` (lower case, dashes for spaces) and a loop that
prints `old name -> new place`. It moves nothing.

```bash
uv run organise_v1.py downloads
```

```
IMG_2041.JPG -> images/img_2041.jpg
IMG_2042.jpg -> images/img_2042.jpg
Meera slides.pdf -> documents/meera-slides.pdf
Refunds copy.csv -> data/refunds-copy.csv
Report Final.xlsx -> sheets/report-final.xlsx
Screenshot 2026-10-20 at 9.14.png -> images/screenshot-2026-10-20-at-9.14.png
archive.zip -> other/archive.zip
enrollments 2026-10-19.csv -> data/enrollments-2026-10-19.csv
enrollments 2026-10-26.csv -> data/enrollments-2026-10-26.csv
invoice oct.pdf -> documents/invoice-oct.pdf
notes.txt -> documents/notes.txt
report-final.xlsx -> sheets/report-final.xlsx
setup.exe -> other/setup.exe
```

Look at the two `sheets` lines: `Report Final.xlsx` and `report-final.xlsx` get the same new name, `sheets/report-final.xlsx`.
If we had moved the files, the second would have replaced the first: one report gone, no error and no undo. That is
exactly why we run a dry run first.

### 4. The sorter, final version

`organise.py` adds `unique(target, taken)`: it starts with the plain name, and while that name is taken (or already
exists on disk) it adds `-2`, `-3`. `Path.with_stem` changes the name and keeps the ending. It also adds
`apply: bool = False`, which Typer turns into the option `--apply`. Only with `--apply` does it create the folder and
call `shutil.move`.

Dry run first:

```bash
uv run organise.py downloads
ls downloads | wc -l
```

```
IMG_2041.JPG -> images/img_2041.jpg
IMG_2042.jpg -> images/img_2042.jpg
Meera slides.pdf -> documents/meera-slides.pdf
Refunds copy.csv -> data/refunds-copy.csv
Report Final.xlsx -> sheets/report-final.xlsx
Screenshot 2026-10-20 at 9.14.png -> images/screenshot-2026-10-20-at-9.14.png
archive.zip -> other/archive.zip
enrollments 2026-10-19.csv -> data/enrollments-2026-10-19.csv
enrollments 2026-10-26.csv -> data/enrollments-2026-10-26.csv
invoice oct.pdf -> documents/invoice-oct.pdf
notes.txt -> documents/notes.txt
report-final.xlsx -> sheets/report-final-2.xlsx
setup.exe -> other/setup.exe
13
```

The second report is now `report-final-2.xlsx`, and `ls` still counts 13 files: the dry run changed nothing. (On macOS
`wc -l` may print spaces before the number.)

Now for real:

```bash
uv run organise.py downloads --apply
uv run tree.py downloads
uv run organise.py downloads
```

The first command prints the same thirteen lines, this time moving the files. Then:

```
downloads/
├── data/
│   ├── enrollments-2026-10-19.csv
│   ├── enrollments-2026-10-26.csv
│   └── refunds-copy.csv
├── documents/
│   ├── invoice-oct.pdf
│   ├── meera-slides.pdf
│   └── notes.txt
├── images/
│   ├── img_2041.jpg
│   ├── img_2042.jpg
│   └── screenshot-2026-10-20-at-9.14.png
├── other/
│   ├── archive.zip
│   └── setup.exe
└── sheets/
    ├── report-final-2.xlsx
    └── report-final.xlsx
```

The last command (running it again) prints nothing, because there is nothing left to do. A script that is safe to run
twice is the best kind. Both reports are still there.

### 5. Read the spreadsheet

`sheets.py` has `summarise(path)`: `load_workbook(path).active` is the sheet that was open when the file was saved,
`iter_rows(min_row=2, values_only=True)` skips the header and gives plain tuples, and two `Counter`s count the
enrollments and add up the rupees for each course.

```bash
uv run read_demo.py
```

```
Enrollments 15 rows, 4 columns
Docker for Python Apps   5  6495
Python Basics            4  5996
Git and GitHub           3  2397
SQL in Two Weeks         2  1998
```

### 6. Write the report

`write_report()` makes a new `Workbook`, names the sheet `Revenue`, appends the header and one row for each course, then
a `Total` row. A formula is only text that starts with `=`, like `=SUM(C2:C5)`. The share column divides each
revenue by the total. Then the looks: number formats (`"Rs "#,##0` and `0%`), a bold white header on a blue fill,
column widths, and `freeze_panes = "A2"`.

```bash
uv run write_demo.py
uv run check_demo.py
```

```
saved report.xlsx
=SUM(C2:C5) "Rs "#,##0
A2 26.0
None
```

`check_demo.py` reads the file back twice. The first line is the formula text and the number format. The second shows the
frozen cell and the width of column A. The last line is `None`: reading with `data_only=True` gives the
calculated value, but openpyxl never calculates anything. It only stores the formula text. The answer is calculated by
Excel or LibreOffice when somebody opens the file.

### 7. See the file honestly with LibreOffice (optional)

LibreOffice runs headless (no window) inside a Docker box and turns the file into a PDF and then a picture:

```bash
docker build -t m22l01-lo lo
docker run --rm -v "$PWD":/work -w /work m22l01-lo sh -c \
  "soffice --headless --convert-to pdf report.xlsx && pdftoppm -r 100 -png -singlefile report.pdf report"
```

```
Warning: failed to launch javaldx - java may not function correctly
convert /work/report.xlsx as a Calc document -> /work/report.pdf using filter : calc_pdf_Export
```

The first build downloads LibreOffice and takes a few minutes. Open `report.png`: the total is Rs 16,886, the shares are
38%, 36%, 14% and 12%, the header is blue and bold. (A picture cannot show a frozen row.)

### 8. Start Mailpit

Mailpit is a fake mail server that catches every message. Its mail port is 22125 and its web page is 22126. Create a
network first (the cron box will use it later):

```bash
docker network create m22l01-net
docker run -d --name m22l01-mail --network m22l01-net \
  -e MP_SMTP_AUTH_ACCEPT_ANY=1 -e MP_SMTP_AUTH_ALLOW_INSECURE=1 \
  -p 22125:1025 -p 22126:8025 axllent/mailpit:v1.32.0
```

The two `-e` settings tell Mailpit to accept any login over a plain connection. That is fine here and only here. A real
mail provider needs `server.starttls()` before the login, which this demo does not run.

### 9. Send an email with an attachment

`mailer.py` builds an `EmailMessage` (headers set like a dictionary, `set_content` for the text, `add_attachment` with the
file bytes, a main type, a subtype and the file name). The subtype for an Excel file is long, so it sits in the constant
`XLSX`. It sends through `smtplib.SMTP`, with host, port, user and password read from the environment: a password never
goes in the code or in git.

```bash
export SMTP_HOST=localhost
export SMTP_PORT=22125
export SMTP_USER=asha
export SMTP_PASSWORD=demo-only
uv run send_demo.py
uv run mailcount.py
```

```
sent
messages in Mailpit: 1
```

Open <http://localhost:22126>. You will see a new message from Asha to Meera, subject
`Weekly report: 19 to 25 October`, with one attachment, `report.xlsx`, about 5 kilobytes.

### 10. The whole job

`job.py` joins the three steps (read the enrollments, write the report, send it) and ends with a log line made by
`logging`: the time, the level and a message. A job that runs alone needs a logbook, because nobody is watching.

### 11. The cron box

Build the small Linux box and prepare a folder for it. The folder `cronapp` is mounted into the box as `/app`:

```bash
docker build -t m22l01-cron:demo -f cron/Dockerfile cron
mkdir -p cronapp/logs cronapp/data
cp job.py mailer.py sheets.py cronapp/
cp data/enrollments_week.xlsx cronapp/data/
cp cron/crontab.v? cron/env.list cronapp/
docker run -d --name m22l01-cron --network m22l01-net -v "$PWD/cronapp":/app m22l01-cron:demo
```

Empty Mailpit, so the counts below start from zero, then run the job by hand inside the box, with the four settings from `env.list` (the box reaches Mailpit by its container name):

```bash
curl -s -X DELETE localhost:22126/api/v1/messages
docker exec -w /app --env-file cron/env.list m22l01-cron python job.py
uv run mailcount.py
```

```
2026-10-29 16:14:54,606 INFO report sent: 4 courses
messages in Mailpit: 1
```

Your date and time will differ. It works, and Mailpit has one message.

### 12. What is cron?

Cron is a program that wakes up every minute, reads a table of jobs (the crontab), and starts the jobs that are due. A
crontab line has five time fields and then the command:

```
minute  hour  day-of-month  month  day-of-week   command
```

A star means "every". So `0 8 * * 1` means: minute 0 of hour 8, any day, any month, when the weekday is Monday, which is
every Monday at 8:00. A few more:

| Line | Meaning |
|------|---------|
| `*/15 * * * *` | every 15 minutes |
| `30 2 * * *` | every day at 02:30 |
| `0 9 1 * *` | the first day of every month at 09:00 |
| `* * * * *` | every minute (what we use for the demo) |

### 13. Four traps, one crontab at a time

Each crontab file is one step of the story. Install one, wait one or two minutes, and look at the log and at Mailpit.
Use `date` in the box to see its clock (it runs UTC).

**Version 0: one line, no output.** `crontab.v0` is `* * * * * python job.py`.

```bash
docker exec m22l01-cron crontab /app/crontab.v0
docker exec m22l01-cron crontab -l
```

```
* * * * * python job.py
```

Wait two minutes and count the messages in Mailpit (`uv run mailcount.py`). Still 1, and no error anywhere.
Cron did run the line, but a cron job's output is sent as mail to the local user, and the box has no mail program, so it
is thrown away. A job that fails in silence is the worst kind. The fix: write everything to a file.

**Version 1: log to a file.** `crontab.v1` adds `>> /app/logs/job.log 2>&1` (`>>` appends the normal output, `2>&1` sends
the error messages to the same place).

```bash
docker exec m22l01-cron crontab /app/crontab.v1
sleep 70
docker exec m22l01-cron cat /app/logs/job.log
```

```
/bin/sh: 1: python: not found
```

By hand, `python` works because your shell has a long `PATH`. Cron starts a job with a tiny `PATH`: only `/usr/bin` and
`/bin`. Here Python lives in `/usr/local/bin`.

**Version 2: set `PATH`.** `crontab.v2` has a `PATH=/usr/local/bin:/usr/bin:/bin` line at the top and the full path of the
script.

```bash
docker exec m22l01-cron crontab /app/crontab.v2
: > cronapp/logs/job.log
sleep 70
docker exec m22l01-cron cat /app/logs/job.log | tail -2
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/enrollments_week.xlsx'
```

(The log shows the whole traceback; this is its last line.) The path is relative, and cron starts the job in the home
folder, not in the project folder. The fix: go to the folder first, or use full paths everywhere.

**Version 3: `cd /app &&`.** `crontab.v3` is `* * * * * cd /app && python job.py >> /app/logs/job.log 2>&1`.

```bash
docker exec m22l01-cron crontab /app/crontab.v3
: > cronapp/logs/job.log
sleep 70
docker exec m22l01-cron cat /app/logs/job.log | tail -2
```

```
    host = os.environ["SMTP_HOST"]
           ~~~~~~~~~~^^^^^^^^^^^
  File "<frozen os>", line 709, in __getitem__
KeyError: 'SMTP_HOST'
```

The report was written, and then the email step could not find its settings. The variables you set in your own terminal
are not there: cron gives a job its own environment, with none of your variables and no virtual environment. The fix: set
them in the crontab, at the top.

**Version 4: the final crontab.**

```
PATH=/usr/local/bin:/usr/bin:/bin
SMTP_HOST=m22l01-mail
SMTP_PORT=1025
SMTP_USER=asha
SMTP_PASSWORD=demo-only
* * * * * cd /app && python job.py >> /app/logs/job.log 2>&1
```

The password is a throw-away demo value. On a real server you keep the settings in a file that only your user can read,
and load it first. Install it, then touch nothing for about three minutes:

```bash
docker exec m22l01-cron crontab /app/crontab.v4
: > cronapp/logs/job.log
sleep 200
docker exec m22l01-cron cat /app/logs/job.log
uv run mailcount.py
```

```
2026-10-29 16:19:01,645 INFO report sent: 4 courses
2026-10-29 16:20:01,958 INFO report sent: 4 courses
2026-10-29 16:21:02,164 INFO report sent: 4 courses
messages in Mailpit: 4
```

Three log lines, one for each minute, one minute apart (your times will differ, and they are UTC; if you waited a few
seconds longer you may see a fourth line), and three new emails in Mailpit next to the one from the run by hand. Cron ran
the job all by itself.

For the real job, the line is `0 8 * * 1 cd /app && python job.py >> /app/logs/job.log 2>&1`: every Monday at 8:00, by the
clock of the machine where cron runs. Windows has the Task Scheduler and macOS has launchd for the same job, in other file
formats. We did not touch them.

### 14. The `schedule` library

`demo_schedule.py` runs jobs inside your own Python program:

```bash
uv run demo_schedule.py
```

```
Job(interval=4, unit=seconds, do=job, args=(), kwargs={})
Job(interval=1, unit=weeks, do=job, args=(), kwargs={})
report runs at 21:43:59
report runs at 21:44:03
```

Two planned jobs are listed, then the four-second job runs again and again (your times will differ). The Monday job waits
for Monday. Press Ctrl+C to stop; you will see a `KeyboardInterrupt` traceback, which is normal for a loop that never
ends. It is simple and works on any system, but your program must keep running: if it stops, or the computer restarts,
nothing runs and nobody catches up.

Three ways to keep time:

- **cron**: the system starts your script, even after a restart. Good for one script on one server.
- **the `schedule` library**: a loop inside your program. Good when the program runs all day anyway, like a small bot.
- **Celery beat** (M18-L02): a clock that sends tasks to workers. Good when you already have workers and many tasks. Its
  `crontab` schedule takes the same five fields.

## Common mistakes

- Moving files without a dry run: two files with the same new name replace each other, silently.
- Forgetting that `openpyxl` stores formulas but never calculates them: a freshly written file has no numbers in its
  formula cells until a spreadsheet program opens it.
- Putting a password in the code. Read it from the environment.
- Letting cron's output disappear. Always redirect it to a log file (`>> file 2>&1`).
- Trusting your terminal's `PATH`, working folder and variables inside cron. Cron has a tiny `PATH`, starts in the home
  folder, has none of your variables and no virtual environment. Use full paths or `cd` first, the full path of the right
  Python, and set the variables in the crontab.
- Not testing with a bare environment: run the same line by hand with only the crontab's settings.

Five habits for a script that runs alone: a dry run first; full paths (or move to the folder first); settings from the
environment; a log file with times; and make it safe to run twice.

## Clean up

```bash
docker rm -f -v m22l01-cron m22l01-mail
docker network rm m22l01-net
docker rmi m22l01-cron:demo m22l01-lo
rm -rf downloads cronapp report.xlsx report.pdf report.png
```

(`docker rmi` complains about an image you never built, such as `m22l01-lo`: that is fine.) If you worked in a copy
(`~/boring`), delete that folder when you are done.

## Next

[M22-L02 · Web Scraping and APIs](../m22-l02-web-scraping-and-apis/)
