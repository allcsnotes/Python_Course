# M13-L04 · Coverage and Property-Based Testing

> Video: Module 13, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- How to measure which lines of your program the tests never run, with `pytest-cov`
- How to read the report: Stmts, Miss, Cover and Missing
- Why branch coverage (`--cov-branch`) is stricter than line coverage
- Why 100 percent coverage does not prove the code is right (tests with no `assert`)
- How Hypothesis invents test inputs, finds a real bug, and shrinks it to the simplest example
- How to set a coverage floor with `--cov-fail-under`

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not needed.
- You should know basic pytest from `m13-l01-your-first-pytest-tests`.
- Create a virtual environment and install the pinned packages (the video uses `uv add --dev pytest-cov`, `pip` works too):

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Each step below has its own small folder, so `cd` into it before running its commands.

## Files in this folder

| File | What it is |
|------|------------|
| `requirements.txt` | pytest 9.1.1, pytest-cov 7.1.0, hypothesis 6.170.9 |
| `step1-start/` | `pricing.py` (the price rules of allcsvideos.com) and Asha's first three tests |
| `step2-coupons/` | Adds `test_coupons.py`: the flat 100 coupon and the unknown code |
| `step3-branches/` | Adds the "bundle of one" test, so every branch is covered |
| `lazy-tests/` | A deliberately broken `pricing.py` (`+` instead of `-`) and a test with no `assert` |
| `props-list/` | First Hypothesis test: reversing a list twice (`test_props1.py` prints the lists, `test_props1q.py` is the quiet version) |
| `props-pricing/` | The property "price is never negative": `test_props2.py` fails, `test_props2v.py` is the verbose version |
| `props-fixed/` | `pricing.py` with the `max(0, ...)` fix, and `test_props.py` with `@example` |
| `props-copy/` | A bad property that copies the code, and still passes |

All prices and coupon codes are demo values.

## Follow along

### 1. Three green tests, but how much ran?

`step1-start/pricing.py`:

```python
def final_price(price: int, coupon: str) -> int:
    """Price in whole rupees after a coupon code."""
    if coupon == "":
        return price
    if coupon == "HALF":
        return price // 2
    if coupon == "FLAT100":
        return price - 100
    raise ValueError(f"unknown coupon: {coupon}")


def bundle_total(price: int, quantity: int) -> int:
    """Buy three or more courses and get ten percent off."""
    total = price * quantity
    if quantity >= 3:
        total = total - total // 10
    return total
```

```bash
cd step1-start
python -m pytest
```

```text
test_pricing.py ...                                                      [100%]

============================== 3 passed in 0.06s ===============================
```

Priya asks: how much of `pricing.py` did these tests run?

### 2. Measure coverage

```bash
python -m pytest --cov=pricing --cov-report=term-missing
```

```text
Name         Stmts   Miss  Cover   Missing
------------------------------------------
pricing.py      13      3    77%   7-9
------------------------------------------
TOTAL           13      3    77%
============================== 3 passed in 0.06s ===============================
```

(Your times will differ. Lines above the table are the usual pytest header.)

- `--cov=pricing` means: measure the module called `pricing`.
- `--cov-report=term-missing` prints the table in the terminal with a Missing column.
- Name is the measured file. Stmts is how many statements can run (13). Miss is how many never ran (3). Cover is the share that ran (10 of 13, 77 percent). Missing lists the line numbers: 7 to 9, the flat 100 coupon and the error for an unknown code.

### 3. Write the missing tests

```bash
cd ../step2-coupons
python -m pytest --cov=pricing --cov-report=term-missing
```

`test_coupons.py` has the flat 100 test (500 becomes 400) and an unknown-code test that uses `pytest.raises(ValueError)`. The result is zero missed lines, 100 percent.

For a web page report, add `--cov-report=html` and open `htmlcov/index.html`. Lines that never ran are painted red.

### 4. Branch coverage

An `if` has two roads out: yes and no. Line coverage only knows whether the lines ran. Add `--cov-branch`:

```bash
python -m pytest --cov=pricing --cov-report=term-missing --cov-branch
```

```text
Name         Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------
pricing.py      13      0      8      1    95%   15->17
--------------------------------------------------------
TOTAL           13      0      8      1    95%
============================== 5 passed in 0.06s ===============================
```

There are 8 roads, 1 is partly covered (BrPart), and `15->17` means: from line 15 the road to line 17 was never taken (the "fewer than three courses" case). Add a test for it (`test_bundle_of_one`, already in `step3-branches/`):

```bash
cd ../step3-branches
python -m pytest --cov=pricing --cov-report=term-missing --cov-branch
```

```text
Name         Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------
pricing.py      13      0      8      0   100%
--------------------------------------------------------
TOTAL           13      0      8      0   100%
============================== 6 passed in 0.07s ===============================
```

From now on, always add `--cov-branch`.

### 5. 100 percent is not proof

