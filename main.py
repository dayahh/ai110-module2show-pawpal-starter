"""PawPal+ testing ground.

A small script that exercises the logic layer end to end: create pets, give
them care tasks, build a recommended daily plan, and print today's schedule.
"""

from datetime import date

from pawpal_system import Pet, DailyPlan


def main() -> None:
    # 1. Create at least two pets.
    rex = Pet.add_pet("Rex", "dog", 3)
    whiskers = Pet.add_pet("Whiskers", "cat", 5)

    # 2. Add at least three tasks (with different durations/priorities).
    rex.add_task("Morning walk", priority=2, duration_minutes=30)
    rex.add_task("Feed breakfast", priority=1, duration_minutes=15)
    whiskers.add_task("Clean litter box", priority=3, duration_minutes=10)
    whiskers.add_task("Give medication", priority=1, duration_minutes=5)

    # 3. Build a recommended schedule from every pet's tasks.
    all_tasks = rex.get_tasks() + whiskers.get_tasks()
    plan = DailyPlan(plan_id="plan-today", day=date.today())
    schedule = plan.recommend_schedule(all_tasks)

    # 4. Print "Today's Schedule".
    print(f"Today's Schedule ({schedule.date})")
    print("-" * 32)
    for task, start, end in schedule.tasks:
        start_str = start.strftime("%H:%M")
        end_str = end.strftime("%H:%M")
        print(f"{start_str}-{end_str}  (priority {task.priority})  {task.description}")


if __name__ == "__main__":
    main()
