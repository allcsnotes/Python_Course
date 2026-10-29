# M05-L03 · Dictionaries

> Video: Module 5, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What a dictionary is: keys, values and pairs
- Read with `[]` or `get`, check with `in`, add and change by assigning, remove with `del` or `pop`
- Loop over keys, values and items
- Count things with a dictionary
- Put dictionaries and lists inside dictionaries
- Which keys are allowed, and the mistakes to avoid

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed. Best after M05-L02 (tuples and unpacking) in the folder `../m05-l02-tuples-and-unpacking/`.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The two-line first dictionary |
| `create.py` | Create, print, type, len, empty |
| `read.py` | Three reads |
| `keyerror.py` | KeyError on purpose |
| `keycase.py` | Keys match exactly: sql is not SQL |
| `get.py` | get with and without a default |
| `incheck.py` | Four checks with in and not in |
| `addupd.py` | Add Java, change SQL |
| `delete.py` | del and pop |
| `del_missing.py` | KeyError when deleting a missing key |
| `loop_keys.py` | for over the dictionary |
| `loop_values.py` | for over prices.values() |
| `loop_items.py` | A full loop with a running total |
| `count_if.py` | Count with if and else |
| `count_bad.py` | KeyError on the first Python |
| `count_get.py` | Four lines become one |
| `count_words.py` | Count words in a sentence |
| `catalog.py` | A catalog: each value is a small dictionary |
| `catalog_loop.py` | Loop over the catalog with items() |
| `lessons.py` | Each course has a list of lesson titles |
| `key_list.py` | TypeError: a list as a key |
| `key_ok.py` | Tuples and numbers as keys |
| `get_none.py` | TypeError on purpose |
| `dup.py` | Python does not complain |
| `loop_del.py` | RuntimeError on purpose |
| `loop_fix.py` | Two loops: collect, then delete |
| `loop_val.py` | Changing the value of an existing key during a loop is fine |
| `tryit.py` | A possible answer to Your turn |

There is nothing to install: every file is plain Python and runs on its own.

## Follow along

Open a terminal in this folder. Each step shows the code, the command, and the output you should see.

### 1. Look up a price by name

Asha wants to ask for SQL and get its price back. Curly brackets hold pairs: a course name, a colon, and its price.

`hook.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["SQL"])
```
```bash
python hook.py
999
```

Python looked up `"SQL"` by its name and found the price. This is a dictionary. The thing you look up is the key; the thing you get back is the value. Keys are unique, you find things by key (never by place), and values can be anything.

### 2. Create a dictionary

Pairs are separated by commas, each pair is a key, a colon, then its value. `len` counts pairs. Empty curly brackets are an empty dictionary.

`create.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices)
print(type(prices))
print(len(prices))
print({})
```
```bash
python create.py
{'Python': 1499, 'SQL': 999, 'Docker': 799}
<class 'dict'>
3
{}
```

### 3. Read a value

Square brackets with the key inside. The value you get back is a normal number, so you can do maths with it.

`read.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["SQL"])
print(prices["Python"])
print(prices["Docker"] + 1)
```
```bash
python read.py
999
1499
800
```

### 4. A key that is not there

Java is not in our price list.

`keyerror.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["Java"])
```
```bash
python keyerror.py
Traceback (most recent call last):
  File "keyerror.py", line 2, in <module>
    print(prices["Java"])
          ~~~~~~^^^^^^^^
KeyError: 'Java'
```

`keycase.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices["sql"])
```
```bash
python keycase.py
Traceback (most recent call last):
  File "keycase.py", line 2, in <module>
    print(prices["sql"])
          ~~~~~~^^^^^^^
KeyError: 'sql'
```

A KeyError means: there is no such key in this dictionary. Nothing is broken in Python; we asked for something that is not in it.

### 5. get: ask without falling over

`get` returns the value when the key exists, and `None` when it does not. A second value is a default that is returned instead of `None`.

`get.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print(prices.get("SQL"))
print(prices.get("Java"))
print(prices.get("Java", 0))
```
```bash
python get.py
999
None
0
```

### 6. in looks at keys only

`key in prices` asks: is this key in the book? `not in` asks the opposite. The last check asks whether 999 is in `prices`.

`incheck.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
print("SQL" in prices)
print("Java" in prices)
print("Java" not in prices)
print(999 in prices)
```
```bash
python incheck.py
True
False
True
False
```

The last one is `False`: `in` looks at the keys only, never at the values. Use square brackets when the key must be there (a missing key would be a bug), `get` when a missing key is normal, and `in` when you want to make a decision.

### 7. Add and change: assign to a key

A new key adds a pair. An existing key has its value replaced, because keys are unique.

