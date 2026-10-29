# M07-L03 · Virtual Environments and uv Projects

> Video: Module 7, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- Why one shared Python goes wrong: "works on my machine", and two projects fighting over one library version
- What a virtual environment is (a folder with its own Python and libraries), and how to make, activate and leave one with `python -m venv`
- The four `uv` commands that cover almost everything: `init`, `add`, `run`, `sync`
- What `pyproject.toml` (the project's ID card), `.python-version` and `uv.lock` (the exact receipt) do, and which ones you share
- How to install your own `src` layout project from lesson M07-L02 and see that it is importable
- Five pitfalls: wrong `pip`, copying `.venv`, leaving `uv.lock` behind, `pip install` inside a uv project, activating on Windows

## Before you start

- Python 3.14 or newer: `python --version` (on some systems the command is `python3`).
- `uv` installed (you did this in Module 1, lesson 2). Check with `uv --version`. This lesson was recorded with uv 0.13.5; newer versions print slightly different messages.
- No Docker needed. (The video ran the first demo inside a clean Docker container so the shared Python was untouched; here we use a throwaway folder instead. Nothing in this lesson installs anything globally.)
- Internet access, to download `httpx`, `rich` and `tzdata` from PyPI.
- Lesson M07-L02 (the `src` layout) is helpful for step 11.
- On Windows, replace `source .venv/bin/activate` with `.venv\Scripts\activate` and `which python` with `where python`.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs-site/main.py` | Asha's courses page: prints a table with the library `rich` |
| `allcs-site/tz.py` | Asha's time zone program from Module 6, lesson 5 (needs `tzdata` on Windows) |
| `allcs-site/pyproject.toml` | The ID card: name, version, `requires-python`, and dependencies `rich` and `tzdata` |
| `allcs-site/uv.lock` | The lock file: the exact version and hash of every package (never edit by hand) |
| `allcs-site/.python-version` | Which Python the project should run on (`3.14`) |
| `allcs-site/.gitignore` | Things Git must never save, including `.venv` |
| `allcs-site/README.md` | The empty note file that `uv init` creates |
| `allcsvideos/` | The `src` layout project made with `uv init allcsvideos`: `pyproject.toml`, `src/allcsvideos/__init__.py` and friends |

The folder `allcs-site/` is the project as it stands at the end of step 10, so you can skip straight to `uv sync` (step 11). You can also build it yourself from nothing, as the video does.

## Follow along

### 1. The problem: one shared shelf

Asha's `main.py` uses the library `rich`. It works on her laptop. Lukas runs the same file and gets `ModuleNotFoundError: No module named 'rich'`. Same file, same Python, different result: on Asha's shelf of libraries `rich` exists, on Lukas's it does not.

Problem two is nastier: libraries get new versions all the time, and a shared shelf has room for one version of each library. The classes project needs `httpx` 0.27.2, the reports project needs 0.28.1.

The video does this on a clean Python. To follow along without touching your own Python, we make a throwaway folder `shelf` that stands in for the shared Python:

```bash
python -m venv shelf
source shelf/bin/activate
python -m pip list
```

```
Package Version
------- -------
pip     26.2.1
```

(Your `pip` version may differ.) Only `pip`, the installer. Now the classes project wants the old version. The double `==` pins an exact version:

```bash
python -m pip install httpx==0.27.2
python -c "import httpx; print(httpx.__version__)"
```

pip prints many download lines. The last one:

```
Successfully installed anyio-4.15.1 certifi-2026.10.23 h11-0.16.0 httpcore-1.0.9 httpx-0.27.2 idna-3.20 sniffio-1.3.1 typing_extensions-4.16.0
```

```
0.27.2
```

Now the reports project asks for the newer one:

```bash
python -m pip install httpx==0.28.1
python -c "import httpx; print(httpx.__version__)"
```

```
    Found existing installation: httpx 0.27.2
    Uninstalling httpx-0.27.2:
      Successfully uninstalled httpx-0.27.2
Successfully installed httpx-0.28.1
0.28.1
```

pip threw the old version away to make room, so the classes project now runs on a version it was never tested with. One shelf means one version. The fix is to give every project its own shelf. Leave the stand-in:

```bash
deactivate
```

### 2. Your own virtual environment

A virtual environment is the Python plus the libraries it can see, made just for one project. Make a folder for the project, step inside, and build the box:

```bash
mkdir classes
cd classes
python -m venv .venv
ls -a
```

`-m` means "run a built-in module as a program"; the module is `venv`; `.venv` is the folder to create. The name is only a habit, and the dot keeps the folder out of the way. No message means done:

```
.  ..  .venv
```

### 3. What is inside the box

```bash
ls .venv
cat .venv/pyvenv.cfg
```

```
bin  include  lib  pyvenv.cfg
```

(Linux also shows `lib64`.) `bin` holds a private copy of the `python` command (on Windows: `Scripts`), `lib` holds the libraries (inside it, `site-packages`, the last room on Python's search list), `include` is for extras, and `pyvenv.cfg` says which Python built the box. The file looks like this (paths are yours):

```
home = /usr/local/bin
include-system-site-packages = false
version = 3.14.9
executable = /usr/local/bin/python3.14
command = /usr/local/bin/python -m venv /home/learner/classes/.venv
```

A virtual environment is not magic. It is a folder. Note the full path in `command`: it matters for pitfall 2 below.

### 4. Activate, install, deactivate

Which `python` runs right now? The shared one, not the box yet:

```bash
which python
```

```
/usr/local/bin/python
```

(yours shows your own Python's path). Step into the box:

```bash
source .venv/bin/activate
which python
python -m pip list
```

The prompt now starts with `(.venv)`, the reminder that you are inside the box. The path goes through your project folder, and the box starts almost empty:

```
/home/learner/classes/.venv/bin/python
Package Version
------- -------
pip     26.2.2
```

Install the old version, only here:

```bash
python -m pip install httpx==0.27.2
python -c "import httpx; print(httpx.__version__)"
```

```
Successfully installed anyio-4.15.1 certifi-2026.10.23 h11-0.16.0 httpcore-1.0.9 httpx-0.27.2 idna-3.20 sniffio-1.3.1 typing_extensions-4.16.0
0.27.2
```

Step out:

```bash
deactivate
which python
```

The prompt is back to normal and `which python` points to the shared Python again. Anything you install while inside the box lands in that box only; the `shelf` stand-in still has 0.28.1. Check it:

```bash
cd ..
source shelf/bin/activate
python -c "import httpx; print(httpx.__version__)"
deactivate
```

```
0.28.1
```

Two projects, two versions, no fight. Recap: `python -m venv .venv` makes the folder; `activate` steps in and `deactivate` steps out; installs land in the active box.

The chores remain: you must remember to create and activate the box, install every library by hand, and nothing writes down what is inside. That is the job of `uv`.

### 5. `uv init`: the project's ID card

```bash
mkdir allcs-site
cd allcs-site
uv init --no-package
ls -a
```

`--no-package` asks for the simplest style: one main file and no `src` folder.

```
Initialized project `allcs-site`
```

```
.  ..  .git  .gitignore  .python-version  README.md  main.py  pyproject.toml
```

(`ls -a` prints these in columns; only the names matter.) The files:

- `main.py` is a starter program with a `main()` function and the `if __name__ == "__main__":` guard from lesson M07-L01:

  ```python
  def main():
      print("Hello from allcs-site!")


  if __name__ == "__main__":
      main()
  ```

- `README.md` is a note for humans, empty for now.
- `.git` is the hidden storage of Git, a tool that saves versions of your code (a later module teaches it). Ignore it for now.
- `pyproject.toml` is the ID card. TOML is a simple format: a heading in square brackets, then `name = value` lines.

  ```toml
  [project]
  name = "allcs-site"
  version = "0.1.0"
  description = "Add your description here"
  readme = "README.md"
  requires-python = ">=3.14"
  dependencies = []
  ```

  `name` comes from the folder name. `version` is your own project's version (by habit: big breaking change, new feature, small fix). `requires-python` is a promise and a guard: uv refuses to run the project on anything older. `dependencies` is the shopping list of libraries you depend on, empty because we bought nothing yet.
- `.python-version` has one line, `3.14`: which Python this project should run on. `requires-python` is the minimum; `.python-version` is the choice. If that Python is missing, uv can download it, so everybody on the team gets the same Python.
- `.gitignore` lists things Git must never save. At the bottom: `.venv`. The box is big and can always be rebuilt, so it never travels with the project.

### 6. `uv run`: no activation needed

```bash
uv run main.py
```

```
Using CPython 3.14.9 interpreter at: /usr/local/bin/python3.14
Creating virtual environment at: .venv
Hello from allcs-site!
```

(Your Python version and path will differ.) uv built the box by itself on the first run. No `python -m venv`, no `activate`.

### 7. Asha's real code, and the missing library

Replace `main.py` with the file from this repo (`allcs-site/main.py`):

```python
from rich.console import Console
from rich.table import Table

table = Table(title="Courses")
table.add_column("Course")
table.add_column("Price")
table.add_row("Python", "999")
table.add_row("SQL Basics", "499")

console = Console()
console.print(table)
```

Also copy `allcs-site/tz.py` next to it (used in step 10). Run it in the new, empty box:

```bash
uv run main.py
```

```
Traceback (most recent call last):
  File "/home/learner/allcs-site/main.py", line 1, in <module>
    from rich.console import Console
ModuleNotFoundError: No module named 'rich'
```

This is Lukas's error from the start: the box has no `rich`.

### 8. `uv add`: install and record

```bash
uv add rich
```

```
Resolved 5 packages in 171ms
Downloading pygments (1.2MiB)
 Downloaded pygments
Prepared 4 packages in 134ms
Installed 4 packages in 17ms
 + markdown-it-py==4.2.0
 + mdurl==0.1.2
 + pygments==2.21.0
 + rich==15.0.0
```

(Timings differ. If `rich` has a newer release by the time you run this, the numbers will be newer too.) uv worked out that `rich` needs three helpers of its own: a helper a library needs is also a dependency. And it wrote the shopping list into the ID card:

```toml
dependencies = [
    "rich>=15.0.0",
]
```

`>=15.0.0` means "15.0.0 or anything newer". Run again:

```bash
uv run main.py
```

```
       Courses        
┏━━━━━━━━━━━━┳━━━━━━━┓
┃ Course     ┃ Price ┃
┡━━━━━━━━━━━━╇━━━━━━━┩
│ Python     │ 999   │
│ SQL Basics │ 499   │
└────────────┴───────┘
```

### 9. `uv.lock`, the exact receipt

```bash
ls -a
```

```
.  ..  .git  .gitignore  .python-version  .venv  README.md  main.py  pyproject.toml  tz.py  uv.lock
```

New: `.venv` (the box `run` made) and `uv.lock`. Why a lock file? The ID card says `rich` 15.0.0 *or newer*. In a year "newer" might mean a version that behaves differently, and Lukas would get a different `rich` from Asha: "works on my machine" again. Think of shopping: the list says "rice, at least one kilo" (the ID card); the receipt says "this exact packet, from this exact shop, on this exact day" (`uv.lock`). One block of it:

```toml
[[package]]
name = "markdown-it-py"
version = "4.2.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "mdurl" },
]
sdist = { url = "https://files.pythonhosted.org/.../markdown_it_py-4.2.0.tar.gz", hash = "sha256:04a2...", size = 82454, ... }
```

Each `[[package]]` block is one package: the exact version (not a range), the source (the public package website, PyPI), and a hash, a fingerprint of the downloaded file. If anybody swapped the file for a changed copy, the fingerprint would not match and uv would refuse it. You never edit the file by hand; uv rewrites it each time you add or remove a library, and you share it next to the ID card.

How does `uv run` pick its Python? It looks for `.venv` in the project folder and uses the Python inside, so you never activate anything:

```bash
which python
uv run which python
uv run python --version
```

```
/usr/local/bin/python
/home/learner/allcs-site/.venv/bin/python
Python 3.14.9
```

(Paths and version are yours.) In VS Code, this is the moment promised in Module 1: open the command palette, choose "Select Interpreter" and pick the Python inside `.venv` (Windows: `.venv\Scripts\python.exe`). The wavy lines vanish because VS Code now sees the same libraries as your program.

### 10. Pay off the promise from Module 6: `tzdata`

`allcs-site/tz.py` is Asha's time zone program:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
berlin = ZoneInfo("Europe/Berlin")
start = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(start)
print(start.astimezone(berlin))
print(start == start.astimezone(berlin))
```

