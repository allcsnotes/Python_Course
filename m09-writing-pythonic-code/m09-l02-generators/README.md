# M09-L02 · Generators

> Video: Module 9, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- The word `yield`, which lets a function pause and carry on later
- How `next()` and a `for` loop drive a generator, and why it is a walker you do not have to write
- Generator expressions: round brackets instead of square brackets
- How to count errors in a 107 MB log with about 0.1 MB of memory
- How to chain generators into a pipeline, and join them with `yield from`
- Three mistakes: `len()`, indexing, and errors that show up late

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed.
- You should have done [M09-L01 · Iterables and Iterators](../m09-l01-iterables-and-iterators/README.md): a generator is a walker.
- The big-log step creates a 107 MB file called `big.log`. You need about 110 MB of free disk; the Clean up section deletes it.

## Files in this folder

| File | What it is |
|------|------------|
| `sizes.py` | List vs round brackets: how many bytes each one takes (the hook) |
| `walk1.py` | A function with `yield`: calling it makes a generator, nothing runs |
| `walk2.py` | Four `next()` calls: follow the pauses |
| `walk3.py` | A `for` loop over the generator |
| `cd_class.py` | The Countdown class from lesson 1 (13 lines) |
| `countdown.py` | The same countdown as a generator (4 lines) |
| `countdown2.py` | A generator is used up after one trip |
| `lesson_numbers.py` | An endless generator that remembers `number` |
| `genexp.py` | List comprehension vs generator expression, `sum` and `max` |
| `usedup.py` | A generator expression is used up too |
| `make_log.py` | Makes a fake server log with N lines: `python make_log.py 2000000 big.log` |
| `eager.py` | Counts ERROR lines the list way and prints the peak memory |
| `lazy.py` | Counts ERROR lines with a generator and prints the peak memory |
| `server.log` | A real-looking server log (about 321 KB) for the pipeline |
| `pipeline.py` | Three generator stations: read, keep errors, cut out the hour |
| `trace.py` | A tiny belt that prints a message at each station |
| `count.py` | The same error count as one line |
| `monday.log` | Two tiny logs for `yield from` |
| `tuesday.log` | Tuesday's log |
| `many0.py` | Reading many files with a loop inside a generator |
| `many.py` | The same with `yield from` |
| `nolen.py` | Mistake 1: `len()` of a generator |
| `noindex.py` | Mistake 2: indexing a generator |
| `late.py` | Mistake 3: the error appears late |

## Follow along

### 1. The hook: a million squares two ways

Asha builds the squares of the numbers up to one million twice: with square brackets (a list comprehension from module 5) and with round brackets. `sys.getsizeof()` answers in bytes. Guess the three lines first.

```python
import sys

squares = [n * n for n in range(1_000_000)]
lazy = (n * n for n in range(1_000_000))

print(sys.getsizeof(squares))
print(sys.getsizeof(lazy))
print(sum(squares) == sum(lazy))
```

```bash
python sizes.py
```

```
8448728
208
True
```

About 8.4 MB (8,448,728 bytes) for the list, only 208 bytes for the round brackets, and `True`: the same sum. The round brackets never build the million squares. They hold a recipe and make a square only when somebody asks. This is a **generator**.

### 2. `yield`: a function that pauses

Think of a baker who bakes one loaf only when a customer asks, and between orders waits with a finger on the recipe card. A generator is a walker (lesson 1) with no list behind it: it makes each item on the spot. One new word does it all: `yield` means "hand over this value and pause right here". The prints are only there so we can watch.

First, just call the function and print the result. Does `start` appear? Guess.

```python
def three_numbers():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")
    yield 3


gen = three_numbers()
print(gen)
```

```bash
python walk1.py
```

```
<generator object three_numbers at 0x102dfac80>
```

No `start`. Calling the function did not run one line of its body. It only made a generator: a walker ready to begin. (The long number is a memory address, so yours will differ.)

