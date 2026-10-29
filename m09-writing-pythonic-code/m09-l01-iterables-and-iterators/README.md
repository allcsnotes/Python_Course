# M09-L01 · Iterables and Iterators

> Video: Module 9, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What an iterable (a "book") and an iterator (a "walker" with a bookmark) are
- How `iter()` and `next()` work, and what `StopIteration` means
- What a `for` loop really does, written out by hand with `while` and `try`
- Why a walker can be used only once, but a list can be looped over again and again
- How to build your own walker with `__iter__` and `__next__`, and a better two-class version
- Why walkers are lazy, and three common mistakes

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed. Everything runs in a plain terminal.
- You should have seen the dunder methods lesson (M08): the `Course` class here is the one from that lesson. No earlier lesson folder is required.

## Files in this folder

| File | What it is |
|------|------------|
| `walker.py` | The list, `iter()` and four `next()` calls: the hook |
| `forloop.py` | A plain `for` loop over the lessons |
| `unmasked.py` | The same loop written by hand with `while`, `try` and `next()` |
| `usedup.py` | Two loops sharing one walker: the second prints nothing |
| `lessons.txt` | Three lines of text for the file example |
| `fileagain.py` | A file is a walker: reading it twice gives 3 then 0 |
| `countdown_v1_no_next.py` | Countdown with `__iter__` only: Python refuses |
| `countdown_v2_next.py` | Countdown with `__next__`: a real walker |
| `countdown_v3_twice.py` | Looping over one Countdown twice: the second loop is empty |
| `countdown_v4_two_classes.py` | Book (`Countdown`) and bookmark (`CountdownWalker`) as two classes |
| `countdown_v5_short.py` | The short version: `__iter__` returns `iter(range(...))` |
| `course.py` | The `Course` class from the dunder methods lesson, explained |
| `tickets.py` | `itertools.count`, a lazy ticket machine |
| `p1_nextlist.py` | Pitfall 1: `next()` on a list |
| `p2_len.py` | Pitfall 2: `len()` of a walker |
| `p3_int.py` | Pitfall 3: a `for` loop over a number |

## Follow along

### 1. The hook: ask a walker four times

Asha has a list of three lessons and one new line, `walker = iter(lessons)`. Then she asks the walker for an item four times with `next()`. Guess the output before you run it.

```python
lessons = ["Intro", "Loops", "Functions"]
walker = iter(lessons)
print(next(walker))
print(next(walker))
print(next(walker))
print(next(walker))
```

```bash
python walker.py
```

```
Intro
Loops
Functions
Traceback (most recent call last):
  File "walker.py", line 6, in <module>
    print(next(walker))
          ~~~~^^^^^^^^
StopIteration
```

Three lessons come out, and the fourth ask ends in `StopIteration`: the walker had nothing left to give. Yet a `for` loop over the same list never shows this error. The rest of the lesson explains why.

### 2. Iterable = book, iterator = walker

An **iterable** is anything you can go through one item at a time: a list, a string, a dictionary, a `range`, a file. An **iterator** (we say *walker*) is the helper that remembers where you are and hands out the next item. `iter()` takes a book and gives you a brand-new walker. `next()` takes a walker and gives the next item.

Open the Python REPL (type `python`, press Enter) and make two walkers over the same list. Each has its own bookmark:

```pycon
>>> lessons = ["Intro", "Loops", "Functions"]
>>> a = iter(lessons)
>>> b = iter(lessons)
>>> next(a)
'Intro'
>>> next(a)
'Loops'
>>> next(b)
'Intro'
>>> type(a)
<class 'list_iterator'>
```

`a` is two steps in, `b` is one step in, and the list never changed. `type(a)` shows that the walker is a small separate object (`list_iterator`), not the list.

### 3. `StopIteration` is not a bug

The fourth `next()` raised `StopIteration`. That is the walker's way of saying "I am finished". If you would rather get a value back than an error, give `next()` a second argument, a default:

```pycon
>>> walker = iter(["Intro", "Loops"])
>>> next(walker, "done")
'Intro'
>>> next(walker, "done")
'Loops'
>>> next(walker, "done")
'done'
```

No error: `next()` with a default never raises `StopIteration`, it returns the default.

