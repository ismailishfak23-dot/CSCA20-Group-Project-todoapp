import streamlit as st
import pandas as pd

# --- Initialize User Data ---
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "goals" not in st.session_state.user_data:
    st.session_state.user_data["goals"] = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

if "editing_goal" not in st.session_state:
    st.session_state.editing_goal = None

goals = st.session_state.user_data["goals"]

# --- Page Title ---
st.title("🎯 Financial Goals Tracker")
st.subheader("Track, edit, and achieve your goals! 🚀")

# --- Tabs for Short-term and Long-term ---
tab1, tab2 = st.tabs(["Short-term Goals", "Long-term Goals"])

for tab, goal_type in zip([tab1, tab2], ["Short-term", "Long-term"]):
    with tab:
        st.markdown(f"### {goal_type} Goals")

        # --- Add/Edit Goal Form ---
        with st.form(f"{goal_type}_goal_form", clear_on_submit=True):
            if st.session_state.editing_goal and st.session_state.editing_goal["type"] == goal_type:
                goal_to_edit = st.session_state.editing_goal
                name = st.text_input("Goal Name", value=goal_to_edit["name"])
                target_amount = st.number_input("Target Amount ($)", min_value=0.0, step=0.01, value=goal_to_edit["target"])
                current_amount = st.number_input("Current Saved ($)", min_value=0.0, step=0.01, value=goal_to_edit["current"])
                target_date = st.date_input("Target Date", value=pd.to_datetime(goal_to_edit["date"]))
                submitted = st.form_submit_button("💾 Save Changes")
                
                if submitted:
                    idx = st.session_state.edit_index
                    st.session_state.user_data["goals"][idx] = {
                        "name": name,
                        "target": target_amount,
                        "current": current_amount,
                        "date": str(target_date),
                        "type": goal_type
                    }
                    st.success(f"Goal '{name}' updated!")
                    st.session_state.edit_index = None
                    st.session_state.editing_goal = None
                    st.experimental_rerun()
            else:
                name = st.text_input("Goal Name")
                target_amount = st.number_input("Target Amount ($)", min_value=0.0, step=0.01)
                current_amount = st.number_input("Current Saved ($)", min_value=0.0, step=0.01)
                target_date = st.date_input("Target Date")
                submitted = st.form_submit_button("➕ Add Goal")

                if submitted and name:
                    st.session_state.user_data["goals"].append({
                        "name": name,
                        "target": target_amount,
                        "current": current_amount,
                        "date": str(target_date),
                        "type": goal_type
                    })
                    st.success(f"Goal '{name}' added! 🎉")
                    st.experimental_rerun()

        # --- Display Existing Goals ---
        filtered_goals = [g for g in st.session_state.user_data["goals"] if g["type"] == goal_type]
        
        if filtered_goals:
            st.markdown("#### Existing Goals")
            for i, goal in enumerate(filtered_goals):
                progress = min(goal["current"]/goal["target"], 1) if goal["target"] > 0 else 0
                st.markdown(f"**{goal['name']}** — Target: ${goal['target']:.2f} | Saved: ${goal['current']:.2f} | Due: {goal['date']}")
                st.progress(progress)

                # --- Edit/Delete Buttons ---
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button(f"✏️ Edit {goal['name']}", key=f"edit_{goal_type}_{i}"):
                        st.session_state.edit_index = i
                        st.session_state.editing_goal = goal
                        st.experimental_rerun()
                with col2:
                    if st.button(f"🗑️ Delete {goal['name']}", key=f"delete_{goal_type}_{i}"):
                        st.session_state.user_data["goals"].remove(goal)
                        st.success(f"Goal '{goal['name']}' deleted!")
                        st.experimental_rerun()
        else:
            st.info(f"No {goal_type.lower()} goals yet. Add one above!")
