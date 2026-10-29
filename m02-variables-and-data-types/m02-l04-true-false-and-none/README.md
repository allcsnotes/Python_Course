# M02-L04 · True, False and None

> Video: Module 2, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- The boolean type `bool` and its two values, `True` and `False` (capital letters)
- The six comparison operators, and why `==` (ask) is different from `=` (store)
- A first look at `and`, `or`, `not` and chained comparisons (full story in Module 3)
- Truthy and falsy values, and what `bool()` says about any value
- `None`: "no value here yet", how to check for it with `is None`, and the `in` operator
- Three pitfalls: `0.1 + 0.2 == 0.3`, the text `"False"`, and maths with `None`

## Before you start

- Python 3.14 or newer (`python --version`). Do [M02-L03](../m02-l03-text-and-strings/) first.
- A terminal opened in this folder. The REPL parts are typed at the `>>>` prompt (start it with `python`).

## Files in this folder

| File | What it is |
|------|------------|
| `bools.py` | Two booleans and their type |
| `lower.py` | `true` with a small t, a `NameError` |
| `mix.py`, `silent.py` | The two ways one `=` goes wrong |
| `cmperr.py` | Comparing a number with text using `<` |
| `float.py` | Comparing decimal results: `==` against `isclose` |
| `none.py`, `noneprint.py` | `None`, and the value `print` gives back |
| `false.py` | The text `"False"` is not `False` |
| `seats_bug.py`, `seats_fixed.py` | Maths with `None`, and the fix |

## Follow along

### 1. Three questions

Each line asks Python a question. In the REPL:

```text
>>> 10 > 3
True
>>> 10 == 3
False
>>> 0.1 + 0.2 == 0.3
False
```

The answers are not numbers and not text: they are a new kind of value. The last one is the float surprise from [M02-L02](../m02-l02-numbers/), explained in pitfall 1.

### 2. Booleans

A boolean (`bool`) is a yes-or-no value, like a light switch. It has exactly two values: `True` and `False`, spelled with a capital first letter. Store two facts about Lukas:

**`bools.py`**

```python
is_enrolled = True
has_paid = False
print(is_enrolled)
print(has_paid)
print(type(is_enrolled))
```

```text
$ python bools.py
True
False
<class 'bool'>
```

A small `true` is just a name nobody created:

**`lower.py`**

```python
is_enrolled = true
print(is_enrolled)
```

```text
$ python lower.py
Traceback (most recent call last):
  File "lower.py", line 1, in <module>
    is_enrolled = true
                  ^^^^
NameError: name 'true' is not defined. Did you mean: 'True'?
```

### 3. Comparison operators

An operator is a symbol that works on values. The six comparison operators produce a boolean: `==` equal, `!=` not equal, `<` less than, `>` greater than, `<=` less than or equal, `>=` greater than or equal. Lukas has a budget of 500 rupees and the course costs 499:

```text
>>> price = 499
>>> budget = 500
>>> price == 499
True
>>> price != 499
False
>>> price < budget
True
>>> price > budget
False
>>> price <= 499
True
>>> price < 499
False
>>> price >= budget
False
```

`<=` and `>=` count the edge case (equal is included). Notice the two equals signs in `==`: one `=` stores, two `==` ask.

Using one `=` when you meant two goes wrong in two ways. Way one is a syntax error:

**`mix.py`**

```python
price = 499
499 = price
print(price)
```

```text
$ python mix.py
  File "mix.py", line 2
    499 = price
    ^^^
SyntaxError: cannot assign to literal here. Maybe you meant '==' instead of '='?
```

Way two is silent. You wanted to ask "is the price 500?" but you wrote an assignment, so the box was overwritten with no error and no warning:

**`silent.py`**

```python
price = 499
price = 500
print(price)
```

```text
$ python silent.py
500
```

### 4. Comparing text and mixed values

```text
>>> "Python" == "Python"
True
>>> "Python" == "python"
False
>>> 5 == 5.0
True
>>> 5 == "5"
False
>>> "apple" < "banana"
True
>>> "10" < "9"
True
```

Capitals matter. `5 == 5.0` is `True` (a whole number and a decimal can be equal), but the number 5 and the text `"5"` are never equal. Text is ordered like words in a dictionary, one character at a time from the left, so the text `"10"` is less than `"9"`. Ordering a number against text is an error:

**`cmperr.py`**

```python
print("start")
print(5 < "10")
```

```text
$ python cmperr.py
start
Traceback (most recent call last):
  File "cmperr.py", line 2, in <module>
    print(5 < "10")
          ^^^^^^^^
TypeError: '<' not supported between instances of 'int' and 'str'
```

`start` is printed, then Python refuses. Compare things of the same kind: numbers with numbers, text with text.

### 5. and, or, not (a preview)

To unlock a video, Asha needs the student to be enrolled and to have paid. `and` needs both to be true (like a cinema: ticket and on time), `or` needs one (card or cash), `not` flips the answer. Module 3 covers this fully with tables.

```text
>>> is_enrolled = True
>>> has_paid = False
>>> is_enrolled and has_paid
False
>>> is_enrolled or has_paid
True
>>> not has_paid
True
```

