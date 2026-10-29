# M21-L02 · Building and Publishing a Package

> Video: Module 21, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What a package is (goods, label, instructions for opening) and the three names it has: `allcsv-cli`, `allcsv_cli`, `allcsv`
- Writing `pyproject.toml` in full: `[project]` metadata, dependencies as ranges, `[project.scripts]` and the build backend
- Building a wheel and an sdist with `uv build`, and opening the wheel to see what is inside
- Versions: semantic versioning, `uv version --bump`, a changelog, and a README that becomes the package page
- Publishing with `uv publish` to a private local index (pypiserver in Docker), then installing from it in a clean environment
- How the real path (TestPyPI, then PyPI, ideally with trusted publishing) differs, and three traps: the same version twice, the name, and data files outside the package

## Before you start

- Python 3.14 or newer (`python --version`) and `uv` (`uv --version`), from Module 7.
- Docker running, for the local package index. The image is pinned: `pypiserver/pypiserver:v2.4.2`.
- Modules 7 (projects and `pyproject.toml`) and 21, lesson 1 (the Typer tool) help. No earlier folder is needed: the small project is in this folder.
- Nothing in this lesson touches the public PyPI or TestPyPI. The real-world commands are shown as text only.

## Files in this folder

| File | What it is |
|------|------------|
| `allcsv-cli/pyproject.toml` | The label and the instructions: metadata, dependencies, `allcsv` command, `uv_build` backend |
| `allcsv-cli/src/allcsv_cli/__init__.py` | Reads the version back from the installed package (`importlib.metadata`) |
| `allcsv-cli/src/allcsv_cli/cli.py` | The Typer app: `allcsv --version`, `allcsv courses list [--json]` |
| `allcsv-cli/src/allcsv_cli/courses.json` | The data file, inside the package folder so it travels in the wheel |
| `allcsv-cli/tests/test_cli.py` | Two small tests (stay out of the wheel) |
| `allcsv-cli/README.md` | The front page shown on the package index |
| `allcsv-cli/LICENSE` | The MIT licence text (goes into the wheel) |
| `allcsv-cli/CHANGELOG.md` | What changed in each version, newest on top |
| `allcsv-cli/.github/workflows/release.yml` | The trusted-publishing workflow, shown as text only (it is not run) |
| `index/htpasswd` | The password file of the local index: one user, `asha` (demo value, only for this throwaway index) |
| `index/demo-login.env` | The two environment variables for `uv publish` (demo values, not a real account) |
| `pitfalls/cli_bad_data.py` | A `cli.py` that looks for `courses.json` outside the package (trap 3) |

## Follow along

Run the commands from this folder (`m21-l02-building-and-publishing-a-package`) unless a step says otherwise. For a tidy test, work in a copy:

```bash
cp -R . ~/l02-try && cd ~/l02-try
```

### 1. The problem: a command that only exists in your project

On a computer without the tool, the shell has never heard of `allcsv`:

```bash
allcsv courses list
```

```
bash: allcsv: command not found
```

(zsh says `zsh: command not found: allcsv`.) Sending the project folder is not a plan: the other person needs the right libraries and the right Python, and must run it from inside that folder. We want one sealed file that anyone can install with one command, after which the `allcsv` command appears.

### 2. What goes in a package

A package has three parts: the goods (code and the data files it needs), the label (name, version, what else must be installed), and the instructions for opening (which command to create). The label and the instructions live in `pyproject.toml`.

List the project:

```bash
cd allcsv-cli
find . -type f -not -path './.venv/*' -not -path './dist/*' | sort
```

```
./.github/workflows/release.yml
./.gitignore
./.python-version
./CHANGELOG.md
./LICENSE
./README.md
./pyproject.toml
./src/allcsv_cli/__init__.py
./src/allcsv_cli/cli.py
./src/allcsv_cli/courses.json
./tests/test_cli.py
```

