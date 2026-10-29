# M07-L02 · Packages and Project Layout

> Video: Module 7, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What a package is: a folder of modules with an `__init__.py` file, and how dotted names read like an address
- That `__init__.py` runs once, on the first import, and can be used to expose a few useful names
- Absolute imports (`from allcsvideos.courses import price_of`) and relative imports (`from .courses import price_of`)
- Why a relative import fails when you run the file directly, and the fix: `python -m`
- The flat layout versus the `src` layout, and why real projects use `src`
- What a circular import is, how to read the error, and two fixes

## Before you start

- Python 3.14 or newer. Check with `python --version` (on some systems the command is `python3`).
- No Docker needed.
- Lesson M07-L01 (modules, `import`, `sys.path`, `__name__`) is assumed. This lesson does not need any files from it.
- Every example is a small project in its own numbered folder. Run each command from the folder named in the step (the "project folder").

## Files in this folder

| Folder | What it is |
|--------|------------|
| `01-first-package/` | The package `allcsvideos` with `courses.py` and `billing.py`, and `main.py` outside it |
| `02-no-init/` | The same import, but the package folder has no `__init__.py` |
| `03-init-runs-once/` | `__init__.py` with a `print` line, to show it runs once |
| `04-relative-import/` | `billing.py` with a relative import, plus `whoami.py` that prints `__name__` and `__package__` |
| `05-absolute-import/` | `billing.py` with an absolute import, run directly (fails) and with `-m` (works) |
| `06-init-shortcut/` | `__init__.py` re-exports `price_of`, so `from allcsvideos import price_of` works |
| `07-flat-layout/` | Flat layout: package, `check.py` and `tests/` side by side |
| `08-src-layout/` | `src` layout: `pyproject.toml`, `src/allcsvideos/`, `tests/` |
| `09-circular-import/` | `students.py` and `courses.py` import each other (fails) |
| `10-fix-third-module/` | Fix 1: shared code moved to `enrollments.py` |
| `11-fix-import-inside/` | Fix 2: the import moved inside the function |
| `12-hyphen-folder/` | A package folder named `my-app` (fails) |

Replace `python` with `python3` if needed. Paths in error messages below are shortened to `~`; yours will show your real folder.

## Follow along

### 1. Your first package

The outer folder is the project, the inner folder `allcsvideos` is the package. Having the same name twice is normal. `main.py` sits outside the package and starts the program.

```
01-first-package/
  main.py
  allcsvideos/
    __init__.py      (empty)
    courses.py
    billing.py
```

`allcsvideos/courses.py`:

```python
PRICES = {"Python Basics": 999, "Web Dev": 1499}


def price_of(title):
    return PRICES[title]
```

`allcsvideos/billing.py` (the full address, from the top of the project):

```python
from allcsvideos.courses import price_of


def total(titles):
    amount = 0
    for title in titles:
        amount += price_of(title)
    return amount


if __name__ == "__main__":
    print(total(["Python Basics", "Web Dev"]))
```

`main.py`:

```python
import allcsvideos.courses
from allcsvideos.billing import total

print(allcsvideos.courses.price_of("Web Dev"))
print(total(["Python Basics", "Web Dev"]))
```

Run it from the project folder:

```bash
cd 01-first-package
python main.py
cd ..
```

```
1499
2498
```

Read `allcsvideos.courses.price_of` like an address, from big to small: in the folder `allcsvideos`, the file `courses`, the function `price_of`.

### 2. Is `__init__.py` really needed?

`02-no-init/` has the same package folder with no `__init__.py`:

```bash
cd 02-no-init
python main.py
cd ..
```

```
1499
```

Modern Python allows it. We still add the file, because tools expect it and because it gives you a place for setup code. The habit: every package folder gets an `__init__.py`.

### 3. `__init__.py` runs once

In `03-init-runs-once/`, `__init__.py` holds one line, `print("allcsvideos is loading")`. `main.py` imports from the package twice (`import allcsvideos.courses` and `from allcsvideos.billing import total`):

```bash
cd 03-init-runs-once
python main.py
cd ..
```

```
allcsvideos is loading
both imports done
```

Once. Python runs `__init__.py` the first time it needs the package and remembers it in `sys.modules`. Keep `__init__.py` short: everything in it runs on the first import, even when someone wanted one small function.

