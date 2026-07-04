"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care app. This module defines the core
data objects (Pet, PetTask) and the scheduling logic (TaskSchedule, DailyPlan).

Skeleton generated from diagrams/draft_uml.mmd.
"""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta


@dataclass
class PetTask:
    """A single care task for a specific pet. Pure data — owned by a Pet."""

    task_id: str
    pet_id: str
    description: str
    priority: int
    duration_minutes: int
    completed: bool = False
    frequency: str = "once"          # "once", "daily", or "weekly"
    due_date: date | None = None

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def create_next_occurrence(self) -> "PetTask | None":
        """Build a fresh (incomplete) task for this task's next occurrence.

        Returns None for a one-time task or one with no due_date. For a
        recurring task, advances the due date with timedelta: +1 day for
        "daily", +1 week for "weekly".
        """
        if self.due_date is None or self.frequency not in ("daily", "weekly"):
            return None

        step = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
        return PetTask(
            task_id=str(uuid.uuid4()),
            pet_id=self.pet_id,
            description=self.description,
            priority=self.priority,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            due_date=self.due_date + step,
        )


@dataclass
class Pet:
    """A pet being cared for. Owns the collection of its care tasks."""

    pet_id: str
    name: str
    species: str
    age: int
    tasks: list[PetTask] = field(default_factory=list)

    @property
    def task_count(self) -> int:
        """How many tasks this pet currently has."""
        return len(self.tasks)

    @staticmethod
    def add_pet(name: str, species: str, age: int) -> "Pet":
        """Create a new pet with a generated unique id and no tasks yet."""
        pet_id = str(uuid.uuid4())
        return Pet(pet_id=pet_id, name=name, species=species, age=age)

    def get_tasks(self) -> list[PetTask]:
        """Return all tasks associated with this pet."""
        return self.tasks

    def filter_tasks(self, completed: bool | None = None) -> list[PetTask]:
        """Return this pet's tasks, optionally filtered by completion status.

        completed=True  -> only completed tasks
        completed=False -> only pending tasks
        completed=None  -> all tasks (the default)
        """
        if completed is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.completed == completed]

    def add_task(
        self,
        description: str,
        priority: int,
        duration_minutes: int,
        frequency: str = "once",
        due_date: date | None = None,
    ) -> PetTask:
        """Create a task for this pet and add it to the collection."""
        task = PetTask(
            task_id=str(uuid.uuid4()),
            pet_id=self.pet_id,
            description=description,
            priority=priority,
            duration_minutes=duration_minutes,
            frequency=frequency,
            due_date=due_date,
        )
        self.tasks.append(task)
        return task

    def complete_task(self, task_id: str) -> "PetTask | None":
        """Mark one of this pet's tasks complete, spawning its next occurrence.

        Finds the task by id and marks it done. If it's a recurring task
        (daily/weekly), a new task for the next occurrence is created and
        added to this pet's collection. Returns the new task, or None if the
        task doesn't recur. Raises ValueError if the task_id isn't found.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    self.tasks.append(next_task)
                return next_task
        raise ValueError(f"No task with id {task_id}")

    def edit_task(self, task_id: str, updates: dict) -> PetTask:
        """Update fields on one of this pet's tasks, found by task_id.

        `updates` maps field names to new values. Raises ValueError if the
        task_id isn't found or a field name isn't editable.
        """
        editable = {"description", "priority", "duration_minutes"}
        for task in self.tasks:
            if task.task_id == task_id:
                for field_name, value in updates.items():
                    if field_name not in editable:
                        raise ValueError(f"Cannot edit field: {field_name}")
                    setattr(task, field_name, value)
                return task
        raise ValueError(f"No task with id {task_id}")

    def delete_task(self, task_id: str) -> bool:
        """Remove one of this pet's tasks by task_id. Returns True if deleted."""
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[i]
                return True
        return False


class TaskSchedule:
    """Holds the ordered list of tasks assigned to time slots for a given day."""

    def __init__(self, schedule_id: str, day: date) -> None:
        self.schedule_id: str = schedule_id
        self.date: date = day
        # Each entry is (task, start, end) so we can check for overlaps.
        self.tasks: list[tuple[PetTask, datetime, datetime]] = []

    def add_task_to_schedule(self, task: PetTask, start_time: time) -> str | None:
        """Place a task at start_time on this schedule's day.

        Uses the task's duration_minutes to compute its end time. If it would
        overlap a task already scheduled, the task is NOT placed and a warning
        message is returned instead of crashing. Returns None when the task is
        placed with no conflict.
        """
        start = datetime.combine(self.date, start_time)
        end = start + timedelta(minutes=task.duration_minutes)
        for scheduled_task, other_start, other_end in self.tasks:
            # Two intervals overlap when each starts before the other ends.
            if start < other_end and other_start < end:
                return (
                    f"Conflict: '{task.description}' "
                    f"({start.strftime('%H:%M')}-{end.strftime('%H:%M')}) conflicts with "
                    f"'{scheduled_task.description}' "
                    f"({other_start.strftime('%H:%M')}-{other_end.strftime('%H:%M')})"
                )
        self.tasks.append((task, start, end))
        return None

    def sort_by_time(self) -> list[tuple[PetTask, datetime, datetime]]:
        """Sort the scheduled tasks by their start time (earliest first).

        Sorts on the start time formatted as an "HH:MM" string. Zero-padded
        24-hour times sort the same lexically as chronologically, so a plain
        string comparison gives the correct order. Sorts in place and also
        returns the list.
        """
        self.tasks.sort(key=lambda entry: entry[1].strftime("%H:%M"))
        return self.tasks


class DailyPlan:
    """Produces a recommended care schedule from a set of tasks."""

    def __init__(self, plan_id: str, day: date) -> None:
        self.plan_id: str = plan_id
        self.date: date = day
        self.ordered_tasks: list[PetTask] = []

    def recommend_schedule(
        self, tasks: list[PetTask], day_start: time = time(8, 0)
    ) -> TaskSchedule:
        """Order tasks by priority and lay them out back-to-back.

        Lower priority numbers are treated as more important, so they get
        scheduled earlier in the day. Tasks are placed one after another
        starting at day_start, using each task's duration_minutes.
        """
        ordered = sorted(tasks, key=lambda task: task.priority)

        schedule = TaskSchedule(schedule_id=str(uuid.uuid4()), day=self.date)
        cursor = datetime.combine(self.date, day_start)
        for task in ordered:
            schedule.add_task_to_schedule(task, cursor.time())
            cursor += timedelta(minutes=task.duration_minutes)

        self.ordered_tasks = ordered
        return schedule
