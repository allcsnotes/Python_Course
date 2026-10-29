# M21-L03 · Working with Other People's Code

> Video: Module 21, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- How to find your way in a big, strange project: the README, the entry points, the tests, `grep`, one feature end to end, and `git log` / `git blame`
- How to run someone else's code safely, in a throwaway Docker box
- Version ranges from the user's side: what `==`, `>=,<` and `~=` allow, and the difference between the range (`pyproject.toml`) and the lock (`uv.lock`)
- Licences in plain words: MIT, Apache 2 and GPL
- The contributing path, run for real on a local Gitea server: issue, fork, branch, commit, push, pull request, review, fixup, merge
- Manners that make maintainers happy

## Before you start

- Python 3.14 or newer (`python --version`), `uv` (`uv --version`) and `git`.
- Docker running. Two things use it: the throwaway "box" (a Python 3.14 container) and a local Gitea server (`gitea/gitea:1.24.6`). Max one container runs at a time.
- Module 7, lesson 4 (checking a package from the outside), Module 13 (pytest) and Module 21, lesson 2 (semantic versioning) help.
- The library we read is **humanize** (MIT licence). It is cloned read-only from its public home. Nothing in this lesson is sent to GitHub, and no real maintainer is contacted: the contributing part runs on your own laptop. GitHub works the same way.
- The numbers below come from the video's clone at commit `6b817b9`. The project moves on, so after cloning run `git checkout 6b817b9` if you want exactly the same output (and `git switch main` to come back).

## Files in this folder

| File | What it is |
|------|------------|
| `box` | A 2-line script: runs a command in a throwaway container with your folder mounted read-only |
| `boximg/Dockerfile`, `boximg/entry.sh` | Build the box image: Python 3.14, git, pytest 9.1.1, freezegun, hatchling, hatch-vcs (pinned) |
| `reader/pyproject.toml` | Asha's tiny project that depends on humanize (starts with an exact `==4.9.0`) |
| `patches/test_naturalsize_zero_v1.py` | Asha's first version of the new test (appended to `tests/test_filesize.py`) |
| `patches/test_naturalsize_zero_v2.py` | The parametrized version, after Meera's review |
| `gitea/start.sh` | Starts the local Gitea, creates two demo users (Meera, Asha) and puts a copy of humanize under Meera |
| `gitea/login.sh` | Makes one clone use the demo login of one Gitea user, without a password prompt or keychain |
| `gitea/stop.sh` | Removes the Gitea container and its data |

The demo password in these scripts (`demo-password-123`) only exists inside your throwaway Gitea. Tokens are generated into `gitea/.local/` (ignored by git).

## Follow along

Run the commands from this folder unless a step says otherwise.

### 1. The question

Asha's course report shows the size of each video file as raw bytes: `2457600`. Priya says a small library prints it as "2.5 MB". Do we just add it? Adding a library is a real decision. In Module 7 we checked a package from the outside (popularity, freshness). Today we go inside.

Reading a big project is like arriving in a strange city: you do not walk every street. At the station you look at the map (the README), you find the main road (the entry points) and you ask where the locals go (the tests, which show how the code is really used and are always up to date). Three tools finish the job: `grep` to find where a name lives, `git log` and `git blame` to see why a line is the way it is, and running it, carefully, in a box. A package is somebody else's code running on your computer.

### 2. Clone it, read-only

humanize turns numbers into words people like: file sizes, durations, counts. Clone it into your home folder, not inside this repository. First remember where this lesson folder is:

```bash
LESSON=$PWD
git clone https://github.com/python-humanize/humanize ~/humanize-read
cd ~/humanize-read
git checkout 6b817b9
```

```
Cloning into '/Users/you/humanize-read'...
Receiving objects: 100% (5579/5579), 1.04 MiB | 3.86 MiB/s, done.
Resolving deltas: 100% (3281/3281), done.
```

The whole history of a well-known project fits in about a megabyte: text is small. (Speeds will differ; the object count grows over time.) We only want to read, so make a mistake impossible: set the push address to nothing.

```bash
git remote set-url --push origin no_push
git remote -v
```

```
origin	https://github.com/python-humanize/humanize (fetch)
origin	no_push (push)
```

