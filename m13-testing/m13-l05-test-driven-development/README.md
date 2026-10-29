# M13-L05 · Test-Driven Development

> Video: Module 13, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- Why a test whose answer is pasted from the code can never catch a mistake
- The cycle red, green, refactor, and how small each trip around it should be
- How to build a real function (`slugify`) one tiny test at a time
- The three levels of tests (unit, integration, end to end) and the testing pyramid
- What a flaky test is, why `sleep` and shared data cause them, and how to fix both
- What is worth testing, and three common pitfalls

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not needed.
- You should know pytest basics from `m13-l01-your-first-pytest-tests`, and `tmp_path` and fixtures from `m13-l02-fixtures-and-parametrize`.
- Create a virtual environment and install pytest:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Every stage of the video is its own small folder. `cd` into a folder, run `python -m pytest`, then go back with `cd ..`.

## Files in this folder

| Folder | What it is |
|--------|------------|
| `hook/` | The opening bug: `slug.py`, `hook_old.py`, `hook_fix.py`, and the two tests `test_after.py` (answer pasted from the code) and `test_first.py` (answer a human wants) |
| `step1-red/`, `step1-green/` | Trip 1: lower case |
| `step2-red/`, `step2-green/` | Trip 2: spaces become dashes |
| `step3-red/`, `step3-green/` | Trip 3: punctuation is dropped |
| `step4-red/`, `step4-green/` | Trip 4: extra spaces collapse |
| `step5-refactor/` | The refactor: anything that is not a letter or digit counts as a space |
| `step6-red/`, `step6-green/` | Trip 5: a title with no letters is an error (the final `slug.py`) |
| `pyramid/` | One unit, one integration and one end-to-end test (`test_levels.py`, with `pages.py` and `site_app.py`) |
| `flaky-sleep/`, `flaky-fixed/` | A flaky test that sleeps and hopes, and the fix with `join()` |
| `order-shared-list/`, `order-fixed/` | A flaky test that depends on another test, and the fix |
| `pitfall-inside-before/`, `pitfall-inside-after/` | A test of a private helper, before and after a harmless refactor |
| `pitfall-no-assert/` | A test with no `assert` that passes on broken code |
| `requirements.txt` | pytest 9.1.1 |

"Red" folders hold the new test and the old code, so the test fails. "Green" folders hold the code that makes it pass.

## Follow along

### 1. The bug, and the pasted answer

```bash
cd hook
python hook_old.py
python hook_fix.py
```

```text
c++-basics!
c---basics-
```

The old function leaves a plus sign and an exclamation mark in a web address. The rewrite (every character that is not a letter or a digit becomes a dash, using `isalnum`) gives `c---basics-`. Asha copies that into a test (`test_after.py`):

```bash
python -m pytest -q test_after.py
```

```text
.                                                                        [100%]
1 passed in 0.72s
```

It passes, and the code is wrong. The test agrees with the code because the answer came from the code. Now the test with the answer a human wants, `c-basics` (`test_first.py`):

```bash
python -m pytest -q test_first.py
```

```text
E       AssertionError: assert 'c---basics-' == 'c-basics'
E         - c-basics
E         + c---basics-
1 failed in 0.80s
```

It fails, which is good: now we know this test can fail. (Times throughout this README will differ on your machine.)

### 2. The cycle: red, green, refactor

- Red: write one small test for something the code cannot do yet. Run it. It must fail.
- Green: write the smallest, simplest code that makes it pass. Not the best, just enough.
- Refactor: change how the code is written without changing what it does. The tests stay green the whole time.

Then start again with the next small test. One trip takes a minute or two.

### 3. Trip 1: lower case

`step1-red/slug.py` holds only a comment, and `test_slug.py` says `slugify("Python") == "python"`.

```bash
cd ../step1-red
python -m pytest -q
```

```text
E   ImportError: cannot import name 'slugify' from 'slug' (.../step1-red/slug.py)
```

