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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
