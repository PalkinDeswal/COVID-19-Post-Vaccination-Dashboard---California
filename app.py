import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("covid19postvaxstatewidestats.csv")
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# Title
st.title("COVID-19 Post-Vaccination Dashboard - California")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📅 Filter by Date")
date_range = st.sidebar.date_input("Select date range:", [df['date'].min(), df['date'].max()])

# Apply filter
if len(date_range) == 2:
    df = df[(df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))]

# Summary Metrics
st.subheader("Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases (Unvaccinated)", f"{df['unvaccinated_cases'].sum():,}")
col2.metric("Total Cases (Vaccinated)", f"{df['vaccinated_cases'].sum():,}")
col3.metric("% Vaccinated Cases", f"{(df['vaccinated_cases'].sum() / df['unvaccinated_cases'].sum()) * 100:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("Deaths (Unvaccinated)", f"{df['unvaccinated_deaths'].sum():,}")
col5.metric("Deaths (Vaccinated)", f"{df['vaccinated_deaths'].sum():,}")
col6.metric("Hosp. (Unvaccinated)", f"{df['unvaccinated_hosp'].sum():,}")

st.markdown("---")

# Line Chart: Cases Over Time
st.subheader("Daily Cases Over Time")
fig_cases = px.line(df, x='date', y=['unvaccinated_cases', 'vaccinated_cases'],
                    labels={'value': 'Cases', 'date': 'Date', 'variable': 'Category'},
                    title='Unvaccinated vs Vaccinated Daily Cases')
st.plotly_chart(fig_cases)

# Bar Chart: Total Deaths Comparison
st.subheader("Total Deaths Comparison")
deaths_data = pd.DataFrame({
    'Group': ['Unvaccinated', 'Vaccinated'],
    'Deaths': [df['unvaccinated_deaths'].sum(), df['vaccinated_deaths'].sum()]
})
fig_deaths = px.bar(deaths_data, x='Group', y='Deaths', color='Group', title='Total Deaths by Group')
st.plotly_chart(fig_deaths)

# Optional Pie Chart: Current Proportion
st.subheader("Vaccinated vs Unvaccinated Cases Proportion")
latest = df[df['date'] == df['date'].max()].iloc[0]
pie_data = pd.DataFrame({
    'Category': ['Unvaccinated', 'Vaccinated'],
    'Cases': [latest['unvaccinated_cases'], latest['vaccinated_cases']]
})
fig_pie = px.pie(pie_data, values='Cases', names='Category', title='Case Proportion on Latest Date')
st.plotly_chart(fig_pie)

 
