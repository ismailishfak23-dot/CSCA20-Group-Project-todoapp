import streamlit as st

# --- Initialize Data ---
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "profile" not in st.session_state.user_data:
    st.session_state.user_data["profile"] = {
        "name": "",
        "age": 0,
        "email": "",
        "occupation": "",
        "country": "",
        "hobbies": "",
        "income": 0.0,
        "spending": 0.0
    }

profile = st.session_state.user_data["profile"]

# --- Page Title ---
st.title("Your Student Profile")
st.subheader("Add your details to get personalized financial insights 🎯")

# --- Form ---
with st.form("profile_form"):
    col1, col2 = st.columns(2)

    with col1:
        profile["name"] = st.text_input("Name", value=profile["name"])
        profile["email"] = st.text_input("Email", value=profile["email"])
        profile["age"] = st.number_input("Age", min_value=0, step=1, value=profile["age"])
        profile["occupation"] = st.text_input("Occupation", value=profile["occupation"])
    
    with col2:
        profile["country"] = st.text_input("Country", value=profile["country"])
        profile["hobbies"] = st.text_input("Hobbies", value=profile["hobbies"])
        profile["income"] = st.number_input("Average Monthly Income ($)", min_value=0.0, step=0.01, value=profile["income"])
        profile["spending"] = st.number_input("Average Monthly Spending ($)", min_value=0.0, step=0.01, value=profile["spending"])
    
    submitted = st.form_submit_button("💾 Save Profile")

if submitted:
    st.success(f"Profile saved! Welcome, {profile['name']} 👋")
    st.session_state.user_data["profile"] = profile

# --- Display Info Card ---
if profile["name"]:
    st.markdown("### Your Profile Snapshot")
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**Name:** {profile['name']}\n\n**Age:** {profile['age']}\n\n**Occupation:** {profile['occupation']}\n\n**Country:** {profile['country']}")
    with col2:
        st.info(f"**Email:** {profile['email']}\n\n**Hobbies:** {profile['hobbies']}\n\n**Income:** ${profile['income']:.2f}\n\n**Spending:** ${profile['spending']:.2f}")

    net_flow = profile["income"] - profile["spending"]
    if net_flow > 0:
        st.success(f"💰 Monthly Net Flow: ${net_flow:.2f} (You’re saving!)")
    elif net_flow < 0:
        st.warning(f"🚨 Monthly Net Flow: -${abs(net_flow):.2f} (Overspending!)")
    else:
        st.info("⚖️ Monthly Net Flow: Breaking even.")
