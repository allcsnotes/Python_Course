# M05-L01 · Lists

> Video: Module 5, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Make a list, read items by place (including negative places) and cut slices
- Change a list in place, and why that is different from a string
- Grow a list with `append`, `insert` and `extend`, and shrink it with `remove`, `pop` and `del`
- Ask questions with `in`, `count` and `index`, and walk through a list with `for`
- Sort with `sorted` or `.sort()`, using `reverse` and `key` (even a lambda) for any rule you like
- Lists inside lists, and why `backup = students` is not a copy

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed. No earlier lesson folder is needed, but the lesson builds on M04 (parameters, lambdas) and M03 (loops).

## Files in this folder

| File | What it is |
|------|------------|
| `first_list.py` | A list of three students and its length |
| `index.py` | Positions 0, 2 and -1 |
| `index_err.py` | IndexError on purpose |
| `change.py` | Replace one item |
| `slice.py` | Four slices of a four-name list |
| `member.py` | `in` on a list |
| `loop.py` | Two loops: by item, and by place |
| `add.py` | append, insert and extend, printed after each step |
| `extend.py` | append a list versus extend with a list |
| `remove.py` | remove, pop and del |
| `remove_err.py` | ValueError on purpose |
| `count_index.py` | count and index on Meera's ratings |
| `stats.py` | sum, max, min and the average |
| `sorted_vs.py` | sorted and sort side by side |
| `sort_rev.py` | sort with reverse |
| `sort_none.py` | Storing the answer of sort |
| `sort_key.py` | sorted with reverse and key=len |
| `sort_lambda.py` | sorted and min with a lambda key |
| `sort_mixed.py` | TypeError on purpose |
| `mixed.py` | Text, a number and a boolean in one list |
| `nested.py` | Nested list |
| `alias.py` | backup is the same list |

There is nothing to install: every file is plain Python and runs on its own.

## Follow along

Open a terminal in this folder. Each step shows the code, the command, and the output you should see.

### 1. Your first list

One label, a pair of square brackets, and the names inside separated by commas. We print the list and its length.

`first_list.py`:
```python
students = ["Lukas", "Priya", "Asha"]
print(students)
print(len(students))
```
```bash
python first_list.py
['Lukas', 'Priya', 'Asha']
3
```

A list is a row of items, kept in order, under one label. `len` tells you how many items it holds.

### 2. Pick one item

Places start at zero. Minus one counts from the right, so it is the last item. For a list with n items, the good places are 0 up to n - 1, or -1 down to -n.

`index.py`:
```python
students = ["Lukas", "Priya", "Asha"]
print(students[0])
print(students[2])
print(students[-1])
```
```bash
python index.py
Lukas
Asha
Asha
```

### 3. Going past the end

The list has places 0, 1 and 2 only. Place 3 does not exist.

`index_err.py`:
```python
students = ["Lukas", "Priya", "Asha"]
print(students[3])
```
```bash
python index_err.py
Traceback (most recent call last):
  File "index_err.py", line 2, in <module>
    print(students[3])
          ~~~~~~~~^^^
IndexError: list index out of range
```

Stay inside 0 to length minus one, or use -1 for the last item. An empty list has no place 0 at all.

### 4. Change an item in place

Unlike a string, a list is mutable: you can change it where it stands.

`change.py`:
```python
students = ["Lukas", "Priya", "Asha"]
students[1] = "Meera"
print(students)
```
```bash
python change.py
['Lukas', 'Meera', 'Asha']
```

### 5. Slices

Slices follow the same rules as for text: start, colon, stop, and the stop is left out. A slice always makes a brand new list; the original is not touched.

`slice.py`:
```python
students = ["Lukas", "Priya", "Asha", "Meera"]
print(students[1:3])
print(students[:2])
print(students[-2:])
print(students[::-1])
```
```bash
python slice.py
['Priya', 'Asha']
['Lukas', 'Priya']
['Asha', 'Meera']
['Meera', 'Asha', 'Priya', 'Lukas']
```

### 6. Is it in the list?

`in` asks whether an item is one of the list's items. The opposite question is `not in`.

`member.py`:
```python
students = ["Lukas", "Priya", "Asha"]
print("Asha" in students)
print("Rahul" in students)
```
```bash
python member.py
True
False
```

