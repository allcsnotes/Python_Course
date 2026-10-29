# M06-L01 · Reading and Writing Files

> Video: Module 6, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why a running program forgets everything, and why a file on the disk does not
- How to write a file, read it back, and add to it (modes `w`, `r` and `a`)
- Why we always open files with `with`
- What encoding means, and why we always write `encoding="utf-8"`
- How to build file paths the safe way with `pathlib.Path`
- How the guessing game remembers its best score between runs

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- A terminal and an empty working folder. Copy the `.py` files of this folder into it and run every command from there (all the programs read and write files in the current folder).
- No earlier lesson folder is needed. Module 1 (folders and the terminal) and the text lesson (`\n`, `strip`) help.
- On Windows, use `type notes.txt` instead of `cat notes.txt`, and `rmdir /s /q data` instead of `rm -r data`.

## Files in this folder

| File | What it is |
|------|------------|
| `best.py` | The guessing-game piece that remembers the best score in `best_score.txt` |
| `w1.py` | First write: `open`, `write`, `close` |
| `w2.py` | Two writes with no new line: Lukas and Priya get glued together |
| `w3.py` | The same, with `\n` at the end of each name |
| `d1.py` | The same file written with a `with` block |
| `d2.py` | Prints `file.closed` inside and after the block |
| `d3.py` | Mistake: writing after the block (closed file) |
| `e1.py` | `file.read()` gives the whole text as one string |
| `e2.py` | A second `read()` returns nothing: the file remembers its place |
| `e3.py` | Loop over the file: blank lines appear |
| `e4.py` | Loop with `line.strip()`: tidy lines |
| `e5.py` | `file.readlines()` gives a list of lines |
| `f1.py` | Mode `"w"` erases the old content |
| `f2.py` | Mode `"a"` adds at the end |
| `g1.py` | Writes and reads `café` with UTF-8 |
| `g2.py` | Reads the same file with the old `latin-1` rule: gibberish |
| `missing.py` | Reads `note.txt` (typo, the file is `notes.txt`): `FileNotFoundError` |
| `p1.py` | Builds `Path("data") / "notes.txt"` and checks `exists()` |
| `p2.py` | `mkdir(exist_ok=True)`, `write_text`, `read_text` |
| `p3.py` | Appends to the file using a `Path` |
| `p4.py` | Mistake: writing into a folder that does not exist |
| `p5.py` | Mistake: `mkdir()` twice without `exist_ok` |
| `k1.py` | Mistake: writing a number (`TypeError`) |
| `k1b.py` | The fix: `str(score)` |
| `k2.py` | Mistake: reading a file opened with `"w"` |

## Follow along

Every command is `python <file>`. The files create their own data files (`notes.txt`, `students.txt`, and so on) in the folder you run them from.

### 1. The hook: a program that remembers

`best.py` keeps the best (lowest) number of tries. Run it three times and type `7`, then `9`, then `4` when asked:

```bash
python best.py
```

```text
How many tries did you need? 7
New best score!
Best so far: 7
```

```bash
python best.py
```

```text
How many tries did you need? 9
Best so far: 7
```

```bash
python best.py
```

```text
How many tries did you need? 4
New best score!
Best so far: 4
```

Every time a program ends, Python forgets all its names. The second run still knew the `7` because the program wrote it to a file. Look at the folder: there is a new file `best_score.txt`, and inside it is one number, `4`. The rest of this lesson shows how that works. We come back to `best.py` in step 16.

Memory is like a whiteboard in a meeting room: wiped when the meeting ends. The disk is like a notebook in a drawer: the page is still there tomorrow. A file has a name (like `notes.txt`) and lives in a folder. A plain name means "in the current folder". `data/notes.txt` means "go into the folder `data`, and find the file there".

Using a file always takes three steps: open it, read from it or write to it, close it.

### 2. Write a file: open, write, close

`w1.py`:

```python
file = open("notes.txt", "w")
file.write("Lukas joined the course")
file.close()
print("Saved")
```

`open` takes the file name and the mode. `"w"` means write, and creates the file if it is missing. It gives back a handle (here `file`) that you read or write through.

```bash
python w1.py
```

