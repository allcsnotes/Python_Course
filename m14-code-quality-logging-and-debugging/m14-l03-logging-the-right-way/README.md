# M14-L03 · Logging the Right Way

> Video: Module 14, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- Why logging beats `print`, and the five levels (10 to 50) and the "volume dial"
- Logger, handler, formatter: who writes, where it goes, how it looks
- `basicConfig`, one logger per file with `getLogger(__name__)`, and the logger family tree
- Why values are passed as arguments (`%s`), not f-strings
- Log files, rotating files, `logger.exception`, JSON lines, and testing logs with `caplog`
- Three traps: doubled handlers, `basicConfig` that does nothing, and secrets in logs

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `pytest` for the last section: `pip install pytest` in a virtual environment (or `uv add --dev pytest`). The video used pytest 9.1.1.
- No Docker needed. Earlier lessons: M14-L02 (debugging), M06 (the log analyser, tracebacks).
- Run each command from inside this folder. Lines that contain a date or time ("yours will differ") change on every run.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py`, `levels.py` | The "where did my messages go?" hook and the level numbers |
| `basic.py`, `basic_error.py` | `basicConfig` with level INFO, then level ERROR |
| `payments.py`, `app.py` | A module that only gets a logger, and a main file that configures logging |
| `hier.py` | Logger family tree (`shop` and `shop.payments`) |
| `lazy.py` | `%s` arguments versus an f-string |
| `handlers.py` | One logger, two handlers (screen at INFO, file at DEBUG) |
| `rotate.py` | A rotating file handler |
| `oops.py` | `logger.error` versus `logger.exception` |
| `jsonlog.py`, `make_events.py`, `count_levels.py` | A JSON formatter, five log calls, and a reader that counts levels |
| `enrol.py`, `test_enrol.py`, `test_quiet.py` | A function that logs, and tests with `caplog` (one passing, one that fails on purpose) |
| `threads.py` | `%(threadName)s` in the format |
| `dup.py`, `dup_fix.py` | Trap one: handlers added twice, and the fix |
| `late.py`, `late_fix.py` | Trap two: `basicConfig` called too late, and `force=True` |
| `secret.py` | Trap three: a password in the log (fake demo value) |

## Follow along

### 1. Four logging calls, but only two lines

`hook.py` has `logging.debug`, `info`, `warning`, `error` (one call each).

```bash
python hook.py
```

```text
WARNING:root:card expires soon
ERROR:root:payment failed
```

Two lines, and each starts with level, a colon, `root`, a colon, the message. Where did debug and info go, and who is `root`?

### 2. Why not print, and the five levels

`print` has no time, no importance, you cannot turn the chatty lines off, and it has one place to go (the screen). Logging fixes all four. Every message has a level (a number for how serious it is) and the logger has a threshold, the dial. Only messages at or above the dial get through.

| Level | Number | Use |
|-------|--------|-----|
| DEBUG | 10 | small details for the developer |
| INFO | 20 | normal events, like a student enrolled |
| WARNING | 30 | something odd, program carries on |
| ERROR | 40 | something failed |
| CRITICAL | 50 | the program may not be able to go on |

```bash
python levels.py
```

```text
10 20 30
40 50
30
```

The root logger's dial is 30, so by default only WARNING and above get through. That is where debug (10) and info (20) went.

The three parts: a logger writes the note, handlers send copies of it to places (screen, file), a formatter decides how each line looks.

### 3. The quick setup: basicConfig

`basic.py` calls `logging.basicConfig` once, at the start, with `level`, `format` and `datefmt`. In the format, `%(asctime)s` is the time, `%(levelname)s` the level name, `%(message)s` your text; everything else is copied as is.

```bash
python basic.py
```

```text
2026-10-26 09:01:01 INFO charging Lukas
2026-10-26 09:01:01 WARNING card expires soon
2026-10-26 09:01:01 ERROR payment failed
```

(Yours will show today's date and time.) Debug is below INFO, so it is dropped. This is exactly the shape of the server log from Module 6. Now move the dial: `basic_error.py` is the same with `level=logging.ERROR`.

```bash
python basic_error.py
```

```text
2026-10-26 09:01:01 ERROR payment failed
```

### 4. One logger per file

`payments.py` only gets a logger (`logging.getLogger(__name__)`, named `payments` inside that file) and writes to it. `app.py` is the main file: it calls `basicConfig` once (level DEBUG, with the logger name in the format) and charges Lukas 499 and Priya 0.

```bash
python app.py
```

```text
INFO __main__: app started
INFO payments: charging Lukas Rs 499
DEBUG payments: payment accepted
INFO payments: charging Priya Rs 0
WARNING payments: nothing to charge for Priya
```

The first line says `__main__` because `app.py` is the file you started. `%s` is a hole for text, `%d` a hole for a whole number; the values come after the message as arguments.

Names can form a family tree with dots: `shop.payments` is a child of `shop`, and a child follows its parent's level unless it has its own.

```bash
python hier.py
```

```text
shop: parent error
```

The child's warning was held back by the parent's dial of ERROR. With names like `allcsvideos.payments`, one line can quieten a whole package.

Rule: modules only get a logger. Only the main program configures logging, once.

### 5. Arguments, not f-strings

`lazy.py` has a `Report` class whose `__str__` prints "building the text..." every time it is called (it stands in for a slow job). The dial is INFO. Three calls: debug with `%s`, debug with an f-string, info with `%s`.

```bash
python lazy.py
```

```text
building the text...
building the text...
INFO:lazy:info: big report
```

Two builds only: the first call was thrown away before the text was built. The f-string builds the text before logging is even called, so that work is wasted. (The two lines may print in a different order on your machine because the log goes to a different stream than `print`; the content is the same.) Pass values as arguments.

### 6. Handlers: screen and file

`handlers.py` makes the logger `allcsvideos` at level DEBUG, one formatter, a screen handler at INFO and a file handler (`app.log`) at DEBUG. A message must pass the logger's dial first, then each handler's own dial.

```bash
python handlers.py
cat app.log
```

```text
2026-10-26 09:01:02 INFO allcsvideos charging Lukas
2026-10-26 09:01:02 ERROR allcsvideos payment failed
2026-10-26 09:01:02 DEBUG allcsvideos cart has two items
2026-10-26 09:01:02 INFO allcsvideos charging Lukas
2026-10-26 09:01:02 ERROR allcsvideos payment failed
```

The first two lines are the screen (info and error); the `cat` shows the file with three, including the debug line. The date and time are yours.

### 7. A rotating file

A file that grows forever fills the disk. `RotatingFileHandler` starts a fresh file when the old one is full: `maxBytes` is the size limit (100 bytes here, only for the demo) and `backupCount` is how many old files to keep.

```bash
python rotate.py
ls audit.log*
head -1 audit.log.2
cat audit.log
```

```text
audit.log  audit.log.1  audit.log.2
line number 7
line number 19
```

(`ls` may print the names one per line.) Lines 0 to 6 are gone. Real servers use megabytes.

### 8. Errors with a traceback

`oops.py` logs a `ZeroDivisionError` twice: with `logger.error(..., err)` and with `logger.exception(...)`.

```bash
python oops.py
```

```text
ERROR could not count seats: division by zero
ERROR could not count seats
Traceback (most recent call last):
  File "oops.py", line 12, in <module>
    seats_left(2, 2)
    ~~~~~~~~~~^^^^^^
  File "oops.py", line 8, in seats_left
    return seats // (seats - taken)
           ~~~~~~^^~~~~~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

