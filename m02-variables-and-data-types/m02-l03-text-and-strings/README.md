# M02-L03 · Text and Strings

> Video: Module 2, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- A string is a row of characters with an index that starts at zero; `len`, negative indexes and slices
- Single, double and triple quotes, escapes (`\n`, `\t`, `\"`, `\\`) and raw strings (`r"..."`)
- Strings cannot change (immutable): build a new string instead; join with `+`, repeat with `*`, convert with `str()`
- f-strings and format specifications (`:.2f`, `:,`, `:02d`, alignment, `=`)
- The everyday methods: `upper`, `lower`, `strip`, `title`, `replace`, `split`, `join`, `startswith`, `endswith`, `find`, `count`, `in`
- Unicode: Hindi and emoji, code points versus bytes, comparing strings, and three real jobs (receipt, cleaning input, a URL slug)

## Before you start

- Python 3.14 or newer (`python --version`). Do [M02-L02](../m02-l02-numbers/) first.
- A terminal opened in this folder. The REPL parts are typed at the `>>>` prompt (start it with `python`).

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening puzzle: `"5" + "5"` and `"5" * 3` |
| `quotes.py`, `triple.py`, `multi.py` | Single, double and triple quotes; a multi-line f-string |
| `escapes.py`, `raw.py` | The five escapes, and the Windows path trap with `r"..."` |
| `immut.py`, `newstr.py` | Trying to change a character, and building a new string instead |
| `concat.py`, `concat_err.py`, `concat_fix.py` | Joining text, and the text-plus-number error and fix |
| `f1.py` to `f4.py` | f-strings: basics, number formats, alignment, the `=` trick |
| `ords.py`, `uni1.py`, `uni2.py`, `thumb.py` | Code points, Hindi and emoji, bytes |
| `receipt.py`, `clean.py`, `slug.py` | The three real jobs |
| `index_error.py`, `pit_index.py`, `pit_empty.py`, `pit_type.py`, `pit_method.py`, `pit_method_fix.py`, `pit_f.py` | The pitfalls |

## Follow along

### 1. The opening puzzle

Quotes turn each `5` into text. Adding sticks two pieces together, and `*` repeats. Guess first:

**`hook.py`**

```python
print("5" + "5")
print("5" * 3)
```

```text
$ python hook.py
55
555
```

Python did no maths at all.

### 2. A string is a row of characters

Think of beads on a thread. Each character (letter, digit, space, symbol) is a bead, and each has a place number called the index. The first bead is number 0, like the start of a ruler. A space is a character too, and the length (`len`) counts every bead:

```text
>>> len("Python")
6
>>> len("a b")
3
>>> len("")
0
>>> len("Hi!")
3
```

### 3. Quotes

Single and double quotes mean the same. Use double quotes when the text has an apostrophe, single quotes when it has double quotes. Triple quotes keep line breaks, so one string can span several lines:

**`quotes.py`**

```python
single = 'Asha'
double = "Asha"
print(single)
print(double)
print("It's Python")
print('She said "hi"')
```

```text
$ python quotes.py
Asha
Asha
It's Python
She said "hi"
```

**`triple.py`**

```python
note = """Dear student,
welcome to Python!
See you in class."""
print(note)
```

```text
$ python triple.py
Dear student,
welcome to Python!
See you in class.
```

A multi-line string is still one string: those line breaks are characters like any other.

### 4. Escapes and raw strings

An escape is a backslash plus a letter. `\n` is a new line, `\t` a tab, `\"` a double quote, `\'` a single quote, `\\` one backslash (you write two to get one):

**`escapes.py`**

```python
print("Name:\tAsha")
print("Line one\nLine two")
print("She said \"hi\"")
print('It\'s Python')
print("C:\\new\\table")
```

```text
$ python escapes.py
Name:	Asha
Line one
Line two
She said "hi"
It's Python
C:\new\table
```

In the REPL you can see a new line is a single character. `"Hi\nthere"` has length 8: 2 + 5 + 1.

```text
>>> "Hi\nthere"
'Hi\nthere'
>>> print("Hi\nthere")
Hi
there
>>> len("Hi\nthere")
8
```

The trap: a Windows path has backslashes. Python sees `\n` and `\t` and makes a new line and a tab. An `r` before the opening quote makes a raw string, and Python leaves every backslash alone:

**`raw.py`**

```python
print("C:\new\table")
print(r"C:\new\table")
```

