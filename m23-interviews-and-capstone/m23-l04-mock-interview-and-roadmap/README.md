# M23-L04 · Mock Interview and Roadmap

> Video: Module 23, Lesson 4. Watch it first, then follow along here.

## What you'll learn
- How a full mock interview runs, in five short rounds, with Rahul as the interviewer and Asha as the candidate
- What made each answer good, and what to improve
- The shape of a good answer: say the rule or the plan first, show one small proof, name what you would still check
- A coding problem solved with the five steps (longest streak of days), with real runs and a measurement
- A roadmap of five directions to learn next, each with a first step small enough for this week

## Before you start
- Python 3.14 or newer. Check with `python --version`.
- Standard library only: no packages, no Docker.
- Lessons [M23-L01](../m23-l01-the-python-gotchas/) to [M23-L03](../m23-l03-the-backend-interview-round/) help but are not required.
- All commands run from inside this folder. For the rounds that are spoken answers, practise out loud with a timer.

## Files in this folder
| File | What it is |
|---|---|
| `done_shared.py` | Round 2, question 1: a list in the class body is shared by every student |
| `done_fixed.py` | The fix: make the list inside `__init__` |
| `plan_shallow.py` | Round 2, question 2: `dict(plan)` is a shallow copy |
| `plan_deep.py` | The fix: `copy.deepcopy` |
| `streak_v1.py` | Round 3, brute force: `longest_streak` with a list |
| `streak_v2.py` | Round 3, improved: a set, and start counting only at the start of a run |
| `try_v1.py`, `try_examples.py` | The two hand examples run against v1 and v2 |
| `edge_cases.py` | Five edge cases against v2 |
| `timing.py` | Times v1 against v2 on 1000, 4000 and 16000 days (timings depend on your machine) |

## Follow along
The plan: a real interview runs about an hour, so each round is shortened. Round 1 an opening question, round 2 Python
questions, round 3 a coding problem, round 4 a design question, round 5 a question about the past. Asha follows one rule in
every round: **think out loud**. An interviewer can only grade what they can hear. A calm answer with its reasoning, even a
half-right one, usually beats a silent, perfect one.

### Round 1: "Tell me about yourself, and about something you built"
Asha: "I am a backend developer. For the last months I have been building allcsvideos, a course platform: a FastAPI
service with Postgres, logins, a Redis cache, a background worker for emails, and a deployment pipeline. I am proudest that
it is tested and observable, so when something is slow, I can see where. Next, I want a team where I keep building
services like this, and learn from people who have run them for years."

- **Good:** under a minute, with a shape (who I am, what I built, what I want next), real pieces and no buzzwords.
- **Improve:** add one result you measured, such as a time before and after. A number makes a claim believable.

### Round 2: two quick Python questions
**Question 1.** A class `Student` has a list `done` written in the class body. Asha creates Lukas and Priya, and adds
`"lesson 1"` to Lukas's list. Guess what Priya's list shows, then run:
```bash
python done_shared.py
```
```
['lesson 1']
True
```
Priya's list shows `lesson 1` too, and the two lists are the very same object. A list written in the class body belongs to
the class, so every student shares it (M08-L02). The fix is `self.done = []` inside `__init__`:
```bash
python done_fixed.py
```
```
[]
['lesson 1']
```

**Question 2.** A student's plan is a dictionary with a list of courses inside. Asha copies it with `dict(plan)` and adds
`"SQL"` to the copy. Is the original changed?
```bash
python plan_shallow.py
```
```
['Python', 'SQL']
```
Yes. A copy made like this is shallow: it copies the outer dictionary, but the list inside is shared (M05-L06). A deep copy
copies everything inside too:
```bash
python plan_deep.py
```
```
['Python']
['Python', 'SQL']
```
The first line is the original (unchanged), the second the deep copy.

- **Good:** the rule in one sentence, then a tiny proof anyone can run.
- **Improve:** Rahul always follows up with "when would you not use deep copy?". Be ready: when the data is big, because it
  is slow, and when sharing is exactly what you want.

### Round 3: the coding problem
Rahul: "Lukas studies on some days. You get the day numbers, as a list of whole numbers, in any order. Return the longest
run of days in a row. For example `[1, 2, 3, 10, 11]` gives 3."

**Step 1, clarify.** Asha does not start typing. Can a day appear twice? Yes. Can the list be empty? Yes, and then the
answer is 0. Is it sorted? No. Three questions, and three assumptions that would have been bugs.

**Step 2, an example by hand, with a trap:** `[7, 3, 4, 5, 9, 6]`. Guess the longest run. It is 5: the days 3, 4, 5, 6
and 7 are all there, just not in order. The order of the list does not matter, only which days exist.

**Step 3, brute force** (`streak_v1.py`). For each day, count upwards (day + 1, day + 2...) for as long as that day is in
the list, and keep the best count.
```bash
python try_v1.py
```
```
3
5
```
It is simple and correct, so it is a good first answer. But is it fast? Looking for a day in a list means looking at the
items one by one, and a long run asks that question again and again. So the work grows at least with the square of the list
length: at least O(n squared).

**Step 4, improve** (`streak_v2.py`). Two ideas. First, put the days in a set (M05-L04): asking whether a day is in a set is
fast. Second, only start counting at the start of a run, a day whose previous day is missing. Then every day is counted once.
```bash
python try_examples.py
```
```
3
5
```
Same answers, new code.

**Step 5, test the edge cases.** Predict each before you run it: empty list, one day, duplicates, negative numbers, a gap.
```bash
python edge_cases.py
```
```
empty -> 0
one day -> 1
duplicates -> 2
negative -> 4
gaps -> 3
```