This is the src layout from Module 7, lesson 2. With this builder, only what sits inside `src` goes into the package: the tests stay at home. Note `courses.json` inside the package folder; it matters in step 14.

Three names, three jobs: the package is `allcsv-cli` (what you install), the folder you import is `allcsv_cli`, and the command people type is `allcsv`.

(To see where it starts: `uv init --package --vcs none allcsv-cli` writes a small starter `pyproject.toml` with `description = "Add your description here"` and a script called `allcsv-cli`. Today we write it in full.)

### 3. The label: `[project]`

Open `pyproject.toml`. The first block has ten lines:

```toml
[project]
name = "allcsv-cli"
version = "0.1.0"
description = "CLI for allcsvideos.com courses"
readme = "README.md"
requires-python = ">=3.14"
license = "MIT"
license-files = ["LICENSE"]
authors = [{ name = "Asha" }]
keywords = ["csv", "cli", "courses"]
```

- `name`: what people type to install it. Names are first come, first served on the index.
- `version`: `0.1.0` (step 8). `description`: one short line, shown in search results.
- `readme`: the text of this file becomes the front page of the package. `requires-python`: an older Python refuses to install it instead of installing something that cannot run.
- `license` and `license-files`: the licence is the written permission to use your code (Module 7, lesson 4). The second line puts the licence text inside the package.
- `authors` and `keywords`: labels for humans.

### 4. Dependencies, scripts, build system

```toml
dependencies = [
    "rich>=15.0.0",
    "typer>=0.27.3",
]

[project.scripts]
allcsv = "allcsv_cli.cli:app"

[build-system]
requires = ["uv_build>=0.13.6,<0.14.0"]
build-backend = "uv_build"
```

- `dependencies` use `>=`: a minimum, not one exact version. Your own project pins exact versions in `uv.lock`, but a library that other people install should allow a range, or it clashes with their other packages.
- `[project.scripts]`: on the left, the command (`allcsv`); on the right, where the work is: the module `allcsv_cli.cli`, a colon, and the name `app`.
- `build-backend` is the program that turns your folder into the sealed files. Here it is `uv_build`, the builder that comes with uv (`hatchling` and `setuptools` do the same job). The `requires` line is a note for the build tool; you never install it yourself.

### 5. What the scripts line really makes

```bash
uv sync
cat .venv/bin/allcsv
uv run allcsv --version
uv run allcsv courses list
```

```
...
 + allcsv-cli==0.1.0 (from file:///.../allcsv-cli)
 + annotated-doc==0.0.5
 + markdown-it-py==4.2.0
 + mdurl==0.1.2
 + pygments==2.21.0
 + rich==15.0.0
 + shellingham==1.5.4
 + typer==0.27.3
```

```
#!/.../allcsv-cli/.venv/bin/python
# -*- coding: utf-8 -*-
import sys
from allcsv_cli.cli import app
if __name__ == "__main__":
    if sys.argv[0].endswith("-script.pyw"):
        sys.argv[0] = sys.argv[0][:-11]
    elif sys.argv[0].endswith(".exe"):
        sys.argv[0] = sys.argv[0][:-4]
    sys.exit(app())
```

```
allcsv 0.1.0
                        Courses
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Id ┃ Title                  ┃ Level        ┃   Price ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
...
```

A command is only a tiny file that imports your `app` and calls it. The installer writes it for you on every computer. (Paths and the first lines of the shebang are yours; the table has five rows: Python Basics, Object-Oriented Python, FastAPI in Practice, Async Python, Docker for Python Apps.)

### 6. Build: a wheel and an sdist

```bash
uv build
ls -l dist
```

```
Building source distribution...
Building wheel from source distribution...
Successfully built dist/allcsv_cli-0.1.0.tar.gz
Successfully built dist/allcsv_cli-0.1.0-py3-none-any.whl
```

