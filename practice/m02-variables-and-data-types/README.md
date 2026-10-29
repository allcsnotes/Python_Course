# M02 · Practice Sheet

> Practice for Module 2 (variables, numbers, text, True/False/None, input and output). Do it after [M02-L05](../../m02-variables-and-data-types/m02-l05-input-and-output/).

20 small exercises, about four per lesson, from easy to harder. Some are "predict the output", some are "fix the broken code", and some build a small program. Nothing needs more than Module 2.

## What is here

| File or folder | What it is |
|----------------|------------|
| [`sheet.md`](sheet.md) | The sheet: the 20 exercises, each with a hint and a worked answer with the real output |
| [`solutions/`](solutions/) | The 20 solution files, `Ex01.py` to `Ex20.py` |

## How to use it

1. You need Python 3.14 or newer. Check with `python --version` (on Mac or Linux the command may be `python3`).
2. Open [`sheet.md`](sheet.md). Read one exercise.
3. Try it yourself first. Make a file named after the exercise (`Ex01.py`, `Ex02.py`, ...) in a folder of your own, and run it with `python Ex01.py`. For "predict the output" exercises, write your guess on paper before you run anything.
4. Stuck? Open only the hint for that exercise. Read it, then try again.
5. When you have an answer (or after a real try), open the worked answer and compare it with yours. Your code can be different and still right, as long as the output matches.
6. To run a ready-made solution, go into the solutions folder and run it:

```bash
cd solutions
python Ex07.py
```

Exercises 19 and 20 ask the person at the keyboard questions (`input()`). To test them without typing, pipe the answers in, as the sheet shows:

```bash
printf '5\n3\n2.5\n' | python Ex19.py
```

Because the answers are piped in, they do not show on the screen, so the questions run together. That is normal.

## Scoring yourself

16 to 20 working programs: you are ready for Module 3. Under 12: rewatch the lessons named above the exercises you missed. Exercises 3, 10 and 15 (reading error messages) are the best practice for every module that follows.

## Next

[M03-L01 · Making Decisions with if](../../m03-decisions-and-loops/m03-l01-making-decisions-with-if/)