```bash
uv run tz.py
```

```
2026-11-02 18:00:00+05:30
2026-11-02 13:30:00+01:00
True
```

On Mac and Linux the computer already has a list of the world's time zones. Windows has none. To see the Windows error on any machine, hide the list with one setting in front of the command (Mac/Linux shell syntax; on Windows you will get the error without it):

```bash
PYTHONTZPATH=/nowhere uv run tz.py
```

The traceback is long. Its two ends are:

```
ModuleNotFoundError: No module named 'tzdata'
...
zoneinfo._common.ZoneInfoNotFoundError: 'No time zone found with key Asia/Kolkata'
```

The fix is the command you know now:

```bash
PYTHONTZPATH=/nowhere uv add tzdata
PYTHONTZPATH=/nowhere uv run tz.py
```

```
Resolved 6 packages in 102ms
Prepared 1 package in 70ms
Installed 1 package in 6ms
 + tzdata==2026.5
2026-11-02 18:00:00+05:30
2026-11-02 13:30:00+01:00
True
```

(`tzdata` may be newer when you run this: it is the time zone list, updated often. The `uv.lock` in this repo pins 2026.5, as in the video.) On Windows, just type `uv add tzdata`. The ID card now lists two dependencies, and `uv tree` draws the family:

```bash
uv tree
```

