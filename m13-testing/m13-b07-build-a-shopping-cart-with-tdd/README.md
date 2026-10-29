# M13-B07 · Build a Shopping Cart with TDD

> Video: Module 13, Build 7. Watch it first, then follow along here.

## What you'll learn

- How to grow a whole feature (a shopping cart with coupons and GST) one red, green, refactor trip at a time
- How to use `pytest.raises`, `parametrize` and fixtures in a real project
- How to keep money in whole rupees, with no floats, and round half up with integer maths
- How tests catch real bugs before customers do (a rounding bug and three coupon bugs)
- How to refactor the inside of a class without touching a single test
- How to measure coverage with branches, check the tests by breaking the code on purpose, and write a strict command for a build server

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not needed.
- You should know the earlier lessons of this module: `m13-l01-your-first-pytest-tests`, `m13-l02-fixtures-and-parametrize`, `m13-l04-coverage-and-property-based-testing` and `m13-l05-test-driven-development`.
- The video makes a small uv project (as in Module 7). With uv, from the `shop/` folder:

```bash
cd shop
uv sync
```

  Without uv, use a virtual environment (this works too):

```bash
cd shop
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install "pytest>=9.1.1" "pytest-cov>=7.1.0"
```

Where this README says `uv run pytest`, you can also run `python -m pytest` inside your activated environment.

## Files in this folder