Now ask with `next()`, four times:

```python
def three_numbers():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")
    yield 3


gen = three_numbers()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
```

```bash
python walk2.py
```

```
start
1
middle
2
end
3
Traceback (most recent call last):
  File "walk2.py", line 14, in <module>
    print(next(gen))
          ~~~~^^^^^
StopIteration
```

Follow the finger. The first `next()` starts the body: `start` prints, `yield 1` hands over 1 and pauses. The second wakes it on the line after the `yield`. The fourth wakes it once more, nothing is left, the body ends and Python raises `StopIteration`: the same signal as in lesson 1.

A `for` loop does all of this for you and quietly catches `StopIteration`. Look at the order: the function and the loop take turns.

```python
def three_numbers():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")
    yield 3


for number in three_numbers():
    print("got", number)
```

```bash
python walk3.py
```

```
start
got 1
middle
got 2
end
got 3
```

`return` gives back a value and ends the function for good. `yield` gives back a value and only pauses the function, keeping the line it stopped on and all its names. One rule: if `yield` appears anywhere inside a function, calling it never runs it, it gives back a generator.

### 3. Thirteen lines became four

In lesson 1 we wrote a countdown walker as a class:

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
python cd_class.py
```

```
3
2
1
Class starts!
```

With a generator the same job is four lines. Python writes `__init__`, `__iter__`, `__next__` and the `StopIteration` for you:

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1


for number in countdown(3):
    print(number)
print("Class starts!")
```

```bash
python countdown.py
```

```
3
2
1
Class starts!
```

And the walker rules still hold. A generator kept in a name is used up after one trip:

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1


timer = countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)
```

```bash
python countdown2.py
```

```
3
2
1
--- again ---
```

If you need the countdown again, call `countdown(3)` again to get a fresh generator.

### 4. Generators remember, and can be endless

The scope lesson (module 4) said local names remember nothing between calls. A generator is the exception: its names stay alive while it is paused. `while True` with no `break` would freeze a normal function, but here it pauses at every `yield`. Guess the output.

```python
def lesson_numbers():
    number = 1
    while True:
        yield number
        number += 1


gen = lesson_numbers()
print(next(gen), next(gen), next(gen))

for number in lesson_numbers():
    if number > 5:
        break
    print(number)
```

```bash
python lesson_numbers.py
```

```
1 2 3
1
2
3
4
5
```

The number is remembered between asks. The `for` loop stops at 5 and the generator is simply thrown away. A generator can describe an endless stream and you take as many as you need.

### 5. Generator expressions

For a small job, round brackets are a shortcut. The first line below is a list, the second is lazy:

```python
titles = [
    "Python Basics",
    "Loops Deep Dive",
    "Data Structures",
]

lengths = [len(title) for title in titles]
lazy = (len(title) for title in titles)

print(lengths)
print(lazy)
print(list(lazy))
print(sum(len(title) for title in titles))
print(max(len(title) for title in titles))
```

```bash
python genexp.py
```

```
[13, 15, 15]
<generator object <genexpr> at 0x107dac660>
[13, 15, 15]
43
15
```

The lazy one is a `generator object` that has made nothing yet; `list(lazy)` asks for everything. When a generator expression is the only thing inside a call you can drop its own pair of brackets: `sum(len(title) for title in titles)`. No list is built; `sum` keeps only a running total.

Rule of thumb: if you walk through the results once (add up, count, find the biggest), use round brackets. If you need the results more than once, the length, or one item by position, use square brackets. A generator expression is used up too:

```python
squares = (n * n for n in range(5))

print(list(squares))
print(list(squares))
```

```bash
python usedup.py
```

```
[0, 1, 4, 9, 16]
[]
```

### 6. A 107 MB log with 0.1 MB of memory

Asha's real log has two million lines. Make the same fake log (it is made from a fixed random seed, so you get the same numbers). This takes a few seconds and creates a file of about 107 MB:

```bash
python make_log.py 2000000 big.log
```

```
wrote 2000000 lines to big.log
```

```bash
wc -l big.log
```

```
 2000000 big.log