```text
Saved
```

A new file `notes.txt` now exists. Open it in VS Code, or run `cat notes.txt`: it holds `Lukas joined the course`.

### 3. `write` is not `print`

`w2.py` writes two names with two `write` calls:

```python
file = open("students.txt", "w")
file.write("Lukas")
file.write("Priya")
file.close()
print("Saved")
```

```bash
python w2.py
```

```text
Saved
```

Open `students.txt`: one line, `LukasPriya`. `print` adds a new line at the end, `write` adds nothing. Ask for a new line yourself with `\n`. `w3.py`:

```python
file = open("students.txt", "w")
file.write("Lukas\n")
file.write("Priya\n")
file.close()
print("Saved")
```

```bash
python w3.py
```

```text
Saved
```

Now `students.txt` has two lines, `Lukas` and `Priya`. The old glued text is gone: mode `"w"` replaces everything.

### 4. Let `with` close the file

If an error happens between `open` and `close`, the `close` line never runs. The safer way is `with`. `d1.py`:

```python
with open("notes.txt", "w") as file:
    file.write("Lukas joined the course\n")
    file.write("Priya joined the course\n")
print("Saved")
```

```bash
python d1.py
```

```text
Saved
```

The indented block is the time the file is open. When the block ends, Python closes the file for you, even if an error happens inside. Now `notes.txt` has two lines.

`d2.py` checks it with `file.closed`:

```python
with open("notes.txt", "w") as file:
    print(file.closed)
    file.write("Lukas joined the course\n")
print(file.closed)
```

```bash
python d2.py
```

```text
False
True
```

(This run replaced `notes.txt` with a single line. You fix that in a moment.)

`d3.py` uses the file after the block, which is the mistake:

```python
with open("notes.txt", "w") as file:
    file.write("Lukas joined the course\n")
file.write("Priya joined the course\n")
```

```bash
python d3.py
```

```text
Traceback (most recent call last):
  File "d3.py", line 3, in <module>
    file.write("Priya joined the course\n")
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: I/O operation on closed file.
```

The fix: keep every use of the file inside the `with` block.

Before the next step, run `python d1.py` again, so `notes.txt` has the two lines `Lukas joined the course` and `Priya joined the course`.

### 5. Read the whole file

`e1.py` (mode `"r"` means read):

```python
with open("notes.txt", "r") as file:
    text = file.read()
print(text)
print(type(text))
```

```bash
python e1.py
```

```text
Lukas joined the course
Priya joined the course

<class 'str'>
```

Four rows: the two lines, an empty line, then the type. The file ends with `\n`, and `print` adds one more. `read()` gives one string with the `\n` characters inside it.

### 6. A file remembers its place

`e2.py` leaves out the mode (the default is `"r"`) and reads twice:

```python
with open("notes.txt") as file:
    first = file.read()
    second = file.read()
print(len(first))
print(len(second))
```

```bash
python e2.py
```

```text
48
0
```

The first `read()` took all 48 characters and left the bookmark at the end. The second starts there, so nothing is left. Read once, and keep the text in a name.

### 7. Loop over the file

`e3.py`:

```python
with open("notes.txt") as file:
    for line in file:
        print(line)
```

```bash
python e3.py
```

```text
Lukas joined the course

Priya joined the course

```

Python holds one line at a time, so this works even for a file with a million lines. The blank lines appear because each line still ends in `\n` and `print` adds another. `e4.py` fixes it with `strip()`:

```python
with open("notes.txt") as file:
    for line in file:
        print(line.strip())
```

```bash
python e4.py
```

```text
Lukas joined the course
Priya joined the course
```

### 8. Read all lines into a list

`e5.py`:

```python
with open("notes.txt") as file:
    lines = file.readlines()
print(lines)
print(len(lines))
```

```bash
python e5.py
```

```text
['Lukas joined the course\n', 'Priya joined the course\n']
2
```

Three ways to read: `read()` for the whole text, a `for` loop for one line at a time, and `readlines()` for a list. The loop with `strip()` is the one you will use most.

### 9. Write erases, append adds

`f1.py` opens `notes.txt` with `"w"` and writes one line:

