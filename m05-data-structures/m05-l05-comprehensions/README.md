# M05-L05 · Comprehensions

> Video: Module 5, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- How to turn the "empty list, loop, append" pattern into a one-line list comprehension
- How to filter with `if` at the end, and how to choose with `if ... else` at the front
- How to build dictionaries and sets the same way
- How a comprehension inside a comprehension builds and flattens a grid
- The most important skill: when to stop and use a plain loop

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Helpful: Module 3 (loops), Lesson 3 (dictionaries) and Lesson 4 (sets). No earlier lesson folder is needed.
- Docker is not used.

## Files in this folder

Every file is a tiny script that prints one result. The `loop_*` files are the plain-loop versions, the `comp_*` files the comprehensions.

| File | What it is |
|------|------------|
| `loop_upper.py`, `comp_upper.py` | Capital titles: loop, then one line |
| `comp_len.py`, `comp_range.py` | A different first part: lengths, squares |
| `loop_filter.py`, `comp_filter.py`, `comp_filter2.py` | Filtering prices |
| `comp_both.py` | Change and filter at once, over three lines |
| `cond.py`, `cond2.py`, `comp_ifelse.py` | `if ... else` as a choice |
| `loop_dict.py`, `comp_dict.py`, `comp_sale.py`, `comp_dict_if.py` | Dictionary comprehensions |
| `comp_set.py` | A list and a set comprehension side by side |
| `comp_nested.py`, `loop_flat.py`, `comp_flat.py` | A grid, and flattening it |
| `bad_else.py`, `fix_else.py` | Mistake: `if` and `else` at the end, and the fix |
| `scope.py`, `scope_loop.py` | A comprehension keeps its variable to itself; a loop does not |
| `cramped.py`, `readable.py` | A hard-to-read comprehension and its loop version |
| `side_effect.py`, `side_loop.py` | Trap: `print` inside a comprehension |
| `tryit.py` | The "try it yourself" answers |

## Follow along

Run every command from this folder. All the outputs below are real and do not depend on your machine.

### 1. Asha's loop: capital titles

Asha has four course titles in small letters and wants capitals for the banners. The long way: an empty list, a loop and `append`.

```python
# loop_upper.py
titles = ["python", "sql", "git", "docker"]
upper = []
for title in titles:
    upper.append(title.upper())
print(upper)
```

```text
$ python loop_upper.py
['PYTHON', 'SQL', 'GIT', 'DOCKER']
```

Five lines for a very simple job. Priya shows her the one-line version, a comprehension.

### 2. The same job in one line

Build it in four steps: keep the name and the square brackets, move in the thing you add (`title.upper()`), copy the `for` line without its colon, close the bracket.

```python
# comp_upper.py
titles = ["python", "sql", "git", "docker"]
upper = [title.upper() for title in titles]
print(upper)
```

```text
$ python comp_upper.py
['PYTHON', 'SQL', 'GIT', 'DOCKER']
```

It is the same loop in a shorter shape. Read it like a sentence: `upper` is `title.upper()` for every `title` in `titles`.

### 3. Change the first part

The first part can be any expression (anything that gives back a value). Here it is the length of each title.

```python
# comp_len.py
titles = ["python", "sql", "git", "docker"]
sizes = [len(title) for title in titles]
print(sizes)
```

```text
$ python comp_len.py
[6, 3, 3, 6]
```

### 4. Loop over anything

The part after `in` can be anything a `for` loop can walk through, such as a `range`.

```python
# comp_range.py
squares = [n * n for n in range(1, 6)]
print(squares)
```

```text
$ python comp_range.py
[1, 4, 9, 16, 25]
```

### 5. Filter with an `if` at the end

Asha wants only the prices under 1500 for a sale page. First the loop with an `if`, then the comprehension. The filter goes last.

```python
# loop_filter.py
prices = [1499, 999, 1999, 499, 2499]
cheap = []
for price in prices:
    if price < 1500:
        cheap.append(price)
print(cheap)
```

```text
$ python loop_filter.py
[1499, 999, 499]
```

```python
# comp_filter.py
prices = [1499, 999, 1999, 499, 2499]
cheap = [price for price in prices if price < 1500]
print(cheap)
```

```text
$ python comp_filter.py
[1499, 999, 499]
```

Two prices failed the `if`, so they were never added.

### 6. The opposite filter