Whatever you do here, nothing can travel back to the original.

### 3. Look around

```bash
ls
ls src/humanize tests
wc -l src/humanize/*.py
```

```
LICENCE
README.md
RELEASING.md
docs
mkdocs.yml
pyproject.toml
requirements-mypy.txt
scripts
src
tests
tox.ini
```

```
src/humanize:
__init__.py
filesize.py
i18n.py
lists.py
locale
number.py
py.typed
time.py

tests:
__init__.py
test_benchmarks.py
test_filesize.py
test_i18n.py
test_lists.py
test_number.py
test_time.py
```

```
      58 src/humanize/__init__.py
     110 src/humanize/filesize.py
     212 src/humanize/i18n.py
      40 src/humanize/lists.py
     603 src/humanize/number.py
     704 src/humanize/time.py
    1727 total
```

Top level: the licence file (`LICENCE`), the README, `pyproject.toml`, a `src` folder (six Python files), a `tests` folder (one test file per area) and `docs`. About 1,727 lines: a real library that one person can read in an afternoon.

### 4. The box: run their code without trusting it

Build the box image and look at the script (`box`):

```bash
docker build -t pyrepo-m21-box boximg
cat box
```

```
#!/bin/sh
# Run a command in a throwaway container. The project folder is mounted read-only,
# and the container is removed when the command ends.
docker run --rm -v "$PWD":/src:ro pyrepo-m21-box "$@"
```

It starts a throwaway container, lets it look at your current folder but never change it, and runs the command you type after it. When the command ends, the container is gone and your files are untouched. Put the script on your PATH for this terminal session, so you can type `box`:

```bash
export PATH="$LESSON:$PATH"
```

(Run `box` from inside the humanize clone.)

### 5. Six steps to read a project

All of these run inside `~/humanize-read`.

**Step 1, the README.** What is it, how do you install it, a short example. This one says: it turns numbers into human-friendly sizes and times, and it is translated into more than thirty languages. Read the first screen and you know what the project promises.

**Step 2, the entry points.** Open `src/humanize/__init__.py`. Each `from ... import` line brings a name to the front door: `naturalsize`, `intcomma`, `naturaltime` and more. The list `__all__` at the bottom is the official front door. Everything else is inside the house. Now use one:

```bash
box python -c 'import humanize; print(humanize.naturalsize(3000000))'
```

```
3.0 MB
```

It works, and we have not read a line of its body yet.

**Step 3, search.** Where does `naturalsize` live? Which files talk about it?

```bash
grep -rn 'def naturalsize' src
grep -rln naturalsize tests docs
```

```
src/humanize/filesize.py:38:def naturalsize(
tests/test_filesize.py
tests/test_benchmarks.py
tests/test_i18n.py
```

One definition: `filesize.py`, line 38. Three files mention it: the tests, the benchmarks and the language tests.

**Step 4, the tests.** Open `tests/test_filesize.py`: a table of inputs and the answer the authors expect (300 gives `300 Bytes`, 1000 gives `1.0 kB`). It is the best manual the project has, and it cannot be out of date, because it runs. Run it in the box:

```bash
box python -m pytest tests/test_filesize.py -q -p no:cacheprovider --color=no
```

```
........................................................................ [ 94%]
....                                                                     [100%]
76 passed in 0.05s
```

Now you know the tests pass on your machine, today: a good sign before you trust any library.

**Step 5, read one feature, top to bottom.** Not the whole library, just `naturalsize` (`src/humanize/filesize.py`, from line 38). It has three parts:

1. Choose the suffixes and the base: decimal (the default: kB, MB, GB, base 1000), binary (KiB, MiB, base 1024) and `gnu` (single letters). The base is picked in one line: `base = 1024 if (gnu or binary) else 1000`.
2. Small numbers: exactly 1 is the word `Byte`, anything below the base just prints the count with its unit. Two `if` lines.
3. The interesting part. Guess first: a file has 999999 bytes, one less than a million. One thousand kilobytes, or one megabyte?

```bash
box python -c 'import humanize; print(humanize.naturalsize(999999))'
```

```
1.0 MB
```

