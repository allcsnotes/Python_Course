# M07-L01 · Splitting Code into Modules

> Video: Module 7, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What a module is: a Python file that other files can borrow from
- The three import forms: `import lines`, `from lines import parse_line`, and `import counting as cnt` (and why `from x import *` is a trap)
- What `import` really does: find the file, run it once, remember it in `sys.modules`
- The `if __name__ == "__main__":` guard, so test code does not run when a file is imported
- Where Python looks for files (`sys.path`), and the two errors you will meet: `ModuleNotFoundError` and `ImportError`
- File names that cause trouble: shadowing `random.py` / `json.py`, and hyphens in names

## Before you start

- Python 3.14 or newer. Check with `python --version` (on some systems the command is `python3`).
- No Docker needed. No earlier lesson folder is needed: this lesson brings its own copy of Asha's log analyser, in the version from before the split.
- Open a terminal in this folder (`m07-l01-splitting-code-into-modules`).

## Files in this folder

| File | What it is |
|------|------------|
| `make_log.py` | Makes a fake `server.log` with 6000 lines (6 of them broken on purpose) for allcsvideos.com |
| `before/analyser.py` | Asha's log analyser as ONE file, 113 lines. The starting point |
| `steps/step1/` | After step 1: `lines.py` is cut out, `analyser.py` says `import lines` |
| `steps/step2/` | After step 2: `counting.py` is cut out too |
| `steps/step3/` | After step 3: `reports.py` is cut out, `analyser.py` is only the boss |
| `project/` | The finished project: four files, with the `__main__` guards |
| `demos/twice/` | A file imported twice runs once (`start.py`, `seen.py`) |
| `demos/guard/` | `show.py` and `use.py`: what `__name__` is |
| `demos/logtool/` | `where.py` prints `sys.path`; `typo.py` and `badimport.py` fail on purpose |
| `demos/shadow/` | Your own `random.py` and `json.py` hiding the real ones |
| `demos/star/` | The star-import trap |
| `demos/alias/` | `import counting as cnt` |
| `demos/hyphen/` | A file with a hyphen in its name, which cannot be imported |

## Follow along

Every step runs in its own folder, so the files always find each other. Replace `python` with `python3` if needed.

### 1. Make the log and run the single-file analyser

```bash
python make_log.py
cp server.log before/
cd before
python analyser.py
cd ..
```

You should see:

```
Wrote 6000 lines to server.log
Read 6000 lines.
Skipped 6 bad lines.
Reports are in the report folder.
```

`before/report/` now holds `report.txt`, `errors_per_hour.csv` and `summary.json`. Keep it: at the end we compare the split program against it.

### 2. Step 1: cut out `lines.py`

Open `before/analyser.py`. At the top are the date format `FORMAT`, the set `LEVELS` and the function `parse_line`. Cut them into a new file `lines.py`. `parse_line` uses `datetime`, so `from datetime import datetime` moves with it: a module brings its own imports.

In `analyser.py`, add `import lines` and change the call from `parse_line(line)` to `lines.parse_line(line)` (the drawer name, a dot, the tool name; the same pattern as `math.sqrt`). The result is in `steps/step1/`:

```bash
cp server.log steps/step1/
cd steps/step1
python analyser.py
cd ../..
```

```
Read 6000 lines.
Skipped 6 bad lines.
Reports are in the report folder.
```

Same three lines as before. The user cannot tell the code now lives in two files: same behaviour, better structure.

### 3. The second import form

Instead of `import lines` you may write `from lines import parse_line`. Then you call `parse_line(line)` directly, without `lines.` in front. Both are fine. Use the first when a bare name could be confusing, the second for a tool you call often. The project uses both.

### 4. Step 2 and step 3: `counting.py` and `reports.py`

Step 2 moves `analyse` to `counting.py`. It brings `import re` and `from collections import Counter`, and since it calls `parse_line`, it does `import lines` itself. `analyser.py` keeps one line for it: `from counting import analyse`.