```

First, the way from the files lesson: `readlines()` gives a list of every line. `tracemalloc` (trace memory allocation) watches every piece of memory Python takes, and `get_traced_memory()[1]` is the peak. Will the peak be less than the file, about the same, or more?

```python
import tracemalloc

tracemalloc.start()

with open("big.log", encoding="utf-8") as f:
    lines = f.readlines()

errors = 0
for line in lines:
    if " ERROR " in line:
        errors += 1

peak = tracemalloc.get_traced_memory()[1]
megabytes = round(peak / 1_000_000, 1)
print(errors, "errors")
print(megabytes, "MB at the peak")
```

```bash
python eager.py
```

```
68197 errors
206.6 MB at the peak
```

About 206 MB, twice the size of the file: every line becomes a Python string with extra bookkeeping and the list keeps all of them at once. (The error count is always the same; the megabytes can differ a little on your machine.)

Now the generator way. `read_lines` opens the file and yields one line at a time:

```python
import tracemalloc


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line


tracemalloc.start()

errors = 0
for line in read_lines("big.log"):
    if " ERROR " in line:
        errors += 1

peak = tracemalloc.get_traced_memory()[1]
megabytes = round(peak / 1_000_000, 1)
print(errors, "errors")
print(megabytes, "MB at the peak")
```

```bash
python lazy.py
```

```
68197 errors
0.1 MB at the peak
```

Same error count, and a peak of about 0.1 MB. It was run on three logs of different size in the video:

| Lines in the log | List peak | Generator peak |
|---|---|---|
| 100,000 | 10.4 MB | 0.1 MB |
| 1,000,000 | 103.2 MB | 0.1 MB |
| 2,000,000 | 206.6 MB | 0.1 MB |

The list grows with the file; the generator stays flat. Each line is born, used and forgotten before the next one is read, like the baker with one loaf on the counter. A ten gigabyte log would need roughly 20 GB as a list, but only about 100 KB with a generator. Only the time grows, not the memory.

### 7. A pipeline of generators

Real jobs have steps: read the lines, keep only the errors, cut out the hour. Think of a conveyor belt with stations; a generator makes a perfect station. `server.log` is a smaller log (about 321 KB) that goes with this lesson.

```python
from collections import Counter


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def only_errors(lines):
    for line in lines:
        if " ERROR " in line:
            yield line


def hour_of(lines):
    for line in lines:
        yield line[11:13]


lines = read_lines("server.log")
errors = only_errors(lines)
hours = hour_of(errors)

print(Counter(hours).most_common(3))
```

```bash
python pipeline.py
```

```
[('14', 96), ('18', 13), ('15', 10)]
```

Hour 14 with 96 errors, then 18 and 15: the same afternoon spike the log analyser found, and no list of lines was ever built. The three lines that set up `lines`, `errors` and `hours` read nothing yet; `Counter` pulls the items through.

How does one item travel? A tiny belt that prints a message at each station. Guess the order of the messages first:

```python
def numbers():
    for n in [1, 2, 3]:
        print("  numbers makes", n)
        yield n


def doubled(items):
    for n in items:
        print("  doubled gets", n)
        yield n * 2


for x in doubled(numbers()):
    print("main got", x)
```

```bash
python trace.py
```

```
  numbers makes 1
  doubled gets 1
main got 2
  numbers makes 2
  doubled gets 2
main got 4
  numbers makes 3
  doubled gets 3
main got 6
```

One item travels the whole belt before the next one starts. The last station pulls: it asks the station before it, which asks the one before that. Nothing is made until it is needed, so on a 10 GB file only one line is alive on the whole belt.

For small jobs you do not even need stations. The same error count in one line, a generator expression fed by a generator function:

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


errors = sum(
    1
    for line in read_lines("server.log")
    if " ERROR " in line
)
print(errors)
```