Never "1000.0 kB": the library rounds, and careful rounding never shows a number as big as its own base. Find the lines that do this (102 to 104 of `filesize.py`, with a comment that tells the story):

```python
    exp = int(min(log(abs_bytes, base), len(suffix)))
    # The suffix is chosen from the unrounded byte count, but `format` rounds the
    # mantissa afterward; rounding can push it up to `base` (e.g. 999999 is
    # 999.999 kB, which formats to "1000.0 kB"). When that happens and a larger
    # suffix is available, step up one suffix so the result reads "1.0 MB".
    if exp < len(suffix) and abs(float(format % (abs_bytes / (base**exp)))) >= base:
        exp += 1
```

The suffix is chosen first, from the exact count. Then the format rounds the number: 999.999 rounds up to 1000. When that happens, one line steps up to the next suffix. A good comment says why, not what.

**Step 6, history.** Who wrote this, and when?

```bash
git log --oneline -4 -- src/humanize/filesize.py
git blame -s -L 102,104 src/humanize/filesize.py | cut -c1-62
git log -1 --format='%h %ad %s' --date=short 823ad609
```

```
2ad3641 Defer importing `math` in `filesize.py` (#397)
8a47cb4 Lazy imports for Python 3.15+ (#335)
823ad60 Fix `naturalsize()` rounding rollover at unit boundaries (#329)
b172d67 Add i18n support for `naturalsize()` and French translation (#294)
```

```
823ad609 102)     # The suffix is chosen from the unrounded by
823ad609 103)     # mantissa afterward; rounding can push it u
823ad609 104)     # 999.999 kB, which formats to "1000.0 kB").
```

```
823ad60 2026-06-30 Fix `naturalsize()` rounding rollover at unit boundaries (#329)
```

The third log line sounds like our lines, and `git blame -s` confirms it: all three comment lines come from the same commit, made on 30 June, in pull request number 329. A bug, found by somebody, fixed, explained and kept in history: that is the answer to "why is this line here?". (Hashes and dates are from the clone at `6b817b9`.)

Six steps, about ten minutes. And the clone is unchanged:

```bash
git status --short
```

(no output: nothing changed. We only read.)

### 6. Choosing a version range

Libraries change, and you choose how much change you accept. You know the three numbers from lesson 2: major, minor, patch. Now write them down as a range. Go to Asha's tiny project (it is in this lesson folder):

```bash
cd "$LESSON/reader"
cat pyproject.toml
uv lock
grep -A1 'name = "humanize"' uv.lock | head -2
```

```
[project]
name = "reader"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["humanize==4.9.0"]
Resolved 2 packages in 601ms
name = "humanize"
version = "4.9.0"
```

Exact is safe, but stuck: no fixes will ever arrive. Loosen it: at least 4.9, below 5. Edit the last line of `pyproject.toml` to:

```toml
dependencies = ["humanize>=4.9,<5"]
```

Minor and patch releases are welcome; a new major is not, because a major may break our code. Now run `uv lock` again. The newest humanize is much newer than 4.9. Guess: does the lock move?

```bash
uv lock
grep -A1 'name = "humanize"' uv.lock | head -2
```

```
Resolved 2 packages in 20ms
name = "humanize"
version = "4.9.0"
```

No. The lock file is a promise: nothing moves until you ask. The range says what is allowed; the lock says what is used. To ask, name the package:

```bash
uv lock --upgrade-package humanize
grep -A1 'name = "humanize"' uv.lock | head -2
```

```
Resolved 2 packages in 436ms
Updated humanize v4.9.0 -> v4.16.0
name = "humanize"
version = "4.16.0"
```

It stopped at the newest one inside our range. (Timings differ. If a newer 4.x appears later, your number will be higher.)

Other tools write the same idea with short signs: in Python, `~=4.9` means at least 4.9, below 5. In JavaScript tools, and in Poetry, a hat, `^4.9`, means the same. A tilde with three numbers, `~=4.9.0`, allows patches only. Learn the idea once and you can read every sign.

What if we ask for a version that does not exist? Change the line to `humanize>=5,<6` and lock:

```bash
uv lock
```

```
error: No solution found when resolving dependencies
  cause: Because only humanize<=4.16.0 is available and your project
         depends on humanize>=5,<6, we can conclude that your
         project's requirements are unsatisfiable.
```

