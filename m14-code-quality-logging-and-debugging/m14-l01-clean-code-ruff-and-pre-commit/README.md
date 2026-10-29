# M14-L01 · Clean Code, Ruff and pre-commit

> Video: Module 14, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What makes code easy to read: names, small functions, named constants, comments that say why
- How `ruff check` (the linter) finds problems and `ruff format` (the formatter) tidies the layout
- How to read a ruff report: the place, the rule code, the message
- How to set ruff up in `pyproject.toml` (line length and rule families)
- How `pre-commit` runs the checks before every Git commit, and four pitfalls

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv` installed (the video uses it), and `git`.
- No Docker needed.
- The running project is `allcsvideos` from Module 13. A fresh folder is fine: this lesson only needs a small `billing.py`.

## Files in this folder

| File | What it is |
|------|------------|
| `billing.py` | The messy starting file: `calc(l, c, t, seen)` |
| `test_billing.py` | Three tests for `calc` |
| `steps/billing_1_names.py` | After renaming: `invoice_total`, `items`, `coupon`, `gst_percent` |
| `steps/billing_2_small_functions.py` | After splitting into `basket_subtotal`, `coupon_discount`, `invoice_total` |
| `steps/billing_3_constants_and_comments.py` | After `GST_PERCENT`, a docstring and a "why" comment |
| `steps/billing_4_after_ruff_fix.py` | After `ruff check --fix` and removing `seen` and `unused` by hand |
| `steps/billing_5_final.py` | The finished, formatted, clean file |
| `steps/test_billing_new_names.py` | The tests, using the new function name |
| `pyproject.toml` | Project file with ruff and the rule families `E`, `F`, `N` |
| `.pre-commit-config.yaml` | The pre-commit hooks: `ruff-check` (with `--fix`) and `ruff-format` |
| `demos/report.py` | Priya's new file with problems (used in the pre-commit test) |
| `demos/report_fixed.py` | The same file, as ruff leaves it after the hand fix |
| `demos/noqa_demo_without.py`, `demos/noqa_demo_with.py` | One line with and without `# noqa: E711` |
| `demos/shout.py` | A file for pitfall two (`--no-verify`) |

## Follow along

### 1. Set up a project and look at the messy file

```bash
mkdir allcsvideos && cd allcsvideos
uv init --bare
uv add --dev pytest
cp ../billing.py ../test_billing.py .
```

(Run the `cp` from the folder where you copied this lesson, adjust the path if needed.) Open `billing.py`. The function `calc` has inputs `l`, `c`, `t`, `seen`, and inside it `s`, `d` and `x`. Is `c` a coupon? Is `t` the tax? You have to guess.

Run the tests:

```bash
uv run pytest -q
```

```text
...                              [100%]
3 passed in 0.00s
```

Green. The code works. But tests only check that the answer is right, not that the code is easy to read.

### 2. Part one: names

Rename: `calc` becomes `invoice_total`, `l` becomes `items`, `c` becomes `coupon`, `t` becomes `gst_percent`, `s` becomes `subtotal`, `d` becomes `discount`, `x` becomes `item`. The result is `steps/billing_1_names.py`. In the test file, only the function name changes (`steps/test_billing_new_names.py`). Use the new test file from here on.

```bash
cp steps/billing_1_names.py billing.py
cp steps/test_billing_new_names.py test_billing.py
uv run pytest -q
```

```text
...                              [100%]
3 passed in 0.00s
```

Renaming changed nothing about the behaviour. Four habits for names:

1. Say what it is, not how it is stored: `prices`, not `list2`.
2. No one-letter names, except a tiny throwaway like `i` in a short loop, or `_`. The letter `l` is the worst, it looks like the number one.
3. One word for one idea, everywhere: `coupon`, not `coupon` here, `code` there and `voucher` somewhere else.
4. A yes/no value starts with `is` or `has` (`is_student`). A function name is an action: `add`, `load`, `calculate`.

### 3. Part two: small functions

`invoice_total` does three jobs: adds the prices, works out the discount, adds the tax. Split it (`steps/billing_2_small_functions.py`):

```python
def basket_subtotal(items):
    subtotal = 0
    for _, price, quantity in items:
        subtotal = subtotal + price*quantity
    return subtotal
```

Notice the loop now unpacks each tuple into `price` and `quantity` instead of `item[1]*item[2]`, and uses `_` for the name we do not need. `coupon_discount` holds the coupon rules, and `invoice_total` is left with three lines that tell the story: get the subtotal, take off the discount, add the tax.

```bash
cp steps/billing_2_small_functions.py billing.py
uv run pytest -q
```

```text
...                              [100%]
3 passed in 0.00s
```

After every small step, run the tests: change the shape, never the behaviour. How small is small? If you cannot say what a function does in one sentence without the word "and", it does two jobs. If you must scroll to read it, it is too long.

### 4. Part three: magic numbers and comments

The `18` in the tax line is a magic number. Give it a name at the top of the file (`GST_PERCENT = 18`). Then comments:

```python
# Noise: repeats the code
count = count + 1   # add one to count

# Good: says WHY
# GST is charged on the price after the discount, as the finance team wants.
tax = after_discount*gst_percent/100
```

