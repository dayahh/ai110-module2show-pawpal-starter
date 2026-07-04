"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care app. This module defines the core
data objects (Pet, PetTask) and the scheduling logic (TaskSchedule, DailyPlan).

Skeleton generated from diagrams/draft_uml.mmd — method bodies are stubs.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Pet:
    """A pet being cared for."""

    pet_id: str
    name: str
    species: str
    age: int

    @staticmethod
    def add_pet(name: str, species: str, age: int) -> "Pet":
        """Create and register a new pet."""
        pass

    def get_tasks(self) -> list["PetTask"]:
        """Return all tasks associated with this pet."""
        pass


@dataclass
class PetTask:
    """A single care task for a specific pet."""

    task_id: str
    pet_id: str
    description: str
    priority: int
    duration_minutes: int

    @staticmethod
    def add_task(pet_id: str, description: str, priority: int) -> "PetTask":
        """Create a new task for a pet."""
        pass

    def edit_task(self, task_id: str, updates: dict) -> "PetTask":
        """Update fields on an existing task."""
        pass

    def delete_task(self, task_id: str) -> bool:
        """Remove a task. Returns True if a task was deleted."""
        pass


class TaskSchedule:
    """Holds the ordered list of tasks assigned to time slots for a given day."""

    def __init__(self, schedule_id: str, day: date) -> None:
        self.schedule_id: str = schedule_id
        self.date: date = day
        self.tasks: list[PetTask] = []

    def add_task_to_schedule(self, task: PetTask, time_slot: str) -> bool:
        """Place a task into a time slot on the schedule. Returns True on success."""
        pass


class DailyPlan:
    """Produces a recommended care schedule from a set of tasks."""

    def __init__(self, plan_id: str, day: date) -> None:
        self.plan_id: str = plan_id
        self.date: date = day
        self.ordered_tasks: list[PetTask] = []

    def recommend_schedule(self, tasks: list[PetTask]) -> TaskSchedule:
        """Order and place tasks into a recommended TaskSchedule."""
        pass