Step 3 moves the three writers (`write_report`, `write_csv`, `write_json`) to `reports.py`, with `import csv` and `import json`. `analyser.py` now imports all three in one line, with commas:

```python
from counting import analyse
from reports import write_csv, write_json, write_report
```

Run each snapshot to check that every step is safe:

```bash
cp server.log steps/step2/ && (cd steps/step2 && python analyser.py)
cp server.log steps/step3/ && (cd steps/step3 && python analyser.py)
```

Both print the same three lines as before.

### 5. The third form: `import ... as ...`

`demos/alias/alias.py` gives the module a nickname that works in this file only:

```python
from pathlib import Path

import counting as cnt

result = cnt.analyse(Path("server.log"))
print(result["total"])
```

```bash
cp server.log demos/alias/
cd demos/alias
python alias.py
cd ../..
```

```
6000
```

You will meet nicknames a lot with libraries in later lessons.

### 6. The trap: `from lines import *`

`demos/star/star.py`:

```python
from lines import *
from reports import *

print(FORMAT)
```

```bash
cd demos/star
python star.py
cd ../..
```

```
%d %b %Y
```

That is not the date format from `lines.py` (`%Y-%m-%d %H:%M:%S`). `reports.py` in this demo also has a name `FORMAT`, and the second star import silently replaced the first: no error, no warning. With a star you cannot tell where a name came from, and a later import can overwrite an earlier one. Rule: no star imports in real code. List the names you need.

### 7. What `import` does: find, run once, remember

`demos/twice/lines.py` has a `print("lines.py is loading")` at the very top. `start.py` imports `counting` (which imports `lines`) and then imports `lines` again:

```bash
cd demos/twice
python start.py
python seen.py
cd ../..
```

```
lines.py is loading
both imported
False
lines.py is loading
True
```

The message prints once. The first import ran `lines.py` and wrote `lines` into `sys.modules`, the dictionary of every module loaded so far. The second import found it there and did not run the file again. `seen.py` asks `"lines" in sys.modules` before and after the import: False, then True. So a module's code runs once, at the first import, however many files import it. The top of a module therefore should mostly hold definitions (functions and constants), not code that does things.

### 8. Add the `__main__` guard

Asha wants a quick self test at the bottom of `lines.py`. Without a guard, every program that imports `lines` would print the test line first. First see the name tag, `__name__` (said "dunder name": double underscore each side). `demos/guard/show.py` is one line, `print("my name is", __name__)`, and `use.py` is `import show`:

```bash
cd demos/guard
python show.py
python use.py
cd ../..
```

```
my name is __main__
my name is show
```

Run directly, a file is called `__main__`. Imported, it is called by its own file name. So the guard reads: "if this file is the one I started". It is already in the finished `project/lines.py`:

```python
if __name__ == "__main__":
    sample = "2026-03-12 14:05:09 ERROR Payment failed for order 512"
    print(parse_line(sample))
```

and `project/analyser.py` ends with:

```python
if __name__ == "__main__":
    main()
```

### 9. Run the finished project and compare

```bash
cp server.log project/
cd project
python lines.py
python analyser.py
cd ..
```

```
(datetime.datetime(2026, 3, 12, 14, 5, 9), 'ERROR', 'Payment failed for order 512')
Read 6000 lines.
Skipped 6 bad lines.
Reports are in the report folder.
```

The test prints only when you start `lines.py` yourself. Now compare with the single-file result:

```bash
diff -r project/report before/report && echo identical
```

```
identical
```

Four files: `analyser.py` (25 lines, reads like a table of contents), `counting.py` (32), `lines.py` (20), `reports.py` (48). Nothing changed except the structure.

After a run, Python may leave a `__pycache__` folder in `project/` with cached copies of `counting`, `lines` and `reports` (none for `analyser.py`, because the file you run directly is not cached). It is safe to delete. (If you do not see it, your environment may set `PYTHONDONTWRITEBYTECODE`.)

### 10. Where Python looks: `sys.path`

`demos/logtool/where.py` prints the first three entries of `sys.path`:

```python
import sys

for folder in sys.path[:3]:
    print(folder)
```

