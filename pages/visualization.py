import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Initialize User Data ---
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "transactions" not in st.session_state.user_data:
    st.session_state.user_data["transactions"] = []

transactions = st.session_state.user_data["transactions"]

# --- Page Title ---
st.set_page_config(page_title="Transactions Visualizer", layout="wide")
st.title("📊 Transactions Visualizer")
st.subheader("See your spending and income trends!")

if transactions:
    df = pd.DataFrame(transactions)
    df["amount"] = pd.to_numeric(df["amount"])
    
    # --- Pie chart: Expenses by category ---
    expense_df = df[df["type"] == "Expense"]
    if not expense_df.empty:
        st.markdown("### 🛒 Expense Distribution by Category")
        category_sum = expense_df.groupby("category")["amount"].sum().reset_index()
        fig_pie = px.pie(category_sum, names='category', values='amount',
                         color_discrete_sequence=px.colors.sequential.Plasma,
                         hole=0.4)
        fig_pie.update_layout(template='plotly_dark', title="Expenses by Category",
                              title_font=dict(size=22, color='cyan'))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # --- Bar chart: Income vs Expenses ---
    st.markdown("### 💰 Income vs Expenses")
    totals = df.groupby("type")["amount"].sum().reset_index()
    fig_bar = px.bar(totals, x='type', y='amount', color='type',
                     color_discrete_map={'Income':'#00ffcc', 'Expense':'#ff3366'})
    fig_bar.update_layout(template='plotly_dark', title="Income vs Expenses",
                          title_font=dict(size=22, color='cyan'),
                          yaxis_title="Amount ($)")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # --- Line chart: Cumulative balance ---
    st.markdown("### ⚖️ Cumulative Balance Over Transactions")
    df["signed_amount"] = df.apply(lambda x: x["amount"] if x["type"]=="Income" else -x["amount"], axis=1)
    df["cumulative_balance"] = df["signed_amount"].cumsum()
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df.index,
        y=df["cumulative_balance"],
        mode='lines+markers',
        line=dict(color='#00ffcc', width=3),
        marker=dict(size=8, color='#ff33aa'),
        name="Balance"
    ))
    fig_line.update_layout(template='plotly_dark', title="Cumulative Balance",
                           title_font=dict(size=22, color='cyan'),
                           xaxis_title="Transaction #",
                           yaxis_title="Balance ($)")
    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("No transactions to visualize yet! Add some transactions first.")
