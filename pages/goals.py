import streamlit as st
# import pandas as pd # Add other imports as needed

# Initialize session state for goals ONCE when the script runs
if "goals" not in st.session_state:
    st.session_state.goals = []

# --- Page Content Starts Here ---
st.title("Goals Overview")
st.header("Set and Track Your Financial Goals")

# Goal Input Form
with st.form("goal_form", clear_on_submit=True):
    goal_name = st.text_input("Enter your goal name:")
    target_amount = st.number_input("Enter the target amount for your goal:", min_value=0.0, step=0.01)
    current_amount = st.number_input("Enter your current amount saved towards this goal:", min_value=0.0, step=0.01)
    target_date = st.date_input("Select a target date for achieving this goal:")
    
    submitted = st.form_submit_button("Add Goal")

    if submitted and goal_name: # Check if button was pressed and goal has a name
        st.session_state.goals.append({
            "name": goal_name,
            "target": target_amount,
            "current": current_amount,
            "date": target_date
        })
        st.success(f"Goal '{goal_name}' with target amount ${target_amount:.2f} added!")
    elif submitted and not goal_name:
        st.error("Please enter a name for your goal.")


# Display Goals
if st.session_state.goals:
    st.subheader("Your Active Goals")
    for goal in st.session_state.goals:
        # Calculate progress percentage
        try:
            progress = goal['current'] / goal['target'] if goal['target'] > 0 else 0
        except ZeroDivisionError:
            progress = 0

        st.markdown(f"**{goal['name']}**")
        st.write(f"Target: \${goal['target']:.2f} | Current: \${goal['current']:.2f} | Deadline: {goal['date']}")
        st.progress(progress)