`ls -l dist` lists two files, the wheel (`allcsv_cli-0.1.0-py3-none-any.whl`, about 3.9 KB) and the sdist (`allcsv_cli-0.1.0.tar.gz`, about 2.7 KB). Exact byte counts depend on your files, so yours will differ a little.

- The wheel is the ready-made one, like assembled furniture: the installer just unpacks it. Installers prefer wheels because they install fast.
- The sdist (source distribution) is the flat pack: the sources and the recipe to build them.
- We publish both, so that every computer finds one it can use.

### 7. Open the wheel and the sdist

A wheel is only a zip file. Guess first: is the `tests` folder inside? And `courses.json`?

```bash
python -m zipfile -l dist/allcsv_cli-0.1.0-py3-none-any.whl
```

```
File Name                                             Modified             Size
allcsv_cli/                                    1980-01-01 00:00:00            0
allcsv_cli/__init__.py                         1980-01-01 00:00:00          139
allcsv_cli/cli.py                              1980-01-01 00:00:00         1431
allcsv_cli/courses.json                        1980-01-01 00:00:00          410
allcsv_cli-0.1.0.dist-info/licenses/           1980-01-01 00:00:00            0
allcsv_cli-0.1.0.dist-info/licenses/LICENSE    1980-01-01 00:00:00         1072
allcsv_cli-0.1.0.dist-info/                    1980-01-01 00:00:00            0
allcsv_cli-0.1.0.dist-info/WHEEL               1980-01-01 00:00:00           80
allcsv_cli-0.1.0.dist-info/entry_points.txt    1980-01-01 00:00:00           47
allcsv_cli-0.1.0.dist-info/METADATA            1980-01-01 00:00:00          504
allcsv_cli-0.1.0.dist-info/RECORD              1980-01-01 00:00:00          643
```

No tests, and yes `courses.json`: it sits inside the package folder. The `dist-info` folder is the label. Read it with `unzip -p`, which prints one file from the wheel:

```bash
unzip -p dist/*.whl '*/METADATA'
unzip -p dist/*.whl '*/entry_points.txt'
```

```
Metadata-Version: 2.4
Name: allcsv-cli
Version: 0.1.0
Summary: CLI for allcsvideos.com courses
Keywords: csv,cli,courses
Author: Asha
License-Expression: MIT
License-File: LICENSE
Requires-Dist: rich>=15.0.0
Requires-Dist: typer>=0.27.3
Requires-Python: >=3.14
Description-Content-Type: text/markdown

# allcsv-cli

Look at the courses of allcsvideos.com from your terminal.

## Install

    uv tool install allcsv-cli

## Use

    allcsv courses list
    allcsv courses list --json
    allcsv --version
[console_scripts]
allcsv = allcsv_cli.cli:app
```

Below the header, the whole README follows: that is what the index shows as the package page. `entry_points.txt` is the same line you wrote; the installer reads it and writes the tiny command file. The sdist is a tar file:

```bash
tar tzf dist/allcsv_cli-0.1.0.tar.gz
```

```
allcsv_cli-0.1.0/PKG-INFO
allcsv_cli-0.1.0/pyproject.toml
allcsv_cli-0.1.0/pyproject.toml.orig
allcsv_cli-0.1.0/
allcsv_cli-0.1.0/LICENSE
allcsv_cli-0.1.0/README.md
allcsv_cli-0.1.0/src
allcsv_cli-0.1.0/src/allcsv_cli
allcsv_cli-0.1.0/src/allcsv_cli/__init__.py
allcsv_cli-0.1.0/src/allcsv_cli/cli.py
allcsv_cli-0.1.0/src/allcsv_cli/courses.json
```

The same code, not yet built.

### 8. Versions

Most projects use semantic versioning: `major.minor.patch`. A patch is a fix and nothing changes for users. A minor is a new feature, old things still work. A major is a breaking change. For allcsv: fixing a typo in the table title is a patch; adding a `--level` option is a minor change; renaming `courses list` to `list courses` would break every script, so that is a major change. Below `1.0.0` a tool is young and anything may change.