(The file path in your traceback is longer.) `logger.exception` is `logger.error` plus the traceback. Use it inside an `except` block. Logging an error is not the same as handling it: decide whether to carry on or raise it again.

### 9. Structured logs: JSON lines

`jsonlog.py` has a `JsonFormatter` that inherits from `logging.Formatter` and overrides `format`: it builds a dictionary (time, level, message, plus the extra fields `student` and `course` if present) and returns `json.dumps(data)`. `make_events.py` logs five events with `extra={"student": ...}`.

```bash
python make_events.py
head -2 app.jsonl
python count_levels.py
```

```text
{"time": "09:01:02", "level": "INFO", "message": "enrolled", "student": "Lukas"}
{"time": "09:01:02", "level": "INFO", "message": "enrolled", "student": "Priya"}
Counter({'INFO': 3, 'WARNING': 1, 'ERROR': 1})
```

(Times are yours.) Every line is a complete JSON object, so a program reads it with `json.loads`, no splitting. Real projects often use a ready-made JSON formatter package, but now you know what it does.

### 10. Testing logs with caplog

`enrol.py` logs an info line when a student is added and a warning if they are already there. `test_enrol.py` uses pytest's `caplog` fixture:

```bash
pytest -v test_enrol.py
```

```text
test_enrol.py::test_enrol_logs_info PASSED                               [ 50%]
test_enrol.py::test_double_enrol_warns PASSED                            [100%]

============================== 2 passed in 0.06s ===============================
```

Test two did not need `at_level` because WARNING is already at the default dial. Now the pitfall: `test_quiet.py` is test one without `caplog.at_level(logging.INFO)`.

```bash
pytest test_quiet.py --tb=short
```

```text
E   AssertionError: assert 'enrolled Lukas' in ''
FAILED test_quiet.py::test_enrol_logs_info - AssertionError: assert 'enrolled...
============================== 1 failed in 0.12s ===============================
```

Nothing was captured, because info is below the default dial of 30. Fix it with `with caplog.at_level(logging.INFO):`. (This test fails on purpose.)

### 11. Threads

```bash
python threads.py
```

```text
Thread-1 (send_email): emailing Lukas
Thread-2 (send_email): emailing Priya
```

`%(threadName)s` shows who wrote what. Logging is safe with threads: two threads never mix text inside one line. A format can also show the function name, line number and process number.

### 12. The three traps

Trap one: `setup()` adds a handler every time it is called.

```bash
python dup.py
python dup_fix.py
```

```text
payment failed
payment failed
payment failed
```

The first run prints the line twice (two handlers), the fixed one (`if not logger.handlers:`) prints it once.

Trap two: a library called `logging.warning` before your `basicConfig`, so the root logger was already set up and `basicConfig` quietly does nothing. Fix: `force=True`.

```bash
python late.py
python late_fix.py
```

```text
WARNING:root:early call
WARNING:root:early call
DEBUG: can we see this?
```

Trap three: no error at all. `secret.py` logs an email and a password (`hunter2` is a fake demo value):

```bash
python secret.py
```

```text
login: lukas@example.com hunter2
login: lukas@example.com
```

The first line is the problem: log files are copied, searched and sent to colleagues. Log who and what happened, never passwords, tokens or payment details.

## Common mistakes

1. Adding a handler every time a setup function runs: every line appears twice. Add a handler only if the logger has none, or configure once in the main program.
2. Calling `basicConfig` after something already logged: it does nothing and does not complain. Configure at the very start, or use `force=True`.
3. Logging secrets (passwords, tokens, payment details).
4. Using f-strings in log calls: the text is built even when the message is thrown away. Pass arguments with `%s`.
5. Forgetting `caplog.at_level(...)` when you test info or debug messages.

## Clean up

```bash
rm -f app.log app.jsonl audit.log audit.log.1 audit.log.2
rm -rf __pycache__ .pytest_cache
```

## Next

[M14-L04 · Design Patterns the Python Way](../m14-l04-design-patterns-the-python-way/)