**The proof: measure.** Random days, best of several runs, v1 (list) against v2 (set):
```bash
python timing.py
```
The video's run printed:
```
  1000 days: list      9.0 ms | set   0.06 ms
  4000 days: list    189.2 ms | set   0.33 ms
 16000 days: list   2676.8 ms | set   1.37 ms
```
Your numbers will differ, but the shape will not. Four times more days made the list version about 20 times slower, and
then about 14 times slower. That is far more than four times: that is the square.

**Say the big O honestly.** The set version is O(n) on average, because set lookups are fast on average. Sorting the days
first and walking through them once is O(n log n): it needs no set, is easy to get right, and many interviewers are happy
with it. Say both, and say which you would choose and why.

- **Good:** questions first, an example, brute force first, an improvement with a reason, edge cases, a measurement.
- **Improve:** say the complexity before the interviewer asks, and write the test as code, not only as a spoken list.

### Round 4: a design question, "the My Courses page is slow. What do you do?"
Asha does not guess. Five steps:
1. **Ask.** Slow for everyone, or some students? Since when? How slow?
2. **Measure,** with what M20 taught: the metrics, a trace, the slow query.
3. **Find the cause.**
4. **Change one thing.**
5. **Measure again,** to prove it worked.

The usual causes, each with its fix:
- Many small queries, one per course (the N+1 problem, M16-L03): load them together.
- A missing index: add one, and check the plan.
- The same answer asked again and again: a cache (M18-L01).
- Too much data in one answer: pagination.

The cache comes last, because it hides the problem and adds a new one: old data.

- **Good:** questions before answers, measure before fixing, one change at a time, a check afterwards.
- **Improve:** for each fix, say what could go wrong and what you will watch afterwards. For a cache: how old may the data be?

### Round 5: "Tell me about a bug you shipped"
This is not a trap. Everyone has shipped one. Rahul wants to hear how you think about a mistake. Asha uses STAR:
Situation, Task, Action, Result.
- **Situation:** I built the email worker for enrollments, and after a restart, some students got the same confirmation twice.
- **Task:** stop the duplicates, without losing any email.
- **Action:** the worker had tried the job again after it stopped halfway. I saved a marker for each enrollment, made the
  worker check it first, and added a test that runs the job twice.
- **Result:** the next restart sent no duplicates, and now, for every job, I ask: what if this runs twice?

- **Good:** she owns it ("I shipped", no blame), the action is specific, the lesson is a habit, not a sentence.
- **Improve:** keep it under two minutes, and say the result in one line first, because Rahul may stop you at any moment.

### The secret of all five answers
Asha did three things every time: she said the rule or the plan before the details; she showed one small proof (a real run,
a measured number, or a test); and she named what she would still check. You can practise this alone, out loud, with a timer.

### The last question: "Do you have any questions for us?"
Say yes, and ask two real ones: "How does your team ship a change to production, and what happens when it goes wrong?" and
"What would my first month look like?" Interviews go both ways: you are also choosing a team.

### The roadmap: five directions, one first step each
| Direction | Honest sentence | First step this week |
|---|---|---|
| Data and machine learning | M22 gave a taster with pandas. This field has its own maths, so do not rush it | Take a public data set, answer three questions with pandas, draw one chart |
| Deeper async | M12 gave the ideas. Next come timeouts, cancelling work and task groups | Rebuild the link checker from M12-B06 with a task group and a timeout, and measure it |
| Rust for Python | You write a small fast piece in Rust and call it from Python (PyO3 and maturin). You will rarely need it: only when a profile shows one hot loop nothing else fixes | Learn the basics of Rust, then make one tiny function Python can call |
| Language models | You already know every piece around a call to one: a request with a timeout, retries, a cache, a rate limit, a test with a fake answer. The model is one more unreliable call over the network | Call one with `httpx`, add a timeout, test it with a fake answer |
| Open source | M21-L03 showed the whole flow. Your first pull request may wait days for an answer | Pick a small library you already use and fix one typo in its documentation |

### A look back
Module 1: a five-line script that prints a welcome banner. Module 3: a number guessing game. Module 13: tests written before
the code. Module 15: your first endpoint. Module 16: a real database, so a second click on Enroll gets a clear answer, not a
second row. Module 19: a pipeline that tests and deploys with a safe way back. Module 20: a service that tells you how it
feels. Module 21: a tool installed from a package index with one command. Module 22: a bot that emails the report every
Monday. From five lines to a deployed, tested, observable service. You will not remember all of it, and nobody does. What
you have now is better: you know where every idea lives and why it exists, so you can find it again in minutes.

## Common mistakes
1. Going silent for a minute, or answering a question nobody asked. A mock interview finds this cheaply.
2. Starting to code before asking questions and working an example.
3. Giving an answer with no proof: no run, no number, no test.
4. Telling a long story. Keep stories under two minutes, with the result first.
5. Blaming others in the "bug I shipped" story. Say "I shipped".
6. Fixing a slow page with a cache before measuring.
7. Answering "any questions for us?" with "no".

## Try it yourself
1. Answer the five rounds out loud, alone, and time yourself.
2. Solve one more problem from the [final practice sheet](../../practice/m23-interviews-and-capstone/) with the same five steps.
3. Pick one direction from the roadmap and do its first step this week.
4. Change `longest_streak` to also return the first day of the longest run, and test it with `edge_cases.py` style cases.

## Clean up
Nothing to clean up. The files only print to the screen. (Delete a `__pycache__` folder if Python made one.)

## Next
That finishes the lessons. Next is the capstone build, from an empty folder:
[M23-B16 · Capstone: Course Copilot-lite](../m23-b16-capstone-course-copilot-lite/).
