import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.title("Financial Visualization")
st.header("Charts and Key Metrics")

# --- 1. Load Data from Session State ---
profile_data = st.session_state.get("profile_data", None)
goals = st.session_state.get("goals", [])

# --- 2. Check for Profile Data ---
if not profile_data or not profile_data.get("name"):
    st.warning("Please go to the **Profile** page and save your financial data to enable visualizations.")
else:
    st.subheader(f"Financial Snapshot for {profile_data['name']}")
    
    # ----------------------------------------------------
    # Chart 1: Income vs. Spending Bar Chart (Monthly Flow)
    # ----------------------------------------------------
    st.subheader("Monthly Income vs. Spending")
    
    # Data preparation
    monthly_data = {
        "Category": ["Income", "Spending", "Net Flow"],
        "Amount": [
            profile_data["income"], 
            profile_data["spending"],
            profile_data["income"] - profile_data["spending"]
        ]
    }
    monthly_df = pd.DataFrame(monthly_data)

    # Use Matplotlib for the bar chart
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    
    # Assign colors based on category
    colors = ['#4CAF50', '#F44336', '#2196F3' if monthly_df.loc[2, 'Amount'] >= 0 else '#FF9800']
    
    # Create bar chart
    bars = ax1.bar(monthly_df["Category"], monthly_df["Amount"], color=colors)
    
    ax1.set_ylabel("Amount ($)")
    ax1.set_title("Monthly Financial Flow")
    ax1.grid(axis='y', linestyle='--')
    
    # Add data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval, f'${yval:,.2f}', va='bottom' if yval > 0 else 'top', ha='center', fontweight='bold')
    
    # Display the chart
    st.pyplot(fig1)
    
    st.markdown("---")

# --- 3. Check for Goals Data ---
if goals:
    # ----------------------------------------------------
    # Chart 2: Goals Progress Bar Chart
    # ----------------------------------------------------
    st.subheader("Goals Progress Tracker")
    
    # Convert goals data to a DataFrame for easier plotting
    goals_df = pd.DataFrame([
        {
            "name": g["name"], 
            "current": g["current"], 
            "target": g["target"],
            "remaining": g["target"] - g["current"]
        } for g in goals
    ])
    
    # Prepare data for stacked horizontal bar chart
    goal_names = goals_df["name"]
    current_amount = goals_df["current"]
    remaining_amount = goals_df["remaining"].clip(lower=0) # Ensures no negative bars
    
    # Create the figure
    fig2, ax2 = plt.subplots(figsize=(10, len(goals) * 1.5))
    
    # Plot 'Current'
    ax2.barh(goal_names, current_amount, color='#00BCD4', label='Current Saved')
    
    # Plot 'Remaining' stacked on top of 'Current'
    ax2.barh(goal_names, remaining_amount, left=current_amount, color='#B2EBF2', label='Remaining Target')
    
    ax2.set_xlabel("Amount ($)")
    ax2.set_title("Current Progress Towards Goals")
    ax2.legend()
    
    # Display the chart
    st.pyplot(fig2)

else:
    st.info("No goals have been set yet. Go to the **Goals** page to add your targets.")