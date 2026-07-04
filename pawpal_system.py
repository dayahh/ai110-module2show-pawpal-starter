"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care app. This module defines the core
data objects (Pet, PetTask) and the scheduling logic (TaskSchedule, DailyPlan).

Skeleton generated from diagrams/draft_uml.mmd — method bodies are stubs.
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

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


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

    def add_task(self, description: str, priority: int, duration_minutes: int) -> PetTask:
        """Create a task for this pet and add it to the collection."""
        task = PetTask(
            task_id=str(uuid.uuid4()),
            pet_id=self.pet_id,
            description=description,
            priority=priority,
            duration_minutes=duration_minutes,
        )
        self.tasks.append(task)
        return task

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

    def add_task_to_schedule(self, task: PetTask, start_time: time) -> bool:
        """Place a task at start_time on this schedule's day.

        Uses the task's duration_minutes to compute its end time and rejects
        the task (returns False) if it overlaps one that's already scheduled.
        Returns True when the task is placed successfully.
        """
        start = datetime.combine(self.date, start_time)
        end = start + timedelta(minutes=task.duration_minutes)
        for _scheduled, other_start, other_end in self.tasks:
            # Two intervals overlap when each starts before the other ends.
            if start < other_end and other_start < end:
                return False
        self.tasks.append((task, start, end))
        return True


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
