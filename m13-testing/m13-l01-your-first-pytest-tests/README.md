# M13-L01 · Your First pytest Tests

> Video: Module 13, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why a one-character bug in the allcsvideos.com link checker slips through, and how a test catches it in a second
- How to add pytest as a dev dependency and run it
- The two naming rules pytest uses to find tests: files and functions that start with `test_`
- How to read pytest output: dots, `F`, the `E` lines, and the short summary
- Arrange, act, assert, and how to check that code raises the right error with `pytest.raises`
- How to run all tests, one test, or tests matching a word, and four mistakes that make tests silently useless

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker is not needed.
- Asha's link checker comes from the end of Module 12 ("Concurrency"). This folder already contains the function you need (`linkrules.py`), so no earlier folder is required.
- The video uses `uv` (Module 7). The commands below show `uv`. If you do not have `uv`, create a virtual environment and use `pip install pytest` instead, then drop the words `uv run` from every command.

## Files in this folder

| File | What it is |
|------|------------|
| `pyproject.toml` | The project file, with `pytest` in the `dev` dependency group |
| `linkrules.py` | The code under test: `is_broken`, `broken_only` and `describe` |
| `test_linkrules.py` | Three tests for `is_broken` (404, 200 and the edge 400) |
| `test_broken_only.py` | One arrange, act, assert test for `broken_only` |
| `test_describe.py` | Three tests for `describe`, including `pytest.raises` with `match=` |
| `hook/hook_before.py`, `hook/hook_after.py` | The opening example: a status report before and after the one-character change |
| `bug/linkrules_bug.py` | `linkrules.py` with `>=` changed to `>` (the bug), to watch the tests fail |
| `bug/describe_no_raises.py` | A test that calls `describe(999)` without `pytest.raises` (fails, on purpose) |
| `bug/describe_raises_only.py` | The same test with `pytest.raises(ValueError)` |
| `bug/describe_did_not_raise.py` | A test that expects an error from a normal status (fails with DID NOT RAISE) |
| `pitfalls/` | The three file-based mistakes: wrong file name, wrong function name, missing `assert` |

Everything runs from this folder. The statuses (200, 404, 500 and so on) are demo numbers. Nothing touches the internet.

## Follow along

### 1. The hook: a bug that raises no error

```bash
python hook/hook_before.py
python hook/hook_after.py
```

You should see:

```text
3 of 5 links are broken
2 of 5 links are broken
```

`hook_before.py` says a link is broken when `status >= 400`. `hook_after.py` has `status > 400`: one character less. Nothing crashes, but a 400 (bad request) is now called fine. Nobody sees it until a user does.

### 2. Install pytest as a dev dependency

In a new project the video runs:

```bash
uv add --dev pytest
```

```text
Resolved 7 packages in 5ms
Installed 5 packages in 13ms
 + iniconfig==2.3.1
 + packaging==26.3
 + pluggy==1.7.0
 + pygments==2.21.0
 + pytest==9.1.1
```

(The first time, `uv` also prints "Creating virtual environment at: .venv".) This folder already has the result, so here you only need:

```bash
uv sync
```

The project file got a new group. `dev` means: needed while we build the project, not when users run it.

```toml
[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
```

Put `uv run` in front so the command uses the project's own environment:

```bash
uv run pytest --version
```

```text
pytest 9.1.1
```

Without `uv`: `python -m venv .venv`, activate it, `pip install pytest==9.1.1`, then `pytest --version`.

### 3. The two naming rules

pytest finds tests without any list, using only names:

1. A test file name starts with `test_` (for example `test_linkrules.py`).
2. A test function name starts with `test_` too.

### 4. The first test

`test_linkrules.py` starts with one test:

```python
from linkrules import is_broken


def test_404_is_broken():
    assert is_broken(404)
```

`assert` is the check from Module 6: nothing happens if it is true, and the test fails if it is false. To see exactly one test, comment out the other two in the file, or just read on. The one-test run looks like this:

```text
=================== test session starts ====================
platform linux -- Python 3.14.9, pytest-9.1.1, pluggy-1.7.0
rootdir: /home/learner/allcs-checker
configfile: pyproject.toml
collected 1 item

test_linkrules.py .                                  [100%]

==================== 1 passed in 0.02s =====================
```

Read it from the top. The header has the operating system, Python version, pytest version and the root folder (skip it for now). `collected 1 item` means pytest found one test. A dot is one passing test. The last line says `1 passed`.

### 5. Three tests in one file

The file in this folder has all three tests: 404 is broken, 200 is fine (written with `not`), and 400 is broken. The edge, where the rule changes from fine to broken, is where bugs hide, so it gets its own test.

```bash
uv run pytest test_linkrules.py
```

```text
=================== test session starts ====================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: /path/to/m13-l01-your-first-pytest-tests
configfile: pyproject.toml
collected 3 items

test_linkrules.py ...                                [100%]

==================== 3 passed in 0.01s =====================
```

