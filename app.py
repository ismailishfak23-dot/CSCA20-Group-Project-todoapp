import streamlit as st
import json
import os

st.set_page_config(
    page_title="CSCA20 Financial App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load CSS ---
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Load Saved Data ---
DATA_FILE = "data/user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

if "user_data" not in st.session_state:
    st.session_state.user_data = load_data()

# --- Home Page Content ---
st.title("Student Finance Hub")
st.subheader("Track smarter. Save easier. Stress less.")

st.markdown("""
Welcome to your **Student Finance Hub** — a modern financial dashboard
designed to help students understand their money clearly and easily.

### What you can do:
- 🧍 Build your student profile  
- 💳 Track daily spending & income  
- 🎯 Set smart goals  
- 📊 Visualize everything with clean charts  
""")

st.markdown("### 💾 Save Progress")
if st.button("Save All Data"):
    save_data(st.session_state.user_data)
    st.success("Your data has been saved successfully!")
# dummy comment to trigger redeploy
