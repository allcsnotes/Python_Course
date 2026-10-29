# M05-L04 · Sets

> Video: Module 5, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- What a set is: a collection that keeps every item once and has no order, so no positions
- How to make sets (`{...}`, `set(a_list)`) and why an empty set is `set()`, not `{}`
- How to add and remove items (`add`, `remove`, `discard`) and ask `in`
- The four set operations: union, intersection, difference and symmetric difference, as symbols and as methods
- Why asking `in` is much faster for a set than for a list, and why set items must be immutable

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No earlier lesson folder is needed, but Lesson 2 (tuples) and Lesson 3 (dictionaries) help.
- Docker is not used.

## Files in this folder

| File | What it is |
|------|------------|
| `dup.py` | The sign-in list: 5 names in a list, 3 in a set |
| `make.py` | A set written with curly brackets |
| `from_list.py` | `set(log)` removes repeats and leaves the list alone |
| `empty.py` | The empty-set trap: `{}` is a dictionary |
| `order.py` | A set has no promised order (run it twice) |
| `loop.py` | Looping over a set |
| `index.py` | Error: a set cannot be indexed |
| `add.py` | `add` |
| `remove.py` | `remove` and `discard` |
| `remove_missing.py` | Error: `remove` on a missing item |
| `member.py` | `in` and `not in` |
| `perf.py` | List against set lookup speed |
| `unhash.py` | Error: a list cannot go inside a set |
| `tuples.py` | The fix: a set of tuples |
| `pit_dict.py` | Pitfall: `add` on an "empty set" that is a dictionary |
| `pit_op.py` | Pitfall: `set | list` |
| `fix_op.py` | The fix: the `union` method accepts a list |

## Follow along

Run every command from this folder.

### 1. Duplicates in a sign-in log

Asha wants to know how many different students joined today's live class on allcsvideos.com.

```python
log = ["Lukas", "Priya", "Lukas", "Asha", "Priya"]
print(len(log))
print(len(set(log)))
```

```bash
python dup.py
```

```
5
3
```

Five names, three different people. A set keeps every item only once.

### 2. Make a set

```bash
python make.py
```

```
{'Lukas', 'Priya'}
2
<class 'set'>
```

`Lukas` was written twice, but Python keeps one copy. That is not an error. (The order of the names in your output may differ.)

### 3. Make a set from a list

```bash
python from_list.py
```

```
{'Asha', 'Priya', 'Lukas'}
['Lukas', 'Priya', 'Lukas', 'Asha', 'Priya']
```

`set(log)` builds a new set; the list is untouched. This is the classic way to remove duplicates. Your set may print in a different order.

### 4. The empty-set trap

```bash
python empty.py
```

```
<class 'dict'>
<class 'set'>
set()
```

`{}` is an empty dictionary. To make an empty set, write `set()`.

### 5. No order

Run `order.py` twice. The same code can print the names in a different order from one run to the next:

```bash
python order.py
python order.py
```

```
{'Lukas', 'Sofia', 'Priya'}
{'Priya', 'Lukas', 'Sofia'}
```

Yours will differ, and that is the point: never depend on the order of a set.

### 6. Loop over a set

```bash
python loop.py
```

```
Sofia
Lukas
Priya
```

Each student comes out exactly once, in an order Python does not promise.

### 7. No positions

```bash
python index.py
```

```
Traceback (most recent call last):
  File "index.py", line 2, in <module>
    print(students[0])
          ~~~~~~~~^^^
TypeError: 'set' object is not subscriptable
```

"Subscript" is the technical word for square brackets after a name. If you need positions, use a list.

### 8. Add and remove

```bash
python add.py
python remove.py
python remove_missing.py
```

```
3
3
```

```
2
2
```

```
Traceback (most recent call last):
  File "remove_missing.py", line 2, in <module>
    students.remove("Arjun")
    ~~~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'Arjun'
```

- Adding `Lukas` a second time changes nothing and gives no error.
- `discard("Arjun")` did nothing and said nothing; `remove("Arjun")` raises `KeyError`.
- Use `remove` when a missing item would be a bug. Use `discard` when you just want the item gone.

### 9. Ask `in`

