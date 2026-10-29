# M01-L04 · What Happens When You Run Python

> Video: Module 1, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- The five stops your file travels through: source text, grammar check, bytecode, virtual machine, output
- Why a syntax error stops everything before line one runs, but a name error only stops at its own line
- What bytecode is (you can look at it with `python -m dis`) and what the `__pycache__` folder is
- The difference between compile time and run time errors, and between a compiler and an interpreter
- Three handy commands: `python -c`, `python -i`, `python -m this`

## Before you start

- Python 3.14 or newer (`python --version`). Do [M01-L03](../m01-l03-your-first-program/) first, you should know how to run a file.
- A terminal opened in this folder.
- Real outputs below were recorded with Python 3.14.7. A different 3.14.x gives the same results, except the version line.

## Files in this folder

| File | What it is |
|------|------------|
| `welcome_bug.py` | Four lines. Lines 1 to 3 print, line 4 asks for a name that does not exist (run time error) |
| `syntax_late.py` | Nine lines, with a bracket never closed on line 9 (compile time error) |
| `syntax_fixed.py` | The same nine lines with the bracket closed |
| `price.py` | Two lines, used to look at bytecode with `python -m dis` |
| `prices.py` | The same two lines plus a `print`, used with `python -i` |
| `late.py`, `late_called.py` | A typo (`totl`) inside a function, first never called, then called |
| `order.py` | Changing a label between two identical `print` lines |
| `zero.py` | The same four lines as `welcome_bug.py`, but the last one divides by zero |
| `pyc_demo/main.py`, `pyc_demo/shop.py` | A tiny two-file program to see `__pycache__` appear |

## Follow along

### 1. The mystery: two files, two behaviours

`welcome_bug.py` has a mistake on line 4. Guess before you run: only an error, or the three messages first?

```python
print("Welcome, Lukas!")
print("Loading your courses...")
print("You have 3 courses.")
print(next_lesson)
```

```text
$ python welcome_bug.py
Welcome, Lukas!
Loading your courses...
You have 3 courses.
Traceback (most recent call last):
  File "welcome_bug.py", line 4, in <module>
    print(next_lesson)
          ^^^^^^^^^^^
NameError: name 'next_lesson' is not defined
```

The three messages come first, then the error. Now `syntax_late.py`, with a mistake on line 9 (a bracket that is opened and never closed):

```python
print("Welcome to All CS Videos")
print("Checking your account...")
print("Account found: Lukas")
print("Loading your courses...")
print("Course 1: Python")
print("Course 2: Java")
print("Course 3: SQL")
print("Everything is ready")
print("Goodbye, Lukas!"
```

```text
$ python syntax_late.py
  File "syntax_late.py", line 9
    print("Goodbye, Lukas!"
         ^
SyntaxError: '(' was never closed
```

Nothing is printed, not even line 1. Python refused to start. The rest of the lesson explains why.

### 2. The journey of your file

1. Source code: the text file you write. To the computer it is just text.
2. Grammar check: Python reads the whole file and checks that every line follows the rules, like a proofreader who checks the entire page first.
3. Bytecode: Python translates the file into a list of very small, simple instructions.
4. Virtual machine: the part of Python that carries out those instructions one by one, top to bottom.
5. Output: whatever your program prints or does.

Text, check, bytecode, machine, output.

### 3. Stop two: the grammar check

Python checks all nine lines of `syntax_late.py` before running any. Line 9 has a syntax error (a grammar mistake), so Python stops there and nothing was ever run. The message names the line, shows it, and points a caret at the bracket. Add the closing bracket (`syntax_fixed.py`) and all nine lines run in order:

```text
$ python syntax_fixed.py
Welcome to All CS Videos
Checking your account...
Account found: Lukas
Loading your courses...
Course 1: Python
Course 2: Java
Course 3: SQL
Everything is ready
Goodbye, Lukas!
```

### 4. Stop three: bytecode

`price.py`:

```python
price = 40
total = price + 5
```

`dis` is short for disassemble: show me the instructions.

```text
$ python -m dis price.py
  0           RESUME                   0

  1           LOAD_SMALL_INT          40
              STORE_NAME               0 (price)

  2           LOAD_NAME                0 (price)
              LOAD_SMALL_INT           5
              BINARY_OP                0 (+)
              STORE_NAME               1 (total)
              LOAD_CONST               1 (None)
              RETURN_VALUE
```

Line 1 became two instructions: load the number 40, store it under the label `price`. Line 2 became four: load `price`, load 5, add, store the answer under `total`. The lines with `RESUME`, `LOAD_CONST` and `RETURN_VALUE` are housekeeping at the start and the end, ignore them. You will never write bytecode yourself, you only need to know it is a simple list of steps. (The exact instruction names can change between Python versions.)

### 5. The `__pycache__` folder

`pyc_demo/shop.py` is a small module with one function. `pyc_demo/main.py` imports it, which just means "use the code from that other file" (Module 7 covers imports properly).

```python
def total(price, qty):
    return price * qty
```

