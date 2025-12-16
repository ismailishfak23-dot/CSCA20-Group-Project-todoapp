import streamlit as st
import pandas as pd

# --- Debug: show session state ---
# st.write(st.session_state)

# --- Initialize User Data ---
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "transactions" not in st.session_state.user_data:
    st.session_state.user_data["transactions"] = []

transactions = st.session_state.user_data["transactions"]

# --- Page Title ---
st.title("💳 Transactions Tracker")
st.subheader("Track your income and spending easily!")

# --- Add Transaction Form ---
with st.form("txn_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        t_type = st.selectbox("Type", ["Income 💰", "Expense 🛒"])
        category = st.selectbox(
            "Category",
            ["Food 🍔", "Rent 🏠", "Transport 🚗", "Entertainment 🎮", "School 📚", "Savings 💵", "Other 📝"]
        )
    with col2:
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        note = st.text_input("Description / Note")
    
    submitted = st.form_submit_button("➕ Add Transaction")
    
    if submitted:
        st.session_state.user_data["transactions"].append({
            "type": t_type.split()[0],  # "Income" or "Expense"
            "amount": amount,
            "category": category,
            "note": note
        })
        st.success(f"{t_type} of ${amount:.2f} added! 🎉")

# --- Show Total Balance ---
income_total = sum(t["amount"] for t in transactions if t["type"] == "Income")
expense_total = sum(t["amount"] for t in transactions if t["type"] == "Expense")
balance = income_total - expense_total

st.markdown("### 💡 Current Balance")
st.info(f"💰 Total Income: ${income_total:.2f}  |  🛒 Total Expenses: ${expense_total:.2f}  |  ⚖️ Balance: ${balance:.2f}")

# --- Display Transactions Table ---
st.markdown("### 📜 Transaction History")
if transactions:
    df = pd.DataFrame(transactions)
    st.table(df)
else:
    st.info("No transactions yet! Use the form above to add your first transaction.")