`addupd.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
prices["Java"] = 1299
print(prices)
prices["SQL"] = 899
print(prices)
print(len(prices))
```
```bash
python addupd.py
{'Python': 1499, 'SQL': 999, 'Docker': 799, 'Java': 1299}
{'Python': 1499, 'SQL': 899, 'Docker': 799, 'Java': 1299}
4
```

After the second assignment the length is still 4: we replaced a value, we did not add a pair.

### 8. Delete: del and pop

`del` removes a pair. `pop(key)` removes it and hands the value back.

`delete.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
del prices["Docker"]
print(prices)
old = prices.pop("SQL")
print(old)
print(prices)
```
```bash
python delete.py
{'Python': 1499, 'SQL': 999}
999
{'Python': 1499}
```

`del_missing.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
del prices["Java"]
```
```bash
python del_missing.py
Traceback (most recent call last):
  File "del_missing.py", line 2, in <module>
    del prices["Java"]
        ~~~~~~^^^^^^^^
KeyError: 'Java'
```

Deleting a key that is not there is a KeyError too, just like reading it.

### 9. Loop over keys

A loop over a dictionary hands over the keys, in the order you added them.

`loop_keys.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
for course in prices:
    print(course)
```
```bash
python loop_keys.py
Python
SQL
Docker
```

### 10. Loop over values

`values()` hands over only the values; the names are gone.

`loop_values.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
for price in prices.values():
    print(price)
```
```bash
python loop_values.py
1499
999
799
```

### 11. Loop over items

`items()` hands over each pair, and we unpack it into two names in the for line, the same unpacking as in the last lesson.

`loop_items.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
total = 0
for course, price in prices.items():
    print(f"{course} costs Rs {price}")
    total += price
print(total)
```
```bash
python loop_items.py
Python costs Rs 1499
SQL costs Rs 999
Docker costs Rs 799
3297
```

Start at zero, add one price per round: the same pattern as in the loops lesson.

### 12. Counting with a dictionary

Meera wants to know how many students enrolled in each course. Think of tally marks on a board: if the course has no row yet, write it with one stroke, otherwise add one more.

`count_if.py`:
```python
orders = ["Python", "SQL", "Python", "Docker", "Python", "SQL"]
counts = {}
for course in orders:
    if course in counts:
        counts[course] += 1
    else:
        counts[course] = 1
print(counts)
```
```bash
python count_if.py
{'Python': 3, 'SQL': 2, 'Docker': 1}
```

### 13. Why the check is needed

What if we simply write `counts[course] += 1`?

`count_bad.py`:
```python
orders = ["Python", "SQL", "Python"]
counts = {}
for course in orders:
    counts[course] += 1
print(counts)
```
```bash
python count_bad.py
Traceback (most recent call last):
  File "count_bad.py", line 4, in <module>
    counts[course] += 1
    ~~~~~~^^^^^^^^
KeyError: 'Python'
```

The first time, the key does not exist, so Python cannot add one to it.

### 14. The shorter way with get

`counts.get(course, 0)` gives the current count, or 0 if the course is new. Add one and store it back.

`count_get.py`:
```python
orders = ["Python", "SQL", "Python", "Docker", "Python", "SQL"]
counts = {}
for course in orders:
    counts[course] = counts.get(course, 0) + 1
print(counts)
```
```bash
python count_get.py
{'Python': 3, 'SQL': 2, 'Docker': 1}
```

`count_words.py`:
```python
text = "the cat saw the dog and the bird"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(counts)
```
```bash
python count_words.py
{'the': 3, 'cat': 1, 'saw': 1, 'dog': 1, 'and': 1, 'bird': 1}
```

The recipe: start with an empty dictionary, and for each item add one to its count using `get` with a default of 0. Python's standard library has a ready-made counter for this, which comes in a later module.

### 15. Dictionaries inside dictionaries

Think of a filing cabinet: one folder per course, and inside it a sheet with the details. Each pair of square brackets opens one level. Read from left to right.

`catalog.py`:
```python
catalog = {
    "Python": {"price": 1499, "level": "beginner"},
    "SQL": {"price": 999, "level": "intermediate"},
    "Docker": {"price": 799, "level": "beginner"},
}
print(catalog["SQL"])
print(catalog["SQL"]["price"])
catalog["SQL"]["price"] = 899
print(catalog["SQL"]["price"])
```
```bash
python catalog.py
{'price': 999, 'level': 'intermediate'}
999
899
```

