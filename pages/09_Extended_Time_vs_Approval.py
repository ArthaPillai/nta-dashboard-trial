import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from utils import extract_extended_time, load_data

# Load data
try:
    df = load_data()
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

st.set_page_config(page_title="Extended Time vs Approval", layout="wide")
st.title("Extended Time vs Approval Rate by Law School")

df['Extended_Time_Percent'] = df['Requested_Accommodations'].apply(extract_extended_time)
df_with_extended_time = df[df['Extended_Time_Percent'].notna()].copy()

law_school_stats = df_with_extended_time.groupby('Law_School').agg({
    'Extended_Time_Percent': 'mean',
    'Approved?': lambda x: (x.isin(['Appv.', 'Appv. Part'])).sum() / len(x) * 100,  
    'Request_ID': 'count' 
}).round(2)

law_school_stats.columns = ['Avg_Extended_Time', 'Approval_Rate', 'Request_Count']
law_school_stats = law_school_stats.reset_index()

fig = px.scatter(law_school_stats, 
                 x='Avg_Extended_Time', 
                 y='Approval_Rate',
                 size='Request_Count',
                 color='Law_School',
                 hover_data=['Law_School', 'Avg_Extended_Time', 'Approval_Rate', 'Request_Count'],
                 title='Extended Time vs Approval Rate by Law School',
                 labels={
                     'Avg_Extended_Time': 'Average Extended Time (%)',
                     'Approval_Rate': 'Approval Rate (%)',
                     'Request_Count': 'Number of Requests'
                 })

fig.update_layout(height=500, width=700)
fig.update_traces(marker=dict(sizeref=2.*max(law_school_stats['Request_Count'])/(40.**2), sizemode='area'))

fig.update_traces(mode='markers+text', textposition='top center')
st.plotly_chart(fig, use_container_width=True)
