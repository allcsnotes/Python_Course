# M23-L01 · The Python Gotchas

> Video: Module 23, Lesson 1. Watch it first, then follow along here.

## What you'll learn
- Ten classic Python traps (gotchas) that interviewers love, and where in the course you met each one
- How to predict the output of a short snippet out loud, before anyone runs it
- The one sentence you can say in an interview for each trap
- Model answers to eighteen of the most-asked Python questions (nine full answers, nine quick-fire cards)

## Before you start
- Python 3.14 or newer. Check with `python --version` (use `python3 --version` if `python` is not found).
- No packages and no Docker. Every file uses only the standard library.
- Earlier lessons help but are not required. Each gotcha below names the lesson where it first appeared.
- Rahul is the interviewer in this lesson. Asha, Lukas, Priya and Meera are the names used in the code.

## Files in this folder
| File | What it is |
|---|---|
| `g00_hook.py` | The opening puzzle: `+=` on a list inside a tuple |
| `g01_default.py` | Gotcha 1: the mutable default argument |
| `g02_late.py` | Gotcha 2: late binding in closures |
| `g03_is.py` | Gotcha 3: `is` versus `==` |
| `g04_copy.py` | Gotcha 4: shallow copy, `deepcopy` and the grid trap |
| `g05_loop.py` | Gotcha 5: changing a list while you loop over it |
| `g06_tuple.py` | Gotcha 6: the hook in slow motion |
| `g07_numbers.py` | Gotcha 7: floor division, modulo, `round`, floats |
| `g08_attrs.py` | Gotcha 8: class attributes versus instance attributes |
| `g09_slots.py` | Gotcha 9: `__slots__` |
| `g10_gil.py` | Gotcha 10: the GIL (timings depend on your machine) |
| `pyproject.toml` | Tiny project file (`requires-python = ">=3.14"`, no dependencies). The video ran the files with `uv run`; plain `python` works the same |

## Follow along
For every gotcha: read the code, guess the output, pause, then run it. The rule is the same each time. Predict, run,
explain.

### 1. The hook
```bash
python g00_hook.py
```
```
error: 'tuple' object does not support item assignment
(1, [2, 3, 4])
```
Both happened. Python complained, and the list still changed. Gotcha 6 explains why.

### 2. Gotcha 1: the mutable default (M04-L02, M08-L02, M08-L06)
```bash
python g01_default.py
```
```
['Lukas']
['Lukas', 'Priya']
['Lukas']
['Priya']
```
The empty list in `def add(name, students=[])` is made once, when Python reads the `def` line. Every call that passes no
list shares it. The fixed version uses `None` and makes a new list inside the function on every call. Data classes refuse
this trap and ask for `default_factory` (M08-L06).

Say: "A default value is made once, when the function is defined. A changeable default is shared by every call. Use
`None` and make the object inside."

### 3. Gotcha 2: late binding in closures (M09-L03)
```bash
python g02_late.py
```
```
['Hello, Meera', 'Hello, Meera', 'Hello, Meera']
['Hello, Lukas', 'Hello, Priya', 'Hello, Meera']
```
A closure carries the name, not the value the name had. Python looks the name up when the function runs, and by then the
loop has ended with `Meera`. In the fix, `lambda name=name:` fills the default at the moment the function is made, so each
function keeps its own value. `functools.partial` (M09-L05) does the same job.

Say: "A closure remembers the variable, not its value at that moment. Fix it by giving each function its own value with a
default argument."

### 4. Gotcha 3: `is` versus `==` (M05-L06, M11-L01)
```bash
python g03_is.py
```
```
True True
True False
True False
```
`==` asks "same contents?". `is` asks "the very same object?". Python keeps ready-made objects for whole numbers from -5
to 256, so `100` is shared and `1000` is not. That is a detail of how Python is built: never depend on it.

Say: "`==` compares values, `is` compares identity. I use `is` only with `None`."

### 5. Gotcha 4: shallow versus deep copy (M05-L06)
```bash
python g04_copy.py
```
```
['Lukas', 'Priya', 'Meera']
['Lukas', 'Priya']
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```
A shallow copy (`.copy()`, `list(x)`, a slice) copies only the outer list, so both lists hold references to the same inner
lists. `copy.deepcopy` copies everything inside. `[[0] * 3] * 3` repeats one row three times: three names for one row.
Build each row separately: `[[0] * 3 for _ in range(3)]`.