### 4. What a `for` loop really does

Here is a plain `for` loop. No walker, no `next()`, no error:

```python
lessons = ["Intro", "Loops", "Functions"]

for lesson in lessons:
    print(lesson)
```

```bash
python forloop.py
```

```
Intro
Loops
Functions
```

And the same loop written by hand. Line 3 asks the book for a walker (once). Then an endless `while` loop asks for the next item; when `StopIteration` arrives, `except` catches it and `break` leaves the loop:

```python
lessons = ["Intro", "Loops", "Functions"]

walker = iter(lessons)
while True:
    try:
        lesson = next(walker)
    except StopIteration:
        break
    print(lesson)
```

```bash
python unmasked.py
```

```
Intro
Loops
Functions
```

The secret of a `for` loop in three steps: call `iter()` on the book once; call `next()` again and again, putting each answer in the loop variable; when `StopIteration` arrives, stop quietly. If the thing after `in` is already a walker, the loop still calls `iter()` on it, and a walker answers `iter()` with itself:

```pycon
>>> lessons = ["Intro", "Loops", "Functions"]
>>> walker = iter(lessons)
>>> iter(walker) is walker
True
>>> iter(lessons) is lessons
False
```

### 5. A walker is used up after one trip

A bookmark only moves forward. What happens when two loops share one walker? Guess first.

```python
lessons = ["Intro", "Loops", "Functions"]
walker = iter(lessons)

for lesson in walker:
    print(lesson)
print("--- again ---")
for lesson in walker:
    print(lesson)
```

```bash
python usedup.py
```

```
Intro
Loops
Functions
--- again ---
```

The first loop walks the bookmark to the end. The second loop gets `StopIteration` straight away and ends quietly, with no error. A book is different: every `list(lessons)` makes a fresh walker.

```pycon
>>> lessons = ["Intro", "Loops", "Functions"]
>>> list(lessons)
['Intro', 'Loops', 'Functions']
>>> list(lessons)
['Intro', 'Loops', 'Functions']
```

A file is a walker too (you saw this in the files lesson). It answers `iter()` with itself, so you can loop over it, but only once. Create `lessons.txt` with three lines and read it twice:

```
Intro
Loops
Functions
```

```python
with open("lessons.txt") as f:
    print(len(list(f)))
    print(len(list(f)))
```

```bash
python fileagain.py
```

```
3
0
```

Three, then zero. If you need the lines twice, keep them in a list or open the file again.

### 6. Build your own walker: `__iter__` and `__next__`

Meera starts a live class with a countdown: 3, 2, 1. We write a class `Countdown` with only `__iter__`, which hands back `self`. Python refuses:

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self


for number in Countdown(3):
    print(number)
```

```bash
python countdown_v1_no_next.py
```

```
Traceback (most recent call last):
  File "countdown_v1_no_next.py", line 9, in <module>
    for number in Countdown(3):
                  ~~~~~~~~~^^^
TypeError: iter() returned non-iterator of type 'Countdown'
```

Python asked for a walker and got something that cannot answer `next()`. A walker needs a method called `__next__`. Add it: if `current` is zero we are finished and raise `StopIteration`; otherwise take one off and return the value.

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


for number in Countdown(3):
    print(number)
print("Class starts!")
```

```bash
python countdown_v2_next.py
```

```
3
2
1
Class starts!
```

A walker is any object with two methods: `__iter__` (returns the walker itself) and `__next__` (returns the next item or raises `StopIteration`). Together they are called the **iterator protocol**.

### 7. Fix the reuse problem: split book and bookmark

Our `Countdown` is the book and the bookmark in one object, so looping over the same timer twice gives nothing the second time:

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


timer = Countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)
```

```bash
python countdown_v3_twice.py
```

```
3
2
1
--- again ---
```

For something you want to loop over again and again, split the roles. `Countdown` is the book (it only keeps the start number) and `CountdownWalker` is the bookmark:

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return CountdownWalker(self.start)


class CountdownWalker:
    def __init__(self, current):
        self.current = current

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


timer = Countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)
```

```bash
python countdown_v4_two_classes.py
```

```
3
2
1
--- again ---
3
2
1
```

