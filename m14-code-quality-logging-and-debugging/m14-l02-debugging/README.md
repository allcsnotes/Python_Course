# M14-L02 · Debugging

> Video: Module 14, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- A method that beats guessing: reproduce, look, test one idea, fix it and add a test
- Print debugging, and where it stops being enough
- The `breakpoint()` function and the pdb commands `l`, `p`, `n`, `s`, `c`, `w`, `u`, `d`, `q`
- Conditional breakpoints, and looking at a crash afterwards (`python -i`, `pdb.pm()`, `python -m pdb`)
- Cutting a problem in half: by hand on a file, and with `git bisect run` on history
- Leaving no debugging code behind (ruff `T20`/`T100`, `PYTHONBREAKPOINT=0`)

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `git` for the bisect step. `pytest` and `ruff` (from Lesson 1) for a few steps: `pip install pytest ruff` in a virtual environment, or `uv add --dev pytest ruff`.
- No Docker needed. Earlier lessons: M14-L01 (ruff), M13-L05 (write the failing test first).

## Files in this folder

| File | What it is |
|------|------------|
| `invoice.py` | The buggy cart: the coupon is taken off inside the loop |
| `invoice_print.py` | The same file with one `print(f"{price=} {total=}")` line |
| `invoice_bp.py` | The same file with `breakpoint()` at the top of the loop |
| `invoice_fixed.py` | The fixed cart: coupon comes off once, after the loop |
| `test_invoice.py` | The test that fails on `invoice.py` and passes on the fix |
| `orders.py`, `orders_plain.py` | 1000 payments, one refund saved with the wrong sign (with and without a conditional breakpoint) |
| `coupon.py` | Crashes with `KeyError` because the coupon was typed in small letters |
| `titles.txt`, `import_courses.py`, `showline.py` | 64 course titles, an importer that takes a first and last line, and a helper to show one line |
| `make_bisect_repo.sh` | Builds a throwaway Git repository with 17 commits for `git bisect` |
| `repro.py` | The minimal reproduction: five lines that still show the bug |
| `leftovers.py` | A file with a forgotten `print` and `breakpoint()` for ruff |

## Follow along

### 1. The bug with no error

Lukas's cart: one Python course at 1500, two SQL courses at 500 each, and a coupon for 10 percent off the whole cart.

```bash
python invoice.py
```

```text
1948.5
```

The right answer is 2250. There is no traceback: a wrong answer with no error is the hardest kind. The method:

1. Reproduce: make the bug happen every time, with the smallest example.
2. Look: find out what the program really does, not what you believe.
3. Test one idea at a time.
4. Fix it, and add a test.

### 2. Print debugging

`invoice_print.py` adds one line at the top of the loop. The `=` after a name in an f-string prints the name and the value.

```bash
python invoice_print.py
```

```text
price=1500 total=0
price=500 total=1350.0
price=500 total=1665.0
1948.5
```

The second line should have `total=1500`, but it is already 1350. Something takes money off in every turn. Print is a fine quick look, but you must guess where to put the prints, every new question means editing and rerunning, and forgotten prints reach production.

### 3. The debugger: breakpoint() and pdb

`invoice_bp.py` has `breakpoint()` where the print was.

```bash
python invoice_bp.py
```

```text
> /path/to/invoice_bp.py(8)cart_total()
-> breakpoint()
(Pdb)
```

(The full path in the first line is yours.) The program stopped at line 8, inside `cart_total`. The `(Pdb)` prompt waits for a command:

| Command | Meaning |
|---------|---------|
| `l` | list the code around the arrow |
| `p expr` | print any value |
| `n` | next: run one line, stop again |
| `s` | step: go inside a function call |
| `c` | continue to the next breakpoint |
| `w` | where: the chain of calls |
| `u` / `d` | move up / down the chain |
| `q` | quit (it asks `y/n`) |

Type these, one per prompt, and compare:

```text
(Pdb) l
  5  	def cart_total(prices, percent):
  6  	    total = 0
  7  	    for price in prices:
  8  ->	        breakpoint()
  9  	        total = total + price
 10  	        total = price_after_coupon(total, percent)
 11  	    return total
(Pdb) p price
1500
(Pdb) p total
0
(Pdb) n
-> total = total + price
(Pdb) n
-> total = price_after_coupon(total, percent)
(Pdb) p total
1500
(Pdb) n
-> for price in prices:
(Pdb) p total
1350.0
```

