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

st.set_page_config(page_title="Correlation Matrix", layout="wide")
st.title("Correlation Heatmap of Accommodations, Diagnoses, Request Type, and Approval")

df_clean = df.copy()
df_clean['Extended_Time'] = df_clean['Requested_Accommodations'].str.contains('Extended Time', na=False).astype(int)
df_clean['Laptop'] = df_clean['Requested_Accommodations'].str.contains('Laptop', na=False).astype(int)
df_clean['Reduced_Distraction'] = df_clean['Requested_Accommodations'].str.contains('Reduced distraction', na=False).astype(int)
df_clean['OTC_Breaks'] = df_clean['Requested_Accommodations'].str.contains('OTC', na=False).astype(int)
df_clean['Large_Print'] = df_clean['Requested_Accommodations'].str.contains('Large Print|18 pt|24 pt', na=False).astype(int)
df_clean['Medication'] = df_clean['Requested_Accommodations'].str.contains('Medication|Medicine', na=False).astype(int)

df_clean['ADHD'] = df_clean['Diagnosis'].str.contains('ADHD', na=False).astype(int)
df_clean['Anxiety'] = df_clean['Diagnosis'].str.contains('Anxiety', na=False).astype(int)
df_clean['Depression'] = df_clean['Diagnosis'].str.contains('Depression', na=False).astype(int)
df_clean['Physical_Condition'] = df_clean['Diagnosis'].str.contains('Glaucoma|Carpal Tunnel|Vertigo|Polyneuropathy|Osteoarthritis', na=False).astype(int)

df_clean['Retake_Request'] = df_clean['Request_Type'].str.contains('Retake', na=False).astype(int)
df_clean['Approved'] = df_clean['Approved?'].str.contains('Appv', na=False).astype(int)

correlation_columns = ['Extended_Time', 'Laptop', 'Reduced_Distraction', 'OTC_Breaks', 
                      'Large_Print', 'Medication', 'ADHD', 'Anxiety', 'Depression', 
                      'Physical_Condition', 'Retake_Request', 'Approved']

correlation_matrix = df_clean[correlation_columns].corr()

fig = px.imshow(correlation_matrix,
                text_auto=True,  
                aspect="auto", 
                color_continuous_scale='RdBu',
                title='Correlation Heatmap of Accommodations, Diagnoses, Request Type, and Approval')

fig.update_layout(
    xaxis_title="Variables",
    yaxis_title="Variables",
    coloraxis_colorbar_title="Correlation",
    height=800, 
    width=1000, 
    margin=dict(l=50, r=50, t=100, b=50) 
)

st.plotly_chart(fig, use_container_width=True)
