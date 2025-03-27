
import streamlit as st
import pandas as pd

# Load the data
df = pd.read_csv("mock_data.csv")

# Title
st.title("📊 Property Sniper Dashboard")
st.markdown("Smart filtering. Live scoring. Built for sniper-grade investment decisions.")

# Sidebar filters
st.sidebar.header("🎯 Investment Filters")
state = st.sidebar.multiselect("State", options=df["State"].unique(), default=df["State"].unique())
min_price = st.sidebar.number_input("Min Price", value=300000, step=10000)
max_price = st.sidebar.number_input("Max Price", value=500000, step=10000)
strategy = st.sidebar.radio("Strategy", ["High Growth", "Cashflow", "Balanced"])
min_score = st.sidebar.slider("Min Investment Score", min_value=0.0, max_value=20.0, value=16.0)

# Strategy-based logic
if strategy == "High Growth":
    sort_col = "Growth 5Y %"
elif strategy == "Cashflow":
    sort_col = "Yield %"
else:
    sort_col = "Investment Score"

# Filter logic
filtered = df[
    (df["State"].isin(state)) &
    (df["Price"] >= min_price) &
    (df["Price"] <= max_price) &
    (df["Investment Score"] >= min_score)
].sort_values(by=sort_col, ascending=False)

# Output
st.subheader("🏘️ Matched Properties")
st.dataframe(filtered)

# Scoring explanation
with st.expander("📈 What is the Investment Score?"):
    st.markdown("""
    The Investment Score is calculated using:
    - 35% weight to 5Y Capital Growth
    - 15% Rental Yield
    - -15% Vacancy Rate
    - 15% Population Growth
    - 10% Stock Pressure
    - 5% Infrastructure Score
    - 5% Under Median Opportunity
    """)

# Export
st.download_button("📥 Download CSV", filtered.to_csv(index=False), "filtered_properties.csv", "text/csv")