```
Resolved 6 packages in 0.66ms
allcs-site v0.1.0
├── rich v15.0.0
│   ├── markdown-it-py v4.2.0
│   │   └── mdurl v0.1.2
│   └── pygments v2.21.0
└── tzdata v2026.5
```

### 11. Sharing with Lukas: `uv sync`

Asha shares only the files that matter: `pyproject.toml`, `uv.lock`, `.python-version` and the code. Not the box. `git status --short` (run in a Git project) lists seven names, and `.venv` is not one of them because it is in `.gitignore`:

```
?? .gitignore
?? .python-version
?? README.md
?? main.py
?? pyproject.toml
?? tz.py
?? uv.lock
```

Lukas gets a fresh copy (with Git this is called a clone; here we simply copy the files into an empty folder):

```bash
mkdir ../fresh
cp pyproject.toml uv.lock .python-version main.py tz.py ../fresh/
cd ../fresh
ls -a
```

```
.  ..  .python-version  main.py  pyproject.toml  tz.py  uv.lock
```

No `.venv`: the recipe for a box, but no box. Now `uv sync`, which makes the box match the lock file. Will Lukas get the newest `rich`, or exactly Asha's?

```bash
uv sync
```

```
Using CPython 3.14.9 interpreter at: /usr/local/bin/python3.14
Creating virtual environment at: .venv
Resolved 6 packages in 0.26ms
Installed 5 packages in 7ms
 + markdown-it-py==4.2.0
 + mdurl==0.1.2
 + pygments==2.21.0
 + rich==15.0.0
 + tzdata==2026.5
```

