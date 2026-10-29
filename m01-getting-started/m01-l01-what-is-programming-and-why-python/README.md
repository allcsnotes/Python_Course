# M01-L01 · What is Programming and Why Python

> Video: Module 1, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What a program is: a list of precise steps, and why a computer needs every step spelled out
- The shape of every program: input goes in, the program works on it, output comes out
- What the Python interpreter does: it translates your code for the computer, one line at a time
- Why Python is a good first language (readable, many jobs, a huge toolbox, friendly but professional)
- How to run a small Python file and read your first two error messages

## Before you start

- Python 3.14 or newer. Check with `python --version` (on some machines the command is `python3`). If you have not installed it yet, [M01-L02](../m01-l02-setting-up-your-tools/) does that step by step. You can still read this lesson first.
- A terminal opened in this folder. No earlier lesson is needed.
- The Java comparison in step 2 is optional. It needs a JDK (Java 11 or newer). Skip it if you do not have one.

## Files in this folder

| File | What it is |
|------|------------|
| `hello.py` | One line: the Python "Hello, world" |
| `Hello.java` | The same task in Java, for the side-by-side comparison (optional) |
| `three.py` | Three `print` lines, run from top to bottom |
| `fan.py`, `fan_cool.py` | A first decision: print a message only if the temperature is above 30 |
| `welcome.py` | The five-line welcome script for allcsvideos.com (Lukas) |
| `welcome_priya.py` | The same script with the name changed to Priya |
| `welcome_wrong.py` | The same script with its first line moved to the top, on purpose, to cause an error |
| `oops.py`, `fixed.py` | A typo (`nmae`) and its fix |
| `broken.py` | A missing closing quote, on purpose |

## Follow along

### 1. Your first program

A program is a list of precise steps. The robot cook in the video could not make a sandwich until every step (open the bag, open the jar, ...) was written down. Python programs are the same, only shorter. Here is the whole of `hello.py`:

```python
print("Hello, world!")
```

Run it from the terminal, in this folder:

```text
$ python hello.py
Hello, world!
```

`python` starts the interpreter, and `hello.py` is the file it reads. The interpreter reads one line, translates it for the computer, the computer does it, and then the next line comes.

### 2. The same task in Java (optional)

This is only to show how much ceremony Python takes away. You do not need to understand it. Count the lines: five, for the same result.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
```

```bash
java Hello.java
```

```text
Hello, world!
```

### 3. Lines run from top to bottom

```python
print("Good morning")
print("Welcome to Python")
print("Let us begin")
```

```text
$ python three.py
Good morning
Welcome to Python
Let us begin
```

The output is in the same order as the code.

### 4. Python reads almost like English

```python
temperature = 35
if temperature > 30:
    print("Turn on the fan")
```

In English: the temperature is 35. If the temperature is above 30, print "Turn on the fan". Do not worry about the details yet, they come in Module 3.

```text
$ python fan.py
Turn on the fan
```

Now change `temperature = 35` to `temperature = 22` (that is `fan_cool.py`) and run it. The test is no longer true, so nothing is printed, and there is no error:

```text
$ python fan_cool.py
```

### 5. The welcome script

Each of the first three lines stores one piece of information under a label (this is called a variable, and all of Module 2 is about them). The last two lines print a message. The letter `f` and the curly brackets drop the stored values into the sentence.

```python
student = "Lukas"
course = "Python"
lessons = 104
print(f"Welcome to allcsvideos.com, {student}!")
print(f"{course} has {lessons} lessons. Time to start.")
```

Before you run it, guess what it will show. Then:

```text
$ python welcome.py
Welcome to allcsvideos.com, Lukas!
Python has 104 lessons. Time to start.
```

Change `"Lukas"` to `"Priya"` (this is `welcome_priya.py`) and run it again. One change in the code, one change on the screen:

```python
student = "Priya"
course = "Python"
lessons = 104
print(f"Welcome to allcsvideos.com, {student}!")
print(f"{course} has {lessons} lessons. Time to start.")
```

```text
$ python welcome_priya.py
Welcome to allcsvideos.com, Priya!
Python has 104 lessons. Time to start.
```

### 6. Order matters

Move the first `print` line to the very top, before `student` exists (`welcome_wrong.py`):

```python
print(f"Welcome to allcsvideos.com, {student}!")
student = "Lukas"
course = "Python"
lessons = 104
print(f"{course} has {lessons} lessons. Time to start.")
```

```text
$ python welcome_wrong.py
Traceback (most recent call last):
  File "welcome_wrong.py", line 1, in <module>
    print(f"Welcome to allcsvideos.com, {student}!")
                                         ^^^^^^^
NameError: name 'student' is not defined
```

Python reads from the top. At line 1 it has never heard of `student`, so it stops. The last line of an error message is the most useful one: the type of error (`NameError`) and a plain-English reason.

### 7. Read your first two errors

A typo. `oops.py` stores a name and then prints `nmae` instead of `name`:

```python
name = "Lukas"
print(nmae)
```

```text
$ python oops.py
Traceback (most recent call last):
  File "oops.py", line 2, in <module>
    print(nmae)
          ^^^^
NameError: name 'nmae' is not defined
```

Read it from the bottom: Python has never heard of anything called `nmae`. The lines above show the file, the line number, the line itself, and `^^^^` under the word that caused the trouble. Fix the typo (`fixed.py`):

```python
name = "Lukas"
print(name)
```

```text
$ python fixed.py
Lukas
```

A missing closing quote (`broken.py`):

```python
print("Hello)
```

```text
$ python broken.py
  File "broken.py", line 1
    print("Hello)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

`SyntaxError` means Python could not understand the grammar. "Unterminated string literal" means a piece of text was started but never finished.

## Common mistakes

- Expecting the computer to guess what you meant. It does exactly what you wrote, in the order you wrote it.
- Using a label before it exists (step 6). Python reads from the top, so create the variable first.
- A typo in a name (`nmae`), which gives a `NameError`. Read the last line first.
- Forgetting a closing quote or bracket, which gives a `SyntaxError`.
- Only watching the video. Type every example yourself and run it: typing builds the skill.

## Clean up

Nothing to clean up. The lesson only creates the files in this folder.

## Next

[M01-L02 · Setting Up Your Tools](../m01-l02-setting-up-your-tools/)