Keep the prices that are 1500 or more. The item that gets in comes out unchanged.

```python
# comp_filter2.py
prices = [1499, 999, 1999, 499, 2499]
big = [price for price in prices if price >= 1500]
print(big)
```

```text
$ python comp_filter2.py
[1999, 2499]
```

### 7. Change and filter at once

Inside brackets Python lets you spread a comprehension over several lines, which is easier to read.

```python
# comp_both.py
titles = ["python", "sql", "git", "docker"]
long_names = [
    title.upper()
    for title in titles
    if len(title) > 3
]
print(long_names)
```

```text
$ python comp_both.py
['PYTHON', 'DOCKER']
```

`sql` and `git` have only three letters, so the filter kept them out.

### 8. A choice with `if` and `else`

`value if condition else other` is a conditional expression. It always gives one of two values.

```python
# cond.py
price = 1999
label = "cheap" if price < 1500 else "pricey"
print(label)
```

```text
$ python cond.py
pricey
```

```python
# cond2.py
price = 999
label = "cheap" if price < 1500 else "pricey"
print(label)
```

```text
$ python cond2.py
cheap
```

### 9. The choice at the front of a comprehension

Nothing is dropped: five prices in, five labels out.

```python
# comp_ifelse.py
prices = [1499, 999, 1999, 499, 2499]
labels = [
    "cheap" if price < 1500 else "pricey"
    for price in prices
]
print(labels)
```

```text
$ python comp_ifelse.py
['cheap', 'cheap', 'pricey', 'cheap', 'pricey']
```

Rule of thumb: with an `else`, the choice goes at the front. With no `else`, the `if` goes at the end (it is a filter).

### 10. Dictionary comprehensions

Curly brackets with `key: value` build a dictionary. First the loop, then the one-liner.

```python
# loop_dict.py
titles = ["python", "sql", "git", "docker"]
sizes = {}
for title in titles:
    sizes[title] = len(title)
print(sizes)
```

```text
$ python loop_dict.py
{'python': 6, 'sql': 3, 'git': 3, 'docker': 6}
```

```python
# comp_dict.py
titles = ["python", "sql", "git", "docker"]
sizes = {title: len(title) for title in titles}
print(sizes)
```

```text
$ python comp_dict.py
{'python': 6, 'sql': 3, 'git': 3, 'docker': 6}
```

The colon between key and value is what tells Python this is a dictionary.

### 11. From a dictionary to a dictionary

`.items()` hands out each key and value. Here every price drops by 200, then a filter keeps only courses under 1000.

```python
# comp_sale.py
prices = {"python": 1499, "sql": 999, "git": 499}
sale = {
    title: price - 200
    for title, price in prices.items()
}
print(sale)
```

```text
$ python comp_sale.py
{'python': 1299, 'sql': 799, 'git': 299}
```

```python
# comp_dict_if.py
prices = {"python": 1499, "sql": 999, "git": 499}
under = {
    title: price
    for title, price in prices.items()
    if price < 1000
}
print(under)
```

```text
$ python comp_dict_if.py
{'sql': 999, 'git': 499}
```

### 12. Set comprehensions

Curly brackets with a single value (no colon) build a set, so repeats disappear. The order of a set is not something to rely on (yours may print in a different order).

```python
# comp_set.py
titles = ["python", "sql", "git", "docker", "go", "rust"]
as_list = [len(title) for title in titles]
as_set = {len(title) for title in titles}
print(as_list)
print(as_set)
```

```text
$ python comp_set.py
[6, 3, 3, 6, 2, 4]
{2, 3, 4, 6}
```

### 13. A comprehension inside a comprehension

Read it from the inside: the inner part makes one row, the outer part repeats it for each row. A list of lists is a grid.

```python
# comp_nested.py
table = [
    [row * col for col in range(1, 4)]
    for row in range(1, 4)
]
print(table)
```

```text
$ python comp_nested.py
[[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

### 14. Flatten the grid

Two `for` parts in a row read in the same order as two loops written one under the other. Two is the limit.

```python
# loop_flat.py
table = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
flat = []
for row in table:
    for number in row:
        flat.append(number)
