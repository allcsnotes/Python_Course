# M01-L03 · Your First Program

> Video: Module 1, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- How to talk to Python live in the REPL (read, evaluate, print, loop)
- `print`: a function, how to call it, and what an argument is
- Strings and quotes, `\n` and `\t`, and why text needs quotes
- Comments with `#`
- How to save a program in a file, run it, and why you must save first
- How to read an error message (last line first) and fix five common beginner mistakes

## Before you start

- Python 3.14 or newer: `python --version` should print `Python 3.14.x`. If not, do [M01-L02](../m01-l02-setting-up-your-tools/) first.
- A terminal opened in this folder (or in your own `allcs-python` folder if you type the files yourself, which is better).

## Files in this folder

| File | What it is |
|------|------------|
| `hello.py` | The first program: `print("Hello, World!")` |
| `quotes.py` | Double quotes, single quotes, and quotes inside text |
| `noquote.py` | `print(Hello)` without quotes, to cause a `NameError` |
| `many.py`, `numtext.py`, `blank.py`, `escape.py` | Printing several things, sum versus text, an empty line, `\n` and `\t` |
| `comments.py` | Three kinds of comment line |
| `welcome.py` | The "Hello, Asha!" file with two prints |
| `calc.py` | A sum with no `print`: nothing is shown for it |
| `exp_text.py`, `exp_twice.py`, `swap.py` | Experiments: change the text, repeat a line, swap two lines |
| `banner.py` | The welcome banner exercise (one solution) |
| `err_quote.py`, `err_name.py`, `err_case.py`, `err_bracket.py`, `err_indent.py` | The five mistakes, each on purpose |

## Follow along

### 1. Talk to Python in the REPL

Type `python` and press Enter. Python prints its version and then the prompt `>>>`. The exact first line (version, date, system) will differ on your machine.

```text
$ python
Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 2 + 3
5
>>> 10 / 4
2.5
>>> "hi"
'hi'
>>> "ha" * 3
'hahaha'
>>> exit()
$
```

Python does not round `10 / 4`: you get `2.5`. The REPL shows text with single quotes as a reminder that it is text. The name REPL stands for Read, Eval, Print, Loop. When you exit, everything you typed is gone, which is why we use files next.

### 2. print is a function

The REPL shows answers by itself, a real program does not. To show something you call `print`: its name followed by round brackets, with the thing to show (the argument) inside.

```text
>>> print("Hello, World!")
Hello, World!
```

`print` shows text the way a person reads it, with no quotes. Text in quotes is called a string. Double and single quotes mean the same, as long as you end with the same kind you started with. Use the other kind when your text contains a quote:

```python
print("Hello")
print('Hello')
print("It's Python")
print('She said "hi"')
```

```text
$ python quotes.py
Hello
Hello
It's Python
She said "hi"
```

Why quotes at all? Remove them (`noquote.py`):

```python
print(Hello)
```

```text
$ python noquote.py
Traceback (most recent call last):
  File "noquote.py", line 1, in <module>
    print(Hello)
          ^^^^^
NameError: name 'Hello' is not defined
```

Without quotes Python does not see text, it sees a name, looks for something called `Hello`, and finds nothing. In the REPL you get the same error:

```text
>>> Hello
Traceback (most recent call last):
  File "<python-input-1>", line 1, in <module>
    Hello
NameError: name 'Hello' is not defined
```

### 3. Print several things, sums, empty lines

Commas between the arguments print them with one space between. On the second line the sum is worked out first.

```python
print("Asha", "is", "learning", "Python")
print("Total:", 2 + 3)
```

```text
$ python many.py
Asha is learning Python
Total: 5
```

Quotes decide: calculate, or leave alone.

```python
print(2 + 3)
print("2 + 3")
print(7, "days")
```

```text
$ python numtext.py
5
2 + 3
7 days
```

An empty `print()` gives an empty line. Backslash n (`\n`) is a line break inside text and backslash t (`\t`) is a tab.

```python
print("Line one")
print()
print("Line two")
```

```text
$ python blank.py
Line one

Line two
```

```python
print("Course:\nPython")
print("Name:\tAsha")
print("City:\tMumbai")
```

```text
$ python escape.py
Course:
Python
Name:	Asha
City:	Mumbai
```

### 4. Comments

A hash `#` makes Python ignore the rest of the line. A comment explains why, and putting `#` in front of code switches that line off ("commenting out").

```python
# Greet the new student
print("Welcome to allcsvideos!")  # shown on screen
# print("This line is switched off")
```

```text
$ python comments.py
Welcome to allcsvideos!
```

Only one line of output: the two comments did nothing, and the switched-off line did nothing either.

### 5. Save a program in a file and run it

In VS Code: open your `allcs-python` folder, click the new file button in the explorer, and name the file `hello.py` (the `.py` tells VS Code and Python it is a Python file). Type the line yourself, do not paste it (VS Code adds the closing bracket and quote for you). Save with Ctrl + S (Command + S on a Mac). A dot on the tab means "not saved yet". Python only sees what is saved on disk, so always save before you run.

```python
print("Hello, World!")
```

Open the terminal in the same folder and run:

```text
$ python hello.py
Hello, World!
```

Python opened the file, ran each line from top to bottom, and stopped at the end. The play button at the top right of the editor does the same with a longer command that includes the full path. Learn the terminal way too: on servers there is no play button.

The save problem for real: change the text to `Hello, Asha!` but forget to save (the dot is still on the tab) and run the file. You get the old message, because the disk still has the old text. Save, run again, and you see `Hello, Asha!`. The rule is: save, then run. Then add a second print line (this is `welcome.py`), save and run:

```python
print("Hello, Asha!")
print("I am learning Python")
```

```text
$ python welcome.py
Hello, Asha!
I am learning Python
```

Two lines, in the same order as the code.

### 6. A file shows nothing unless you print

In the REPL a sum shows its answer automatically. In a file it does not:

```python
2 + 3
print(10 / 4)
```

```text
$ python calc.py
2.5
```

Only `2.5` appears. The sum on line 1 was worked out, but nobody asked to see it, so it was thrown away. In a file, if you want to see something, print it.

### 7. Read an error message

Take `noquote.py` from step 2. Read the parts of the message:

- First line: `Traceback (most recent call last):` means "here is the trail that led to the problem".
- Second line: the file and the line number. `in <module>` means the top level of the file. Ignore it for now.
- Third line: the code on that line.
- The carets `^^^^^` point at the exact piece Python had trouble with.
- Last line: the type of error and a plain-English reason. This is the most useful line.

The recipe: read the last line first, go to the line number, look at the carets, fix one thing, run again.

Mistake 1, a missing closing quote:

```python
print("Hello, World!)
```

```text
$ python err_quote.py
  File "err_quote.py", line 1
    print("Hello, World!)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

A `SyntaxError` means Python could not understand the grammar. There is no Traceback line, because Python checks the grammar before it runs anything. Fix: add the missing quote.

Mistake 2, a typing slip:

```python
prnt("Hello, World!")
```

```text
$ python err_name.py
Traceback (most recent call last):
  File "err_name.py", line 1, in <module>
    prnt("Hello, World!")
    ^^^^
NameError: name 'prnt' is not defined. Did you mean: 'print'?
```

Python has never heard of `prnt` and guesses the fix for you: "Did you mean: 'print'?". Read that hint and use it.

Mistake 3, a capital letter:

```python
Print("Hello, World!")
```

```text
$ python err_case.py
Traceback (most recent call last):
  File "err_case.py", line 1, in <module>
    Print("Hello, World!")
    ^^^^^
NameError: name 'Print' is not defined. Did you mean: 'print'?
```

Python is case sensitive: `Print` and `print` are different names. The function is always lower case.

Mistake 4, a bracket that never closes:

```python
print("Hello, World!"
```

```text
$ python err_bracket.py
  File "err_bracket.py", line 1
    print("Hello, World!"
         ^
SyntaxError: '(' was never closed
```

The caret points at the opening bracket that has no partner. Whenever you open a bracket or a quote, close it.

Mistake 5, one stray space at the start of the line:

```python
 print("Hello, World!")
```

```text
$ python err_indent.py
  File "err_indent.py", line 1
    print("Hello, World!")
IndentationError: unexpected indent
```

Indentation is the empty space at the start of a line. In Python it has a meaning (Module 3). For now start your lines at the very left edge. There is no caret, so look at the start of the line yourself.

### 8. Experiments

Always ask: what if I change this? The computer never gets tired.

`exp_twice.py` prints the same line twice, `swap.py` swaps the order of two prints:

```python
print("Hello, World!")
print("Hello, World!")
```

```text
$ python exp_twice.py
Hello, World!
Hello, World!
```

```python
print("I am learning Python")
print("Hello, World!")
```

```text
$ python swap.py
I am learning Python
Hello, World!
```

The output swaps too: Python runs the lines from top to bottom, in the order you wrote them Changing the text is `exp_text.py`:

```text
$ python exp_text.py
Hello, Asha!
```


Your turn: print a welcome banner for allcsvideos.com with Asha's name, four lines, using `"=" * 30` for the border. Pause and try it before you open this solution:

```python
# Welcome banner for allcsvideos.com
print("=" * 30)
print("  Welcome to allcsvideos.com")
print("  Your guide today: Asha")
print("=" * 30)
```

```text
$ python banner.py
==============================
  Welcome to allcsvideos.com
  Your guide today: Asha
==============================
```

Yours may look a little different, and that is fine, as long as it runs without an error.

## Common mistakes

- Forgetting to save before running (the old output appears).
- Leaving out quotes around text (`NameError`) or the closing quote (`SyntaxError`).
- A typo or wrong capital in `print` (`NameError`, with a "Did you mean" hint).
- An unclosed bracket, or a stray space at the start of a line (`IndentationError`).
- Expecting a file to show a sum without `print`.
- Pasting the code instead of typing it. Typing builds the skill.

## Clean up

Nothing to clean up. Delete the `err_*.py` files if you copied them somewhere you do not want errors.

## Next

[M01-L04 · What Happens When You Run Python](../m01-l04-what-happens-when-you-run-python/)