In `lazy-tests/`, `pricing.py` has been broken on purpose (line 8 is `price + 100`), and `test_lazy.py` calls `final_price(500, "FLAT100")` without any `assert`:

```bash
cd ../lazy-tests
python -m pytest --cov=pricing --cov-report=term-missing --cov-branch
```

```text
Name         Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------
pricing.py      13      0      8      0   100%
--------------------------------------------------------
TOTAL           13      0      8      0   100%
============================== 6 passed in 0.07s ===============================
```

Six passed, 100 percent, and the price code is wrong. Coverage tells you where the tests have been, never what they checked. The honest test from `step3-branches/test_coupons.py` would fail here.

### 6. Hypothesis: your first property

A property is a rule that holds for every input. `props-list/test_props1.py`:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_reversing_twice(items):
    print(items)
    assert items[::-1][::-1] == items
```

```bash
cd ../props-list
python -m pytest -s -q test_props1.py
```

You should see lists such as these (yours will differ, Hypothesis chooses them):

```text
[]
[0]
[-583325]
[-20655585952882028]
[-20655585952882028, -88187050715]
```

Hypothesis loves awkward values: empty, zero, negative, enormous. To see its statistics, run the quiet version:

```bash
python -m pytest --hypothesis-show-statistics test_props1q.py
```

```text
  - during generate phase (0.10 seconds):
    - Typical runtimes: ~ 0-1 ms, of which < 1ms in data generation
    - 100 passing, 0 failing, and 14 invalid test cases

  - Stopped because settings.max_examples=100
```

By default Hypothesis makes 100 inputs. "Invalid" cases are inputs it made and threw away itself; ignore them. The count (14 here, 16 in the video) varies.

### 7. A property that finds a real bug

`props-pricing/test_props2.py`: whatever the price and coupon, the final price is never negative and never more than the price.

```python
@given(
    st.integers(min_value=0, max_value=100_000),
    st.sampled_from(["", "HALF", "FLAT100"]),
)
def test_price_never_negative(price, coupon):
    assert 0 <= final_price(price, coupon) <= price
```

```bash
cd ../props-pricing
python -m pytest test_props2.py
```

```text
E       AssertionError: assert 0 <= -100
E        +  where -100 = final_price(0, 'FLAT100')
E       Failing test case: test_price_never_negative(
E           price=0,
E           coupon='FLAT100',
E       )

FAILED test_props2.py::test_price_never_negative - AssertionError: assert 0 <...
```

Even with 100 percent coverage, a free course with the flat 100 coupon would pay the customer 100 rupees. Hypothesis names the input.

### 8. Shrinking (verbose run)

```bash
python -m pytest -q -s test_props2v.py
```

The verbose version prints every test case. Hypothesis does not start at price 0: on a typical run you see several inputs pass, then a failure such as `price=99, coupon='FLAT100'` (99 minus 100 is minus 1). Then it shrinks: it tries smaller and simpler inputs while the test still fails, and stops at the simplest one, `price=0`. The exact inputs differ from run to run.

### 9. Fix it and keep the lesson

`props-fixed/pricing.py` wraps the sum in `max`: `return max(0, price - 100)`. `props-fixed/test_props.py` also adds `@example(price=0, coupon="FLAT100")`, so that input is always tried (Hypothesis also remembers failures in a hidden `.hypothesis` folder).

```bash
cd ../props-fixed
python -m pytest -v
```

```text
test_props.py::test_price_never_negative PASSED                          [100%]

============================== 1 passed in 0.10s ===============================
```

Add `--hypothesis-show-statistics` to see `100 passing, 0 failing`.

### 10. A coverage floor

Back in `step1-start`, set a minimum so the number cannot quietly fall:

```bash
cd ../step1-start
python -m pytest --cov=pricing --cov-fail-under=90
```

```text
FAIL Required test coverage of 90% not reached. Total coverage: 76.92%
============================== 3 passed in 0.06s ===============================
```

The three tests still pass, but the whole command fails (exit code 1). A build server uses this to stop a bad change.

## Common mistakes

- A typo after `--cov=`. With `--cov=prising` pytest passes, the table is gone, and you get a warning "Module prising was never imported" and "No data was collected". The name must be the module or folder you want to measure. (Try it in `step3-branches/`.)
- Chasing 100 percent. Teams soon write tests like the lazy one. Read the asserts, not only the number.
- A property that copies the code. `props-copy/test_copy.py` asserts `final_price(price, "FLAT100") == price - 100`, which is the very line with the bug, so it passes on the broken code:

```bash
cd ../props-copy
python -m pytest
```

```text
test_copy.py .                                                           [100%]
============================== 1 passed in 0.09s ===============================
```

A good property states a rule from the outside, like "never negative".

## Clean up

Delete the `.hypothesis`, `htmlcov`, `.pytest_cache` and `__pycache__` folders and any `.coverage` files that the runs created, and the `.venv` folder when you are done.

## Next

[M13-L05 · Test-Driven Development](../m13-l05-test-driven-development/)