### 7. Walk through a list

`for` walks through the items one by one. If you also need the place number, loop over `range(len(...))`.

`loop.py`:
```python
students = ["Lukas", "Priya", "Asha"]
for name in students:
    print(f"Welcome, {name}!")

for i in range(len(students)):
    print(i, students[i])
```
```bash
python loop.py
Welcome, Lukas!
Welcome, Priya!
Welcome, Asha!
0 Lukas
1 Priya
2 Asha
```

### 8. Grow a list: append, insert, extend

`append` writes at the end, `insert(place, item)` squeezes an item in at a place, `extend` adds several items at the end. All three change the list itself.

`add.py`:
```python
students = ["Lukas", "Priya"]
students.append("Asha")
print(students)
students.insert(0, "Meera")
print(students)
students.extend(["Rahul", "Sara"])
print(students)
```
```bash
python add.py
['Lukas', 'Priya', 'Asha']
['Meera', 'Lukas', 'Priya', 'Asha']
['Meera', 'Lukas', 'Priya', 'Asha', 'Rahul', 'Sara']
```

### 9. Append against extend

A very common mix-up. `append` adds one thing; `extend` adds many things.

`extend.py`:
```python
students = ["Lukas"]
students.append(["Priya", "Asha"])
print(students)
print(len(students))

students = ["Lukas"]
students.extend(["Priya", "Asha"])
print(students)
print(len(students))
```
```bash
python extend.py
['Lukas', ['Priya', 'Asha']]
2
['Lukas', 'Priya', 'Asha']
3
```

Append put the whole list in as one single item, so the length is 2. Extend added the names one by one, so the length is 3.

### 10. Shrink a list: remove, pop, del

`remove` takes a value. `pop` takes a place and hands the item back (with no number it takes the last item). `del` with a place deletes the line and hands nothing back. If a value appears twice, `remove` crosses out only the first one.

`remove.py`:
```python
students = ["Lukas", "Priya", "Asha", "Meera"]
students.remove("Priya")
print(students)
left = students.pop()
print(left)
del students[0]
print(students)
```
```bash
python remove.py
['Lukas', 'Asha', 'Meera']
Meera
['Asha']
```

### 11. Removing something that is not there

`remove_err.py`:
```python
students = ["Lukas", "Priya", "Asha"]
students.remove("Rahul")
```
```bash
python remove_err.py
Traceback (most recent call last):
  File "remove_err.py", line 2, in <module>
    students.remove("Rahul")
    ~~~~~~~~~~~~~~~^^^^^^^^^
ValueError: list.remove(x): x not in list
```

Ask first with `in`: `if "Rahul" in students:` and then remove. `index` behaves the same way, and `pop` on an empty list gives an IndexError, because there is no last item.

### 12. Count and find

`count` says how many times an item appears. `index` says at which place the first one sits.

`count_index.py`:
```python
ratings = [5, 4, 5, 3, 3]
print(ratings.count(5))
print(ratings.index(4))
print(ratings.index(3))
```
```bash
python count_index.py
2
1
3
```

`index(3)` says 3, the first 3, even though another one is at the end. `index` always finds the first match.

### 13. sum, max, min and the average

Three plain functions for lists of numbers. Dividing the sum by the length gives the average.

`stats.py`:
```python
ratings = [5, 4, 5, 3, 3]
print(sum(ratings))
print(max(ratings))
print(min(ratings))
print(sum(ratings) / len(ratings))
```
```bash
python stats.py
20
5
3
4.0
```

### 14. sorted against sort

`sorted(prices)` builds a new sorted list and leaves `prices` alone. `prices.sort()` sorts the list itself. The smallest comes first by default.

`sorted_vs.py`:
```python
prices = [1999, 499, 1499, 999]
print(sorted(prices))
print(prices)
prices.sort()
print(prices)
```
```bash
python sorted_vs.py
[499, 999, 1499, 1999]
[1999, 499, 1499, 999]
[499, 999, 1499, 1999]
```

### 15. Biggest first

Add `reverse=True`. It works for `sort` and for `sorted`.