A range is a wish; the index decides if the wish can be kept. Before you move a major version, read the release notes, and let your tests say if it still works (Module 13). `pip-audit` (Module 17, lesson 4) tells you if the version you use has a known weakness.

### 7. Licences, in plain words

Reading is free. Using needs permission, and the permission is the licence. Three famous ones:

- **MIT**: do almost anything, keep the copyright notice.
- **Apache 2**: the same, and it also gives you a clear permission for patents.
- **GPL**: if you give your program to others with this code inside, you must give them your source too, under the GPL.

This is a card, not legal advice: for a company, ask a lawyer. The habit is simple: find the licence file before you add a library. humanize has one, and `pyproject.toml` says it too (run inside `~/humanize-read`):

```bash
grep -n '^license' pyproject.toml
```

```
15:license = "MIT"
16:license-files = [ "LICENCE" ]
```

And no licence at all means nobody may use the code.

### 8. Contributing: the whole path, for real, on a local server

While reading, Asha noticed that no test calls `naturalsize` with 0. It works today, but nothing protects it. A perfect small gift for the project. The famous path is: an issue, a fork, a branch, a commit, a push, a pull request, a review, and a merge. We walk it on a small server like GitHub, named Gitea, in Docker. Two throwaway users: Meera, who looks after the project, and Asha, who contributes. A copy of humanize lives under Meera.

Start it (this uses your clone as the content, at the same commit):

```bash
cd "$LESSON"
./gitea/start.sh ~/humanize-read
```

```
Gitea is running at http://localhost:21303  (users: meera, asha; demo password: demo-password-123)
Tokens are in .../gitea/.local/ (local, demo, not for sharing)
```

Open <http://localhost:21303> in a browser: log in as `meera`, and see `meera/humanize`. (If port 21303 is busy, change it in the three scripts.) Keep the two tokens handy for the commands below (the web page does the same with clicks):

```bash
API=http://localhost:21303/api/v1
ASHA=$(cat gitea/.local/asha.token)
MEERA=$(cat gitea/.local/meera.token)
```

**Rules of the house.** Real projects write them down. In humanize, `.github/CONTRIBUTING.md` says how to run the tests (with `tox`), how to run the linter, and that docstrings follow Google style. `.github/PULL_REQUEST_TEMPLATE.md` is the template for pull requests ("Fixes #", "Changes proposed in this pull request"). Bigger projects add a `CODE_OF_CONDUCT.md`: be kind. This one has none, and kindness still applies.

**Second: an issue first.** As Asha, open an issue in `meera/humanize` (web: Issues, New Issue), and ask if a pull request is welcome. As Meera, answer: yes please, keep it small, and include the test. Asking first costs a minute and can save a week. The same with the API:

```bash
curl -s -X POST $API/repos/meera/humanize/issues -H "Authorization: token $ASHA" \
  -H 'Content-Type: application/json' \
  -d '{"title":"No test for naturalsize(0)","body":"While reading filesize.py I noticed that no test calls naturalsize() with 0. It works today, but nothing protects it. Would a pull request with a small test be welcome?"}'
curl -s -X POST $API/repos/meera/humanize/issues/1/comments -H "Authorization: token $MEERA" \
  -H 'Content-Type: application/json' -d '{"body":"Yes please. Keep it small, and include the test."}'
```

**Third: the fork.** You cannot change Meera's repository: it is hers. A fork is your own copy of it, on the same server. As Asha: on the repository page, click Fork (about a second). Or:

```bash
curl -s -X POST $API/repos/meera/humanize/forks -H "Authorization: token $ASHA" \
  -H 'Content-Type: application/json' -d '{}'
```

The page says "forked from meera/humanize".

**Bring the fork to the laptop.** Clone Asha's copy (into your home folder), tell the clone to log in as Asha, and add a second address named `upstream` for Meera's original:

```bash
git clone http://localhost:21303/asha/humanize.git ~/asha-humanize
cd ~/asha-humanize
"$LESSON/gitea/login.sh" asha
git remote add upstream http://localhost:21303/meera/humanize.git
git remote -v
```

