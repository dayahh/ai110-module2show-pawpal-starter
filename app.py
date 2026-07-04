from datetime import date

import streamlit as st

from pawpal_system import Pet, DailyPlan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant. Add your pets, give them
care tasks, and generate a conflict-free schedule for the day.
"""
)

# --- Application "memory" -------------------------------------------------
# Streamlit reruns this whole script on every interaction. Store the pets in
# st.session_state so they survive reruns instead of being recreated empty.
# The "check before create" pattern: only initialize the list if it's not
# already in the session vault.
if "pets" not in st.session_state:
    st.session_state.pets = []

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

    tcol1, tcol2, tcol3 = st.columns(3)
    with tcol1:
        task_title = st.text_input("Task title", value="Morning walk")
    with tcol2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with tcol3:
        priority_word = st.selectbox("Priority", ["high", "medium", "low"])

    if st.button("Add task"):
        chosen_pet.add_task(
            description=task_title,
            priority=PRIORITY_TO_INT[priority_word],
            duration_minutes=int(duration),
        )

    # Show each pet and its current tasks (task_count comes from the property).
    st.markdown("### Current pets and tasks")
    for pet in st.session_state.pets:
        st.write(f"**{pet.name}** ({pet.species}, age {pet.age}) — {pet.task_count} task(s)")
        for task in pet.get_tasks():
            status = "✅" if task.completed else "⬜"
            st.write(
                f"&nbsp;&nbsp;{status} {task.description} "
                f"— {task.duration_minutes} min, priority {INT_TO_PRIORITY[task.priority]}",
                unsafe_allow_html=True,
            )

st.divider()

# --- Generate schedule ----------------------------------------------------
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    # Gather every task across all pets and let DailyPlan order and place them.
    all_tasks = []
    for pet in st.session_state.pets:
        all_tasks.extend(pet.get_tasks())

    if not all_tasks:
        st.warning("No tasks to schedule yet. Add some tasks first.")
    else:
        pet_names = {pet.pet_id: pet.name for pet in st.session_state.pets}
        plan = DailyPlan(plan_id="plan-today", day=date.today())
        schedule = plan.recommend_schedule(all_tasks)

        rows = []
        for task, start, end in schedule.tasks:
            rows.append(
                {
                    "Time": f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')}",
                    "Pet": pet_names[task.pet_id],
                    "Task": task.description,
                    "Priority": INT_TO_PRIORITY[task.priority],
                }
            )
        st.table(rows)