Exactly Asha's: the numbers come from `uv.lock`, not from today's newest. Run both programs:

```bash
uv run main.py
uv run tz.py
```

You get the same table and the same three time lines as before. The sentence "works on my machine" has become "works on every machine". Delete the `fresh` folder when you are done (see Clean up).

Tip: this repo's `allcs-site/` folder is exactly this project. Open a terminal there and run `uv sync`, then `uv run main.py`.

### 12. The `src` layout project: keeping the promise from lesson M07-L02

Run `uv init` with no flag and give it a name:

```bash
uv init allcsvideos
cd allcsvideos
ls -a
ls -R src
```

```
Initialized project `allcsvideos` at `/home/learner/allcsvideos`
```

```
.  ..  .git  .gitignore  .python-version  README.md  pyproject.toml  src
```

```
src:
allcsvideos

src/allcsvideos:
__init__.py
```

No `main.py`; instead the package sits inside `src`, exactly the layout of lesson M07-L02. `src/allcsvideos/__init__.py` holds:

```python
def main() -> None:
    print("Hello from allcsvideos!")
```

(The arrow and `None` are a small label that a later module explains.) The ID card has two new parts at the bottom:

```toml
[project.scripts]
allcsvideos = "allcsvideos:main"

[build-system]
requires = ["uv_build>=0.13.5,<0.14.0"]
build-backend = "uv_build"
```