`catalog_loop.py`:
```python
catalog = {
    "Python": {"price": 1499, "level": "beginner"},
    "SQL": {"price": 999, "level": "intermediate"},
    "Docker": {"price": 799, "level": "beginner"},
}
for name, info in catalog.items():
    print(name, info["level"], info["price"])
```
```bash
python catalog_loop.py
Python beginner 1499
SQL intermediate 999
Docker beginner 799
```

### 16. Lists inside dictionaries

Square brackets with a key for a dictionary, square brackets with a number for a list.

`lessons.py`:
```python
lessons = {
    "Python": ["Variables", "Loops", "Functions"],
    "SQL": ["Select", "Join"],
}
print(lessons["Python"][0])
lessons["SQL"].append("Group by")
print(lessons["SQL"])
print(len(lessons["Python"]))
```
```bash
python lessons.py
Variables
['Select', 'Join', 'Group by']
3
```

### 17. Which keys are allowed?

Keys must be immutable: text, numbers and tuples are fine. A list is not, because if a key could change after it was filed, the pair would be lost.

`key_list.py`:
```python
bad = {["a", "b"]: 1}
```
```bash
python key_list.py
Traceback (most recent call last):
  File "key_list.py", line 1, in <module>
    bad = {["a", "b"]: 1}
          ^^^^^^^^^^^^^^^
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```

`key_ok.py`:
```python
seats = {("A", 1): "Lukas", ("A", 2): "Priya"}
print(seats[("A", 2)])
codes = {101: "Python", 102: "SQL"}
print(codes[102])
```
```bash
python key_ok.py
Priya
SQL
```

"Unhashable" is Python's word for: this can change, so it cannot be a key.

### 18. Mistake 1: get gives None

`None` cannot be added to a number.

`get_none.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
new = prices.get("Java") + 100
```
```bash
python get_none.py
Traceback (most recent call last):
  File "get_none.py", line 2, in <module>
    new = prices.get("Java") + 100
          ~~~~~~~~~~~~~~~~~~~^~~~~
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

Give `get` a default like 0, check with `in` first, or, if a missing price is a bug, use square brackets and let the error show.

### 19. Mistake 2: the same key twice

`dup.py`:
```python
prices = {"SQL": 999, "SQL": 899}
print(prices)
```
```bash
python dup.py
{'SQL': 899}
```

The dictionary keeps the last one. If a dictionary has fewer pairs than you typed, look for a repeated key.

### 20. Mistake 3: changing the dictionary while looping

Loop over `prices` and delete every course under 1000.

`loop_del.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
for course in prices:
    if prices[course] < 1000:
        del prices[course]
```
```bash
python loop_del.py
Traceback (most recent call last):
  File "loop_del.py", line 2, in <module>
    for course in prices:
                  ^^^^^^
RuntimeError: dictionary changed size during iteration
```

It is like tearing pages out of a book while you read it.

### 21. The fix: collect first, delete after

Collect the names to remove in a list, and delete them in a second loop.

`loop_fix.py`:
```python
prices = {"Python": 1499, "SQL": 999, "Docker": 799}
cheap = []
for course in prices:
    if prices[course] < 1000:
        cheap.append(course)
for course in cheap:
    del prices[course]
print(prices)
```
```bash
python loop_fix.py
{'Python': 1499}
```

`loop_val.py`:
```python
prices = {"Python": 1499, "SQL": 999}
for course in prices:
    prices[course] = prices[course] + 1
print(prices)
```
```bash
python loop_val.py
{'Python': 1500, 'SQL': 1000}
```

Changing the value of an existing key during a loop is fine. It is adding or removing keys that breaks the loop.

### 22. Your turn

Count the words in `to be or not to be`, print the whole dictionary, print how many times `be` appears, then loop over items and print each word with its count. Here is one answer:

`tryit.py`:
```python
text = "to be or not to be"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(counts)
print(counts["be"])
for word, count in counts.items():
    print(word, count)
```
```bash
python tryit.py
{'to': 2, 'be': 2, 'or': 1, 'not': 1}
2
to 2
be 2
or 1
not 1
```

## Common mistakes

- `prices["Java"]` on a missing key is a `KeyError`; keys match exactly, so `"sql"` is not `"SQL"`.
- `get` returns `None` for a missing key, and `None + 100` is a `TypeError`. Give `get` a default.
- `in` looks at the keys only, never at the values.
- Writing the same key twice in one dictionary keeps the last value, with no error.
- Never add or remove keys while looping over the dictionary (`RuntimeError`); collect first, then delete.
- A list cannot be a key (`TypeError: unhashable type`); use text, numbers or tuples.
- `counts[course] += 1` fails on the first sight of a course; use `counts.get(course, 0) + 1`.

## Clean up

Nothing to clean up: these scripts create no files.

## Next

[M05-L04 - Sets](../m05-l04-sets/)