A docstring (`"""Return the total in rupees: discount first, then GST."""`) is for people who call the function. A comment is for people who read the code. See `steps/billing_3_constants_and_comments.py`.

```bash
cp steps/billing_3_constants_and_comments.py billing.py
uv run pytest -q
```

```text
...                              [100%]
3 passed in 0.00s
```

The function is readable now, but the layout is crowded, quotes are mixed and there is a star import. That is a job for a tool.

### 5. Install ruff

```bash
uv add --dev ruff
uv run ruff --version
```

```text
Resolved 8 packages in 5ms
Installed 1 package in 2ms
 + ruff==0.17.2
ruff 0.17.2
```

Your `pyproject.toml` now lists `ruff` next to `pytest` in the `dev` group. (The video starts the problems from the original `calc` file; if you want exactly the five problems of the video, run the next command on the original `billing.py`.)

### 6. Ruff check: the linter

On the original messy `billing.py` the video shows:

```bash
uv run ruff check --output-format concise billing.py
```

```text
billing.py:1:1: I001 [*] Import block is un-sorted or un-formatted
billing.py:1:8: F401 [*] `os` imported but unused
billing.py:1:12: F401 [*] `sys` imported but unused
billing.py:4:27: B006 Do not use mutable data structures for argument defaults
billing.py:12:5: F841 Local variable `unused` is assigned to but never used
Found 5 errors.
[*] 3 fixable with `--fix` (2 unsafe fixes available with `--fix --unsafe-fixes`).
```

Read one line: `billing.py` line 1, column 8 is the place. `F401` is the rule code (`F` = Pyflakes, leftovers and real mistakes). `[*]` means ruff can fix it. Then the message.

For more detail, pick one rule and drop `--output-format concise`:

```bash
uv run ruff check --select F401 billing.py
uv run ruff rule F401
```

The first shows the line with arrows under the problem and a `help:` line. The second explains what the rule does, why it is bad, and whether the fix is safe. You never have to memorise a code.

Now run it on the file as you have it after step 4 (all five problems are still there, at new line numbers):

```bash
uv run ruff check --output-format concise
```

```text
billing.py:1:1: I001 [*] Import block is un-sorted or un-formatted
billing.py:1:8: F401 [*] `os` imported but unused
billing.py:1:12: F401 [*] `sys` imported but unused
billing.py:18:64: B006 Do not use mutable data structures for argument defaults
billing.py:21:5: F841 Local variable `unused` is assigned to but never used
Found 5 errors.
[*] 3 fixable with `--fix` (2 unsafe fixes available with `--fix --unsafe-fixes`).
```

### 7. Let ruff fix what it safely can

```bash
uv run ruff check --fix --output-format concise
```

```text
billing.py:17:64: B006 Do not use mutable data structures for argument defaults
billing.py:20:5: F841 Local variable `unused` is assigned to but never used
Found 4 errors (2 fixed, 2 remaining).
2 unsafe fixes available with `--fix --unsafe-fixes`.
```

The import line is gone. Two remain, and ruff will not touch them because their fixes are "unsafe": they could change what the program does. A person decides. Nothing uses `seen`, so delete that parameter. Nothing uses `unused`, so delete that line. The result is `steps/billing_4_after_ruff_fix.py`.

```bash
cp steps/billing_4_after_ruff_fix.py billing.py
uv run ruff check
uv run pytest -q
```

```text
All checks passed!
...                              [100%]
3 passed in 0.00s
```

### 8. Ruff format: the formatter

```bash
uv run ruff format --diff billing.py
```

Lines with `-` are removed, lines with `+` are added: two empty lines between functions, spaces around `*`, `+` and `/`, one-line `if` statements split into two lines, single quotes changed to double quotes. None of it changes what the program does. Now do it for real:

```bash
uv run ruff format
uv run ruff format --check
uv run pytest -q
```

```text
1 file reformatted, 2 files left unchanged
3 files already formatted
...                              [100%]
3 passed in 0.00s
```

`--check` changes nothing: it only answers "is every file already formatted?". A build server uses it and fails when somebody forgot. Letting a tool decide the layout means there is nothing left to argue about in reviews.

### 9. Settings in pyproject.toml

Add this to `pyproject.toml` (see `pyproject.toml` in this folder):

```toml
[tool.ruff]
line-length = 79

[tool.ruff.lint]
extend-select = ["E", "F", "N"]
```

`E` is pycodestyle, `F` is Pyflakes, `N` is naming. `extend-select` keeps the default set and adds these. `uv run ruff linter` lists every family (`B` is bugbear, `I` import order, and many more). Run the check again:

```bash
uv run ruff check --output-format concise
```

```text
billing.py:1:1: F403 `from math import *` used; unable to detect undefined names
billing.py:14:18: E711 Comparison to `None` should be `cond is not None`
billing.py:26:80: E501 Line too long (80 > 79)
Found 3 errors.
1 unsafe fix available with `--fix --unsafe-fixes`.
```

