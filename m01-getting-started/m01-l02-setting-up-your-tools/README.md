# M01-L02 · Setting Up Your Tools

> Video: Module 1, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- The four tools of a programmer's kitchen: Python, uv, VS Code and the terminal
- How to install uv, then Python 3.14 with uv, then VS Code with its Python extension
- The terminal in five commands: `pwd`, `ls`, `cd`, `cd ..` and `mkdir`
- How to open a folder in VS Code and find your way around its screen
- The four most common set-up problems and their quick fixes

## Before you start

- A laptop or desktop (Mac, Windows or Linux) and an internet connection. You do this set-up once.
- Nothing needs to be installed before this lesson. At the end you will have all four tools.
- The terminal captures below were recorded on a clean Debian Linux machine (user `learner`). On a Mac the paths look like `/Users/yourname/...`, on Windows like `C:\Users\yourname\...`. Version numbers, download sizes and paths will differ on your machine, and that is fine.

## Files in this folder

| File | What it is |
|------|------------|
| `check.py` | A one-line test file (`print("Setup complete")`) used in pitfall 3, the wrong folder |

This lesson is mostly installing and typing commands, so there is little code to keep.

## Follow along

### 1. Open the terminal

- Mac: press Command + Space, type `terminal`, press Enter.
- Windows: open the Start menu, type `PowerShell`, open it.
- Linux: press Ctrl + Alt + T, or look for Terminal in your apps.

You see a window with a blinking cursor. It waits for a command. The text before the cursor is the prompt. In this course we draw the prompt as just `$`, and you never type the `$`.

### 2. Install uv

uv installs Python versions and, later, your libraries. Use the line from the official uv documentation.

Mac and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

The Linux run printed this (version and CPU type will differ on your machine):

```text
downloading uv 0.13.5 aarch64-unknown-linux-gnu
installing to /home/learner/.local/bin
  uv
  uvx
everything's installed!

To add $HOME/.local/bin to your PATH, either restart your shell or run:

    source $HOME/.local/bin/env (sh, bash, zsh)
    source $HOME/.local/bin/env.fish (fish)
```

It asks you to restart your shell. In plain words: close the terminal and open a new one (pitfall 1 explains why). Then check:

```bash
uv --version
```

```text
uv 0.13.5 (aarch64-unknown-linux-gnu)
```

If you see a version number, the install worked.

### 3. Install Python 3.14 with uv

```bash
uv python install 3.14
python3.14 --version
uv run --python 3.14 python --version
```

```text
Downloading cpython-3.14.9-linux-aarch64-gnu (download) (29.2MiB)
 Downloaded cpython-3.14.9-linux-aarch64-gnu (download)
Installed Python 3.14.9 in 6.68s
 + cpython-3.14.9-linux-aarch64-gnu (python3.14)
Python 3.14.9
Python 3.14.9
```

Now try the short name:

```bash
python --version
```

```text
bash: python: command not found
```

By default uv only creates the long name `python3.14`. In this course we always type just `python`, so run the install once more with a flag:

```bash
uv python install 3.14 --default
python --version
python3 --version
```

```text
warning: The `--default` option is experimental and may change without warning. Pass `--preview-features python-install-default` to disable this warning
Installed Python 3.14.9 in 30ms
 + cpython-3.14.9-linux-aarch64-gnu (python, python3)
Python 3.14.9
Python 3.14.9
```

The warning says "experimental". That is fine, it works. On Windows the commands are the same, only the first install line differs.

### 4. Install VS Code and the Python extension

VS Code is an ordinary app. Download it from `code.visualstudio.com`.

- Mac: download the zip, open it, drag Visual Studio Code into Applications.
- Windows: run the installer and click Next. Keep the option "Add to PATH" ticked.
- Linux: download the `.deb` (Ubuntu, Debian) or `.rpm` (Fedora) file and open it with your software installer.

Then open VS Code and add the extension:

1. On the left edge, click the fifth icon (four squares): Extensions.
2. Type `python` in the search box.
3. Choose the one by Microsoft and click Install.

This gives VS Code colours, hints and a run button for Python. To check VS Code itself, open the About window (Mac: Code menu, About Visual Studio Code. Windows and Linux: Help menu, About). You should see a version number.

Recap of the three checks: `uv --version`, `python --version` (Python 3.14.x), and VS Code's About window plus the Python extension in the list.

### 5. The terminal in five commands

The terminal always stands in one folder, the current folder. Folders live inside other folders like branches of a tree. The address of a folder is its path, for example `/home/learner/Documents`.

```bash
pwd
ls
cd Documents
pwd
cd ..
pwd
mkdir allcs-python
ls
```