```text
$ python raw.py
C:
ew	able
C:\new\table
```

### 5. Index, slice, and the off-by-one

```text
>>> name = "Python"
>>> name[0]
'P'
>>> name[1]
'y'
>>> name[5]
'n'
>>> name[-1]
'n'
>>> name[-2]
'o'
>>> len(name)
6
```

A character comes back in quotes because it is a string of length one. Negative indexes count from the right: `-1` is the last character. The last index of a string of length n is n - 1. Ask for a place that does not exist and you get an off-by-one error:

**`index_error.py`**

```python
name = "Python"
print(name[6])
```

```text
$ python index_error.py
Traceback (most recent call last):
  File "index_error.py", line 2, in <module>
    print(name[6])
          ~~~~^^^
IndexError: string index out of range
```

A slice cuts out a piece: `[start:stop]`. Picture the numbers on the lines between the beads. The slice starts at the start line and stops at the stop line, so the stop is left out. Both are optional, a negative number counts from the right, and a stop that is too big does not complain:

```text
>>> name = "Python"
>>> name[0:2]
'Py'
>>> name[2:5]
'tho'
>>> name[:3]
'Pyt'
>>> name[2:]
'thon'
>>> name[-3:]
'hon'
>>> name[0:100]
'Python'
```

A third number is the step. A negative step walks backwards, so `[::-1]` reverses a string:

```text
>>> name = "Python"
>>> name[::2]
'Pto'
>>> name[1:5:2]
'yh'
>>> name[::-1]
'nohtyP'
```

### 6. Strings cannot change

**`immut.py`**

```python
name = "Python"
name[0] = "J"
```

```text
$ python immut.py
Traceback (most recent call last):
  File "immut.py", line 2, in <module>
    name[0] = "J"
    ~~~~^^^
TypeError: 'str' object does not support item assignment
```

A string is immutable: it can never be changed after it is made. (If parts of a program could change a shared string, other parts would be surprised.) To get "Jython", build a new string from pieces and put a label on it. The old string is untouched:

**`newstr.py`**

```python
name = "Python"
new_name = "J" + name[1:]
print(new_name)
print(name)
```

```text
$ python newstr.py
Jython
Python
```

### 7. Joining, repeating and converting

`+` (concatenation) joins exactly what you give it, so add the space yourself. `*` repeats:

**`concat.py`**

```python
first = "Asha"
last = "Rao"
full = first + " " + last
print(full)
print("-" * 20)
print("ha" * 3)
```

```text
$ python concat.py
Asha Rao
--------------------
hahaha
```

Joining text and a number is a `TypeError`: Python will not guess whether `+` should add or join. Fix it by turning the number into text with `str()`:

**`concat_err.py`**

```python
students = 3
print("Students: " + students)
```

```text
$ python concat_err.py
Traceback (most recent call last):
  File "concat_err.py", line 2, in <module>
    print("Students: " + students)
          ~~~~~~~~~~~~~^~~~~~~~~~
TypeError: can only concatenate str (not "int") to str
```

**`concat_fix.py`**

```python
students = 3
print("Students: " + str(students))
```

```text
$ python concat_fix.py
Students: 3
```

```text
>>> str(499)
'499'
>>> str(3.5)
'3.5'
>>> len(str(12345))
5
```

### 8. f-strings

Put an `f` right before the opening quote, and anything in curly braces is filled in, like blanks in a form letter. You can put any expression in the braces, even a method call:

**`f1.py`**

```python
name = "Lukas"
course = "Python"
print(f"{name} enrolled in {course}")
print(f"2 + 3 = {2 + 3}")
print(f"{name.upper()} is in!")
```

```text
$ python f1.py
Lukas enrolled in Python
2 + 3 = 5
LUKAS is in!
```

After a colon comes a format specification. `.2f` is two digits after the decimal point, `,` adds thousands separators, `02d` is a whole number padded with zeros to width 2:

**`f2.py`**

```python
price = 1499.5
students = 1234567
print(f"Price: {price}")
print(f"Price: {price:.2f}")
print(f"Students: {students:,}")
print(f"Rs {price * 100:,.2f}")
lesson = 7
print(f"Lesson {lesson:02d}")
```

```text
$ python f2.py
Price: 1499.5
Price: 1499.50
Students: 1,234,567
Rs 149,950.00
Lesson 07
```

`>`, `<` and `^` right-align, left-align and centre inside a width. A character before them is the fill:

