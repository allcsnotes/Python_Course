# M05-L06 · Names, Objects and Mutability

> Video: Module 5, Lesson 6. Watch it first, then follow along here.

## What you'll learn

- What a name really is: a label on an object, and why `=` never copies
- Why two names can share one list (aliasing), and how to check with `id`, `is` and `==`
- Which values can change (mutable) and which cannot (immutable)
- What happens when you give a list to a function
- Shallow and deep copies, and the `[[0] * 3] * 3` grid trap

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Helpful: Lesson 1 (lists), Lesson 2 (tuples) and Lesson 5 (comprehensions). No earlier lesson folder is needed.
- Docker is not used.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening surprise: the backup changes the original |
| `alias.py` | Slow motion: two labels, one list |
| `ids.py` | `id()` of two names on one object |
| `same.py` | `==` against `is` |
| `num.py`, `text.py` | Numbers and text never change in place |
| `strerr.py`, `tup.py` | A string and a tuple refuse item assignment |
| `move.py` | Moving a label with `=` against changing in place |
| `func.py`, `reset.py` | A function changing the caller's list, and a function moving its own label |
| `copies.py` | Three ways to make a (shallow) copy |
| `shallow.py`, `deep.py` | The shallow-copy trap and the deep-copy fix |
| `rowone.py`, `grid.py`, `gridfix.py` | The grid trap and its fix |
| `isword.py` | Pitfall: `is` with a text value |
| `tuplelist.py` | Pitfall: a list inside a tuple |

## Follow along

Run every command from this folder. Outputs are real; the one that depends on your machine (`id`) is marked.

### 1. The surprise

Asha keeps the guest list for an online class on allcsvideos.com. She makes a backup, then adds a name to the backup only.

```python
# hook.py
team = ["Lukas", "Priya"]
backup = team
backup.append("Asha")
print(team)
```

```text
$ python hook.py
['Lukas', 'Priya', 'Asha']
```

Asha is in the original too, and there is no error. The rest of the lesson explains why.

### 2. Two labels, one object

A name is only a label stuck on an object (every value in Python is an object living in memory). The equals sign sticks a label; it never makes a copy. So `backup = team` puts a second label on the same list. Programmers call this aliasing.

```python
# alias.py
team = ["Lukas", "Priya"]
backup = team
print(team)
print(backup)
backup.append("Asha")
print(team)
print(backup)
```

```text
$ python alias.py
['Lukas', 'Priya']
['Lukas', 'Priya']
['Lukas', 'Priya', 'Asha']
['Lukas', 'Priya', 'Asha']
```

Both lists show Asha after the `append`, because there is only one list.

### 3. Check with `id`

`id()` gives an object's serial number while it lives.

```python
# ids.py
team = ["Lukas", "Priya"]
backup = team
print(id(team))
print(id(backup))
```

```text
$ python ids.py
4310079040
4310079040
```

The same number twice means one object with two labels. Your number will look different on your computer; only the match matters.

### 4. `==` against `is`

`==` asks: same contents? `is` asks: the very same object? That is why we write `is None`: there is only one `None`.

```python
# same.py
a = ["Lukas", "Priya"]
b = ["Lukas", "Priya"]
c = a
print(a == b)
print(a is b)
print(a is c)
print(a == c)
```

```text
$ python same.py
True
False
True
True
```

Two photocopies: `==` is `True`, `is` is `False`. One document with two links: both are `True`.

### 5. Why numbers never surprise you

`b + 1` does not change the 5. It makes a new object, 6, and the equals moves the label `b` onto it. Numbers can never change once they exist: they are immutable.

```python
# num.py
a = 5
b = a
b = b + 1
print(a, b)
```

```text
$ python num.py
5 6
```

### 6. Text is immutable too

`+` made a new text. The first text was never touched.

```python
# text.py
name = "Lukas"
other = name
other = other + "!"
print(name, other)
```

```text
$ python text.py
Lukas Lukas!
```

### 7. Immutable objects refuse to change

A string and a tuple both refuse item assignment. That refusal is what immutable means: only the labels can move.

```python
# strerr.py
name = "Lukas"
name[0] = "P"
```

```text
$ python strerr.py
Traceback (most recent call last):
  File "strerr.py", line 2, in <module>
    name[0] = "P"
    ~~~~^^^
TypeError: 'str' object does not support item assignment
```

```python
# tup.py
point = (3, 4)
point[0] = 9
```

```text
$ python tup.py
Traceback (most recent call last):
  File "tup.py", line 2, in <module>
    point[0] = 9
    ~~~~~^^^
TypeError: 'tuple' object does not support item assignment
```

Immutable: whole numbers, decimals, text, `True`/`False`, `None`, tuples. Mutable (can change in place): lists, dictionaries, sets.

### 8. Move the label or change the object

Way one: move a label with `=`. Way two: change the object in place with a method like `append`. `backup + [...]` builds a new list, so `team` is not affected.

