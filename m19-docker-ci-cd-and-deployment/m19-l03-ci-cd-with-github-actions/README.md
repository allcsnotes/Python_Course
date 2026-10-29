# M19-L03 · CI/CD with GitHub Actions

> Video: Module 19, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What CI (continuous integration) and CD (continuous delivery) mean, and why a robot runs the same checks on every push
- How a GitHub Actions workflow file is built: `on`, `jobs`, `runs-on`, `steps`, `uses`, `run`, a `matrix`, `services` and `needs`
- How to run the whole workflow on your laptop with `act`, and how a green run and three red runs look (lint, a broken test, a coverage floor)
- How CD adds a `deploy` job that only runs on `main`, with a secret that is never in the file
- Three pitfalls: an out-of-date lock file, a secret in a log, and borrowed actions pinned to a movable tag

## Before you start

- Python 3.14 (`python --version`) and Docker running. For the "run it with act" part you also need `act` (`brew install act`, version 0.2.89 in the video) and a network connection: `act` downloads a 2 GB runner image and fetches the GitHub actions named in the file. This repo never calls GitHub itself and nothing is deployed anywhere.
- This lesson continues the project from M19-L02 (`../m19-l02-configuration-the-12-factor-way/`). The folder `allcs/` is that project plus `.github/workflows/ci.yml`, `.actrc` and the CI tools in `pyproject.toml`.
- IMPORTANT about the outputs below: the workflow outputs marked "captured" were recorded with a real `act` run on the video machine, and are copied here as they were. I did not re-run `act` for this README. The pieces that need no GitHub (ruff, the tests with coverage, the pre-commit hook) WERE re-run, and their outputs are real runs of this folder (the numbers match the video exactly).
- All tokens are fake (`demo-token-not-real`). Nothing here deploys: the `deploy` job only runs an `echo`.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/.github/workflows/ci.yml` | The workflow: jobs `lint`, `typecheck`, `test` (matrix 3.13 and 3.14, Postgres and Redis services), `image` and `deploy` |
| `allcs/.actrc` | Settings for `act`: the runner image, `arm64`, one job at a time (see the note below) |
| `allcs/pyproject.toml`, `uv.lock` | The project, with the CI tools (`ruff`, `pyright`, `pytest-cov`) and their settings (`[tool.ruff]`, `[tool.coverage]`, `[tool.pyright]`) |
| `allcs/.python-version` | `3.14` |
| `allcs/Dockerfile`, `.dockerignore`, `.env.example` | From the earlier lessons |
| `allcs/app/`, `tests/`, `migrations/` | The backend (38 tests) |
| `scenarios/reports.py` | A 50-line module with no tests (for the coverage scenario) |
| `scenarios/mask-demo.yml` | A tiny workflow that prints a secret (for the masking pitfall) |

## Follow along

### 1. The hook that was skipped

A pre-commit hook can be skipped with `--no-verify`, so it cannot be the last guard. This is a throwaway repository with one Python file and a hook that runs `ruff check`:

```bash
pip install ruff pre-commit
mkdir hookdemo && cd hookdemo
git init -q -b main
git config user.name Priya && git config user.email priya@example.com
printf 'def final_price(price, discount):\n    return price - discount\n' > prices.py
printf 'repos:\n  - repo: local\n    hooks:\n      - id: ruff-check\n        name: ruff check\n        entry: ruff check\n        language: system\n        types: [python]\n' > .pre-commit-config.yaml
printf '[tool.ruff]\nline-length = 60\n' > pyproject.toml
git add -A && git commit -q --no-verify -m "start"
pre-commit install
printf 'import json\n\n\ndef final_price(price, discount):\n    return price - discount\n' > prices.py
git add prices.py
git commit -m "quick fix"
```

```
ruff check...............................................................Failed
- hook id: ruff-check
- exit code: 1

F401 [*] `json` imported but unused
 --> prices.py:1:8
...
Found 1 error.
```

The hook blocks the commit (exit code 1). Priya skips it, and the problem goes in:

```bash
git commit --no-verify -m "quick fix"
ruff check .
```

```
[main 63e15d8] quick fix
 1 file changed, 3 insertions(+)
F401 [*] `json` imported but unused
...
Found 1 error.
```

(The commit id differs.) Zero means "all is well", anything else means problems. Delete the `hookdemo` folder afterwards. A robot on the server cannot be skipped: that is CI.

### 2. Read the workflow

Open `allcs/.github/workflows/ci.yml`. Words: an event starts it (a push), a workflow is the file, a job is a group of steps on one fresh machine (a runner), a step is one command or one borrowed action.

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
```