**`f3.py`**

```python
name = "Priya"
print(f"[{name:>10}]")
print(f"[{name:<10}]")
print(f"[{name:^10}]")
print(f"[{name:*^11}]")
```

```text
$ python f3.py
[     Priya]
[Priya     ]
[  Priya   ]
[***Priya***]
```

An `=` at the end of the braces prints the expression, an equals sign and its value, which is handy when testing:

**`f4.py`**

```python
course = "Python"
price = 1499
print(f"{course = }")
print(f"{price = }")
print(f"{price * 2 = }")
```

```text
$ python f4.py
course = 'Python'
price = 1499
price * 2 = 2998
```

Triple quotes with an `f` in front give a multi-line message:

**`multi.py`**

```python
name = "Lukas"
msg = f"""Hello {name},
your course is ready.
Happy learning!"""
print(msg)
```

```text
$ python multi.py
Hello Lukas,
your course is ready.
Happy learning!
```

To print real curly braces, double them:

```text
>>> name = "Asha"
>>> f"{{name}} is {name}"
'{name} is Asha'
```

Cheat sheet: `.2f` decimals, `,` thousands, `02d` zero padding, `>` `<` `^` alignment with a width.

### 9. String methods

A method is a function that belongs to a value: write the value, a dot, the method name, then round brackets. Methods never change the original string, they return a new one.

```text
>>> text = "  Intro to Python  "
>>> text.upper()
'  INTRO TO PYTHON  '
>>> text.lower()
'  intro to python  '
>>> text.strip()
'Intro to Python'
>>> text.strip().title()
'Intro To Python'
>>> text.replace("Python", "Java")
'  Intro to Java  '
>>> text
'  Intro to Python  '
```

`strip` removes spaces at both ends only. `title` capitalises each word. Two methods in a row (`strip().title()`) work from left to right. The last line shows the original is unchanged. If you want to keep the new string, put a label on it.

`split` cuts a string into a list (a row of pieces, covered in Module 5), `join` glues pieces back with the string in front as the glue:

```text
>>> title = "Intro to Python"
>>> words = title.split()
>>> words
['Intro', 'to', 'Python']
>>> "a,b,c".split(",")
['a', 'b', 'c']
>>> "-".join(words)
'Intro-to-Python'
```

Yes/no questions and searching:

```text
>>> title = "Intro to Python"
>>> title.startswith("Intro")
True
>>> title.endswith("on")
True
>>> title.find("to")
6
>>> title.find("Java")
-1
>>> title.count("o")
3
>>> "Py" in title
True
>>> "Java" in title
False
```

`find` gives the index where a piece starts, or `-1` if it is not there.

### 10. Hindi, emoji, Unicode

Python counts code points. Unicode is a giant list that gives every symbol in every language its own number (a code point). The Hindi word below is built from several pieces (consonants, a joining mark, a vowel sign), so its length is 6, and the smiling face has length 1:

**`uni1.py`**

```python
word = "नमस्ते"
print(word)
print(len(word))
face = "😀"
print(len(face))
```

```text
$ python uni1.py
नमस्ते
6
1
```

`ord` gives a character's number and `chr` turns a number back into a character:

**`ords.py`**

```python
print(ord("A"))
print(ord("a"))
print(ord("अ"))
print(chr(72))
```

```text
$ python ords.py
65
97
2309
H
```

Careful with emoji: a thumbs up with a skin colour looks like one picture, but it is the thumb plus a colour code:

**`thumb.py`**

```python
thumb = "👍🏽"
print(thumb)
print(len(thumb))
```

```text
$ python thumb.py
👍🏽
2
```

Files store text as bytes (small units of storage). The standard way is UTF-8, and Python reads and writes UTF-8 by default. A letter takes 1 byte, Hindi letters 3, an emoji 4:

**`uni2.py`**

```python
word = "नमस्ते"
face = "😀"
print(len(word.encode("utf-8")))
print(len(face.encode("utf-8")))
print(len("Python".encode("utf-8")))
```

```text
$ python uni2.py
18
4
6
```

Indexing, slicing, f-strings and every method work on Hindi and emoji just like English.

### 11. Comparing strings

`==` asks whether two strings are the same. A capital and a small letter are different characters, so a login form must make both sides lower case first. Strings can be put in order too: Python compares the code numbers, so every capital letter comes before every small letter:

