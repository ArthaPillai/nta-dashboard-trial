import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from utils import get_data_path

# Load data
try:
    df = pd.read_excel(get_data_path())
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

st.set_page_config(page_title="Extended Time by Law School", layout="wide")
st.title("Average Extended Time Requests by Law School")

df['Extended_Time_Percent'] = df['Requested_Accommodations'].apply(extract_extended_time)

df_with_extended_time = df[df['Extended_Time_Percent'].notna()].copy()

law_school_analysis = df_with_extended_time.groupby('Law_School').agg({
    'Extended_Time_Percent': ['mean', 'median', 'std', 'count'],
    'Approved?': lambda x: (x == 'Appv.').sum() / len(x) * 100  
}).round(2)

law_school_analysis.columns = ['Avg_Extended_Time', 'Median_Extended_Time', 'Std_Extended_Time', 'Request_Count', 'Approval_Rate']
law_school_analysis = law_school_analysis.reset_index()

law_school_analysis = law_school_analysis.sort_values('Avg_Extended_Time', ascending=False)

fig = px.bar(law_school_analysis, 
             x='Law_School', 
             y='Avg_Extended_Time',
             title='Average Extended Time Requests by Law School',
             labels={'Avg_Extended_Time': 'Average Extended Time (%)', 'Law_School': 'Law School'},
             color='Avg_Extended_Time',
             color_continuous_scale='Viridis',
             text='Avg_Extended_Time')

fig.update_layout(height=500, width=800, xaxis_tickangle=-45)
fig.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig, use_container_width=True)