- `lint`, `typecheck` and `test` all run on `ubuntu-latest`, each on a clean machine: `actions/checkout@v4` copies the code, `astral-sh/setup-uv@v6` installs uv, then `uv sync --locked` (exactly the versions in `uv.lock`; it fails if the lock and the project disagree), then `uv run ruff check .` and `uv run ruff format --check .`, or `uv run pyright`.
- `test` has a `matrix` (`python: ["3.13", "3.14"]`, two jobs from one description) and `services` for Postgres (`postgres:17.11`, with a health check) and Redis (`redis:8`). The addresses reach the tests through `env` (the Settings class from lesson 2 reads them). The test step: `uv run pytest -q --cov --cov-fail-under=90` (a coverage floor of 90 percent).
- `image` has `needs: [lint, typecheck, test]`: it waits for all three and never starts if one is red. It builds the image with a tag made from `${{ github.sha }}`.
- `deploy` has `needs: image`, `if: github.ref == 'refs/heads/main'` and `environment: production`, and only runs an `echo` here.

### 3. Run the same checks yourself (verified)

These are the commands the robot runs. They need the two services; start them on the ports the workflow uses:

```bash
docker run -d --name pyrepo-m19-l03-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs_test -p 5432:5432 postgres:17.11
docker run -d --name pyrepo-m19-l03-redis -p 6379:6379 redis:8
cd allcs
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install celery==5.6.3 redis==8.1.0 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pyjwt==2.15.1 pydantic-settings==2.16.1 httpx==0.28.1 pytest==9.1.1 pytest-cov ruff==0.17.3
export DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:5432/allcs_test
export REDIS_URL=redis://localhost:6379/15
ruff check .
ruff format --check .
pytest -q --cov --cov-fail-under=90
```

(If port 5432 or 6379 is already in use on your machine, stop the other program or change both the `-p` mapping and the two variables. The video uses `uv sync --locked` and `uv run` instead of `pip`.)

```
All checks passed!
36 files already formatted
...
TOTAL                          488     24     32      7    94%
Required test coverage of 90% reached. Total coverage: 94.04%
38 passed in 4.44s
```

(Times differ.) `pyright` (the type check job) is not re-run here: it downloads its own Node.js. In the video it reported `0 errors, 0 warnings, 0 informations`.

### 4. Run the whole workflow with `act` (captured)

`act` runs the workflow on your laptop in Docker containers. `act -l` lists the jobs, in stages (stage 0 can run in parallel, `image` waits, `deploy` last):

```bash
cd allcs
act -l
```

```
Stage  Job ID     Job name   Workflow name  Workflow file  Events
0      lint       lint       ci             ci.yml         push,pull_request
0      typecheck  typecheck  ci             ci.yml         push,pull_request
0      test       test       ci             ci.yml         push,pull_request
1      image      image      ci             ci.yml         push,pull_request
2      deploy     deploy     ci             ci.yml         push,pull_request
```

`.actrc` makes `act` use the runner image `catthehacker/ubuntu:act-latest`, the `arm64` architecture (remove that line on an Intel machine), `--pull=false` and one job at a time (both Python versions would otherwise fight for the same Postgres port on one laptop). The git history needs to be in place, since `act` pretends to be a push to `main`: work in a git repository on the branch `main`. Then, one leg of the matrix at a time:

```bash
act push --matrix python:3.14
act push -j test --matrix python:3.13
```

Captured output of a green run (selected lines from the `act` log; the first run also pulls the 2 GB runner image and the actions):

```
[ci/lint     ]   ✅  Success - Main uv sync --locked [14.99s]
[ci/lint     ]   | All checks passed!
[ci/lint     ] 🏁  Job succeeded
[ci/typecheck]   | 0 errors, 0 warnings, 0 informations
[ci/typecheck] 🏁  Job succeeded
[ci/test     ]   | TOTAL                          488     24     32      7    94%
[ci/test     ]   | Required test coverage of 90% reached. Total coverage: 94.04%
[ci/test     ]   | 38 passed in 11.92s
[ci/test     ] 🏁  Job succeeded
```

The image job builds the Docker image tagged with the commit, and deploy runs last: five jobs, all green. The second leg (Python 3.13) also passes the same 38 tests (coverage 94.30%).