```text
>>> email = "Lukas@Mail.com"
>>> email == "lukas@mail.com"
False
>>> email.lower() == "lukas@mail.com"
True
>>> "Zebra" < "apple"
True
>>> ord("Z")
90
>>> ord("a")
97
```

### 12. Three real jobs

Job 1, a receipt. Priya bought Python Basics at 1499 rupees plus 18 percent tax. The course name is left-aligned in 20 places, the numbers right-aligned in 10, so the prices line up:

**`receipt.py`**

```python
student = "Priya"
course = "Python Basics"
price = 1499
tax = price * 0.18
total = price + tax
print("=" * 30)
print(f"{'RECEIPT':^30}")
print("=" * 30)
print(f"Student: {student}")
print(f"{course:<20}{price:>10,.2f}")
print(f"{'GST 18%':<20}{tax:>10,.2f}")
print("-" * 30)
print(f"{'Total':<20}{total:>10,.2f}")
```

```text
$ python receipt.py
==============================
           RECEIPT            
==============================
Student: Priya
Python Basics         1,499.00
GST 18%                 269.82
------------------------------
Total                 1,768.82
```

Job 2, cleaning what people type. `split` cuts the name at every run of spaces and drops them, `join` glues it back with one space. `strip` and `lower` clean the email:

**`clean.py`**

```python
raw_name = "   lukas    WEBER  "
raw_email = " Lukas.Weber@Example.COM "
name = " ".join(raw_name.split()).title()
email = raw_email.strip().lower()
print(f"Welcome, {name}!")
print(email)
print(email.endswith("@example.com"))
```

```text
$ python clean.py
Welcome, Lukas Weber!
lukas.weber@example.com
True
```

Job 3, the problem from the start: a course title with extra spaces and odd capitals becomes a slug, a short web-friendly name for a page address:

**`slug.py`**

```python
title = "  Python  for   Absolute BEGINNERS "
slug = "-".join(title.lower().split())
print(slug)
print(f"https://allcsvideos.com/courses/{slug}")
```

```text
$ python slug.py
python-for-absolute-beginners
https://allcsvideos.com/courses/python-for-absolute-beginners
```

## Interview tip

"Why can't you change a character in a Python string?" Strings are immutable. Once made, a string never changes, which makes it safe to share and to use as a dictionary key. To "change" it you build a new string and attach the name to that.

## Common mistakes

- Off by one: `name[len(name)]` is out of range. The last index is `len(name) - 1`, or just `-1`.

**`pit_index.py`**

```python
name = "Python"
print(name[len(name)])
```

```text
$ python pit_index.py
Traceback (most recent call last):
  File "pit_index.py", line 2, in <module>
    print(name[len(name)])
          ~~~~^^^^^^^^^^^
IndexError: string index out of range
```

- Asking for the first character of an empty string raises an error, but a slice such as `nickname[:1]` is forgiving and gives an empty string.

**`pit_empty.py`**

```python
nickname = ""
print(nickname[0])
```

```text
$ python pit_empty.py
Traceback (most recent call last):
  File "pit_empty.py", line 2, in <module>
    print(nickname[0])
          ~~~~~~~~^^^
IndexError: string index out of range
```

- Joining text and a number with `+`:

**`pit_type.py`**

```python
total = 1768.82
print("Total: " + total)
```

```text
$ python pit_type.py
Traceback (most recent call last):
  File "pit_type.py", line 2, in <module>
    print("Total: " + total)
          ~~~~~~~~~~^~~~~~~
TypeError: can only concatenate str (not "float") to str
```

- Forgetting that methods return a new string. Nobody kept the result of `title.upper()`:

**`pit_method.py`**

```python
title = "python basics"
title.upper()
print(title)
```

```text
$ python pit_method.py
python basics
```

Put a label on the result:

**`pit_method_fix.py`**

```python
title = "python basics"
title = title.upper()
print(title)
```

```text
$ python pit_method_fix.py
PYTHON BASICS
```

- Forgetting the `f`. Without it the braces are printed as they are:

**`pit_f.py`**

```python
name = "Asha"
print("Hello, {name}!")
print(f"Hello, {name}!")
```

```text
$ python pit_f.py
Hello, {name}!
Hello, Asha!
```

## Your turn

Store your full name, with extra spaces, in a label. Print it clean and in title case, followed by how many letters it has (without the spaces).

## Clean up

Nothing to clean up.

## Next

[M02-L04 · True, False and None](../m02-l04-true-false-and-none/)