Every loop gets its own fresh walker. There is also a shorter way: `__iter__` can borrow a walker that already exists, such as `iter()` of a `range` counting down. No second class:

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return iter(range(self.start, 0, -1))


timer = Countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)
```

```bash
python countdown_v5_short.py
```

```
3
2
1
--- again ---
3
2
1
```

Now the line from the dunder methods lesson finally makes sense. A `Course` keeps its lessons in a list, and `__iter__` returns `iter(self.lessons)`: a fresh walker from the list's own book.

```python
class Course:
    def __init__(self, title, lessons):
        self.title = title
        self.lessons = lessons

    def __iter__(self):
        return iter(self.lessons)


basics = Course("Python Basics", ["Intro", "Loops"])
walker = iter(basics)
print(next(walker))
print(next(walker))
for lesson in basics:
    print(lesson)
```

```bash
python course.py
```

```
Intro
Loops
Intro
Loops
```

### 8. Walkers are lazy

A walker makes an item only when you ask for it. That is called **lazy**: do the work only when it is needed, like a ticket machine that prints one ticket when you press the button, not a thousand in advance. `itertools.count` is that machine. It could go on forever, because there is no list of all the numbers, only a bookmark that moves.

```python
from itertools import count

tickets = count(101)
print(next(tickets))
print(next(tickets))
print(next(tickets))
```

```bash
python tickets.py
```

```
101
102
103
```

`zip`, `enumerate`, `chain` and files are walkers too, so they are lazy and single use:

```pycon
>>> names = ["Lukas", "Priya"]
>>> prices = [499, 299]
>>> pairs = zip(names, prices)
>>> next(pairs)
('Lukas', 499)
>>> list(pairs)
[('Priya', 299)]
>>> list(pairs)
[]
```

`range` is a book, not a walker: `next()` on it fails, but `iter()` of it gives a walker that works:

```pycon
>>> numbers = range(3)
>>> next(numbers)
Traceback (most recent call last):
  File "<python-input-1>", line 1, in <module>
    next(numbers)
    ~~~~^^^^^^^^^
TypeError: 'range' object is not an iterator
>>> walker = iter(numbers)
>>> next(walker)
0
>>> next(walker)
1
```

This is why such tools can handle huge amounts of data: a walker only holds its place, never the whole book. The next lesson writes lazy walkers with almost no code.

### 9. The three pitfalls

Pitfall 1: `next()` on a list. A list is a book, not a walker.

```python
lessons = ["Intro", "Loops", "Functions"]
print(next(lessons))
```

```bash
python p1_nextlist.py
```

```
Traceback (most recent call last):
  File "p1_nextlist.py", line 2, in <module>
    print(next(lessons))
          ~~~~^^^^^^^^^
TypeError: 'list' object is not an iterator
```

Pitfall 2: `len()` of a walker. A walker does not know how many items are left. Ask the book instead.

```python
lessons = ["Intro", "Loops", "Functions"]
walker = iter(lessons)
print(len(walker))
```

```bash
python p2_len.py
```

```
Traceback (most recent call last):
  File "p2_len.py", line 3, in <module>
    print(len(walker))
          ~~~^^^^^^^^
TypeError: object of type 'list_iterator' has no len()
```

Pitfall 3: a `for` loop over a number. A number is not a book.

```python
for number in 5:
    print(number)
```

```bash
python p3_int.py
```

```
Traceback (most recent call last):
  File "p3_int.py", line 1, in <module>
    for number in 5:
                  ^
TypeError: 'int' object is not iterable
```

## Common mistakes

1. Calling `next()` on a list. Call `iter()` first, then `next()` on the walker.

2. Asking a walker for its `len()`. Ask the book (`len(lessons)`). Turning the walker into a list works but uses it up.

3. Looping over a walker twice and expecting the items again. A walker is single use; keep a list or make a new walker.

4. Writing `for i in 5:`. To repeat five times, loop over `range(5)`.

5. Making a class with `__iter__` returning `self` and no `__next__`: Python says `iter() returned non-iterator`.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M09-L02 · Generators](../m09-l02-generators/README.md). A walker class took a dozen lines; one new word, `yield`, writes the same walker for you.

Your turn first: change `Countdown` so it counts up from 1 to a limit, loop over it twice, and check that the second loop works.