```python
with open("notes.txt", "w") as file:
    file.write("Meera joined the course\n")
```

```bash
python f1.py
cat notes.txt
```

```text
Meera joined the course
```

Lukas and Priya are gone: `"w"` empties the file the moment it opens. `f2.py` uses `"a"` (append):

```python
with open("notes.txt", "a") as file:
    file.write("Rahul joined the course\n")
```

```bash
python f2.py
cat notes.txt
```

```text
Meera joined the course
Rahul joined the course
```

The three modes: `"r"` reads (the file must exist, and it is the default), `"w"` creates the file or erases it, `"a"` creates the file or adds at the end.

### 10. Encoding

A file stores bytes, not letters. Encoding is the rule that turns text into bytes and back. UTF-8 handles English, accents, Hindi and emoji. `g1.py`:

```python
with open("chai.txt", "w", encoding="utf-8") as file:
    file.write("Priya paid for chai at the café")

with open("chai.txt", encoding="utf-8") as file:
    print(file.read())
```

```bash
python g1.py
```

```text
Priya paid for chai at the café
```

`g2.py` reads the same file with an older rule:

```python
with open("chai.txt", encoding="latin-1") as file:
    print(file.read())
```

```bash
python g2.py
```

```text
Priya paid for chai at the cafÃ©
```

The bytes were fine, the reader used the wrong rule. If you leave `encoding` out, Python uses your computer's default, which is not the same everywhere. So always write `encoding="utf-8"`, for reading and for writing.

### 11. A missing file

`missing.py` asks for `note.txt`, but the file is `notes.txt`:

```python
with open("note.txt", encoding="utf-8") as file:
    print(file.read())
```

```bash
python missing.py
```

```text
Traceback (most recent call last):
  File "missing.py", line 1, in <module>
    with open("note.txt", encoding="utf-8") as file:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'note.txt'
```

Read it from the bottom: the error name, the reason, then the file name Python looked for. Two usual causes: a typo in the name, or the right name in the wrong folder. Reading a missing file is an error; `"w"` and `"a"` create it. Catching this error politely is lesson 3 of this module.

### 12. Paths with pathlib

`p1.py`:

```python
from pathlib import Path

path = Path("data") / "notes.txt"
print(path)
print(path.exists())
```

```bash
python p1.py
```

```text
data/notes.txt
False
```

`Path` builds the address; the `/` joins the pieces (it is not division) and uses the right slash on every system. On Windows the first line shows `data\notes.txt`. `exists()` asks whether something lives at the address. Nothing does yet.

### 13. Make a folder, write and read in one go

`p2.py`:

```python
from pathlib import Path

folder = Path("data")
folder.mkdir(exist_ok=True)
path = folder / "notes.txt"
text = "Lukas joined the course"
path.write_text(text, encoding="utf-8")
print(path.exists())
print(path.read_text(encoding="utf-8"))
```

```bash
python p2.py
```

```text
True
Lukas joined the course
```

`exist_ok=True` means: if the folder is already there, do nothing. `write_text` and `read_text` open, use and close the file by themselves, the shortest way for small files.

A path can go anywhere a file name goes. `p3.py` appends with `open`:

```python
from pathlib import Path

path = Path("data") / "notes.txt"
with open(path, "a", encoding="utf-8") as file:
    file.write("\nPriya joined the course")
print(path.read_text(encoding="utf-8"))
```

```bash
python p3.py
```

```text
Lukas joined the course
Priya joined the course
```

### 14. Two folder mistakes

First, delete the folder (`rm -r data`, on Windows `rmdir /s /q data`). `p4.py` writes into `data/notes.txt` without making `data`:

```python
from pathlib import Path

path = Path("data") / "notes.txt"
text = "Lukas joined the course"
path.write_text(text, encoding="utf-8")
```

```bash
python p4.py
```

```text
Traceback (most recent call last):
  File "p4.py", line 5, in <module>
    path.write_text(text, encoding="utf-8")
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  ...
FileNotFoundError: [Errno 2] No such file or directory: 'data/notes.txt'
```