Python also lets you chain comparisons, like in maths: "1 is at most rating, which is at most 5":

```text
>>> rating = 4
>>> 1 <= rating <= 5
True
>>> rating = 7
>>> 1 <= rating <= 5
False
```

### 6. True is 1, False is 0

Underneath, `True` is the number 1 and `False` is 0. You do not need this today, just do not be surprised when you see it. It means you can count yes answers by adding them.

```text
>>> True + True
2
>>> int(True)
1
>>> int(False)
0
>>> True == 1
True
>>> is_enrolled = True
>>> has_paid = False
>>> is_enrolled + has_paid
1
```

### 7. Truthy and falsy

Can Python treat any value as a yes or no? The function `bool()` answers `True` if the value is something and `False` if it is nothing, like asking whether a glass has anything in it.

```text
>>> bool(0)
False
>>> bool(7)
True
>>> bool(-3)
True
>>> bool(0.0)
False
>>> bool("")
False
>>> bool("hi")
True
>>> bool(" ")
True
>>> bool([])
False
>>> bool([1, 2, 3])
True
>>> bool(None)
False
```

The rule: zero, empty things and `None` count as no. Everything else counts as yes. A negative number is still something, and so is a single space. A value that counts as `False` is called falsy, one that counts as `True` is truthy. (`[]` is an empty list, a collection covered in Module 5.)

### 8. None

`None` (capital N, no quotes) is the value for "there is nothing here yet", like an empty certificate box on a shelf. It has its own type:

**`none.py`**

```python
certificate = None
print(certificate)
print(type(certificate))
```

```text
$ python none.py
None
<class 'NoneType'>
```

`None` is not zero and not empty text. Three different things: a zero, an empty text, and no value at all.

```text
>>> None == 0
False
>>> None == ""
False
>>> bool(None)
False
```

`None` comes from two common places: a variable with no real value yet, and a function that has nothing to give back. `print` shows a message but returns nothing, so the box named `result` holds `None`:

**`noneprint.py`**

```python
result = print("Welcome, Lukas")
print(result)
```

```text
$ python noneprint.py
Welcome, Lukas
None
```

To check whether a box is empty use `is None` and `is not None`. You may see `== None` in other people's code. It usually gives the same answer, but `is None` is the habit to build.

```text
>>> certificate = None
>>> certificate is None
True
>>> certificate is not None
False
>>> certificate = "CERT-0042"
>>> certificate is None
False
>>> certificate is not None
True
```

The kinds of value you know now:

```text
>>> type(True)
<class 'bool'>
>>> type(5)
<class 'int'>
>>> type(2.5)
<class 'float'>
>>> type("hi")
<class 'str'>
>>> type(None)
<class 'NoneType'>
```

### 9. The `in` operator

`in` asks whether a piece of text is inside another. Capitals matter, `not in` flips it, and a real use is a rough check of an email address:

```text
>>> title = "Python for Beginners"
>>> "Python" in title
True
>>> "python" in title
False
>>> "Java" in title
False
>>> "Java" not in title
True
>>> "@" in "asha@allcsvideos.com"
True
>>> "@" in "asha.allcsvideos.com"
False
```

### 10. The pitfalls

Pitfall 1: comparing decimal results with `==`. The computer stores a tiny error, so ask whether the numbers are close enough (`math.isclose`), or round first:

**`float.py`**

```python
import math
total = 0.1 + 0.2
print(total == 0.3)
print(math.isclose(total, 0.3))
print(round(total, 2) == 0.3)
```

```text
$ python float.py
False
True
True
```

Pitfall 2: the text `"False"` is not `False`. Any text with something in it is truthy, so `bool("False")` is `True`. Soon a person will type answers into your program, and everything they type arrives as text. Compare the text, not the boolean:

**`false.py`**

```python
answer = "False"
print(bool(answer))
print(answer == False)
is_enrolled = answer == "True"
print(is_enrolled)
```

```text
$ python false.py
True
False
False
```

Pitfall 3: maths with `None`. You cannot add one to nothing:

**`seats_bug.py`**

```python
seats = None
print(seats + 1)
```

```text
$ python seats_bug.py
Traceback (most recent call last):
  File "seats_bug.py", line 2, in <module>
    print(seats + 1)
          ~~~~~~^~~
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

Give the box a real starting value (after Module 3 you will also learn to check for `None` first):

**`seats_fixed.py`**

```python
seats = 0
print(seats + 1)
```

```text
$ python seats_fixed.py
1
```

Two more traps from this lesson: capital `T` and `F`, and one equals sign versus two.

## Interview tip

"What counts as falsy in Python?" `False`, `None`, zero of any number type, and empty things such as empty text or an empty list. Everything else is truthy.

## Common mistakes

- Writing `true` or `false` in lower case (`NameError`).
- Using `=` when you meant `==`.
- Comparing a number with text, or expecting `"10" < "9"` to be `False`.
- Comparing floats with `==`.
- Treating the text `"False"` as the boolean `False`.
- Doing maths on `None`.

## Clean up

Nothing to clean up.

## Next

[M02-L05 · Input and Output](../m02-l05-input-and-output/)