```
Cloning into '/Users/you/asha-humanize'...
This clone now acts as asha on http://localhost:21303
origin	http://localhost:21303/asha/humanize.git (fetch)
origin	http://localhost:21303/asha/humanize.git (push)
upstream	http://localhost:21303/meera/humanize.git (fetch)
upstream	http://localhost:21303/meera/humanize.git (push)
```

`origin` is where you push (your fork). `upstream` is where you read news.

**Fourth: a branch.** Never work on `main`. One branch for one idea:

```bash
git switch -c test-naturalsize-zero
```

```
Switched to a new branch 'test-naturalsize-zero'
```

**Fifth: the change.** Append the test from `patches/test_naturalsize_zero_v1.py` (without its first comment line) to the end of `tests/test_filesize.py`:

```python
def test_naturalsize_zero() -> None:
    assert humanize.naturalsize(0) == "0 Bytes"
    assert humanize.naturalsize(0, binary=True) == "0 Bytes"
    assert humanize.naturalsize(0, gnu=True) == "0B"
```

Run the whole file in the box (from inside `~/asha-humanize`, with `box` on your PATH as in step 4), then look at what changed, and commit with a message that says what and where:

```bash
box python -m pytest tests/test_filesize.py -q -p no:cacheprovider --color=no
git status --short
git diff --stat
git commit -a -m 'Add a test for naturalsize(0)'
```

```
........................................................................ [ 93%]
.....                                                                    [100%]
77 passed in 0.04s
 M tests/test_filesize.py
 tests/test_filesize.py | 6 ++++++
 1 file changed, 6 insertions(+)
[test-naturalsize-zero de5d883] Add a test for naturalsize(0)
 1 file changed, 6 insertions(+)
```

77 passed: 76 old and one new. (The commit hash is yours.)

**A trap: pushing straight to upstream.** What if Asha pushes to Meera's repository? The server says no, of course: strangers cannot write to your project.

```bash
git push upstream test-naturalsize-zero
```

```
remote: 
remote: error:        
remote: error: User permission denied for writing.        
remote: error:        
To http://localhost:21303/meera/humanize.git
 ! [remote rejected] test-naturalsize-zero -> test-naturalsize-zero (pre-receive hook declined)
error: failed to push some refs to 'http://localhost:21303/meera/humanize.git'
```

You push to your own fork, and ask for your change to be taken:

```bash
git push -u origin test-naturalsize-zero
```

```
remote: Create a new pull request for 'test-naturalsize-zero':        
remote:   http://localhost:21303/asha/humanize/pulls/new/test-naturalsize-zero        
remote: 
remote: . Processing 1 references        
remote: Processed 1 references in total        
To http://localhost:21303/asha/humanize.git
 * [new branch]      test-naturalsize-zero -> test-naturalsize-zero
branch 'test-naturalsize-zero' set up to track 'origin/test-naturalsize-zero'.
```

The server even prints the address where you can open the pull request.

**Sixth: the pull request.** It says: please take the change on this branch into your `main`. Open the printed address (or use the API), give it a clear title and fill in the template: `Fixes #1` (the issue) and a short list of what changed. The page shows one commit, six lines added. It is pull request number 2, because the issue was number 1.

```bash
curl -s -X POST $API/repos/meera/humanize/pulls -H "Authorization: token $ASHA" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Add a test for naturalsize(0)","head":"asha:test-naturalsize-zero","base":"main","body":"Fixes #1\n\nChanges proposed in this pull request:\n\n* Add a test for `naturalsize(0)`: plain, binary and GNU style"}'
```

**Seventh: the review.** As Meera, open `http://localhost:21303/meera/humanize/pulls/2`, go to the Files changed tab, and leave a comment on the first line of the new test: "Please make this one parametrized test, so each case shows up on its own in the test report." Choose "Request changes". A review is a conversation, and a request for a change is normal, not an insult. (API version: `POST $API/repos/meera/humanize/pulls/2/reviews` with `event` set to `REQUEST_CHANGES` and a `comments` list holding `path`, `new_position` and `body`.)

**Eighth: the fixup.** As Asha, replace the new test with the parametrized version in `patches/test_naturalsize_zero_v2.py` (the file already imports `pytest`), run the file in the box, and make a fixup commit. `--fixup HEAD` makes git write the message for you: "fixup!" and the title of the commit it fixes.

