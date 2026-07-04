from datetime import date, time

import streamlit as st

from pawpal_system import Pet, TaskSchedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant. Add your pets, give them
care tasks with a preferred time, and generate today's schedule. The scheduler
sorts tasks by time and warns you about any conflicts.
"""
)

# --- Application "memory" -------------------------------------------------
# Streamlit reruns this whole script on every interaction. Store state in
# st.session_state so it survives reruns instead of being recreated empty.
# The "check before create" pattern: only initialize a key if it's missing.
if "pets" not in st.session_state:
    st.session_state.pets = []
if "task_times" not in st.session_state:
    # Maps a task_id -> its preferred start time (chosen when the task is added).
    st.session_state.task_times = {}

# UI priorities are friendly words; the scheduler uses ints where a LOWER
# number means MORE important (so "high" must map to the smallest number).
PRIORITY_TO_INT = {"high": 1, "medium": 2, "low": 3}
INT_TO_PRIORITY = {value: key for key, value in PRIORITY_TO_INT.items()}

st.divider()

# --- Add a pet ------------------------------------------------------------
st.subheader("Add a pet")
col1, col2, col3 = st.columns(3)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    new_pet_age = st.number_input("Age", min_value=0, max_value=40, value=3)

if st.button("Add pet"):
    st.session_state.pets.append(
        Pet.add_pet(new_pet_name, new_pet_species, int(new_pet_age))
    )
    st.success(f"Added {new_pet_name} the {new_pet_species}.")

if not st.session_state.pets:
    st.info("No pets yet. Add one above to get started.")

st.divider()

# --- Add a task to a pet --------------------------------------------------
if st.session_state.pets:
    st.subheader("Add a task")

    # Map a display label to each pet so the selectbox can identify which one.
    pet_labels = {
        f"{pet.name} ({pet.species})": pet for pet in st.session_state.pets
    }
    chosen_label = st.selectbox("Which pet?", list(pet_labels.keys()))
    chosen_pet = pet_labels[chosen_label]

    tcol1, tcol2 = st.columns(2)
    with tcol1:
        task_title = st.text_input("Task title", value="Morning walk")
        priority_word = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    with tcol2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        start_time = st.time_input("Preferred start time", value=time(8, 0))
        due = st.date_input("Due date", value=date.today())

    if st.button("Add task"):
        new_task = chosen_pet.add_task(
            description=task_title,
            priority=PRIORITY_TO_INT[priority_word],
            duration_minutes=int(duration),
            frequency=frequency,
            due_date=due,
        )
        # Remember the preferred time for this task (used when scheduling).
        st.session_state.task_times[new_task.task_id] = start_time
        st.success(f"Added '{task_title}' for {chosen_pet.name} at {start_time.strftime('%H:%M')}.")

    # --- Current tasks, with a completion-status filter -------------------
    st.markdown("### Current pets and tasks")
    status_filter = st.radio(
        "Show tasks", ["All", "Pending", "Completed"], horizontal=True
    )
    # Translate the choice into the argument filter_tasks() expects.
    completed_arg = {"All": None, "Pending": False, "Completed": True}[status_filter]

    for pet in st.session_state.pets:
        tasks = pet.filter_tasks(completed=completed_arg)
        st.write(f"**{pet.name}** ({pet.species}, age {pet.age}) — {pet.task_count} task(s) total")
        if not tasks:
            st.caption("No tasks match this filter.")
            continue
        for task in tasks:
            status = "✅" if task.completed else "⬜"
            freq_note = "" if task.frequency == "once" else f", {task.frequency}"
            text_col, btn_col = st.columns([4, 1])
            with text_col:
                st.write(
                    f"{status} {task.description} — {task.duration_minutes} min, "
                    f"priority {INT_TO_PRIORITY[task.priority]}{freq_note}"
                )
            with btn_col:
                # Only pending tasks get a Complete button (completing a done
                # task again would wrongly spawn another recurrence).
                if not task.completed and st.button("Complete", key=f"done-{task.task_id}"):
                    next_task = pet.complete_task(task.task_id)
                    if next_task is not None:
                        # Carry the preferred time over to the next occurrence.
                        st.session_state.task_times[next_task.task_id] = (
                            st.session_state.task_times.get(task.task_id, time(8, 0))
                        )
                        st.success(
                            f"Completed '{task.description}'. Next {task.frequency} "
                            f"occurrence added for {next_task.due_date}."
                        )
                    else:
                        st.success(f"Completed '{task.description}'.")
                    st.rerun()

st.divider()

# --- Generate schedule ----------------------------------------------------
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    # Gather every task across all pets, remembering which pet each belongs to.
    pet_names = {pet.pet_id: pet.name for pet in st.session_state.pets}
    all_tasks = []
    for pet in st.session_state.pets:
        all_tasks.extend(pet.get_tasks())

    if not all_tasks:
        st.warning("No tasks to schedule yet. Add some tasks first.")
    else:
        # Place higher-priority tasks first, so on a clash the important one
        # keeps its slot and the other gets the conflict warning.
        all_tasks.sort(key=lambda task: task.priority)

        schedule = TaskSchedule(schedule_id="plan-today", day=date.today())
        conflicts = []
        for task in all_tasks:
            preferred = st.session_state.task_times.get(task.task_id, time(8, 0))
            warning = schedule.add_task_to_schedule(task, preferred)
            if warning:
                conflicts.append(f"{pet_names[task.pet_id]} — {warning}")

        # Show the schedule chronologically using the scheduler's own sort.
        schedule.sort_by_time()

        if conflicts:
            st.warning("Some tasks could not be scheduled due to time conflicts:")
            for message in conflicts:
                st.write(f"- {message}")
        else:
            st.success("All tasks scheduled with no conflicts. 🎉")

        rows = [
            {
                "Time": f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')}",
                "Pet": pet_names[task.pet_id],
                "Task": task.description,
                "Priority": INT_TO_PRIORITY[task.priority],
            }
            for task, start, end in schedule.tasks
        ]
        st.table(rows)