Three new problems. The star import loads every name from `math` and nobody can tell where a name came from. `== None` can be fooled by a class, `is not None` cannot. And one comment line is 80 characters, limit 79. Fix all three by hand: delete the star import, write `is not None`, split the comment over two lines. The result is `steps/billing_5_final.py`.

```bash
cp steps/billing_5_final.py billing.py
uv run ruff check
uv run ruff format --check
uv run pytest -q
```

```text
All checks passed!
2 files already formatted
...                              [100%]
3 passed in 0.00s
```

(The video shows `3 files already formatted` because it also had the config-free `test_billing.py` and one more file; your count depends on the files in your folder.)

### 10. Silence one line on purpose

Compare `demos/noqa_demo_without.py` and `demos/noqa_demo_with.py`:

```bash
uv run ruff check demos/noqa_demo_without.py --output-format concise
uv run ruff check demos/noqa_demo_with.py --output-format concise
```

```text
noqa_demo_without.py:2:21: E711 Comparison to `None` should be `cond is None`
Found 1 error.
1 unsafe fix available with `--fix --unsafe-fixes`.
All checks passed!
```

(The path in the first line may show `demos/` in front.) The comment `# noqa: E711` tells ruff to skip that rule on that line only. Use it rarely, and say why.

### 11. pre-commit: run the checks before every commit

A tool you must remember to run is a tool people forget. Git can run a small program just before each commit (a "hook"), and `pre-commit` looks after the hooks.

```bash
git init
git add -A
git commit -m "Clean up billing"
uv add --dev pre-commit
cp ../.pre-commit-config.yaml .      # from this lesson folder
cat .pre-commit-config.yaml
```

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.17.2
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
```

`repos` is the list of places to get hooks from. `rev` is the exact version. Turn it on once:

```bash
uv run pre-commit install
```

```text
pre-commit installed at .git/hooks/pre-commit
```

Commit the new files. The first time, pre-commit builds a private environment for ruff (this needs internet). The hooks are skipped because the commit holds no Python files:

```bash
git add -A
git commit -m "Add ruff and pre-commit"
```

```text
[INFO] Initializing environment for https://github.com/astral-sh/ruff-pre-commit.
[INFO] Installing environment for https://github.com/astral-sh/ruff-pre-commit.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
ruff check...........................................(no files to check)Skipped
ruff format..........................................(no files to check)Skipped
[main a59bc65] Add ruff and pre-commit
 3 files changed, 134 insertions(+)
 create mode 100644 .pre-commit-config.yaml
```

(The commit hash differs on your machine.)

### 12. The real test: a commit that gets blocked

Copy `demos/report.py` into the project root. It has an unused import, a space before a colon, a comparison with `None` and cramped spaces. Guess: will the commit go through?

```bash
cp demos/report.py .
git add report.py
git commit -m "Add greeting"
```

The video's output (trimmed):

```text
ruff check...............................................................Failed
- hook id: ruff-check
- exit code: 1
- files were modified by this hook

E711 Comparison to `None` should be `cond is None`
 --> report.py:2:16
...
Found 2 errors (1 fixed, 1 remaining).
1 unsafe fix available with `--fix --unsafe-fixes`.

ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted
```

Blocked, and no commit line at the end. Even though ruff fixed the file, the hook still fails: the file on disk now differs from what you added. Look at it:

```bash
git status --short
```

```text
AM report.py
```

`A` means added, `M` means modified since. Fix the last problem by hand (`is None`; the result is `demos/report_fixed.py`), add again, commit again:

```bash
git add report.py
git commit -m "Add greeting"
```

```text
ruff check...............................................................Passed
ruff format..............................................................Passed
[main c11b87c] Add greeting
 1 file changed, 5 insertions(+)
 create mode 100644 report.py
```

`git log --oneline` now shows three commits. To check every file, not only the committed ones (useful for an old project or on a build server):

```bash
uv run pre-commit run --all-files
```

```text
ruff check...............................................................Passed
ruff format..............................................................Passed
```

The loop is: edit, add, commit. Hooks run. If they pass, the commit is saved. If they fail, fix and try again.

## Common mistakes

1. Turning on every rule at once. `ruff check --select ALL` on our clean 27-line file gives 13 complaints (missing docstrings, a copyright notice, type hints on every argument), and some rules contradict each other. Start with a small set and add a family only when you know why.
2. Skipping the checks. `git commit --no-verify` skips the hooks, so a file like `demos/shout.py` (`text.upper()+"!"`) gets in. Hooks are a helper, not a guarantee. The build server must run the same checks (Module 19).
3. Hooks do not travel with the project. They live in Git's hidden `.git` folder, which is not shared. After every `git clone`, run `uv run pre-commit install` once.
4. Formatting an old project all at once. Hundreds of files change and the one real change hides in the noise. Format the whole project in a commit of its own, say so in the message, and keep every other change out of it.

## Clean up

Delete the scratch project folder (`allcsvideos`), including its hidden `.git` and `.venv` folders. pre-commit keeps a cache in `~/.cache/pre-commit`; remove it if you want the space back (`uv run pre-commit clean`).

## Next

[M14-L02 · Debugging](../m14-l02-debugging/)