`uv` does the arithmetic. `--dry-run` shows the result without changing the file:

```bash
uv version
uv version --bump patch --dry-run
uv version --bump minor --dry-run
uv version --bump major --dry-run
```

```
allcsv-cli 0.1.0
allcsv-cli 0.1.0 => 0.1.1
allcsv-cli 0.1.0 => 0.2.0
allcsv-cli 0.1.0 => 1.0.0
```

Without `--dry-run`, uv writes the new number into `pyproject.toml`. Note the minor bump sets the patch back to 0.

Two habits: keep `CHANGELOG.md` (newest on top, written when you make the change), and keep the version in one place only, `pyproject.toml`. `allcsv_cli/__init__.py` reads it back from the installed package, so `allcsv --version` always tells the truth.

The README is the front page: write it for a stranger. What is it? How do I install it? How do I use it?

### 9. Run your own package shop (local index)

The public index, PyPI, is open to the whole world, and an upload there is public and permanent. So we practise on our own index: pypiserver in Docker. Go back to the lesson folder first (`cd ..`), then:

```bash
mkdir -p pypi-data/packages
cp index/htpasswd pypi-data/htpasswd
docker run -d --name pyrepo-m21-pypi -p 21802:8080 \
  -v "$PWD/pypi-data:/data" pypiserver/pypiserver:v2.4.2 \
  run -P /data/htpasswd -a update /data/packages
docker ps --filter name=pyrepo-m21-pypi --format 'table {{.Image}}\t{{.Status}}\t{{.Ports}}'
```

```
IMAGE                          STATUS         PORTS
pypiserver/pypiserver:v2.4.2   Up 2 seconds   0.0.0.0:21802->8080/tcp, [::]:21802->8080/tcp
```

`-d` runs it in the background, `-p 21802:8080` connects port 21802 on your computer to the box, `-v` gives the box a folder for its files, `-P` is the password file and `-a update` means: logging in is needed to upload, anyone may download. (The container id and the "Up ..." time will differ. If port 21802 is busy, change the number everywhere below.)

The password file holds one user, `asha`, with a demo password that only exists for this lab. `uv publish` reads the login from two environment variables, so the password never appears on screen or in a file you share (Module 17, lesson 4):

```bash
source index/demo-login.env
```

### 10. Publish

Before the upload the index has nothing for our package (HTTP 303 means "go to the package list", which is empty):

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:21802/simple/allcsv-cli/
```

```
303
```

Now upload both files, then ask the index what it has:

```bash
cd allcsv-cli
uv publish --publish-url http://localhost:21802/ dist/*
curl -s http://localhost:21802/simple/allcsv-cli/ | grep "<a "
cd ..
```

```
Publishing 2 files to http://localhost:21802/
Hashing allcsv_cli-0.1.0-py3-none-any.whl (3.8KiB)
Uploading allcsv_cli-0.1.0-py3-none-any.whl (3.8KiB)
Hashing allcsv_cli-0.1.0.tar.gz (2.6KiB)
Uploading allcsv_cli-0.1.0.tar.gz (2.6KiB)
            <a href="/packages/allcsv_cli-0.1.0-py3-none-any.whl#sha256=e0b7d5...">allcsv_cli-0.1.0-py3-none-any.whl</a><br>
            <a href="/packages/allcsv_cli-0.1.0.tar.gz#sha256=b3446e...">allcsv_cli-0.1.0.tar.gz</a><br>
```

No error, so the index accepted both. After each name comes `#sha256=` and a long fingerprint (cut short here, and yours will differ): installers check it, so a changed file is caught, like the hash in `uv.lock`.

### 11. Install on "Priya's laptop": a clean environment

A brand-new, empty environment, no project folder, no source code:

```bash
uv venv --python 3.14 clean
uv pip install --python clean/bin/python --index http://localhost:21802/simple/ allcsv-cli
```

