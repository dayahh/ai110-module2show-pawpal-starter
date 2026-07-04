"""Simple tests for the PawPal+ logic layer."""

from datetime import date, time

from pawpal_system import DailyPlan, Pet, TaskSchedule


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task from not-done to done."""
    pet = Pet.add_pet("Rex", "dog", 3)
    task = pet.add_task("Morning walk", priority=1, duration_minutes=30)

    assert task.completed is False   # starts incomplete

    task.mark_complete()

    assert task.completed is True    # now complete


def test_add_task_increases_task_count():
    """Adding a task to a Pet should increase that pet's task_count by one."""
    pet = Pet.add_pet("Whiskers", "cat", 5)

    assert pet.task_count == 0       # no tasks yet

    pet.add_task("Feed breakfast", priority=1, duration_minutes=15)

    assert pet.task_count == 1       # one task after adding


# --- Sorting correctness ---------------------------------------------------


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should order scheduled tasks earliest start first."""
    pet = Pet.add_pet("Rex", "dog", 3)
    evening = pet.add_task("Evening walk", priority=1, duration_minutes=30)
    morning = pet.add_task("Morning walk", priority=2, duration_minutes=30)

    schedule = TaskSchedule(schedule_id="s1", day=date(2026, 7, 4))
    # Add out of chronological order on purpose.
    schedule.add_task_to_schedule(evening, time(17, 0))
    schedule.add_task_to_schedule(morning, time(8, 0))

    ordered = schedule.sort_by_time()

    start_times = [start.time() for _task, start, _end in ordered]
    assert start_times == [time(8, 0), time(17, 0)]
    assert ordered[0][0] is morning
    assert ordered[1][0] is evening


def test_recommend_schedule_orders_by_priority_back_to_back():
    """DailyPlan should place lower-priority-number tasks first, back-to-back."""
    pet = Pet.add_pet("Rex", "dog", 3)
    low = pet.add_task("Low priority", priority=3, duration_minutes=30)
    high = pet.add_task("High priority", priority=1, duration_minutes=15)

    plan = DailyPlan(plan_id="p1", day=date(2026, 7, 4))
    schedule = plan.recommend_schedule([low, high], day_start=time(8, 0))

    ordered = schedule.sort_by_time()
    tasks = [entry[0] for entry in ordered]
    starts = [entry[1].time() for entry in ordered]

    # High priority (1) scheduled first at day_start, then low priority after.
    assert tasks == [high, low]
    assert starts == [time(8, 0), time(8, 15)]


# --- Recurrence logic ------------------------------------------------------


def test_complete_daily_task_creates_next_day_occurrence():
    """Completing a daily task should spawn a fresh task due the next day."""
    pet = Pet.add_pet("Rex", "dog", 3)
    task = pet.add_task(
        "Morning walk",
        priority=1,
        duration_minutes=30,
        frequency="daily",
        due_date=date(2026, 7, 4),
    )

    next_task = pet.complete_task(task.task_id)

    assert task.completed is True                 # original marked done
    assert next_task is not None                  # a new occurrence was made
    assert next_task.completed is False           # new one starts incomplete
    assert next_task.due_date == date(2026, 7, 5)  # advanced by one day
    assert pet.task_count == 2                     # original + next occurrence


def test_complete_once_task_creates_no_occurrence():
    """A one-time task should not spawn a follow-up when completed."""
    pet = Pet.add_pet("Rex", "dog", 3)
    task = pet.add_task(
        "Vet visit",
        priority=1,
        duration_minutes=60,
        frequency="once",
        due_date=date(2026, 7, 4),
    )

    next_task = pet.complete_task(task.task_id)

    assert next_task is None
    assert pet.task_count == 1


# --- Conflict detection ----------------------------------------------------


def test_duplicate_start_time_is_flagged_and_not_added():
    """Two tasks at the exact same time: the second is rejected with a warning."""
    pet = Pet.add_pet("Rex", "dog", 3)
    first = pet.add_task("Feed", priority=1, duration_minutes=30)
    second = pet.add_task("Walk", priority=2, duration_minutes=30)

    schedule = TaskSchedule(schedule_id="s1", day=date(2026, 7, 4))

    assert schedule.add_task_to_schedule(first, time(8, 0)) is None   # placed
    warning = schedule.add_task_to_schedule(second, time(8, 0))       # conflict

    assert warning is not None
    assert "Conflict" in warning
    assert len(schedule.tasks) == 1   # second task was NOT scheduled


def test_back_to_back_tasks_do_not_conflict():
    """A task starting exactly when another ends should be allowed."""
    pet = Pet.add_pet("Rex", "dog", 3)
    first = pet.add_task("Feed", priority=1, duration_minutes=30)   # 08:00-08:30
    second = pet.add_task("Walk", priority=2, duration_minutes=30)  # 08:30-09:00

    schedule = TaskSchedule(schedule_id="s1", day=date(2026, 7, 4))

    assert schedule.add_task_to_schedule(first, time(8, 0)) is None
    assert schedule.add_task_to_schedule(second, time(8, 30)) is None
    assert len(schedule.tasks) == 2