print(flat)
```

```text
$ python loop_flat.py
[1, 2, 3, 2, 4, 6, 3, 6, 9]
```

```python
# comp_flat.py
table = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
flat = [number for row in table for number in row]
print(flat)
```

```text
$ python comp_flat.py
[1, 2, 3, 2, 4, 6, 3, 6, 9]
```

### 15. Mistake 1: `if` and `else` at the end

At the end of a comprehension, `if` can only be a filter, and a filter has no `else`.

```python
# bad_else.py
prices = [1499, 999, 1999]
cheap = [price for price in prices if price < 1500 else 0]
print(cheap)
```

```text
$ python bad_else.py
  File "bad_else.py", line 2
    cheap = [price for price in prices if price < 1500 else 0]
                                                       ^^^^
SyntaxError: invalid syntax
```

The fix: a choice that keeps every item goes at the front.

### 16. Fix for mistake 1

```python
# fix_else.py
prices = [1499, 999, 1999]
cheap = [price if price < 1500 else 0 for price in prices]
print(cheap)
```

```text
$ python fix_else.py
[1499, 999, 0]
```

### 17. Mistake 2: the name does not stay

A comprehension keeps its loop variable to itself. A `for` loop leaves its last value behind.

```python
# scope.py
numbers = [1, 2, 3]
doubled = [n * 2 for n in numbers]
print(doubled)
print(n)
```

```text
$ python scope.py
[2, 4, 6]
Traceback (most recent call last):
  File "scope.py", line 4, in <module>
    print(n)
          ^
NameError: name 'n' is not defined
```

```python
# scope_loop.py
numbers = [1, 2, 3]
for n in numbers:
    pass
print(n)
```

```text
$ python scope_loop.py
3
```

If you need the last value afterwards, use a loop.

### 18. Mistake 3: round brackets

Swapping the square brackets for round ones does not give a tuple. It gives a generator, which makes values one at a time, only when asked (Module 9 has a lesson on it). For a list, use square brackets.

### 19. When to stop: a cramped comprehension

Three labels in one comprehension is correct, but hard to read. The same job as a plain loop is longer and clearer.

```python
# cramped.py
prices = [1499, 0, 1999, 499]
labels = [
    "free" if price == 0 else "cheap" if price < 1500
    else "pricey" for price in prices
]
print(labels)
```

```text
$ python cramped.py
['cheap', 'free', 'pricey', 'cheap']
```

```python
# readable.py
prices = [1499, 0, 1999, 499]
labels = []
for price in prices:
    if price == 0:
        labels.append("free")
    elif price < 1500:
        labels.append("cheap")
    else:
        labels.append("pricey")
print(labels)
```

```text
$ python readable.py
['cheap', 'free', 'pricey', 'cheap']
```

Both print the same. Readable code beats short code.

### 20. Trap: using a comprehension for actions

`print` returns `None`, so the comprehension collects two useless `None` values. To do things, use a `for` loop.

```python
# side_effect.py
names = ["Asha", "Lukas"]
result = [print(name) for name in names]
print(result)
```

```text
$ python side_effect.py
Asha
Lukas
[None, None]
```

```python
# side_loop.py
names = ["Asha", "Lukas"]
for name in names:
    print(name)
```

```text
$ python side_loop.py
Asha
Lukas
```

### 21. Try it yourself

Take the five prices. Make a list with every price 100 lower, keep only the prices above 1000, and build a dictionary from each title to its length.

```python
# tryit.py
prices = [1499, 999, 1999, 499, 2499]
off = [price - 100 for price in prices]
above = [price for price in prices if price > 1000]
titles = ["python", "sql", "git"]
sizes = {title: len(title) for title in titles}
print(off)
print(above)
print(sizes)
```

```text
$ python tryit.py
[1399, 899, 1899, 399, 2399]
[1499, 1999, 2499]
{'python': 6, 'sql': 3, 'git': 3}
```

## Common mistakes

- Putting `if` and `else` at the end of a comprehension. A filter (at the end) has no `else`; a choice with `else` goes at the front.
- Expecting the loop variable to exist after a comprehension. It does not (`NameError`).
- Using round brackets and expecting a tuple. You get a generator.
- Cramming several decisions into one line. If it needs `else if`, comments or several steps, use a plain loop.
- Using a comprehension to do things (like `print`). It collects `None` values. Use a `for` loop.

## Clean up

Nothing to clean up.

## Next

[M05-L06 · Names, Objects and Mutability](../m05-l06-names-objects-and-mutability/)