```bash
python member.py
```

```
True
False
True
```

### 10. Combine two sets in the REPL

The Python class and the SQL class overlap. Start the REPL with `python` and type the lines after `>>>`:

```python
>>> python_class = {"Lukas", "Priya", "Sofia", "Arjun"}
>>> sql_class = {"Priya", "Arjun", "Chen", "Mia"}
>>> python_class | sql_class
{'Mia', 'Sofia', 'Priya', 'Chen', 'Lukas', 'Arjun'}
>>> python_class & sql_class
{'Arjun', 'Priya'}
>>> python_class - sql_class
{'Sofia', 'Lukas'}
>>> sql_class - python_class
{'Chen', 'Mia'}
>>> python_class ^ sql_class
{'Mia', 'Sofia', 'Chen', 'Lukas'}
```

| Operation | Symbol | Meaning |
|-----------|--------|---------|
| Union | `\|` | everything from both |
| Intersection | `&` | only what is in both |
| Difference | `-` | in the first, but not in the second |
| Symmetric difference | `^` | in one, but not in both |

Order matters only for difference: `sql_class - python_class` is the other side. The order of items inside each printed set may differ on your machine.

### 11. The same four, as methods

```python
>>> python_class.union(sql_class)
{'Mia', 'Sofia', 'Priya', 'Chen', 'Lukas', 'Arjun'}
>>> python_class.intersection(sql_class)
{'Arjun', 'Priya'}
>>> python_class.difference(sql_class)
{'Sofia', 'Lukas'}
>>> python_class.symmetric_difference(sql_class)
{'Mia', 'Sofia', 'Chen', 'Lukas'}
```

The methods read like words, and they also accept a list (see the pitfalls).

### 12. Measure the speed

```bash
python perf.py
```

```
True
True
list: 15.3186 ms
set:  0.0027 ms
```

In the video the list needed 6.5399 ms and the set 0.0034 ms. Yours will differ, because every computer is different, but the huge gap will be there too. A list checks items one by one; a set turns the item into a number (its hash) and opens that "locker" directly. The price of a set: more memory, and no order. If you ask "is it in here?" many times, put the items in a set first.

### 13. What can go inside a set

Items must be immutable (never change): numbers, text, `True`/`False`, `None` and tuples are fine. Lists, dictionaries and sets are not.

```bash
python unhash.py
```

```
Traceback (most recent call last):
  File "unhash.py", line 1, in <module>
    groups = {["Lukas", "Priya"], ["Sofia", "Chen"]}
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: cannot use 'list' as a set element (unhashable type: 'list')
```

"Unhashable" means it has no fixed locker number, because it can change. The fix is a tuple:

```bash
python tuples.py
```

```
2
True
```

A set of pairs is handy for remembering which two students are already teamed up.

### 14. Two more mistakes

```bash
python pit_dict.py
python pit_op.py
python fix_op.py
```

```
Traceback (most recent call last):
  File "pit_dict.py", line 2, in <module>
    tags.add("python")
    ^^^^^^^^
AttributeError: 'dict' object has no attribute 'add'
```

```
Traceback (most recent call last):
  File "pit_op.py", line 2, in <module>
    print(asked | ["Sofia"])
          ~~~~~~^~~~~~~~~~~
TypeError: unsupported operand type(s) for |: 'set' and 'list'
```

```
{'Priya', 'Lukas', 'Sofia'}
```

Fix 1: write `tags = set()`. Fix 2: turn the list into a set first, or use the `union` method, which accepts a list.

### Try it yourself

Make two sets of course names: the courses Lukas has bought and the courses Priya has bought. Find the courses they both bought, and the courses only Lukas has bought.

## Common mistakes

- `{}` is an empty dictionary. Use `set()` for an empty set.
- Relying on the order of a set, or indexing it with `[0]`.
- Using `remove` for an item that may be missing (use `discard`).
- Putting a list, dictionary or set inside a set. Use a tuple.
- Mixing a set and a list with an operator (`|`). Use the method, or convert the list.

## Clean up

Nothing to clean up.

## Next

[M05-L05 · Comprehensions](../m05-l05-comprehensions/)