```bash
python count.py
```

```
204
```

204 errors, matching the log analyser exactly.

### 8. `yield from`: join generators

One log file per day, and we want all lines as one stream. The long way has an inner loop that only passes things along:

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def read_many(paths):
    for path in paths:
        for line in read_lines(path):
            yield line


paths = ["monday.log", "tuesday.log"]
for line in read_many(paths):
    print(line)
```

```bash
python many0.py
```

```
2026-03-12 09:01:10 INFO GET /courses 200 41ms
2026-03-12 09:04:52 ERROR Payment failed for order 312
2026-03-13 10:15:03 INFO Student 447 enrolled in course 7
2026-03-13 10:16:40 WARNING Video 204 is buffering
```

Python has a shorthand: `yield from` means "yield every item this other generator gives, one by one". Three lines became two:

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def read_many(paths):
    for path in paths:
        yield from read_lines(path)


paths = ["monday.log", "tuesday.log"]
for line in read_many(paths):
    print(line)
```

```bash
python many.py
```

```
2026-03-12 09:01:10 INFO GET /courses 200 41ms
2026-03-12 09:04:52 ERROR Payment failed for order 312
2026-03-13 10:15:03 INFO Student 447 enrolled in course 7
2026-03-13 10:16:40 WARNING Video 204 is buffering
```

Monday's two lines and Tuesday's two lines come out as one stream.

### 9. The three mistakes

Mistake 1: asking a generator for its length. It has not made the items yet, so it cannot know. If you need a length, use a list.

```python
squares = (n * n for n in range(5))

print(len(squares))
```

```bash
python nolen.py
```

```
Traceback (most recent call last):
  File "nolen.py", line 3, in <module>
    print(len(squares))
          ~~~^^^^^^^^^
TypeError: object of type 'generator' has no len()
```

Mistake 2: picking one item by position. A generator only goes forward.

```python
squares = (n * n for n in range(5))

print(squares[0])
```

```bash
python noindex.py
```

```
Traceback (most recent call last):
  File "noindex.py", line 3, in <module>
    print(squares[0])
          ~~~~~~~^^^
TypeError: 'generator' object is not subscriptable
```

Mistake 3 is hidden: errors show up late. We call a generator function with a file that does not exist, print "made it", and only then ask for the first line.

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


lines = read_lines("missing.log")
print("made it")
print(next(lines))
```

```bash
python late.py
```

```
made it
Traceback (most recent call last):
  File "late.py", line 9, in <module>
    print(next(lines))
          ~~~~^^^^^^^
  File "late.py", line 2, in read_lines
    with open(path, encoding="utf-8") as f:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'missing.log'
```

`made it` prints first. The `FileNotFoundError` comes only at `next()`, from inside the generator, because the body does not run until the first ask. Read the traceback: the lower lines point inside the function.

## Common mistakes

1. Calling `len()` on a generator, or indexing it with `[0]`. Use a list if you need a length or a position.

2. Looping over a generator twice and expecting the items again. It is used up after one trip: call the function again for a fresh one.

3. Expecting an error from a generator function at the line that calls it. Nothing runs until the first `next()`.

4. Calling `list()` on a generator that never ends. It would fill the memory and never stop.

5. Using a generator when you need to loop many times, know the length or pick by position. Use a list then.

## Clean up

The big log is about 107 MB. Delete it when you are done:

```bash
rm big.log
```

## Next

Next lesson: [M09-L03 · Closures and Decorators](../m09-l03-closures-and-decorators/README.md). You will see how a function can remember, and how to wrap one function inside another.

Your turn first: write a generator `even_numbers(limit)`, turn it into a generator expression, build a pipeline over `server.log` that keeps only the `WARNING` lines, and loop over a generator twice to watch what happens.