```python
import shop

print("Total:", shop.total(40, 3))
```

Before running, the folder has just the two files:

```bash
cd pyc_demo
ls
```

```text
main.py
shop.py
```

Run `main.py`:

```text
$ python main.py
Total: 120
```

List the folder again:

```bash
ls
ls __pycache__
```

```text
__pycache__
main.py
shop.py
shop.cpython-314.pyc
```

A new folder appeared. The `.pyc` file is the saved bytecode of `shop.py` ("compiled Python"); its name records which Python made it (CPython 3.14). Python saves it to speed up the next run: if `shop.py` has not changed, it skips the translation and loads the saved bytecode. It is safe to delete (Python just makes a new one). Python saves bytecode only for imported files: the file you run directly, `main.py`, is translated again each time, which is very fast.

### 6. Stop four: the virtual machine

The machine keeps a "finger" on the instruction that comes next (many books call it the program counter). It moves down one step at a time. `order.py`:

```python
name = "Lukas"
print("Hello,", name)
name = "Priya"
print("Hello,", name)
```

Guess: the same `print` line appears twice. Will it print the same thing twice?

```text
$ python order.py
Hello, Lukas
Hello, Priya
```

One line of code, two results. At each moment Python uses what is true at that moment.

### 7. Compile time and run time errors

Back to `welcome_bug.py`. The grammar of line 4 (`print(next_lesson)`) is perfect, and Python cannot know in advance whether that name will exist, so the check passes, the bytecode is made, and the machine starts. Lines 1 to 3 print, then line 4 fails: a run time error (found while the program runs). `zero.py` is the same with a different run time error:

```python
print("Welcome, Lukas!")
print("Loading your courses...")
print("You have 3 courses.")
print(3 / 0)
```

```text
$ python zero.py
Welcome, Lukas!
Loading your courses...
You have 3 courses.
Traceback (most recent call last):
  File "zero.py", line 4, in <module>
    print(3 / 0)
          ~~^~~
ZeroDivisionError: division by zero
```

| Error | Found at | Did earlier lines run? |
|---|---|---|
| `SyntaxError` | grammar check (compile time) | No, nothing runs |
| `NameError`, `ZeroDivisionError` | run time | Yes, everything above that line has run |

An error does not undo the lines before it. If an earlier line already saved a file or sent an email, that work is done. When you see an error, ask: did anything print? If nothing ran, suspect a syntax error. If some lines ran, it is a run time error and the traceback names the line where the machine stopped.

### 8. Compiler, interpreter, and CPython

A compiler is like translating a whole book first, then reading it. An interpreter is like a live interpreter at a conference, sentence by sentence. Python does both: it translates the whole file into bytecode first, then the virtual machine carries it out step by step. Because that second part is what you see, people call Python an interpreted language.

The program that does all this is CPython, the standard Python (written in C):

```text
$ python -c "import sys; print(sys.implementation.name)"
cpython
```

```text
$ python --version
Python 3.14.7
```

`3` is the major version, `14` the minor version, `7` the patch number (yours may differ). Bytecode can change between versions, which is why the `.pyc` file name says `cpython-314`.

### 9. Three handy commands

`-c` runs one line of Python and exits:

```text
$ python -c "print(2 + 2)"
4
```

`-i` runs a file and then drops you into the REPL with everything the file created still there. `prices.py` is:

```python
price = 40
total = price + 5
print("Total:", total)
```

```text
$ python -i prices.py
Total: 45
>>> total
45
>>> price * 2
80
>>> exit()
```

`-m this` runs a module that comes with Python, the Zen of Python (a short poem about the Python way of thinking). It begins:

```text
$ python -m this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
...
Readability counts.
...
Errors should never pass silently.
Unless explicitly silenced.
```

Run it yourself to read the whole poem.

## Common mistakes

- Thinking "no error means no bug". `late.py` has a typo, but it is inside a function nobody calls:

```python
def show_total():
    print(totl)


print("Program started")
```

```text
$ python late.py
Program started
```

Calling the function (`late_called.py`) finds the mistake:

```text
$ python late_called.py
Program started
Traceback (most recent call last):
  File "late_called.py", line 6, in <module>
    show_total()
    ~~~~~~~~~~^^
  File "late_called.py", line 2, in show_total
    print(totl)
          ^^^^
NameError: name 'totl' is not defined
```

The grammar check only looks at grammar, and the machine never ran that line. Run every part of your code at least once.
- Fixing the mistake in the editor but forgetting to save. Python reads the file on the disk. A dot on the VS Code tab means unsaved.
- Being afraid of `__pycache__`, or editing the files inside. Python makes it and uses it. Delete it any time, and leave it out when you use Git later.

## Clean up

If you ran `pyc_demo/main.py` inside this folder, delete the folder Python made:

```bash
rm -rf pyc_demo/__pycache__
```

## Next

You have finished Module 1. [M02-L01 · Variables as Labels on Boxes](../../m02-variables-and-data-types/m02-l01-variables-as-labels-on-boxes/)