The total fell from 1500 to 1350 in the middle of adding. Now `c` to continue to the second stop:

```text
(Pdb) c
(Pdb) p price, total
(500, 1350.0)
```

It should be 1500 here. The coupon is taken off again and again, once per price. Quit with `q` then `y`.

### 4. Step inside a function

`n` treats a function call as one step. To look inside, run again, press `n` twice to reach the coupon line (line 10), then `s`:

```text
(Pdb) s
--Call--
> invoice_bp.py(1)price_after_coupon()
-> def price_after_coupon(price, percent):
(Pdb) w
  invoice_bp.py(16)<module>()
-> print(cart_total(prices, 10))
  invoice_bp.py(10)cart_total()
-> total = price_after_coupon(total, percent)
> invoice_bp.py(1)price_after_coupon()
-> def price_after_coupon(price, percent):
(Pdb) p price
1500
(Pdb) p percent
10
(Pdb) n
(Pdb) n
--Return--
> invoice_bp.py(2)price_after_coupon()->1350.0
(Pdb) p total
*** NameError: name 'total' is not defined
(Pdb) u
> invoice_bp.py(10)cart_total()
(Pdb) p total
1500
```

Inside `price_after_coupon` the first value is called `price`, but `cart_total` handed over its running total, so the function takes 10 percent off the whole running total. The `NameError` is scope (Module 4): a function sees only its own names, and the debugger obeys the same rules. `u` moves up into `cart_total`, where `total` exists. Quit with `q`, `y`.

Cause found: the coupon belongs after the loop, once.

### 5. Fix it, with a test that fails first

```bash
pip install pytest        # or: uv add --dev pytest
pytest -q
```

```text
>       assert cart_total([1500, 500, 500], 10) == 2250
E       assert 1948.5 == 2250
E        +  where 1948.5 = cart_total([1500, 500, 500], 10)

test_invoice.py:5: AssertionError
=========================== short test summary info ============================
FAILED test_invoice.py::test_coupon_comes_off_the_whole_cart - assert 1948.5 ...
1 failed in 0.02s
```

Red: the test sees the bug. Now use the fix (add up the prices in the loop, take the coupon off the total once, after the loop):

```bash
cp invoice_fixed.py invoice.py
pytest -q
```

```text
.                                                                        [100%]
1 passed in 0.00s
```

### 6. A conditional breakpoint

1000 payments of 500 should total 500000, but the program prints 499000.

```bash
python orders_plain.py
```

```text
499000
```

A print would write 1000 lines. A plain `breakpoint()` would stop 1000 times. Put an ordinary `if` around it (`orders.py`):

```python
for index, amount in enumerate(amounts):
    if amount < 0:
        breakpoint()
```

```bash
python orders.py
```

```text
> orders.py(5)total_paid()
-> breakpoint()
(Pdb) p index, amount
(612, -500)
(Pdb) p total
306000
(Pdb) c
499000
```

It stops once, at the odd payment: position 612 (counting from zero) is a refund saved with the wrong sign. Pdb can also do this without editing code: at its prompt, `b file.py:LINE, condition` (type `help b` for details).

### 7. Look at a crash afterwards

`coupon.py` crashes: the coupon `save20` was typed in small letters. Run it interactively with `-i`, so Python stays open after the crash:

```bash
python -i coupon.py
```

```text
2250.0
Traceback (most recent call last):
  ...
KeyError: 'save20'
>>>
```

At the `>>>` prompt:

```python
import pdb
pdb.pm()
```

`pm` means post mortem. You land on the line that raised the error:

```text
> coupon.py(5)percent_for()
-> return COUPONS[code]
(Pdb) p code
'save20'
(Pdb) p COUPONS
{'SAVE10': 10, 'SAVE20': 20}
(Pdb) u
> coupon.py(9)checkout()
(Pdb) p price
2500
```

The keys are capital letters, ours was small letters. A shortcut that opens the debugger at the crash by itself:

```bash
python -m pdb coupon.py
```

Type `c` at the first prompt. When the program crashes it says `Uncaught exception. Entering post mortem debugging`. Leave with `q` (and `exit()` if you came through `python -i`).

### 8. VS Code, same ideas