```
Using CPython 3.14.7 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14
Creating virtual environment at: clean
Activate with: source clean/bin/activate
Using Python 3.14.7 environment at: clean
Resolved 8 packages in 809ms
Downloading pygments (1.2MiB)
 Downloaded pygments
Prepared 8 packages in 400ms
Installed 8 packages in 7ms
 + allcsv-cli==0.1.0
 + annotated-doc==0.0.5
 + markdown-it-py==4.2.0
 + mdurl==0.1.2
 + pygments==2.21.0
 + rich==15.0.0
 + shellingham==1.5.4
 + typer==0.27.3
```

uv found `allcsv-cli` in our index and installed eight packages: ours, and seven helpers that came from the public PyPI (reading from it is free and harmless; nothing of ours goes there). Timings and paths differ on your machine. Now run it:

```bash
clean/bin/allcsv --version
clean/bin/allcsv courses list
```

```
allcsv 0.1.0
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
```

A clean environment, no project folder, and the data file travelled inside the package.

### 12. The real public path (shown, not run)

The real path has the same steps with two changes: the address and who you are. It has a safety net, TestPyPI: a separate copy of the index at `test.pypi.org`, with its own accounts, cleaned out from time to time. You upload there first, install from there, and only then go to the real PyPI.

To upload you create an account, turn on two-step login, and create an API token in your settings. A token is a long secret string that works like a password, only for uploading. Keep it in your password manager and give it to uv through an environment variable. Never type it into a file, a chat, or a video. Commands, for reading only:

```bash
export UV_PUBLISH_TOKEN="..."   # from your password manager
uv publish --publish-url https://test.pypi.org/legacy/ dist/*
uv pip install --index https://test.pypi.org/simple/ allcsv-cli
uv publish dist/*
```

The last line, with no address, goes to the real PyPI. A real upload is forever. You can hide a version (called yanking it), but you can never upload that number again. That is why we practise first.

Even better than a token is no token: trusted publishing. In your PyPI settings you say: "releases made by this workflow, in this repository, may publish". The workflow proves who it is with a pass that lives a few minutes, so there is no secret to steal. The workflow is `allcsv-cli/.github/workflows/release.yml` (text only, like Module 19, lesson 3):

```yaml
name: release
on:
  push:
    tags: ["v*"]
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v7
      - run: uv build
      - run: uv publish
```

It runs only when you push a tag that starts with `v`. `id-token: write` lets the job ask for the short pass. The last command has no password at all.

### 13. Traps 1 and 2: the same version twice, and the name

Trap 1. You fix a typo, build again and upload again with the same version number. (Here we upload the same files again, which is what the index sees.)

```bash
cd allcsv-cli
uv publish --publish-url http://localhost:21802/ dist/*
echo $?
cd ..
```

```
Publishing 2 files to http://localhost:21802/
Hashing allcsv_cli-0.1.0-py3-none-any.whl (3.8KiB)
Uploading allcsv_cli-0.1.0-py3-none-any.whl (3.8KiB)
error: Failed to publish `dist/allcsv_cli-0.1.0-py3-none-any.whl` to `http://localhost:21802/`
  cause: Server returned status code 409 Conflict. Server says:
             ...
                     <pre>Package &#039;allcsv_cli-0.1.0-py3-none-any.whl&#039; already exists!
           You may start server with `--overwrite` option.</pre>
             ...