```python
# move.py
team = ["Lukas", "Priya"]
backup = team
backup = backup + ["Asha"]
print(team)
print(backup)
print(team is backup)
```

```text
$ python move.py
['Lukas', 'Priya']
['Lukas', 'Priya', 'Asha']
False
```

Rule: moving a label never affects other names. Changing an object in place is seen through every name on it.

### 9. A function call sticks a label too

The parameter `roster` lands on the very object `team` points to. No copy.

```python
# func.py
def add_student(roster):
    roster.append("Asha")

team = ["Lukas", "Priya"]
add_student(team)
print(team)
```

```text
$ python func.py
['Lukas', 'Priya', 'Asha']
```

The function changed the caller's list.

### 10. A function can move its own label

`roster = []` moves only the function's own label.

```python
# reset.py
def clear_roster(roster):
    roster = []

team = ["Lukas", "Priya"]
clear_roster(team)
print(team)
```

```text
$ python reset.py
['Lukas', 'Priya']
```

The caller's list is untouched. Inside a function, `=` is safe; a method like `append` changes the shared object. If a function must not change your list, give it a copy.

### 11. Three ways to copy a list

A copy is a new list object with the same items: `list(team)`, `team.copy()` and the slice `team[:]`.

```python
# copies.py
team = ["Lukas", "Priya"]
a = list(team)
b = team.copy()
c = team[:]
a.append("Asha")
print(team)
print(a)
print(b == c, b is c)
```

```text
$ python copies.py
['Lukas', 'Priya']
['Lukas', 'Priya', 'Asha']
True False
```

Each way made its own new list. Most people write `.copy()` because it reads clearly.

### 12. The shallow-copy trap

A list holds arrows to its items, not the items themselves. `.copy()` makes a new outer list, but the arrows point to the same inner lists.

```python
# shallow.py
batches = [["Lukas", "Priya"], ["Asha"]]
backup = batches.copy()
backup[0].append("Meera")
print(batches)
print(backup)
print(batches is backup)
print(batches[0] is backup[0])
```

```text
$ python shallow.py
[['Lukas', 'Priya', 'Meera'], ['Asha']]
[['Lukas', 'Priya', 'Meera'], ['Asha']]
False
True
```

Meera appears in both. This is a shallow copy: only the top level is copied.

### 13. The fix: a deep copy

`copy.deepcopy` copies the list and every list inside it, all the way down.

```python
# deep.py
import copy

batches = [["Lukas", "Priya"], ["Asha"]]
backup = copy.deepcopy(batches)
backup[0].append("Meera")
print(batches)
print(backup)
print(batches[0] is backup[0])
```

```text
$ python deep.py
[['Lukas', 'Priya'], ['Asha']]
[['Lukas', 'Priya', 'Meera'], ['Asha']]
False
```

For a list of plain values (names, numbers) a shallow copy is enough. For lists or dictionaries inside lists, use a deep copy. It costs more time, so do not use it everywhere.

### 14. The grid trap

`[0] * 3` repeats the items. First one row:

```python
# rowone.py
row = [0] * 3
print(row)
```

```text
$ python rowone.py
[0, 0, 0]
```

### 15. Three rows with `*`

Repeating copies the arrows, not the objects: all three rows are one list.

```python
# grid.py
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
print(grid[0] is grid[1])
```

```text
$ python grid.py
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
True
```

### 16. Fix: build each row separately

A list comprehension (last lesson) makes a new inner list on every round. `_` is the usual name for a value you do not need.

```python
# gridfix.py
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)
print(grid[0] is grid[1])
```

```text
$ python gridfix.py
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
False
```

The `0 * 3` inside is safe, because numbers cannot change.

### 17. Pitfall: `is` to compare values

It prints `same name`, but first Python warns. It may work by luck, because Python sometimes reuses the same text object, and it can fail with other texts. Use `==` for values and keep `is` for `None`.

```python
# isword.py
name = "Lukas"
if name is "Lukas":
    print("same name")
```

```text
$ python isword.py
same name
isword.py:2: SyntaxWarning: "is" with 'str' literal. Did you mean "=="?
  if name is "Lukas":
```

### 18. Pitfall: a tuple that holds a list

A tuple cannot change, but a mutable object inside it can.

```python
# tuplelist.py
row = (1, [2, 3])
row[1].append(4)
print(row)
```

```text
$ python tuplelist.py
(1, [2, 3, 4])
```

The tuple still holds the same two objects; it is the list that changed. Immutable means you cannot swap what a tuple holds.

## Common mistakes

- Thinking `backup = team` makes a copy. It sticks a second label on the same list.
- Using `is` to compare values. Use `==`, and keep `is` for `None`.
- Using `.copy()`, `list()` or `[:]` on a list of lists and expecting a full copy. Use `copy.deepcopy`.
- Building a grid with `[[0] * 3] * 3`. Use a comprehension.
- Expecting a tuple to be completely frozen when it holds a list.

## Clean up

Nothing to clean up.

## Next

[M05-B02 · Build an Expense Tracker](../m05-b02-build-an-expense-tracker/)