Three dots, three passed. Your platform, Python version, path and timing will differ.

### 6. Bring the bug back and watch a test fail

Make backups of the two good files, then copy the buggy version over the good one:

```bash
cp linkrules.py linkrules.good
cp test_describe.py test_describe.good
cp bug/linkrules_bug.py linkrules.py
uv run pytest test_linkrules.py
```

You should see two dots and a capital `F`:

```text
test_linkrules.py ..F                                [100%]

========================= FAILURES =========================
____________________ test_400_is_broken ____________________

    def test_400_is_broken():
>       assert is_broken(400)
E       assert False
E        +  where False = is_broken(400)

test_linkrules.py:13: AssertionError
================= short test summary info ==================
FAILED test_linkrules.py::test_400_is_broken - assert False
=============== 1 failed, 2 passed in 0.02s ================
```

How to read it:

- The line of underscores names the failing test.
- The `>` marks the exact line that failed.
- Lines starting with `E` (for error) show the real values: the function was called with `400` and returned `False`. You wrote no message and no `print`. pytest took your `assert` apart and showed what was inside.
- The last lines give `FAILED`, the file name, two colons and the test name. That is easy to copy when you want to run only that test.

Tests are different from the `assert` of Module 6: `python -O` switches asserts off, so real input checks must not use `assert`. Nobody ships tests to users, and pytest even rewrites each `assert` so it can show you the values.

Restore the good code:

```bash
cp linkrules.good linkrules.py
uv run pytest test_linkrules.py
```

You should see `3 passed` again.

### 7. Arrange, act, assert

`test_broken_only.py` shows the shape of every good test:

```python
from linkrules import broken_only


def test_keeps_the_bad_ones():
    statuses = [200, 301, 404, 500, 400]
    result = broken_only(statuses)
    assert result == [404, 500, 400]
```

- Arrange: prepare what the test needs (a list of five statuses).
- Act: do the one thing you are testing (call `broken_only`).
- Assert: say what must be true.

With the bug in the code, comparing two lists gives a very clear failure:

```bash
cp bug/linkrules_bug.py linkrules.py
uv run pytest test_broken_only.py
```

```text
test_broken_only.py F                                [100%]

========================= FAILURES =========================
_________________ test_keeps_the_bad_ones __________________

    def test_keeps_the_bad_ones():
        statuses = [200, 301, 404, 500, 400]
        result = broken_only(statuses)
>       assert result == [404, 500, 400]
E       assert [404, 500] == [404, 500, 400]
E         
E         Right contains one more item: 400
E         Use -v to get more diff

test_broken_only.py:7: AssertionError
================= short test summary info ==================
FAILED test_broken_only.py::test_keeps_the_bad_ones - ass...
==================== 1 failed in 0.01s =====================
```

Left is the real result (two items), right is what you expected (three). Add `-v` for the full diff. Fix the code again with `cp linkrules.good linkrules.py`.

Habit: a test name should say what must be true (`test_keeps_the_bad_ones`), and one test checks one idea. If it checks five things, a failure does not tell you which one broke.

### 8. Testing that an error is raised

`describe(status)` says "broken" or "fine", but raises `ValueError` for a status outside 100 to 599. A first try that just calls it (file `bug/describe_no_raises.py`):

```bash
cp bug/describe_no_raises.py test_describe.py
uv run pytest test_describe.py
```

```text
test_describe.py ..F                                 [100%]

========================= FAILURES =========================
____________________ test_describe_999 _____________________

    def test_describe_999():
>       describe(999)

test_describe.py:13: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

status = 999

    def describe(status):
        if status < 100 or status > 599:
>           raise ValueError(f"not a real status: {status}")
E           ValueError: not a real status: 999

linkrules.py:11: ValueError
================= short test summary info ==================
FAILED test_describe.py::test_describe_999 - ValueError: ...
=============== 1 failed, 2 passed in 0.01s =====================
```

The error escaped and crashed the test. But the error is exactly what we want, so the test is wrong, not the code. Use `pytest.raises`:

```bash
cp bug/describe_raises_only.py test_describe.py
uv run pytest test_describe.py
```

```text
test_describe.py ...                                 [100%]

==================== 3 passed in 0.01s =====================
```

The key lines:

```python
def test_describe_999():
    with pytest.raises(ValueError):
        describe(999)
```

`with ... :` means "I expect this block to raise a `ValueError`". If it does, the test passes. If the block finishes quietly, or raises another kind of error, the test fails.

You can check the message too, with `match=`, which tests that a piece of text appears in the error message. This is the final `test_describe.py` in the folder:

```python
def test_describe_999_names_the_status():
    with pytest.raises(ValueError, match="999"):
        describe(999)
```

The other direction: a normal status raises nothing, so a test that expects an error fails:

