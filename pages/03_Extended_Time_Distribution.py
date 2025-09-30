import streamlit as st
import pandas as pd
import plotly.express as px
from ..utils import extract_extended_time

# Load data
file_path = get_data_path()
try:
    df = pd.read_excel(file_path)
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

st.set_page_config(page_title="Extended Time Distribution", layout="wide")
st.title("Distribution of Extended Time Requests")

df['Extended_Time_Percent'] = df['Requested_Accommodations'].apply(extract_extended_time)

extended_time_counts = df['Extended_Time_Percent'].value_counts().sort_index()

fig = px.bar(x=extended_time_counts.index, 
             y=extended_time_counts.values,
             title='Distribution of Extended Time Requests',
             labels={'x': 'Extended Time Percentage', 'y': 'Number of Requests'},
             color=extended_time_counts.values,
             color_continuous_scale='Viridis')

fig.update_layout(height=400, width=600, coloraxis_colorbar_title="No. of Requests")
st.plotly_chart(fig, use_container_width=True)