Say: "`.copy()`, `list()` and a slice make shallow copies that share the inner objects. Deep copy copies everything and
costs more time. I decide which one I need first."

### 6. Gotcha 5: changing a list while looping (M05-L03, M05-L05)
```bash
python g05_loop.py
```
```
['intro', 'demo 2', 'wrap-up']
['intro', 'wrap-up']
```
`demo 2` survives. The loop walks by position (0, 1, 2...). At position 1 it removes `demo 1`, the list closes up, and
`demo 2` now sits at position 1. The loop moves on to position 2 and never looks at it. A dictionary raises an error for
this (M05-L03); a list stays silent.

Say: "I never change the list I am looping over. I build a new list with a comprehension, or loop over a copy."

### 7. Gotcha 6: `+=` inside a tuple (M05-L06)
```bash
python g06_tuple.py
```
```
(1, [2, 3, 4])
Traceback (most recent call last):
  File "g06_tuple.py", line 5, in <module>
    row[1] = inner
    ~~~^^^
TypeError: 'tuple' object does not support item assignment
```
(The path in the traceback line is your own folder. The error is meant to happen: it is the last line of the file.)

`inner += [4]` changes the list in place, and that works because a list can change. Assigning back into the tuple fails,
because a tuple cannot be assigned to. `row[1] += [4]` does both steps in one line, so both things happen. To avoid the
error, call `row[1].extend([4])`.

Say: "Immutable means the tuple cannot swap what it holds. A list inside can still change. And `+=` does two things: it
changes in place, then assigns back."