(The `...` stands for a few lines inside Python's own code, which I trimmed. Read your own line and the last line.) Python creates a missing file, never a missing folder.

`p5.py` makes the folder without `exist_ok`:

```python
from pathlib import Path

Path("data").mkdir()
print("Made the folder")
```

```bash
python p5.py
python p5.py
```

```text
Made the folder
```

The second run fails:

```text
Traceback (most recent call last):
  File "p5.py", line 3, in <module>
    Path("data").mkdir()
    ~~~~~~~~~~~~~~~~~~^^
  ...
FileExistsError: [Errno 17] File exists: 'data'
```

That is why `exist_ok=True` is in `p2.py`: you can run it as often as you like.

### 15. Pitfalls with numbers and modes

`k1.py` writes a number:

```python
score = 42
with open("score.txt", "w", encoding="utf-8") as file:
    file.write(score)
```

```bash
python k1.py
```

```text
Traceback (most recent call last):
  File "k1.py", line 3, in <module>
    file.write(score)
    ~~~~~~~~~~^^^^^^^
TypeError: write() argument must be str, not int
```

A file holds text only. Also look at the folder: `score.txt` exists and is empty, because `"w"` created and emptied it before the error. `k1b.py` is the fix:

```python
score = 42
with open("score.txt", "w", encoding="utf-8") as file:
    file.write(str(score))

with open("score.txt", encoding="utf-8") as file:
    print(file.read())
```

```bash
python k1b.py
```

```text
42
```

It comes back as text. Use `int(...)` to get a number again.

`k2.py` opens `notes.txt` with `"w"` and then tries to read it:

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    print(file.read())
```

```bash
python k2.py
```

```text
Traceback (most recent call last):
  File "k2.py", line 2, in <module>
    print(file.read())
          ~~~~~~~~~^^
io.UnsupportedOperation: not readable
```

Worse, `"w"` already erased `notes.txt`: it is now empty. Before you type `"w"`, ask yourself: do I really want an empty file?

### 16. The promise: a best score that survives

Now read `best.py` from step 1 again:

```python
from pathlib import Path

path = Path("best_score.txt")


def load_best():
    if not path.exists():
        return 0
    return int(path.read_text(encoding="utf-8"))


def save_best(score):
    path.write_text(str(score), encoding="utf-8")


best = load_best()
tries = int(input("How many tries did you need? "))
if best == 0 or tries < best:
    best = tries
    save_best(best)
    print("New best score!")
print(f"Best so far: {best}")
```

`load_best` returns `0` when there is no file (first run), otherwise it reads the text and converts it with `int`. `save_best` converts the score with `str`, because a file holds text only. To see the first-run case, delete `best_score.txt` and run it twice, typing `6` and then `8`:

```text
How many tries did you need? 6
New best score!
Best so far: 6
```

```text
How many tries did you need? 8
Best so far: 6
```

To put this into your own guessing game from Module 3 only two lines change: paste the `path` line and the two functions above the game, change `best = 0` to `best = load_best()`, and add `save_best(best)` right after `best = tries`.

## Common mistakes

- Forgetting that `"w"` erases the file the moment it opens, before anything is written.
- Forgetting `\n`: `write` is not `print`.
- Using the file after the `with` block: `ValueError: I/O operation on closed file.`
- Looping over a file and printing without `strip()`: blank lines between the rows.
- Reading twice with `read()`: the second time gives an empty string.
- Writing a number without `str(...)`, and forgetting a number comes back as text.
- Leaving out `encoding="utf-8"`: the file may be read wrongly on another computer.
- `FileNotFoundError`: a typo in the name, or the terminal stands in the wrong folder. Python never creates a missing folder, so `mkdir(exist_ok=True)` first.
- Opening with `"w"` and then reading from it (`not readable`, and the old content is gone).

Interview tip. Why do we open files with `with`? Because it closes the file automatically when the block ends, even if an error happens inside. A forgotten `close()`, or an error before it, can leave the file open and half written, and use up the limited number of open files. It is also shorter and easier to read.

## Clean up

Delete the files these programs created in your working folder: `best_score.txt`, `notes.txt`, `students.txt`, `chai.txt`, `score.txt` and the folder `data`.

## Next

[M06-L02 · CSV and JSON](../m06-l02-csv-and-json/README.md)