2
```

(The HTML page in the middle is shortened here.) The index refuses on purpose: a version, once uploaded, never changes. The public index refuses too. The fix: bump the version, build again, upload.

Trap 2: the name. Names are first come, first served, and the index treats dashes, dots, underscores and capital letters as the same. So ask before you choose. In the video, one request to the public index per name, read-only, nothing uploaded: `requests` answered `200` (taken), and `allcsv-cli` answered `404` (free that day):

```bash
curl -s -o /dev/null -w "%{http_code}" https://pypi.org/pypi/requests/json
curl -s -o /dev/null -w "%{http_code}" https://pypi.org/pypi/allcsv-cli/json
```

(Not run in this repo: it needs the internet, and the answer can change any day. Try it yourself if you like.) Never choose a name that looks almost like a famous package: that is typo squatting (Module 7, lesson 4).

### 14. Trap 3: the data file outside the package

The most common trap. Here Asha keeps `courses.json` in a `data` folder next to `src`, and finds it from the position of the code file (`pitfalls/cli_bad_data.py`):

```python
from pathlib import Path
# ...
def load_courses() -> list[dict]:
    root = Path(__file__).parents[2]
    text = (root / "data" / "courses.json").read_text()
```

The good version (what we published) uses `files` from `importlib.resources`, which finds the folder where the package is installed, wherever that is:

```python
from importlib.resources import files
# ...
def load_courses() -> list[dict]:
    folder = files("allcsv_cli")
    text = folder.joinpath("courses.json").read_text()
```

Make a bad copy of the project and try it:

```bash
mkdir bad && cp -R allcsv-cli/. bad/ && cd bad
rm -rf .venv dist
mkdir data
mv src/allcsv_cli/courses.json data/courses.json
cp ../pitfalls/cli_bad_data.py src/allcsv_cli/cli.py
uv sync -q
uv run allcsv courses list
```

From the project folder it works, and the table appears. So she thinks all is well. Now build, count the wheel lines that mention `courses.json`, install into a clean environment and run:

```bash
uv build
python -m zipfile -l dist/*.whl | grep -c courses.json
uv venv --python 3.14 ../badclean
uv pip install --python ../badclean/bin/python dist/*.whl
../badclean/bin/allcsv courses list
cd ..
```

```
0
...
FileNotFoundError: [Errno 2] No such file or directory: 
'/.../badclean/lib/python3.14/data/courses.json'
```

Zero lines: the `data` folder is outside `src`, so it was never packaged. The run fails with `FileNotFoundError` inside a long traceback (only its last lines are shown): the path is built from where the code is, and installed code lives deep inside the environment, where there is no `data` folder. The fix is to put the file inside the package folder and read it with `files(...)`, as in the good version.

### 15. The four checks before every upload

1. List the wheel (`python -m zipfile -l`).
2. Install it into a clean environment.
3. Run the command once.
4. Make sure the version is new.

Five minutes, and no embarrassing second version.

### 16. Interview tip

Rahul asks: how do you publish a Python library safely? A good answer: describe the package in `pyproject.toml` (name, a semantic version, the Python it needs, dependencies as ranges); build a wheel and an sdist with `uv build` and open the wheel to check what is inside; try a test index first; publish with a token from the environment or, better, trusted publishing so no secret is stored; and never upload a version twice: a fix means a new version and a line in the changelog.

### 17. Your turn

Make a project with `uv init --package`. Add a command, build it, and list the wheel. Start pypiserver, publish, and install into a clean environment. Then bump the version and publish again. Last, move the data file outside the package and watch what happens.

## Common mistakes

- Uploading the same version twice: the index answers `409 Conflict`. Bump the version and build again.
- Choosing a name that is already taken, or one that looks almost like a famous package.
- Keeping a data file outside the package folder: it is not in the wheel, so the installed command cannot find it. Put it inside the package and read it with `importlib.resources.files`.
- Pinning exact dependency versions in a library: use ranges (`>=`) so it fits next to other packages.
- Publishing without opening the wheel and installing it into a clean environment first.
- Typing a token or password into a file, a chat or a command line. Use an environment variable, or trusted publishing.

## Clean up

```bash
docker rm -f -v pyrepo-m21-pypi
rm -rf pypi-data clean bad badclean allcsv-cli/dist allcsv-cli/.venv
```

(If you worked in a copy, delete the copy: `rm -rf ~/l02-try`.)

## Next

[M21-L03 · Working with Other People's Code](../m21-l03-working-with-other-peoples-code/)
