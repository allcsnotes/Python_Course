# M02-L02 · Numbers

> Video: Module 2, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- The two kinds of number: `int` (whole) and `float` (has a decimal point)
- All seven arithmetic operators, including `//` (floor division), `%` (modulo) and `**` (power), and the order they run in
- Update shortcuts such as `+=`, converting with `int()`, `float()` and `round()` (and banker's rounding)
- The helpers `abs`, `min`, `max`, `pow`, `divmod`, and the `math` module
- Why `0.1 + 0.2` is not `0.3`, how to compare floats, and why money is kept in whole paise
- Two common errors: `ZeroDivisionError` and joining text with a number using `+`

## Before you start

- Python 3.14 or newer (`python --version`). Do [M02-L01](../m02-l01-variables-as-labels-on-boxes/) first.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `types_demo.py` | `type()` of an int, a float and `5.0` |
| `gst.py` | GST (tax) on a course price, as floats |
| `discount.py`, `discount_brackets.py` | A 20 percent discount, and the same with brackets in the wrong place |
| `cart.py` | A shopping cart updated with `+=`, `-=`, `*=` |
| `convert.py` | `int`, `float` and `round` |
| `helpers.py` | `abs`, `min`, `max`, `pow`, `divmod` |
| `mathdemo.py` | The `math` module: `sqrt`, `ceil`, `floor`, `pi` |
| `bigint.py` | A huge whole number, and underscores in numbers |
| `floatbug.py`, `fixes.py`, `hidden.py` | The `0.1 + 0.2` surprise, two fixes, and the exact number a float stores |
| `paise.py` | GST again, with money kept in whole paise |
| `zero.py`, `mixup.py`, `mixup_fixed.py` | Two errors and the fix |

## Follow along

### 1. The surprise

Open the REPL (`python`) and add two small numbers:

```text
>>> 0.1 + 0.2
0.30000000000000004
```

Python did not break: every language gives this answer. Step 9 explains why. First, the basics.

### 2. int and float

Counting gives whole numbers (`int`), measuring gives numbers with parts (`float`). The quick test: a decimal point means float, even for `5.0`.

**`types_demo.py`**

```python
students = 25
price = 499.5
print(type(students))
print(type(price))
print(type(5.0))
```

```text
$ python types_demo.py
<class 'int'>
<class 'float'>
<class 'float'>
```

### 3. The seven operators

Use the REPL as a calculator. The Python course costs 1999 rupees:

```text
>>> 1999 + 3
2002
>>> 1999 - 200
1799
>>> 1999 * 3
5997
>>> 10 / 2
5.0
>>> 7 / 2
3.5
>>> 17 // 5
3
>>> 17 % 5
2
>>> 2 ** 10
1024
```

- `+`, `-`, `*`: add, subtract, multiply. Whole numbers stay whole.
- `/`: true division. It always gives a float, even for `10 / 2`.
- `//`: floor division, "how many whole times". 17 sweets shared by 5 children: 3 each.
- `%`: modulo, "what is left over". 2 sweets are left. Together: `17 = 5 * 3 + 2`. Think modulo whenever something wraps around or repeats: clocks, weekdays, even and odd (`n % 2`).
- `**`: power. Two to the power of ten is 1024.

### 4. Order of operations

Brackets first, then power, then `*` `/` `//` `%` (left to right), then `+` `-`.

```text
>>> 2 + 3 * 4
14
>>> (2 + 3) * 4
20
```

When in doubt, add brackets. They cost nothing and tell the next reader what you meant.

GST (a tax) of 18 percent on the course. `*` and `/` are on the same level, so Python goes left to right:

**`gst.py`**

```python
price = 1999
gst = price * 18 / 100
total = price + gst
print(gst)
print(total)
```

```text
$ python gst.py
359.82
2358.82
```

A 20 percent discount: multiplication and division first, then the subtraction.

**`discount.py`**

```python
price = 2500
percent = 20
final = price - price * percent / 100
print(final)
```

```text
$ python discount.py
2000.0
```

Put brackets around the subtraction and Python subtracts first, so the answer is very different:

**`discount_brackets.py`**

```python
price = 2500
percent = 20
final = (price - price * percent) / 100
print(final)
```

```text
$ python discount_brackets.py
-475.0
```

### 5. Update shortcuts

`cart = cart + 1999` works the right side out first, then puts the label on the answer. Python has a shortcut for this: `cart += 1999`. The same exists for `-=`, `*=`, `/=`, `//=`, `%=` and `**=`.

**`cart.py`**

```python
cart = 0
cart += 1999
print(cart)
cart += 1499
print(cart)
cart -= 300
print(cart)
cart *= 2
print(cart)
```

```text
$ python cart.py
1999
3498
3198
6396
```

### 6. Converting and rounding

`int()` does not round, it chops off the decimal part. `round()` rounds, and the second number is how many decimals to keep. Look at `round(2.5)`: Python uses banker's rounding, so an exact halfway number goes to the even neighbour (`2.5` gives `2`, `3.5` gives `4`, `0.5` gives `0`, `1.5` gives `2`). Always rounding halves up would push the small errors in one direction. Over a million prices that adds up.

**`convert.py`**

```python
print(int(3.99))
print(float(7))
print(round(3.14159, 2))
print(round(2.5))
print(round(3.5))
print(round(0.5))
print(round(1.5))
```

```text
$ python convert.py
3
7.0
3.14
2
4
0
2
```

### 7. Helpers and the math module

**`helpers.py`**

```python
print(abs(-250))
print(min(1999, 1499, 2999))
print(max(1999, 1499, 2999))
print(pow(2, 10))
print(divmod(17, 5))
```

```text
$ python helpers.py
250
1499
2999
1024
(3, 2)
```

`abs` drops the minus sign, `min` and `max` pick the smallest and largest, `pow(2, 10)` is the same as `2 ** 10`, and `divmod(17, 5)` gives "how many each" and "how many left over" as a pair.

For more mathematics, `import math` brings in a toolbox, and you write `math.` before each tool. allcsvideos.com shows 10 lessons per page. A course has 47 lessons. `47 / 10` is 4.7, but four pages would hide seven lessons, so we round up with `math.ceil`:

**`mathdemo.py`**

```python
import math

lessons = 47
per_page = 10
print(math.sqrt(144))
print(math.ceil(lessons / per_page))
print(math.floor(4.8))
print(math.pi)
```

```text
$ python mathdemo.py
12.0
5
4
3.141592653589793
```

`math.pi` is a fixed value, not a tool, so it has no brackets.

### 8. Big numbers

In many languages a whole number has a fixed size and overflows. A Python `int` can be as big as your memory allows, and every digit is exact. Underscores make long numbers readable, and Python ignores them:

**`bigint.py`**

```python
print(2 ** 200)
salary = 1_200_000
print(salary)
```

```text
$ python bigint.py
1606938044258990275541962092341162602522202993782792835301376
1200000
```

Python also has complex numbers (`3 + 4j`), used by engineers and scientists. We do not need them in this course.

### 9. Why 0.1 + 0.2 is not 0.3

One third in decimal is `0.3333...` forever, so you can never write it exactly. Computers count in binary, and in binary one tenth has the same problem. A float has room for only about 17 digits, so the computer cuts the endless pattern short. The `decimal` module can show the exact number a float really stores:

**`hidden.py`**

```python
from decimal import Decimal

print(Decimal(0.1))
```

```text
$ python hidden.py
0.1000000000000000055511151231257827021181583404541015625
```

0.2 is cut in the same way. Add two numbers that are each a hair off and the sum is a hair off too. This is not a Python bug: Java, JavaScript, C and almost every other language give the same answers.

**`floatbug.py`**

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

```text
$ python floatbug.py
0.30000000000000004
False
```

Fix 1: never ask whether two floats are exactly equal (`==`). Ask whether they are close enough with `math.isclose`.
Fix 2: when you need exact decimal arithmetic, use the `decimal` module, with the numbers written as text.

**`fixes.py`**

```python
import math
from decimal import Decimal

print(math.isclose(0.1 + 0.2, 0.3))
print(Decimal("0.1") + Decimal("0.2"))
```

```text
$ python fixes.py
True
0.3
```

### 10. Money: keep whole paise

A payment system that is wrong by a tiny fraction on every order loses real money over a year. So the rule is: never store money as a float. Store it as a whole number of its smallest unit (paise in India, cents elsewhere). Here is the GST example again, in paise (199900 paise is 1999 rupees):

**`paise.py`**

```python
price = 199900
gst = price * 18 // 100
total = price + gst
rupees, paise = divmod(total, 100)
print(gst)
print(total)
print(rupees, paise)
```

```text
$ python paise.py
35982
235882
2358 82
```

Only at the very end, when you show the price to a person, turn paise into rupees (here `divmod(total, 100)` splits them). Decide on one rounding rule (such as always round half up) and use it everywhere.

The money rule in three parts: keep money in whole paise or cents; compare floats with `isclose`, never `==`; use `Decimal` when you need exact decimals.

### 11. Two common errors

Dividing by zero. Today the batch has zero students:

**`zero.py`**

```python
revenue = 5000
students = 0
print(revenue / students)
```

```text
$ python zero.py
Traceback (most recent call last):
  File "zero.py", line 3, in <module>
    print(revenue / students)
          ~~~~~~~~^~~~~~~~~~
ZeroDivisionError: division by zero
```

`ZeroDivisionError`: the carets point at the slash. In maths you cannot divide by zero, and Python refuses too.

Joining text and a number with `+`:

**`mixup.py`**

```python
price = 499
print("Total: " + price)
```

```text
$ python mixup.py
Traceback (most recent call last):
  File "mixup.py", line 2, in <module>
    print("Total: " + price)
          ~~~~~~~~~~^~~~~~~
TypeError: can only concatenate str (not "int") to str
```

`+` between two pieces of text joins them, `+` between two numbers adds them, and Python will not guess when you mix a word and a number. For now, the fix is the comma from Module 1:

**`mixup_fixed.py`**

```python
price = 499
print("Total:", price)
```

```text
$ python mixup_fixed.py
Total: 499
```

## Interview tip

"Why does 0.1 + 0.2 not equal 0.3 in Python?" Answer: floats are stored in binary, and 0.1 and 0.2 have no exact binary form, so each is stored a hair off. The sum is a hair off too. It is not a Python bug. Compare floats with `math.isclose`, and use `Decimal` or whole paise for money.

## Common mistakes

- Expecting `/` to give a whole number: it always gives a float. Use `//` for whole division.
- Comparing floats with `==`, and storing money in a float.
- Forgetting brackets, so the order of operations gives a different answer (`discount_brackets.py`).
- Expecting `int(3.99)` to round: it chops.
- Dividing by zero, or joining text and a number with `+`.

## Clean up

Nothing to clean up.

## Next

[M02-L03 · Text and Strings](../m02-l03-text-and-strings/)