(The path in your message is your own.) That is red too: the function does not exist yet. In `step1-green/` the code is two lines, `return title.lower()`.

```bash
cd ../step1-green
python -m pytest -q
```

```text
1 passed in 0.59s
```

### 4. Trip 2: spaces become dashes

In `step2-red/` the test `slugify("Learn Go") == "learn-go"` is new, the code is not:

```bash
cd ../step2-red
python -m pytest -q
```

```text
E       AssertionError: assert 'learn go' == 'learn-go'
FAILED test_slug.py::test_spaces_become_dashes - AssertionError: assert 'lear...
1 failed, 1 passed in 0.61s
```

`step2-green/slug.py` adds `.replace(" ", "-")`:

```bash
cd ../step2-green
python -m pytest -q
```

```text
2 passed in 0.55s
```

### 5. Trip 3: the punctuation bug from the hook

`step3-red/` adds `slugify("C++ Basics!") == "c-basics"`:

```bash
cd ../step3-red
python -m pytest -q
```

```text
E       AssertionError: assert 'c++-basics!' == 'c-basics'
1 failed, 2 passed in 0.66s
```

`step3-green/slug.py` loops over the two marks we know (`"+!"`) and removes each:

```bash
cd ../step3-green
python -m pytest -q
```

```text
3 passed in 0.61s
```

### 6. Trip 4: untidy spaces

`step4-red/` adds `slugify(" Learn  Go ") == "learn-go"`:

```bash
cd ../step4-red
python -m pytest -q
```

```text
E       AssertionError: assert '-learn--go-' == 'learn-go'
1 failed, 3 passed in 0.65s
```

`step4-green/` uses split and join: `"-".join(slug.split())`.

```bash
cd ../step4-green
python -m pytest -q
```

```text
4 passed in 0.51s
```

### 7. Refactor with the tests as a safety net

The loop lists only the marks we happened to think of. `step5-refactor/slug.py` uses a better rule: anything that is not a letter or digit counts as a space.

```python
def slugify(title):
    title = title.lower()
    chars = [c if c.isalnum() else " " for c in title]
    words = "".join(chars).split()
    return "-".join(words)
```

```bash
cd ../step5-refactor
python -m pytest -q
```

```text
4 passed in 0.51s
```

The whole inside changed, and not one test did. A test says what the function does, not how.

### 8. Trip 5: a title with no letters is an error

What should `slugify("!!!")` do? We decide: it is an error. `step6-red/` has the test, using `pytest.raises(ValueError)`:

```bash
cd ../step6-red
python -m pytest -q
```

```text
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE ValueError
1 failed, 4 passed in 0.57s
```

`step6-green/slug.py` raises `ValueError("no letters or digits")` when there are no words:

```bash
cd ../step6-green
python -m pytest -v
```

```text
test_slug.py::test_lowercase PASSED
test_slug.py::test_spaces_become_dashes PASSED
test_slug.py::test_punctuation_is_dropped PASSED
test_slug.py::test_extra_spaces_collapse PASSED
test_slug.py::test_no_letters_is_an_error PASSED
============================== 5 passed in 0.56s ===============================
```

Read the names like a manual: the tests were the description of the function from the start.

### 9. Three levels of tests: the pyramid

`pyramid/test_levels.py` has a unit test (`slugify` alone), an integration test (saves a page into `tmp_path`, checks the file is named by the slug) and an end-to-end test (a tiny web server in a fixture with `yield`, asked over HTTP on port 8135).

```bash
cd ../pyramid
python -m pytest -v --durations=3
```

```text
test_levels.py::test_unit_slug PASSED                                    [ 33%]
test_levels.py::test_integration_page_file PASSED                        [ 66%]
test_levels.py::test_end_to_end_over_http PASSED                         [100%]

============================== slowest 3 durations ==============================
0.03s call     test_levels.py::test_end_to_end_over_http
0.01s teardown test_levels.py::test_end_to_end_over_http
0.01s setup    test_levels.py::test_integration_page_file
============================== 3 passed in 0.66s ===============================
```