### 5. Red: three ways to fail

Each of these was captured with `act`; the first two and the third's numbers you can reproduce yourself with the commands from step 3.

1. Priya pushes her unused import (add `import json` as the first line of `app/routers/courses.py`):

```
[ci/lint     ]   | Found 1 error.
[ci/lint     ]   ❌  Failure - Main uv run ruff check . [1.21s]
[ci/lint     ] 🏁  Job failed
[ci/typecheck] 🏁  Job succeeded
[ci/test     ] 🏁  Job succeeded
```

Lint is red; type check and test are green (they do not need lint). The run stops after that stage: `image` and `deploy` never start. Locally: `ruff check .` prints `F401 [*] json imported but unused ... Found 1 error.`

2. A duplicate sign up should answer 400, not 409 (change `error(409, ...)` to `error(400, ...)` in `app/errors.py`):

```
[ci/test     ]   | 2 failed, 36 passed in 5.60s
[ci/test     ]   ❌  Failure - Main uv run pytest -q --cov --cov-fail-under=90
[ci/test     ] 🏁  Job failed
```

The failing assertion reads `assert 400 == 409` (and the test `test_the_same_email_twice_is_409` is in the list). The test job is red, so `image` and `deploy` never start.

3. A new module with no tests (copy `scenarios/reports.py` to `app/reports.py`): every old test still passes, but

```
[ci/test     ]   | TOTAL                          536     72     54      7    83%
[ci/test     ]   | FAIL Required test coverage of 90% not reached. Total coverage: 82.88%
[ci/test     ]   | 38 passed in 3.42s
[ci/test     ]   ❌  Failure - Main uv run pytest -q --cov --cov-fail-under=90
```

The new lines ran in no test, and the floor caught it.

### 6. CD: deploy only on main

The `deploy` job has `if: github.ref == 'refs/heads/main'`. Push from a branch named `priya/fix-title` and lint, type check, test and image all run and pass, while `deploy` is skipped. With `act -v` the detailed log says the expression `github.ref == 'refs/heads/main'` evaluated to false (captured). Everything was checked, nothing went out. A real deploy needs a key to the server: that key is never in the file, it lives in the repository settings as a secret, and the file only names it (`secrets.deploy_token`). `environment: production` can also require a human to approve. One more piece lives on GitHub, not in the file: branch protection for `main` (no direct pushes, a pull request, and the checks `lint`, `typecheck` and `test` must be green).

### 7. Pitfalls

**The lock file.** A package is added to `pyproject.toml` without running `uv lock`. The lint job stops at `uv sync --locked` (captured):

```
error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.
hint: To update the lockfile, run `uv lock`.
```

On a laptop plain `uv sync` would quietly change the lock file. Fix: run `uv lock` and commit it.

**A secret in a log.** `scenarios/mask-demo.yml` prints the token. Run it with a fake token:

```bash
cp ../scenarios/mask-demo.yml .github/workflows/mask-demo.yml
act push -W .github/workflows/mask-demo.yml -s DEPLOY_TOKEN=demo-token-not-real
```

```
[mask-demo/show]   | token is ***
[mask-demo/show] 🏁  Job succeeded
```

(captured.) GitHub hides values it knows are secrets, but only exact copies: a changed or cut-up secret can leak. Delete the demo file afterwards (`rm .github/workflows/mask-demo.yml`).

**Borrowed steps are borrowed code.** `actions/checkout@v4` is a tag, and its owner can move a tag. Pin the full commit hash (and let a tool such as Dependabot keep it fresh), and never run a borrowed action with more permissions than it needs.

## Common mistakes

- Trusting a pre-commit hook as the only guard (`--no-verify` skips it). The robot on the server cannot be skipped.
- Running `uv sync` (not `--locked`) in CI: the robot would guess instead of refusing.
- Putting a secret in the workflow file. Name it (`secrets.NAME`) and store it in the repository settings.
- Printing a secret, or a changed copy of it, in a step.
- Pinning an action to a tag only.
- A coverage floor that nobody ever raises, or tests that fake everything. The floor is a guard, not a goal.

## Clean up

```bash
docker rm -f -v pyrepo-m19-l03-pg pyrepo-m19-l03-redis
rm -rf .venv .coverage .pytest_cache .ruff_cache
rm -rf ../hookdemo
```

## Next

[M19-L04 · Running in Production](../m19-l04-running-in-production/README.md)
