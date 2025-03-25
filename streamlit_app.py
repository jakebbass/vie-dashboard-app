import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load Excel Data
@st.cache_data
def load_data():
    file_path = "userdash.xlsx"
    xls = pd.ExcelFile(file_path)
    return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

sheets = load_data()

# --- User Input Section ---
frontend = sheets['frontend']
st.title("Vie Dashboard")

st.header("Monthly Deposit")
default_deposit = int(frontend.iloc[0, 0].replace(",", "").strip())
user_deposit = st.number_input("How much are you looking at depositing each month?", min_value=0, value=default_deposit)

# --- Loan Schedule Visualization ---
loan_df = sheets['Lift Off Loan Schedule'].iloc[2:].copy()
loan_df.columns = ["Year", "StartingBalance", "YouPaid", "Interest", "Principal", "EndingBalance", "FinanceCharge", "LoanBalance"]
loan_df = loan_df.dropna(subset=["Year"])

st.subheader("Loan Balance Over Time")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=loan_df['Year'], y=loan_df['LoanBalance'], mode='lines+markers', name='Lift-off Loan Balance'))
fig1.update_layout(title='Lift-off Loan Balance', xaxis_title='Year', yaxis_title='Balance ($)')
st.plotly_chart(fig1)

# --- Accumulation Visualization ---
acc_df = sheets['Accumulation'].iloc[2:].copy()
acc_df.columns = ["Year", "BeginCash", "VieDeposits", "CustDeposits", "PolicyCredit", "CreditedAmount", "PolicyCash"]

st.subheader("Policy Cash Value Over Time")
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=acc_df['Year'], y=acc_df['PolicyCash'], name='Cash Value'))
fig2.update_layout(title='Policy Cash Value', xaxis_title='Year', yaxis_title='Value ($)')
st.plotly_chart(fig2)

# --- Distribution Visualization ---
dist_df = sheets['Distribution'].iloc[2:].copy()
dist_df.columns = ["Year", "BeginBal", "Spent", "LoanRate", "LoanInterest", "EndLoan"]

st.subheader("Spending vs Loan Interest")
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=dist_df['Year'], y=dist_df['Spent'], name='Spent', mode='lines+markers'))
fig3.add_trace(go.Scatter(x=dist_df['Year'], y=dist_df['LoanInterest'], name='Loan Interest', mode='lines+markers'))
fig3.update_layout(title='Spending and Loan Interest Over Time', xaxis_title='Year', yaxis_title='Amount ($)')
st.plotly_chart(fig3)

# --- Asset Value Visualization ---
av_df = sheets['Asset Value'].iloc[2:].copy()
av_df.columns = ["Year", "AssetValue", "OwedLoan", "AvailInvesting", "AvailSpending"]

st.subheader("Available for Investing vs Spending")
fig4 = go.Figure()
fig4.add_trace(go.Bar(x=av_df['Year'], y=av_df['AvailInvesting'], name='For Investing'))
fig4.add_trace(go.Bar(x=av_df['Year'], y=av_df['AvailSpending'], name='For Spending'))
fig4.update_layout(barmode='stack', title='Available Funds Over Time', xaxis_title='Year', yaxis_title='Amount ($)')
st.plotly_chart(fig4)

# --- Summary ---
st.markdown("---")
st.header("Summary")
st.write(f"Based on a monthly deposit of **${user_deposit}**, here’s how your policy evolves across value, loans, and spendable cash. All data is sourced directly from backend logic with no manual calculations required.")