`sort_rev.py`:
```python
prices = [1999, 499, 1499, 999]
prices.sort(reverse=True)
print(prices)
```
```bash
python sort_rev.py
[1999, 1499, 999, 499]
```

### 16. The famous mistake: label = list.sort()

It reads so nicely, but look at what `prices` holds afterwards.

`sort_none.py`:
```python
prices = [1999, 499, 1499, 999]
prices = prices.sort()
print(prices)
```
```bash
python sort_none.py
None
```

`sort` changes the list in place and gives back `None`. Methods that change a list in place give back `None`. Call `prices.sort()` on its own line, or use `sorted`.

### 17. Sorting text and the key argument

Text sorts alphabetically. `key=len` orders the titles by their length: `sorted` calls `len` on every title and orders by those answers. A tie keeps the old order, so Python and Docker stay as they were.

`sort_key.py`:
```python
courses = ["Python", "SQL", "Go", "Docker"]
print(sorted(courses))
print(sorted(courses, reverse=True))
print(sorted(courses, key=len))
```
```bash
python sort_key.py
['Docker', 'Go', 'Python', 'SQL']
['SQL', 'Python', 'Go', 'Docker']
['Go', 'SQL', 'Python', 'Docker']
```

### 18. Sort by any rule with a lambda

The live classes start at 9, 14, 18 and 20. Lukas is free from 17. We order the hours by how far each is from 17, and `min` with the same key gives the closest hour.

`sort_lambda.py`:
```python
hours = [9, 14, 18, 20]
print(sorted(hours, key=lambda hour: abs(hour - 17)))
print(min(hours, key=lambda hour: abs(hour - 17)))
```
```bash
python sort_lambda.py
[18, 14, 20, 9]
18
```

Eighteen is 1 away so it comes first. Fourteen and twenty are both 3 away, so they keep their old order. Nine is 8 away, so it is last.

### 19. Sorting things that cannot be compared

`sort_mixed.py`:
```python
print(sorted(["Lukas", 3, "Asha"]))
```
```bash
python sort_mixed.py
Traceback (most recent call last):
  File "sort_mixed.py", line 1, in <module>
    print(sorted(["Lukas", 3, "Asha"]))
          ~~~~~~^^^^^^^^^^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'int' and 'str'
```

Python can only sort things it can compare. Keep one kind of value in a list that you want to sort.

### 20. Lists can hold anything

Each item keeps its own type: `student[1] + 1` is 25.

`mixed.py`:
```python
student = ["Lukas", 24, True]
print(student)
print(student[1] + 1)
```
```bash
python mixed.py
['Lukas', 24, True]
25
```

### 21. A list inside a list

To reach the word Python we need two steps: `student[1]` picks the inner list, then `[0]` picks its first item. Read the brackets from left to right.

`nested.py`:
```python
student = ["Lukas", ["Python", "SQL"]]
print(student[1][0])
print(len(student))
```
```bash
python nested.py
Python
2
```

The outer list has only two items, the name and the list of courses, so the length is 2.

### 22. A second label is not a copy

A peek at lesson 6. `backup = students` looks like a copy, but it is not.

`alias.py`:
```python
students = ["Lukas", "Priya"]
backup = students
students.append("Asha")
print(backup)
```
```bash
python alias.py
['Lukas', 'Priya', 'Asha']
```

Backup has Asha too. The equals sign did not copy the list; it stuck a second label on the very same list. How to make a real copy, and why this happens, is the topic of lesson 6 in this module (M05-L06).

### 23. Your turn

Make a list of five prices, sort it cheapest first, remove the most expensive one with `pop`, and print the average. Write it in a file of your own, for example `my_prices.py`, and check it against what you learned above.

## Common mistakes

- Asking for a place that does not exist gives an `IndexError`. Stay inside 0 to length minus one.
- Removing a value that is not there gives a `ValueError`. Ask with `in` first.
- Writing `label = list.sort()` stores `None`. Call `sort()` on its own line, or use `sorted`.
- Sorting a list that mixes text and numbers gives a `TypeError`.
- `append` adds one thing, `extend` adds many things.
- `backup = students` is a second label on the same list, not a copy.

## Clean up

Nothing to clean up: these scripts create no files.

## Next

[M05-L02 - Tuples and Unpacking](../m05-l02-tuples-and-unpacking/)