Stand one folder higher and run it:

```bash
cd demos
python logtool/where.py
cd ..
```

```
/path/to/m07-l01-splitting-code-into-modules/demos/logtool
/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python314.zip
/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14
```

Yours will differ in the exact paths. The first folder is the folder of the script, not the folder where your terminal stands. The next ones belong to the standard library. Keep your files together in one folder and imports between them just work (lesson 2 shows what to do with many folders).

### 11. Two errors you will meet

```bash
cd demos/logtool
python typo.py
python badimport.py
cd ../..
```

`typo.py` is `import report` (a typo for `reports`):

```
Traceback (most recent call last):
  File ".../demos/logtool/typo.py", line 1, in <module>
    import report
ModuleNotFoundError: No module named 'report'
```

Python searched every folder on the list and found nothing. Check the spelling and that the file is next to your script.

`badimport.py` is `from reports import write_html`:

```
Traceback (most recent call last):
  File ".../demos/logtool/badimport.py", line 1, in <module>
    from reports import write_html
ImportError: cannot import name 'write_html' from 'reports' (.../demos/logtool/reports.py)
```

This time the file was found, but it has no tool with that name. Check the spelling inside the file.

### 12. Shadowing: a file named like a standard module

`demos/shadow/` has Asha's helper `random.py`, and a `json.py` that prints a message when it loads. `draw.py` does `import random` and calls `random.choice`; `summary.py` does `import json`:

```bash
cd demos/shadow
python draw.py
python summary.py
cd ../..
```

```
Traceback (most recent call last):
  File ".../demos/shadow/draw.py", line 4, in <module>
    print(random.choice(students))
          ^^^^^^^^^^^^^
AttributeError: module 'random' has no attribute 'choice' (consider renaming '.../demos/shadow/random.py' since it has the same name as the standard library module named 'random' and prevents importing that standard library module)
```

```
my own json file
Traceback (most recent call last):
  File ".../demos/shadow/summary.py", line 3, in <module>
    print(json.dumps({"total": 6000}))
          ^^^^^^^^^^
AttributeError: module 'json' has no attribute 'dumps' (consider renaming '.../demos/shadow/json.py' since it has the same name as the standard library module named 'json' and prevents importing that standard library module)
```

The script's folder comes first on `sys.path`, so Python used Asha's file and never opened the real drawer. A clue: if you see output you did not expect from an import, look for a file with the same name. The fix is to rename your file.

### 13. Hyphens in file names

`demos/hyphen/log-tools.py` exists, but `main.py` (`import log-tools`) fails:

```bash
cd demos/hyphen
python main.py
cd ../..
```

```
  File ".../demos/hyphen/main.py", line 1
    import log-tools
              ^
SyntaxError: invalid syntax
```

Python reads `log-tools` as `log` minus `tools`. Name modules with lowercase letters, digits and underscores (`log_tools.py`).

## Common mistakes

- Copying a function into another file instead of importing it: the two copies drift apart.
- Forgetting that a module lists its own imports. `lines.py` needs `from datetime import datetime` itself.
- Using `from x import *`: you cannot tell where a name comes from, and a later import silently overwrites an earlier one.
- Putting code that does things at the top of a module: it runs at import time, once. Use the `__main__` guard.
- Naming your file `random.py`, `json.py`, `csv.py`, `math.py`, `time.py`, `string.py`, `email.py` or `test.py`. It shadows the real module.
- Spaces or hyphens in file names. Use lowercase letters, digits and underscores.
- Thinking the terminal's folder matters. The folder of the script you run comes first.

## Clean up

Run these from this folder to remove what the lesson created:

```bash
rm -rf server.log before/server.log before/report before/__pycache__
rm -rf steps/*/server.log steps/*/report steps/*/__pycache__
rm -rf project/server.log project/report project/__pycache__
rm -rf demos/*/__pycache__ demos/alias/server.log
```

## Next

Four files in one folder is easy. What about forty? Continue with [M07-L02 · Packages and Project Layout](../m07-l02-packages-and-project-layout/README.md).