### 4. Relative imports, and the famous error

In `04-relative-import/`, `billing.py` uses a relative import. One dot means "this same package"; `from . import courses` imports the whole module; two dots would mean one folder up.

```python
from .courses import price_of
```

Run it directly, the way you run any other file:

```bash
cd 04-relative-import
python allcsvideos/billing.py
```

```
Traceback (most recent call last):
  File "~/04-relative-import/allcsvideos/billing.py", line 1, in <module>
    from .courses import price_of
ImportError: attempted relative import with no known parent package
```

A dot means "my package", but a file run directly is a lone script: it does not know it lives in a package. See it with `allcsvideos/whoami.py`, which is `print(__name__, "|", __package__)`:

```bash
python allcsvideos/whoami.py
python -m allcsvideos.whoami
```

```
__main__ | None
__main__ | allcsvideos
```

`-m` means "run this as a module of a package". Use the dotted name, with no `.py` at the end. Now the fix:

```bash
python -m allcsvideos.billing
cd ..
```

```
2498
```

### 5. The absolute version, run directly

`05-absolute-import/` has the absolute import in `billing.py`:

```bash
cd 05-absolute-import
python allcsvideos/billing.py
```

```
Traceback (most recent call last):
  File "~/05-absolute-import/allcsvideos/billing.py", line 1, in <module>
    from allcsvideos.courses import price_of
ModuleNotFoundError: No module named 'allcsvideos'
```

The first folder on `sys.path` is the folder of the script you run: `allcsvideos/` itself, and inside it there is no folder called `allcsvideos`. The project folder, one level up, was never searched. With `-m`, run from the project folder, Python starts its search there:

```bash
python -m allcsvideos.billing
cd ..
```

```
2498
```

The rule: run code that lives in a package with `python -m ...` from the project folder, or start it from a small file at the top, like `main.py`. PEP 8 recommends absolute imports (clearest, same everywhere); relative imports are fine inside a package and survive renaming it. Many teams pick one and stick to it.

### 6. Use `__init__.py` as a shortcut

`06-init-shortcut/allcsvideos/__init__.py` has one relative import:

```python
from .courses import price_of
```

Now `price_of` sits directly on the package, and `main.py` can say:

```python
from allcsvideos import price_of

print(price_of("Python Basics"))
```

```bash
cd 06-init-shortcut
python main.py
cd ..
```

```
999
```

Use this only for the few names other people use most. It also hides your internal file names.

### 7. Flat layout

In `07-flat-layout/`, the package sits right next to `check.py` and `tests/`:

```
07-flat-layout/
  check.py
  allcsvideos/
    __init__.py
    courses.py
  tests/
    test_courses.py
```

`check.py` is `import allcsvideos` then `print(allcsvideos.__file__)`:

```bash
cd 07-flat-layout
python check.py
cd ..
```

```
~/07-flat-layout/allcsvideos/__init__.py
```

It found the local folder, simply because it was next to the file. Nothing was installed. That is the trap: when you test, you want to test the installed copy your users get, but the local folder sneaks in first, so a test can pass on your laptop while the installed copy is broken.

### 8. `src` layout

The package moves one level down into `src/`. `tests/` sits beside it (never inside), and `pyproject.toml` holds the project settings (lesson M07-L03 explains it).

```
08-src-layout/
  pyproject.toml
  check.py
  src/
    allcsvideos/
      __init__.py
      courses.py
  tests/
    test_courses.py
```

`pyproject.toml` here is just the start:

```toml
[project]
name = "allcsvideos"
```

Run the same check:

```bash
cd 08-src-layout
python check.py
cd ..
```

```
Traceback (most recent call last):
  File "~/08-src-layout/check.py", line 1, in <module>
    import allcsvideos
ModuleNotFoundError: No module named 'allcsvideos'
```

This is the good news: nothing is importable by accident. You must install the project first, so every test uses the real installed copy. That is exactly what lesson M07-L03 does. Flat layout is fine for a quick script; for a real project, use `src`.

### 9. A circular import

In `09-circular-import/`, `students.py` needs `seats_left` from `courses.py`, and `courses.py` needs `enrolled_count` from `students.py`. Each file imports the other on its first line.

`allcsvideos/students.py`:

