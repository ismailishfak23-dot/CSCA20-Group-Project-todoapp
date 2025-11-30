import streamlit as st
def show():
 st.title("Goals Overview")
 st.header("Set and Track Your Financial Goals")

goal_name = st.text_input("Enter your goal name:")
target_amount = st.number_input("Enter the target amount for your goal:", min_value=0.0, step=0.01)
current_amount = st.number_input("Enter your current amount saved towards this goal:", min_value=0.0, step=0.01)
target_date = st.date_input("Select a target date for achieving this goal:")

if "goals" not in st.session_state:
    st.session_state.goals = []

if st.button("Add Goal"):
    st.session_state.goals.append({
        "name": goal_name,
        "target": target_amount,
        "current": current_amount,
        "date": target_date
    })
    st.success(f"Goal '{goal_name}' with target amount ${target_amount} added!")

# This is displaying  all the goals
if st.session_state.goals:
    st.subheader("Your Goals")
    for goal in st.session_state.goals:
        st.write(f"{goal['name']}: ${goal['current']}/{goal['target']} by {goal['date']}")