| pdb | VS Code |
|-----|---------|
| `breakpoint()` | click left of the line number: a red dot |
| run the file | Run and Debug, or F5 |
| `p` | Variables panel |
| `w` | Call Stack panel |
| `c` | Continue, F5 |
| `n` | Step Over, F10 |
| `s` | Step Into, F11 |
| `b file:line, cond` | right-click the red dot, type the condition |

Use both: pdb works everywhere (even on a server with only a terminal), VS Code is friendlier on your own machine.

### 9. Bisect a file by hand

`titles.txt` has 64 course titles and one of them is blank (but you cannot see it). The importer takes a first and last line after the file name:

```bash
python import_courses.py titles.txt 1 64
python import_courses.py titles.txt 1 32
python import_courses.py titles.txt 33 64
python import_courses.py titles.txt 33 48
python import_courses.py titles.txt 33 40
python import_courses.py titles.txt 41 48
python import_courses.py titles.txt 41 44
python import_courses.py titles.txt 41 42
python import_courses.py titles.txt 41 41
python showline.py titles.txt 41
```

```text
error: a title is blank
ok: 32 titles
error: a title is blank
error: a title is blank
ok: 8 titles
error: a title is blank
error: a title is blank
error: a title is blank
error: a title is blank
'   '
```

Six cuts for 64 lines. The title looked empty because it was spaces. For 1000 lines it takes 10 cuts, for a million only 20.

### 10. Bisect history with git

```bash
bash make_bisect_repo.sh     # makes ./bisect_repo with 17 commits
cd bisect_repo
python check.py
```

```text
4072
```

`check.py` prints the total and fails when it is not 2655. It passed at the commit called "Add 18 percent GST". Find the commit that broke it among those after it:

```bash
git log --oneline          # note the hash next to "Add 18 percent GST"
git bisect start
git bisect bad
git bisect good <that hash>
git bisect run python check.py
```

The last lines:

```text
f062d5edb066267a163e4df0763b6bf2ff5398d2 is the first bad commit
    Move the GST rate into a constant
 cart.py | 5 ++++-
bisect found first bad commit
```

Four test runs for 14 commits (hashes differ on your machine, but the commit message is the same). The new line says `GST_PERCENT = 81`: somebody turned 18 around. Go back to where you were:

```bash
git bisect reset
```

### 11. Two free habits

- The rubber duck: explain the bug out loud, line by line, to a rubber duck or to Priya. You must say what the code really does, not what you hoped.
- The minimal reproduction: delete everything the bug does not need. `repro.py` is five lines:

```bash
python repro.py
```

```text
1665.0
```

(1800 is right.) Priya, or a stranger on the internet, understands it in ten seconds, and often you find the bug while shrinking.

### 12. Leave nothing behind

`leftovers.py` has a forgotten `print` and a `breakpoint()`. Ruff knows both:

```bash
ruff check --select T20,T100 --output-format concise leftovers.py
```

```text
leftovers.py:3:5: T201 `print` found
leftovers.py:4:5: T100 Trace found: `breakpoint` used
Found 2 errors.
1 unsafe fix available with `--fix --unsafe-fixes`.
```

A safety net: the environment variable `PYTHONBREAKPOINT=0` makes every `breakpoint()` call do nothing.

```bash
PYTHONBREAKPOINT=0 python invoice_bp.py     # Windows PowerShell: $env:PYTHONBREAKPOINT = "0"
```

```text
1948.5
```

(That is the output from the buggy version. If you already copied the fix over `invoice.py`, `invoice_bp.py` is still the buggy copy, so you see 1948.5.) The print that is allowed to stay in your code has another name: a log message (next lesson).

## Common mistakes

1. Debugging code left behind: a `breakpoint()` in a server stops everything and waits for a keyboard nobody has. Run ruff with `T20` and `T100`, and set `PYTHONBREAKPOINT=0` where nobody can type.
2. Changing things at random: change a line, run, change another line, run. Every change can add a new bug and you learn nothing. Stop, reproduce, look, test one idea at a time.
3. Fixing the symptom instead of the cause: adding a line that adds the missing money back looks right for one case, and the bug lives on. Keep asking why until you reach the cause (here, the coupon inside the loop).
4. Fixing the bug without a test. Write the failing test first, then the bug is guarded for good.

## Clean up

```bash
rm -rf bisect_repo __pycache__ .pytest_cache .ruff_cache
```

If you copied `invoice_fixed.py` over `invoice.py`, restore it from this repo to start again.

## Next

[M14-L03 · Logging the Right Way](../m14-l03-logging-the-right-way/)
