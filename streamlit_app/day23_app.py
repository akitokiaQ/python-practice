import streamlit as st
import pandas as pd

# Google Sheets URL (Microsoft repositories data)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1UBzE-wBxYbHDKEw-yb5iEESq5iFfou1Y_RJITuHYYW4/export?format=csv&gid=2060793365"
# Data load
data = pd.read_csv(SHEET_URL, parse_dates=['created_at', 'updated_at'])

st.title("Microsoft Repositories Visualization")

# Date range filtering
st.sidebar.header("Date Range Filter")
date_column = st.sidebar.selectbox("Date Column for Filtering", ["created_at", "updated_at"])

date_min = data[date_column].min()
date_max = data[date_column].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [date_min.date(), date_max.date()],
    min_value=date_min.date(),
    max_value=date_max.date()
)

# Unify dates in UTC (align time zones)
start_date = pd.to_datetime(start_date).tz_localize('UTC')
end_date = pd.to_datetime(end_date).tz_localize('UTC')

filtered_data = data[(data[date_column] >= start_date) & (data[date_column] <= end_date)]

# Metric selection
st.sidebar.header("Metric Selection")
metric = st.sidebar.radio(
    "Select Metric to Visualize",
    ("watchers_count", "forks_count", "stargazers_count")
)

# Plot the data
st.subheader(f"{metric.replace('_', ' ').title()} over repositories")
st.bar_chart(filtered_data.set_index('name')[metric])

# Display filtered data
st.subheader("Filtered Data Table")
st.dataframe(filtered_data[['name', 'created_at', 'updated_at', 'watchers_count', 'forks_count', 'stargazers_count']])