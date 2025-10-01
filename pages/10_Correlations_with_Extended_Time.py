import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from utils import extract_extended_time_numeric, count_accommodations, load_data

# Load data
try:
    df = load_data()
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

st.set_page_config(page_title="Correlations with Extended Time", layout="wide")
st.title("Correlations with Extended Time Percentage")

df['Extended_Time_Numeric'] = df['Requested_Accommodations'].apply(extract_extended_time_numeric)
df['Num_Accommodations'] = df['Requested_Accommodations'].apply(count_accommodations)

df['Is_Fully_Approved'] = (df['Approved?'] == 'Appv.').astype(int)
df['Is_Partially_Approved'] = (df['Approved?'] == 'Appv. Part').astype(int)
df['Is_Previously_Examined'] = (df['Approved?'] == 'Prev. Exam').astype(int)
df['Is_New_Request'] = (df['Request_Type'] == 'New Request').astype(int)
df['Is_Retake_Same'] = (df['Request_Type'] == 'Retake - Same Request').astype(int)
df['Is_Retake_Changed'] = (df['Request_Type'] == 'Retake - Changed Request').astype(int)

extended_time_correlations = df[[
    'Extended_Time_Numeric', 'Num_Accommodations',
    'Is_Fully_Approved', 'Is_Partially_Approved', 'Is_Previously_Examined',
    'Is_New_Request', 'Is_Retake_Same', 'Is_Retake_Changed'
]].corr()['Extended_Time_Numeric'].drop('Extended_Time_Numeric')

fig = go.Figure()
fig.add_trace(go.Bar(
    x=extended_time_correlations.index,
    y=extended_time_correlations.values,
    marker_color=['red' if x < 0 else 'blue' for x in extended_time_correlations.values],
    text=[f'{x:.3f}' for x in extended_time_correlations.values],
    textposition='auto'
))

fig.update_layout(
    title='Correlations with Extended Time Percentage',
    xaxis_title='Variables',
    yaxis_title='Correlation Coefficient',
    height=500,
    width=800,
    xaxis_tickangle=-45
)

fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)

st.plotly_chart(fig, use_container_width=True)