The end-to-end test is the slowest. Here everything is tiny; in a real project it takes seconds. So: many unit tests at the bottom, fewer integration tests, very few end-to-end tests at the top.

### 10. Flaky test 1: sleep and hope

`flaky-sleep/` has a `Report` that builds on a thread for 0.01 to 0.1 seconds. The test starts it, sleeps 0.05 seconds, and asserts it is ready.

```bash
cd ../flaky-sleep
python -m pytest -q
```

It may pass. Now run it ten times:

```bash
for i in 1 2 3 4 5 6 7 8 9 10; do python -m pytest -q | tail -1; done
```

A real run here gave a mix such as:

```text
1 failed in 0.73s
1 passed in 1.09s
1 failed in 1.09s
...
```

Yours will differ: the number of failures varies from run to run (8 of 10 failed in the video). Same code, same test. (On Windows PowerShell use `1..10 | % { python -m pytest -q }`.)

The fix in `flaky-fixed/`: `start()` returns the thread, and the test calls `worker.join()` to wait for the thing itself.

```bash
cd ../flaky-fixed
for i in 1 2 3 4 5 6 7 8 9 10; do python -m pytest -q | tail -1; done
```

```text
1 passed in 0.69s
1 passed in 0.64s
...
```

Ten passes out of ten.

### 11. Flaky test 2: tests that depend on each other

`order-shared-list/` has a list outside the functions. The second test only passes because the first one ran before it.

```bash
cd ../order-shared-list
python -m pytest -q
python -m pytest test_users.py::test_one_user_signed_up
```

```text
2 passed in 0.68s
```

```text
E       assert 0 == 1
E        +  where 0 = len([])
1 failed in 1.04s
```

`order-fixed/` makes every test build its own data:

```bash
cd ../order-fixed
python -m pytest -q
python -m pytest test_users.py::test_one_user_signed_up -q
```

```text
2 passed in 0.75s
1 passed in 0.73s
```

Other usual suspects: the clock, random numbers, the network, and files left over by an earlier run. Fake them as in `m13-l03-mocking`. Never just rerun a flaky test until it turns green.

### 12. What is worth testing

- Worth it: your business rules, the edges (empty, one, many, smallest, biggest), errors and wrong input, and every bug you ever fixed (write the failing test first).
- Not worth it: Python and library code itself, tiny code with no decision in it, and the inside details of your function.

## Common mistakes

- Testing the inside. In `pitfall-inside-before/` both tests pass. In `pitfall-inside-after/` the helper `_fix` has been merged into `slugify` (a harmless refactor): the real test stays green, the helper test goes red.

```bash
cd ../pitfall-inside-after
python -m pytest -q
```

```text
E       AttributeError: module 'slug' has no attribute '_fix'
FAILED test_slug.py::test_fix_helper - AttributeError: module 'slug' has no a...
1 failed, 1 passed in 1.01s
```

- Writing the tests after the code and pasting the answer. In TDD you always see a test fail first, so you know it can.
- A test with no `assert`. In `pitfall-no-assert/`, `slugify` returns `"oops"`, yet:

```bash
cd ../pitfall-no-assert
python -m pytest -q
```

```text
1 passed in 1.01s
```

- Steps that are too big (twenty tests first, then all the code). Take a smaller step: one test, one behaviour. TDD is also not for everything: when you are exploring an idea or shaping a screen, write the code first.

## Clean up

Delete `__pycache__` and `.pytest_cache` folders, and the `.venv` folder when you are done. The end-to-end test starts its server on port 8135 and shuts it down itself.

## Next

[M13-B07 · Build a Shopping Cart with TDD](../m13-b07-build-a-shopping-cart-with-tdd/)