```python
from allcsvideos.courses import seats_left

ENROLLED = {"Python Basics": ["Lukas", "Priya"]}


def enrolled_count(title):
    return len(ENROLLED[title])


def describe(name, title):
    left = seats_left(title)
    return f"{name}: {left} seats left in {title}"
```

`allcsvideos/courses.py`:

```python
from allcsvideos.students import enrolled_count

SEATS = {"Python Basics": 30}


def seats_left(title):
    return SEATS[title] - enrolled_count(title)
```

`main.py` is `from allcsvideos.students import describe` and `print(describe("Lukas", "Python Basics"))`.

```bash
cd 09-circular-import
python main.py
cd ..
```

```
Traceback (most recent call last):
  File "~/09-circular-import/main.py", line 1, in <module>
    from allcsvideos.students import describe
  File "~/09-circular-import/allcsvideos/students.py", line 1, in <module>
    from allcsvideos.courses import seats_left
  File "~/09-circular-import/allcsvideos/courses.py", line 1, in <module>
    from allcsvideos.students import enrolled_count
ImportError: cannot import name 'enrolled_count' from partially initialized module 'allcsvideos.students' (most likely due to a circular import) (~/09-circular-import/allcsvideos/students.py)
```

Follow it: `main` loads `students`; on its first line `students` asks for `courses`; on its first line `courses` asks for `students`. But `students` is stuck on line 1 and has not defined `enrolled_count` yet, so Python finds the module half built ("partially initialized") and stops.

### 10. Fix 1: move shared code to a third module

`10-fix-third-module/` moves `ENROLLED` and `enrolled_count` into `allcsvideos/enrollments.py`. `courses.py` now starts with `from allcsvideos.enrollments import enrolled_count`; `students.py` keeps only `describe` and imports `seats_left` from `courses`. The arrows run one way, so there is no circle.

```bash
cd 10-fix-third-module
python main.py
cd ..
```

```
Lukas: 28 seats left in Python Basics
```

### 11. Fix 2: import inside the function

`11-fix-import-inside/allcsvideos/courses.py` drops the first line and imports where it is needed:

```python
SEATS = {"Python Basics": 30}


def seats_left(title):
    from allcsvideos.students import enrolled_count
    return SEATS[title] - enrolled_count(title)
```

```bash
cd 11-fix-import-inside
python main.py
cd ..
```

```
Lukas: 28 seats left in Python Basics
```

An import inside a function runs only when the function is called, by which time both modules are fully loaded. Fix 1 is the cleaner design and removes the circle for good; fix 2 is a quick patch. A circle often hints that two files are really one idea, or share a third idea that deserves its own file.

### 12. A hyphen in a package folder name

`12-hyphen-folder/` has a package folder called `my-app` and `main.py` is `import my-app`:

```bash
cd 12-hyphen-folder
python main.py
cd ..
```

```
  File "~/12-hyphen-folder/main.py", line 1
    import my-app
             ^
SyntaxError: invalid syntax
```

Python reads the dash as a minus sign. Use an underscore (`my_app`). By convention, package names are short and all lowercase.

## Common mistakes

- Running a package file with `python path/to/file.py` and getting "attempted relative import with no known parent package". Run `python -m package.module` from the project folder.
- Forgetting that the first folder on `sys.path` is the folder of the script you run, so `No module named 'allcsvideos'` appears when you run a file inside the package directly.
- Hyphens (or spaces) in a package folder name. Use lowercase and underscores.
- Putting a lot of code in `__init__.py`: it runs on every first import.
- Two files that import each other at the top. When you see "partially initialized", think circle: move shared code to a third module, or import inside the function.
- Putting `tests/` inside the package, so tests are shipped to users. Keep it beside `src/`.

## Interview question

Rahul asks: what is a circular import, and how do you fix it? Model answer: module A imports module B while B imports A, so one of them is only partly loaded when the other asks for a name, and Python raises an import error. I fix it by moving the shared code into a third module, so imports only go one way. As a quick patch, I import inside the function that needs it.

## Clean up

Nothing to clean up if you only ran the commands above with Python's default settings, apart from `__pycache__` folders, which are safe to delete:

```bash
find . -name __pycache__ -type d -exec rm -rf {} +
```

## Next

Continue with [M07-L03 · Virtual Environments and uv Projects](../m07-l03-virtual-environments-and-uv-projects/README.md), where the `src` layout project gets installed for real.
