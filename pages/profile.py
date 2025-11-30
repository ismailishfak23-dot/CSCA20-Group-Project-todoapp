import streamlit as st

# --- Initialization ---
# Initialize session state for the user profile if it doesn't exist
if "profile_data" not in st.session_state:
    st.session_state.profile_data = {
        "name": "",
        "age": 0,
        "email": "",
        "occupation": "",
        "income": 0.0,
        "spending": 0.0,
        "current_savings": 0.0,
        "investments": 0.0
    }

# --- Page Content and Form ---
st.title("User Profile")
st.header("Your Personal Information")

# Use a form to group inputs and prevent unnecessary reruns on every keystroke
with st.form("profile_form"):
    
    # Pre-populate inputs with existing session state data for a smooth user experience
    data = st.session_state.profile_data
    
    st.subheader("Personal Details")
    name = st.text_input("Name:", value=data["name"])
    age = st.number_input("Age:", min_value=0, step=1, value=data["age"])
    email = st.text_input("Email Address:", value=data["email"])
    occupation = st.text_input("Occupation:", value=data["occupation"])
    
    st.subheader("Financial Overview (Monthly/Current)")
    income = st.number_input("Monthly Income ($):", min_value=0.0, step=0.01, value=data["income"])
    spending = st.number_input("Average Monthly Spending ($):", min_value=0.0, step=0.01, value=data["spending"])
    current_savings = st.number_input("Current Savings ($):", min_value=0.0, step=0.01, value=data["current_savings"])
    investments = st.number_input("Total Investments ($):", min_value=0.0, step=0.01, value=data["investments"])

    submitted = st.form_submit_button("Save Profile")

# --- Submission Logic ---
if submitted:
    # Update the session state with the new values
    st.session_state.profile_data.update({
        "name": name,
        "age": age,
        "email": email,
        "occupation": occupation,
        "income": income,
        "spending": spending,
        "current_savings": current_savings,
        "investments": investments
    })
    st.success(f"Profile saved for {name}! Data is now available to other pages.")

# --- Display Saved Data ---
st.markdown("---")
st.subheader("Current Profile Snapshot")
if st.session_state.profile_data["name"]:
    profile = st.session_state.profile_data
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Age:** {profile['age']}")
        st.write(f"**Occupation:** {profile['occupation']}")
        st.write(f"**Email:** {profile['email']}")

    with col2:
        st.write(f"**Monthly Income:** ${profile['income']:.2f}")
        st.write(f"**Monthly Spending:** ${profile['spending']:.2f}")
        st.write(f"**Total Savings:** ${profile['current_savings']:.2f}")
        st.write(f"**Total Investments:** ${profile['investments']:.2f}")

    # Display simple budget summary
    net_flow = profile['income'] - profile['spending']
    if net_flow > 0:
        st.info(f"💰 Monthly Net Flow: You are saving \${net_flow:.2f} per month.")
    elif net_flow < 0:
        st.warning(f"🚨 Monthly Net Flow: You are overspending by \${abs(net_flow):.2f} per month.")
    else:
        st.info("⚖️ Monthly Net Flow: You are breaking even.")

else:
    st.info("Please fill out the form above and click 'Save Profile' to see your snapshot.")