`[project.scripts]` creates a command named `allcsvideos` that calls `main` from the package. `[build-system]` says how to turn the folder into an installable package (here uv's own builder). You rarely touch either. (On a computer where Git knows your name, `uv init` may also add an `authors` line; that is fine.)

Is the package importable? With the shared Python:

```bash
python -c "import allcsvideos"
```

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import allcsvideos
ModuleNotFoundError: No module named 'allcsvideos'
```

Nothing installed it there. Now `uv run`:

```bash
uv run allcsvideos
```

```
Using CPython 3.14.9 interpreter at: /usr/local/bin/python3.14
Creating virtual environment at: .venv
   Building allcsvideos @ file:///home/learner/allcsvideos
      Built allcsvideos @ file:///home/learner/allcsvideos
Installed 1 package in 1ms
Hello from allcsvideos!
```

The first run made the box and then installed your own project into it, just like `rich`. Prove it is the real project:

```bash
uv run python -c "import allcsvideos; print(allcsvideos.__file__)"
uv pip list
```

```
/home/learner/allcsvideos/src/allcsvideos/__init__.py
Package     Version Editable project location
----------- ------- -------------------------
allcsvideos 0.1.0   /home/learner/allcsvideos
```

(Paths are yours.) "Editable" means the box holds a link to your folder, not a frozen copy: change the code and the very next run sees the change. This is the installed copy that lesson M07-L02 wanted you to test. The finished project from this step is in this repo's `allcsvideos/` folder.

### The four commands on one card

- `uv init` starts a project and writes the ID card.
- `uv add` installs a library and records it in `pyproject.toml` and `uv.lock`.
- `uv run` runs your code inside the project's box.
- `uv sync` builds the box from the lock file, for example on a fresh copy.

## Common mistakes

1. Installed it, still "no module named": you ran `pip install` into a different Python than the one that runs your code. In a uv project always use `uv add` and `uv run`, so installing and running use the same box.
2. Copying or sharing `.venv`: a box is tied to the place it was made (see the `command =` line in `pyvenv.cfg`). Never copy it and never save it in Git. Share `pyproject.toml` and `uv.lock`, and run `uv sync`.
3. Leaving `uv.lock` behind: with only `pyproject.toml` the ranges are back, and so is the surprise. Always share `uv.lock`, and never edit it by hand.
4. `pip install` inside a uv project: the library lands in the box but is not written in `pyproject.toml` or `uv.lock`. It works for you and fails for Lukas. Use `uv add`.
5. Activating on Windows: the path differs (`.venv\Scripts\activate`) and PowerShell may refuse to run the script ("running scripts is disabled"). Avoid it: `uv run` needs no activation.

## Interview question

Rahul asks: what is a virtual environment, and why does a project keep a `uv.lock` file? Model answer: a virtual environment is an isolated folder with its own Python and its own libraries, so every project gets exactly the versions it needs without affecting the others. The `uv.lock` file records the exact version and hash of every library, direct and indirect, so every developer and every server installs the identical set.

## Try it yourself

Make a project with `uv init --no-package`. Add `rich`, then change `main.py` to print a small table of your own. Delete the `.venv` folder, and bring it back with `uv sync`.

## Clean up

Everything was created in the folders you made. Remove them when you are finished:

```bash
cd ..
rm -rf shelf classes fresh allcs-site allcsvideos
```

Run this from the folder where you created them (not from inside this lesson's repo folder, whose `allcs-site/` and `allcsvideos/` you want to keep). If you ran `uv run` inside this repo's `allcs-site/` or `allcsvideos/`, delete the `.venv` folders that appeared there.

## Next

Where do all these libraries come from? Continue with [M07-L04 · Third-Party Packages and PyPI](../m07-l04-third-party-packages-and-pypi/README.md).