| File | What it is |
|------|------------|
| `shop/cart.py` | The finished cart: `Cart`, `Coupon`, `Line`, the coupon table and the error classes |
| `shop/test_cart.py` | The 31 tests, as at the end of the video |
| `shop/conftest.py` | The fixtures `cart` (an empty cart) and `full_cart` (Lukas's cart) |
| `shop/demo.py` | Lukas's cart, printed: subtotal, discount, tax, total |
| `shop/pyproject.toml`, `shop/uv.lock`, `shop/.python-version` | The uv project: no dependencies, with `pytest` and `pytest-cov` as dev tools |
| `shop/.github/workflows/tests.yml` | The build-server file from the end of the video (text only, you do not run it here) |
| `stages/` | A snapshot of the code after every red or green step in the video (18 small folders, `a-` to `r-`) |

All prices, coupon codes and names are demo values. The cart lives only in memory.

## Run it

Lukas has one Python course at 1500 rupees and two SQL courses at 500 each, and uses the coupon SAVE10:

```bash
cd shop
uv run python demo.py
```

```text
subtotal   2500
discount    250
tax         405
total      2655
```

Run all the tests, and then the strict command used by a build server:

```bash
uv run pytest -q
uv run pytest -q --cov=cart --cov-branch --cov-report=term-missing --cov-fail-under=100
```

```text
...............................                                          [100%]
31 passed in 0.04s
```

```text
Name      Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------
cart.py      54      0     14      0   100%
-----------------------------------------------------
TOTAL        54      0     14      0   100%
Required test coverage of 100% reached. Total coverage: 100.00%
31 passed in 0.10s
```

(Test times will differ on your machine.)

## Build it step by step

The plan: the cart holds items (a price and a quantity from 1 to 10 each), accepts one coupon (percent off, or flat amount off), adds GST at 18 percent, and counts only in whole rupees. Four rules agreed with finance: (1) the discount comes first, and GST is charged on what is left; (2) a percent discount rounds down, but tax rounds half up; (3) a coupon never takes off more than the cart is worth; (4) a flat coupon can ask for a minimum cart.

To follow a step, open the matching folder in `stages/`, read its `test_cart.py` and `cart.py`, and run `python -m pytest -q` inside that folder (pytest must be installed; the folder `stages/` has its own `pytest.ini`, so the folders do not mix with `shop/`). A "red" folder holds the new test and the old code, so you see the failure. If you prefer to type the code yourself, start an empty `cart.py` and `test_cart.py` in a scratch folder and add the code from each step in order.

### Step 1: the first items (add and subtotal)

1. `stages/a-red-empty-cart`: a new cart has subtotal zero. There is no `cart.py` yet:

```text
E   ModuleNotFoundError: No module named 'cart'
ERROR test_cart.py
1 error in 0.41s
```

This counts as red. The error message tells you what is missing.

2. `stages/b-green-empty-cart`: the simplest code, a `Cart` whose `subtotal` returns 0 (it looks like cheating, on purpose). `1 passed`.
3. `stages/c-red-add`: adding a Python course at 1500 makes the subtotal 1500.

```text
E   AttributeError: 'Cart' object has no attribute 'add'
1 failed, 1 passed in 0.08s
```

4. `stages/d-green-add`: an `items` dictionary, an `add` method, and a `subtotal` that adds up price times quantity with a generator expression. `2 passed`.
5. `stages/e-red-same-item-twice`: two more tests, quantity and adding the same course twice. Three pass at once, one fails, because the second `add` replaced the first:

```text
E   assert 500 == 1000
1 failed, 3 passed
```

6. `stages/f-green-same-item-twice`: store the old quantity plus the new one. `4 passed`.

### Step 2: guard rails

The cart raises its own errors: bad quantity (0, -1, 11), bad price (0, negative, 99.5), going over 10 in total, and removing an item that is not in the cart. The tests use `pytest.raises` and `parametrize` with `ids`.

7. `stages/g-red-error-names-missing`: the tests import `InvalidPrice`, which does not exist yet.

```text
E   ImportError: cannot import name 'InvalidPrice' from 'cart' (...)
1 error in 0.18s
```

8. `stages/h-red-errors-not-raised`: only the names, a `CartError` parent and three children. Now the red we want:

```text
9 failed, 4 passed
FAILED test_cart.py::test_bad_quantity_is_refused[zero] - Failed: DID NOT RAISE InvalidQuantity
...
```

9. `stages/i-green-guard-rails`: the real checks in `add`, and `remove` raising `UnknownItem` with the item name. `13 passed`.
10. `stages/j-refactor-fixtures`: refactor the tests. A `cart` fixture in `conftest.py` replaces `cart = Cart()` in every test, and a second fixture `full_cart` is Lukas's cart. Still `13 passed`. The same count means the refactor is safe.

### Step 3: coupons

11. `stages/k-red-percent-coupons`: SAVE10 on a 2500 cart gives 250 off, 999 rupees rounds down to 99, and no coupon means no discount.

```text
5 failed, 13 passed
```

(Run with `--tb=no` to keep the list short.)

12. `stages/l-green-percent-coupons`: a frozen `Coupon` data class (kind, value, minimum), a `COUPONS` table, `apply_coupon` and `discount` (`subtotal * value // 100`, floor division rounds down, the finance rule). `18 passed`.
13. `stages/m-red-flat-coupons`: flat coupons and their traps. Three of the four new tests fail:

```text
FAILED test_cart.py::test_flat_coupon_needs_a_minimum_cart - assert 200 == 0
FAILED test_cart.py::test_discount_never_goes_above_the_cart - assert 500 == 300
FAILED test_cart.py::test_unknown_coupon_is_refused - KeyError: 'NOPE'
3 failed, 19 passed
```

Three real bugs, caught before any customer met them.

14. `stages/n-green-flat-coupons`: no coupon or a cart below the minimum gives 0, a flat coupon gives `min(value, subtotal)`, and `apply_coupon` raises `InvalidCoupon` with the code in the message. `22 passed`.

### Step 4: GST

15. `stages/o-red-gst`: tax is 18 percent of what is left after the discount, in whole rupees, half rounds up (2 gives 0, 3 gives 1, 25 gives 5, 100 gives 18, 1000 gives 180), and Lukas's total with SAVE10 is 2655. The obvious first code is `round(amount * 18 / 100)`:

```text
E   assert 4 == 5
FAILED test_cart.py::test_gst_in_whole_rupees[half-up] - assert 4 == 5
1 failed, 27 passed
```

25 rupees at 18 percent is 4.5, and Python's `round` gives 4 (halves go to the even number). The finance rule says up.

16. `stages/p-green-gst`: no floats at all: `(taxable * 18 + 50) // 100`. Adding 50, half of 100, turns the floor into round half up. `28 passed`, and the total is 2655, the same as the first run of `demo.py`.

### Step 5: refactor, coverage and a strict command

17. `stages/q-refactor-line-class`: items were tuples and `p * q` is hard to read, so the cart now stores a small `Line` data class. `add` and `subtotal` change; no test does. `28 passed`. The tests only call public methods, so they survive. Test what the cart does, not how it keeps things inside.

18. Coverage:

```bash
uv run pytest -q --cov=cart --cov-branch --cov-report=term-missing
```

Result: 54 statements, 14 branches, nothing missed, 100 percent. But 100 percent does not mean correct. Make three small mistakes on purpose in `cart.py` (undo each one afterwards):

| Mistake | What you should see |
|---------|---------------------|
| `GST_PERCENT = 17` | `4 failed, 24 passed` |
| `return coupon.value` instead of `return min(coupon.value, subtotal)` | `1 failed, 27 passed` |
| `subtotal < coupon.minimum` changed to `subtotal <= coupon.minimum` | `28 passed`, and coverage still 100 percent |

The third mistake is invisible: every line ran, but no test stood exactly on the edge, a cart of exactly 1000.

19. `stages/r-edge-test` (this is also `shop/`): the missing test, parametrized: 999 gets nothing, exactly 1000 gets 200, 1001 gets 200. With the mistake still in place:

```text
FAILED test_cart.py::test_flat_coupon_minimum_is_inclusive[exactly-the-minimum] - assert 0 == 200
1 failed, 30 passed
```

Undo the mistake: `31 passed`. Run `uv run pytest -v` to list every test by name. Read it like a specification of the cart: empty cart, quantities, errors, coupons, tax, and the edge of the minimum.

20. The build-server command is the strict one from "Run it": quiet mode, coverage, branch coverage, missing lines and `--cov-fail-under=100`. If coverage ever drops below 100, pytest exits with a failure code and the build goes red. `shop/.github/workflows/tests.yml` is the GitHub Actions file that runs it on every push (check out, set up uv, `uv sync`, run the command). It is shown as text only; Module 19 runs CI for real.

## What tests cannot promise

- Coverage tells you a line ran, not that it was checked (the missed edge above).
- If finance gives you a wrong rule, your tests will protect the wrong rule.
- This cart lives in memory only. A real shop saves carts in a database, which needs the middle layer of the pyramid (Module 16).

## Upgrades to try, tests first

A stock limit for each course. Coupons that expire (use a fake clock, as in `m13-l03-mocking`). One coupon per customer. A Hypothesis property: the total is never negative. A receipt that prints each line.

## Common mistakes

- Skipping the red step. Always watch the new test fail first, so you know it can fail.
- Running a stage folder from inside `shop/` or without `pytest.ini` nearby, so the wrong `cart.py` is imported. Run each stage from its own folder under `stages/`.
- Using `round()` for money. It rounds half to the even number. Use integer maths.
- Using floats for rupees. Keep whole numbers.

## Clean up

Delete the `.venv` folder (if you made one), and any `__pycache__`, `.pytest_cache`, `.coverage` and `.hypothesis` files and folders that the runs created. Nothing else was created.

## Next

[M14-L01 · Clean Code, Ruff and pre-commit](../../m14-code-quality-logging-and-debugging/m14-l01-clean-code-ruff-and-pre-commit/)
