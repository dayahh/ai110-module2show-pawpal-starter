"""PawPal+ testing ground.

Exercises the logic layer end to end: create pets, give them care tasks,
place those tasks on a schedule OUT OF ORDER, then use sort_by_time() and
filter_tasks() to prove the sorting and filtering methods work.
"""

from datetime import date, time

from pawpal_system import Pet, TaskSchedule


def print_schedule(title: str, schedule: TaskSchedule, pet_names: dict) -> None:
    """Print a schedule's entries in their current order."""
    print(title)
    print("-" * 40)
    for task, start, end in schedule.tasks:
        start_str = start.strftime("%H:%M")
        end_str = end.strftime("%H:%M")
        print(f"{start_str}-{end_str}  {pet_names[task.pet_id]}: {task.description}")
    print()


def main() -> None:
    # 1. Create two pets and give them tasks.
    rex = Pet.add_pet("Rex", "dog", 3)
    whiskers = Pet.add_pet("Whiskers", "cat", 5)

    walk = rex.add_task("Morning walk", priority=2, duration_minutes=30)
    feed = rex.add_task("Feed breakfast", priority=1, duration_minutes=15)
    litter = whiskers.add_task("Clean litter box", priority=3, duration_minutes=10)
    meds = whiskers.add_task("Give medication", priority=1, duration_minutes=5)

    pet_names = {rex.pet_id: rex.name, whiskers.pet_id: whiskers.name}

    # 2. Place the tasks on a schedule OUT OF ORDER (times not increasing).
    schedule = TaskSchedule(schedule_id="sched-today", day=date.today())
    schedule.add_task_to_schedule(walk, time(9, 0))     # 09:00
    schedule.add_task_to_schedule(feed, time(7, 0))     # 07:00  (earlier!)
    schedule.add_task_to_schedule(litter, time(10, 0))  # 10:00
    schedule.add_task_to_schedule(meds, time(8, 0))     # 08:00  (out of order)

    # 3. Show they were added out of order, then sort by time.
    print_schedule("BEFORE sort_by_time (insertion order):", schedule, pet_names)
    schedule.sort_by_time()
    print_schedule("AFTER sort_by_time (chronological):", schedule, pet_names)

    # 4. Mark some tasks complete, then filter by completion status.
    feed.mark_complete()
    walk.mark_complete()

    print(f"Rex has {rex.task_count} task(s) total.")
    print("Completed:", [task.description for task in rex.filter_tasks(completed=True)])
    print("Pending:  ", [task.description for task in rex.filter_tasks(completed=False)])
    print()

    # 5. Try to schedule two tasks at the same time and confirm we get a warning.
    # "Morning walk" already occupies 09:00-09:30, so scheduling this at 09:15 overlaps it.
    vet_call = rex.add_task("Vet phone call", priority=1, duration_minutes=20)
    print("Attempting to schedule 'Vet phone call' at 09:15 (overlaps the walk)...")
    warning = schedule.add_task_to_schedule(vet_call, time(9, 15))
    if warning:
        print(warning)
    else:
        print("Scheduled with no conflict.")


if __name__ == "__main__":
    main()