```bash
box python -m pytest tests/test_filesize.py -q -p no:cacheprovider --color=no
git commit -a --fixup HEAD
git log --oneline -3
git push
```

```
........................................................................ [ 91%]
.......                                                                  [100%]
79 passed in 0.04s
[test-naturalsize-zero 3e6bad5] fixup! Add a test for naturalsize(0)
 1 file changed, 10 insertions(+), 4 deletions(-)
3e6bad5 fixup! Add a test for naturalsize(0)
de5d883 Add a test for naturalsize(0)
6b817b9 Benchmark with Python 3.15 (#483)
remote: 
remote: Visit the existing pull request:        
remote:   http://localhost:21303/meera/humanize/pulls/2        
remote: 
remote: . Processing 1 references        
remote: Processed 1 references in total        
To http://localhost:21303/asha/humanize.git
   de5d883..3e6bad5  test-naturalsize-zero -> test-naturalsize-zero
```

79 passed: three cases, each its own test. A plain `git push` is enough because the branch is already linked. The pull request updates by itself, and Meera can look again. (Some projects like to squash fixups later, and some merge them as they are. Follow what the project asks.)

**Ninth: the merge.** As Meera: approve ("Looks good. Thank you!") and merge with the squash option, so the two commits become one, with the pull request number in its name: `Add a test for naturalsize(0) (#2)`. The page says merged, and because the description said `Fixes #1`, the issue closes by itself.

**Last step: bring the news home.** As Asha:

```bash
git switch main
git pull upstream main
git log --oneline -3
git push origin main
```

```
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
From http://localhost:21303/meera/humanize
 * branch            main       -> FETCH_HEAD
 * [new branch]      main       -> upstream/main
Updating 6b817b9..c0ae8ff
Fast-forward
 tests/test_filesize.py | 12 ++++++++++++
 1 file changed, 12 insertions(+)
c0ae8ff Add a test for naturalsize(0) (#2)
6b817b9 Benchmark with Python 3.15 (#483)
cd41f2b Update github-actions (#482)
```

The new commit arrives with the pull request number in its name, and a push to `origin` brings Asha's fork up to date. The test Asha noticed is now part of the project. (The hash will differ.)

### 9. Manners that make maintainers happy

1. Small pull requests: one idea, a few lines, easy to review.
2. An issue first, for anything bigger than a typo.
3. Tests included, as Asha did.
4. Read the contributing file, and follow its style.
5. Be patient and kind. Maintainers are often volunteers.

A review can take days. A request for changes is a normal part of it. Sometimes the answer is no, because your idea does not fit. That is not about you: you keep your fork, and you learned something.

### 10. Interview tip

Rahul asks: you join a team with a large codebase you have never seen. How do you start? A model answer: read the README, find the entry points and the tests, run the tests, search with `grep` for the feature you need, read it end to end, and use `git log` and `git blame` to understand why it is the way it is. Then make a small change, with a test.

### 11. Your turn

Pick a small library you use. Clone it with the push address set to `no_push`, and read its README and its tests. Run its tests in a box. Find one line with `git blame` and read the commit behind it. Then find its licence.

## Common mistakes

- Cloning a library without setting the push address to `no_push`, then running `git push` by accident. Make the mistake impossible.
- Running an unknown package straight on your laptop. Run it in a box (a throwaway container, folder read-only).
- Thinking the lock file follows the range. It does not: nothing moves until you ask with `uv lock --upgrade-package`.
- Adding a library without finding its licence first. No licence means nobody may use the code.
- Working on `main` of your fork, or pushing to the upstream repository. Use one branch for one idea, and push to your own fork.
- A big pull request with no issue and no test.

## Clean up

```bash
cd "$LESSON"
./gitea/stop.sh                       # removes the Gitea container, its data and the tokens
docker rmi pyrepo-m21-box             # the box image
rm -rf reader/uv.lock reader/.venv    # what step 6 made
rm -rf ~/humanize-read ~/asha-humanize
```

## Next

[M21-B14 · Build and Publish allcsv-cli](../m21-b14-build-and-publish-allcsv-cli/)
