import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from utils import extract_extended_time, get_data_path

# Load data
try:
    df = pd.read_excel(get_data_path())
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

st.set_page_config(page_title="Extended Time Distribution by Law School", layout="wide")
st.title("Distribution of Extended Time Requests by Law School (%)")

df['Extended_Time_Percent'] = df['Requested_Accommodations'].apply(extract_extended_time)
df_with_extended_time = df[df['Extended_Time_Percent'].notna()].copy()

extended_time_pivot = df_with_extended_time.pivot_table(
    index='Law_School', 
    columns='Extended_Time_Percent', 
    values='Request_Type',  # Use a non-sensitive column for counting (instead of File_Name)
    aggfunc='count', 
    fill_value=0
)

extended_time_pct = extended_time_pivot.div(extended_time_pivot.sum(axis=1), axis=0) * 100

fig = go.Figure()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
extended_time_values = [25, 50, 100] 

for i, time_pct in enumerate(extended_time_values):
    if time_pct in extended_time_pct.columns:
        fig.add_trace(go.Bar(
            name=f'{time_pct}% Extended Time',
            x=extended_time_pct.index,
            y=extended_time_pct[time_pct],
            marker_color=colors[i % len(colors)]
        ))

fig.update_layout(
    title='Distribution of Extended Time Requests by Law School (%)',
    xaxis_title='Law School',
    yaxis_title='Percentage of Requests',
    barmode='stack',
    legend_title_text='Extended Time %',
    height=500,
    width=800,
    xaxis_tickangle=-45
)
st.plotly_chart(fig, use_container_width=True)