```text
$ pwd
/home/learner
$ ls
Documents
Downloads
$ cd Documents
$ pwd
/home/learner/Documents
$ cd ..
$ pwd
/home/learner
$ mkdir allcs-python
$ ls
Documents
Downloads
allcs-python
```

- `pwd` (print working directory): where am I?
- `ls` (list): what is here?
- `cd folder`: go into a folder. No output is normal: in the terminal, silence usually means success.
- `cd ..`: go one folder up. The two dots mean "the folder above this one".
- `mkdir name` (make directory): create a folder.

Now use them together to make the course folder structure:

```bash
cd allcs-python
pwd
mkdir lessons
ls
cd lessons
pwd
cd ..
pwd
ls -R
```

```text
$ cd allcs-python
$ pwd
/home/learner/allcs-python
$ mkdir lessons
$ ls
lessons
$ cd lessons
$ pwd
/home/learner/allcs-python/lessons
$ cd ..
$ pwd
/home/learner/allcs-python
$ ls -R
.:
lessons

./lessons:
```

`ls -R` lists everything inside a folder, all the way down the tree. Two last helpers: `clear` wipes the screen (nothing is deleted), and the Up arrow key brings back your previous command. On Windows PowerShell all of these work too.

### 6. Open your folder in VS Code

Your project is simply a folder (here `allcs-python`, which you can create anywhere, for example inside Documents). Always open the folder, not a single file.

- Way one, menus: File, Open Folder, choose `allcs-python`, click Open. When VS Code asks whether you trust the authors, it is your own folder, so click yes.
- Way two, terminal: step into the folder with `cd`, then type `code .` (the dot means "this folder"). On a Mac do this once first: in VS Code press Command + Shift + P, type `shell command`, and choose "Install code command in path". Then open a new terminal.

The VS Code screen:

- Left: the explorer, showing the files and folders of your project.
- Middle: the editor. Each open file gets a tab.
- Bottom: the terminal panel (Terminal menu, New Terminal). It starts inside your project folder.
- Top right of the editor: the run button (a small triangle) for Python files. We use it in the next lesson.
- Bottom right: the status bar, which shows which Python VS Code is using.

### 7. The four pitfalls

Pitfall 1: command not found. Right after the install, `uv --version` fails because the terminal's list of folders (the path) did not yet include `~/.local/bin`:

```text
bash: uv: command not found
```

On a Mac the message reads `zsh: command not found: uv`. The computer only looks in a short list of folders, called the path. Fix: close the terminal and open a new one. The new window reads the updated list. After the fix the PATH starts with the new folder:

```text
$ echo $PATH
/home/learner/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

Pitfall 2: `python`, `python3` or `py`. Different computers use different names. If `python` says "command not found", `python3.14` always works as a long name, and `uv run --python 3.14 python` works everywhere. The real fix is `uv python install 3.14 --default`, as in step 3. On Windows, if typing `python` opens the Microsoft Store, close it and run the same fix.

Pitfall 3: the wrong folder. `check.py` (in this folder) prints `Setup complete`. If you run it from a different folder you get:

```text
$ pwd
/home/learner/allcs-python
$ ls
lessons
$ python check.py
python: can't open file '/home/learner/allcs-python/check.py': [Errno 2] No such file or directory
```

Python is fine. The terminal is just standing in a folder that does not contain the file. Use `pwd` and `ls` to look, then `cd` to the folder where the file lives. Here `check.py` lives in `Documents`:

```text
$ cd ../Documents
$ ls
check.py
```

```text
$ python check.py
Setup complete
```

Pitfall 4: VS Code picks the wrong Python. You may see a yellow wavy line under correct code, or the file runs with another Python version. Look at the status bar (bottom right). If it does not say 3.14, click it and pick the Python 3.14 from the list. You can also press Command + Shift + P (Ctrl + Shift + P on Windows and Linux), type `Python: Select Interpreter`, and press Enter.

When something fails, check three things: did I open a new terminal? Am I in the right folder? Is VS Code using the right Python?

### 8. Final check

You should be able to see all four on your own screen:

1. `uv --version` prints a version number.
2. `python --version` prints `Python 3.14.x`.
3. VS Code opens your `allcs-python` folder and the Python extension is installed.
4. `pwd` tells you where you are and `ls` shows what is there.

## Common mistakes

- Not opening a new terminal after installing uv (`command not found`).
- Typing `python` when only `python3` or `python3.14` exists. Use `uv python install 3.14 --default`.
- Running a file from the wrong folder (`can't open file`). Check with `pwd` and `ls`.
- Opening a single file in VS Code instead of the project folder.
- VS Code using another Python. Check the status bar at the bottom right.

## Clean up

Nothing to clean up. You want to keep everything you installed. The `allcs-python` folder you made is the place for all your course files.

## Next

[M01-L03 · Your First Program](../m01-l03-your-first-program/)
