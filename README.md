# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
Me example is below:
'''
Today's Schedule (2026-07-04)
--------------------------------
08:00-08:15  (priority 1)  Feed breakfast
08:15-08:20  (priority 1)  Give medication
08:20-08:50  (priority 2)  Morning walk
08:50-09:00  (priority 3)  Clean litter box
'''

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

**Confidence level:** 4 / 5

Sample test output:

```
platform win32 -- Python 3.13.1, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\ohday\Desktop\CodePath\AI-Class2026\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 8 items

tests\test_pawpal.py ........                                                                              [100%]

======================================= 8 passed in 0.04s =======================================
```

## 📐 Smarter Scheduling

The scheduling logic lives in `pawpal_system.py`. Each feature below names the
method that implements it.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `DailyPlan.recommend_schedule()`, `TaskSchedule.sort_by_time()` | `recommend_schedule` orders tasks by priority (lower number = more important) and lays them out back-to-back from a start time; `sort_by_time` reorders an existing schedule chronologically by start time. |
| Filtering | `Pet.filter_tasks(completed=...)` | Returns a pet's tasks filtered by completion status (`True` = done, `False` = pending, `None` = all). Filtering *by pet* is inherent to the design — each `Pet` owns its own tasks, so choosing the pet is the filter. |
| Conflict handling | `TaskSchedule.add_task_to_schedule()` | Computes each task's end time from its `duration_minutes` and checks for overlaps. On a conflict it returns a warning message (and skips the task) instead of crashing; returns `None` when placed cleanly. |
| Recurring tasks | `PetTask.create_next_occurrence()`, `Pet.complete_task()` | `create_next_occurrence` uses `timedelta` to advance the due date (+1 day for `"daily"`, +1 week for `"weekly"`). `complete_task` marks a task done and, if it recurs, adds the next occurrence to the pet's task list. One-time tasks (`"once"`) spawn nothing. |

## 📸 Demo Walkthrough

PawPal+ has a Streamlit UI (`app.py`) and a command-line test harness (`main.py`).

### What you can do in the app

- **Add a pet** — name, species, and age. Pets persist across interactions using `st.session_state`.
- **Add a task to a pet** — title, priority (high / medium / low), duration, a preferred start time, and a frequency (once / daily / weekly) with a due date.
- **Filter tasks** — a radio toggle shows All / Pending / Completed tasks, backed by `Pet.filter_tasks()`.
- **Complete a task** — a per-task "Complete" button marks it done; for a daily or weekly task it automatically adds the next occurrence.
- **Generate today's schedule** — places every task at its preferred time, sorts the result chronologically, and displays it in a table.

### Example workflow

1. **Add a pet** — e.g. "Rex", a dog, age 3.
2. **Add a task** — "Morning walk", high priority, 30 min, starting at 08:00, frequency "daily".
3. **Add another task** at an overlapping time — e.g. "Vet call" starting at 08:15 — to see conflict handling.
4. **Filter** the task list to *Pending* to confirm the new tasks show up.
5. **Click Generate schedule** — the higher-priority task keeps its slot; the overlapping one raises a conflict warning.
6. **Click Complete** on the daily task — it's marked done and the next day's occurrence appears automatically.

### Key scheduler behaviors shown

- **Sorting** — the schedule table is ordered by start time (`TaskSchedule.sort_by_time()`), and the daily plan orders by priority (`DailyPlan.recommend_schedule()`).
- **Conflict warnings** — overlapping tasks are reported with a readable message instead of crashing (`TaskSchedule.add_task_to_schedule()`); a clean run shows an "all scheduled" success message.
- **Filtering** — tasks can be viewed by completion status (`Pet.filter_tasks()`).
- **Recurring tasks** — completing a daily/weekly task spawns its next occurrence (`Pet.complete_task()` + `PetTask.create_next_occurrence()`).

### Sample CLI output (`python main.py`)

`main.py` exercises the logic layer directly — sorting a schedule that was built out of order, filtering by completion status, and detecting a time conflict:

```
BEFORE sort_by_time (insertion order):
----------------------------------------
09:00-09:30  Rex: Morning walk
07:00-07:15  Rex: Feed breakfast
10:00-10:10  Whiskers: Clean litter box
08:00-08:05  Whiskers: Give medication

AFTER sort_by_time (chronological):
----------------------------------------
07:00-07:15  Rex: Feed breakfast
08:00-08:05  Whiskers: Give medication
09:00-09:30  Rex: Morning walk
10:00-10:10  Whiskers: Clean litter box

Rex has 2 task(s) total.
Completed: ['Morning walk', 'Feed breakfast']
Pending:   []

Attempting to schedule 'Vet phone call' at 09:15 (overlaps the walk)...
Conflict: 'Vet phone call' (09:15-09:35) conflicts with 'Morning walk' (09:00-09:30)
```
