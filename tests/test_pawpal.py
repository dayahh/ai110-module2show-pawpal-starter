"""Simple tests for the PawPal+ logic layer."""

from pawpal_system import Pet


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