```bash
cp bug/describe_did_not_raise.py test_describe.py
uv run pytest test_describe.py
```

```text
test_describe.py F                                   [100%]

========================= FAILURES =========================
_________________ test_describe_404_raises _________________

    def test_describe_404_raises():
>       with pytest.raises(ValueError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError

test_describe.py:6: Failed
================= short test summary info ==================
FAILED test_describe.py::test_describe_404_raises - Faile...
==================== 1 failed in 0.01s =====================
```

A test for an error fails when the error is missing, and that is the point.

Step 8 overwrites `test_describe.py`, and step 7 and 8 overwrite `linkrules.py`. Put the good files back before the next step:

```bash
cp linkrules.good linkrules.py
cp test_describe.good test_describe.py
```

### 9. Run the whole project, one test, or a word

With the good files in place:

```bash
uv run pytest
```

```text
collected 7 items

test_broken_only.py .                                [ 14%]
test_describe.py ...                                 [ 57%]
test_linkrules.py ...                                [100%]

==================== 7 passed in 0.01s =====================
```

Add `-v` (verbose) to get one line per test:

```bash
uv run pytest -v
```

```text
test_broken_only.py::test_keeps_the_bad_ones PASSED  [ 14%]
test_describe.py::test_describe_404 PASSED           [ 28%]
test_describe.py::test_describe_200 PASSED           [ 42%]
test_describe.py::test_describe_999_names_the_status PASSED [ 57%]
test_linkrules.py::test_404_is_broken PASSED         [ 71%]
test_linkrules.py::test_200_is_fine PASSED           [ 85%]
test_linkrules.py::test_400_is_broken PASSED         [100%]
```

Run just one test: file name, two colons, test name.

```bash
uv run pytest test_linkrules.py::test_400_is_broken -v
```

```text
collected 1 item

test_linkrules.py::test_400_is_broken PASSED         [100%]

==================== 1 passed in 0.01s =====================
```

Or run every test whose name contains a word, with `-k`:

```bash
uv run pytest -k describe -v
```

```text
collected 7 items / 4 deselected / 3 selected

test_describe.py::test_describe_404 PASSED           [ 33%]
test_describe.py::test_describe_200 PASSED           [ 66%]
test_describe.py::test_describe_999_names_the_status PASSED [100%]

============= 3 passed, 4 deselected in 0.01s ==============
```

## Common mistakes

Each one comes from the `pitfalls/` folder. Start from a project that has only `linkrules.py` (and move the other `test_*.py` files away while you try them).

1. Wrong file name. A file called `linkrules_tests.py` ends with `tests` instead of starting with `test_`:

   ```bash
   cp pitfalls/linkrules_tests.py .
   uv run pytest
   ```

   ```text
   collected 0 items

   ================== no tests ran in 0.01s ===================
   ```

   No error, just nothing.

2. Wrong function name. In `pitfalls/wrong_function_name.py` the second function is `check_500_is_broken`, not `test_...`. pytest ignores it. Two tests written, one dot:

   ```bash
   cp pitfalls/wrong_function_name.py test_linkrules.py
   uv run pytest
   ```

   ```text
   test_linkrules.py .                                  [100%]

   ==================== 1 passed in 0.02s =====================
   ```

   Always compare the number of dots with the number of tests you wrote.

3. Forgetting `assert`. `pitfalls/no_assert.py` writes `is_broken(400) == True` without `assert`. With the bug in `linkrules.py` the test still passes:

   ```bash
   cp pitfalls/no_assert.py test_linkrules.py
   cp bug/linkrules_bug.py linkrules.py
   uv run pytest
   ```

   ```text
   test_linkrules.py .                                  [100%]

   ==================== 1 passed in 0.01s =====================
   ```

   A test that cannot fail is worse than no test, because it gives false peace. Always `assert`.

4. Running `pytest` on its own. Outside the project's environment, the terminal says `pytest: command not found`, and `python -m pytest` says `No module named pytest`. The library lives in the project's environment, not in the global Python. Run it with `uv run pytest` (or activate your `.venv` first).

## Clean up

Put the good file back and remove the files you copied and the cache:

```bash
cp linkrules.good linkrules.py
cp test_describe.good test_describe.py
rm -f linkrules.good test_describe.good linkrules_tests.py
rm -rf .pytest_cache __pycache__
```

If you overwrote `test_linkrules.py` with a file from `pitfalls/` (mistakes 2 and 3), restore it by copying the original from this lesson's folder in the repo (it has the three tests from step 5), or run `git checkout test_linkrules.py` if you cloned the repo.

## Next

Your tests look alike and repeat the same setup lines. The next lesson shows how to write setup once with fixtures and one test for many inputs with parametrize: [M13-L02 · Fixtures and Parametrize](../m13-l02-fixtures-and-parametrize/README.md).