### 8. Gotcha 7: numbers (M02-L02)
```bash
python g07_numbers.py
```
```
-4
2
0 2 2
False
True
```
- `-7 // 2` is `-4`: floor division rounds down, to the lower whole number.
- `-7 % 3` is `2`: the result takes the sign of the number on the right.
- `round(0.5)`, `round(1.5)`, `round(2.5)` give `0 2 2`: on an exact half, `round` goes to the even neighbour (banker's rounding).
- `0.1 + 0.2 == 0.3` is `False`: floats are stored in binary and `0.1` has no exact form. Compare with `math.isclose`.
- Keep money in whole paise, or use the `decimal` module.

Say: "Floor division rounds down, `round` picks the even number on a tie, and I never compare floats with `==`."

### 9. Gotcha 8: class versus instance attributes (M08-L02)
```bash
python g08_attrs.py
```
```
['Lukas']
1 0
```
A class attribute lives on the class and every object reads it. `.append` changes the one shared list, so `sql` sees
`Lukas`. But `c.total += 1` reads the class value, adds one, and assigns the answer to the object. That creates a new
instance attribute and leaves `Counter.total` at 0. A list is changed in place, a number is replaced.

Say: "A class attribute is shared by all objects, an instance attribute belongs to one. Changing data goes in
`__init__`. Assigning through an object never changes the class."

### 10. Gotcha 9: `__slots__` (M10-L03)
```bash
python g09_slots.py
```
```
{'price': 100, 'pirce': 90}
Traceback (most recent call last):
  File "g09_slots.py", line 17, in <module>
    b.pirce = 90
    ^^^^^^^
AttributeError: 'Slim' object has no attribute 'pirce' and no __dict__ for setting new attributes. Did you mean: 'price'?
```
The plain object accepted the typo `pirce`. The slotted object raised an error and even suggested `price`. An ordinary
object keeps its attributes in a hidden dictionary, so any new name goes in. `__slots__` gives the class exactly the
places it names. It also saves memory (measured in M10-L03).

Say: "Slots removes the dictionary from every object: less memory, no surprise attributes. The price is flexibility."

### 11. Gotcha 10: the GIL (M11-L03, M12-L02)
```bash
python g10_gil.py
```
The video's run printed:
```
GIL on: True
1 worker:  1.36 s
4 workers: 1.49 s
```
Your seconds will differ, because they depend on your CPU and on what else is running. The line to look at is the shape:
on a quiet machine with the normal build of Python, four workers are not faster than one. (If your machine is busy, the
numbers get noisy; close other programs and run it again.)

In the normal build of Python only one thread runs Python code at a time; the GIL (global interpreter lock) is the lock
that decides which. So threads do not speed up computing. They help when the work is waiting (network, disk), because a
waiting thread lets go of the lock. For computing, use processes (M12-L03). Python 3.14 also offers a free-threaded build
without the lock (measured in M11-L03).

Say: "The GIL lets one thread run Python code at a time. Threads help with waiting, processes help with computing, and
async handles many waits cheaply."

### 12. Your turn
Predict first, then run:
```bash
python -c "a=[1,2,3]; b=a; b+=[4]; print(a)"
```
```
[1, 2, 3, 4]
```
`b = a` makes a second name for the same list, and `+=` changes a list in place, so `a` changed too. Then write a closure
trap of your own and fix it two ways (a default argument, and `functools.partial`). Say each answer out loud, in two
sentences.

## The eighteen questions
Nine with spoken model answers, then nine quick-fire cards. The full list of forty is in the
[final practice sheet](../../practice/m23-interviews-and-capstone/) at the end of this module.

1. **List versus tuple?** A list can change, a tuple cannot. A tuple can be a dictionary key if everything inside it is hashable. Use a tuple for a small fixed record, a list for a collection that grows.
2. **What is a decorator?** A function that takes a function and returns a new one, usually a wrapper that adds behavior before or after the call. `@name` above a `def` is shorthand for `f = name(f)`. Put `functools.wraps` on the wrapper to keep the original name.
3. **What is a generator, and why use one?** A function with `yield`. It makes one value at a time, when you ask, so it uses almost no memory, even for a huge or endless stream. The price: you can walk through it only once.
4. **Threads, processes or async?** Ask what the program waits for. Network or disk: threads or async. Computing, with the normal GIL: processes. Measure before choosing.
5. **How does Python free memory?** Reference counting: an object is freed the moment its last reference goes. A cycle collector catches objects that only point at each other. A leak is something that still points at an object, like a cache that only grows.
6. **What are `*args` and `**kwargs`?** In a definition, `*args` collects extra positional values into a tuple and `**kwargs` collects extra named values into a dictionary. In a call, the stars do the opposite: they unpack.
7. **What does `with` do?** It runs setup when the block starts and cleanup when it ends, even if an error happens. Files, locks and database sessions use it, and you can write your own with `__enter__` and `__exit__`.
8. **Why must dictionary keys be hashable?** A dictionary finds a key through its hash, a number made from the value. If the value could change, the number would change and Python would look in the wrong place. Lists cannot be keys; tuples of numbers and text can.
9. **Instance, class and static methods?** An instance method gets `self`, one object. A class method gets `cls`, the class, and is often a second way to build an object. A static method gets neither: a plain function that lives in the class.

Quick fire:

10. **What does `if __name__ == "__main__"` do?** Runs code only when the file is started directly, not when it is imported.
11. **Compiled or interpreted?** Both. Python compiles to bytecode, and a virtual machine runs the bytecode.
12. **`try`, `except`, `else`, `finally`?** `except` handles the error, `else` runs when there was none, `finally` always runs.
13. **Why a virtual environment?** Each project gets its own packages and versions, so projects never fight.
14. **Does Python check type hints?** No. A checker like pyright does, before the program runs. Pydantic and FastAPI use them while it runs.
15. **Data class or normal class?** A data class writes `__init__`, `__repr__` and `__eq__` for you, so it suits a class that mostly holds data.
16. **Fixture or mock?** A fixture prepares what a test needs. A mock replaces something the test must not really call.
17. **What is a race condition?** The result depends on thread timing, for example two threads reading, changing and writing the same number. Avoid sharing, or use a lock or a queue.
18. **How do you store passwords?** As a slow, salted hash. Never plain text, never a fast hash.

## Common mistakes
1. Answering from a guess instead of tracking which names point at which objects, and which objects can change.
2. Using `is` to compare values, or relying on small numbers being shared. Use `is` only with `None`.
3. Using `[[0] * 3] * 3` for a grid. Build each row separately.
4. Removing items from a list inside a `for` loop over that same list.
5. Comparing floats with `==` instead of `math.isclose`, or storing money as floats.
6. Expecting threads to speed up pure computing under the GIL.
7. Giving only the output. A good answer is: predict out loud, give the rule, name the fix. If you are not sure, say which small test you would run.

## Clean up
Nothing to clean up. The files only print to the screen. (If Python made a `__pycache__` folder next to the files, you
can delete it.)

## Next
[M23-L02 · The Coding Round Toolkit](../m23-l02-the-coding-round-toolkit/)
