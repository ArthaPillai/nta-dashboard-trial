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

st.set_page_config(page_title="Approval by Request Type", layout="wide")
st.title("Approval Status by Request Type (%)")

approval_by_request = pd.crosstab(df['Request_Type'], df['Approved?'], normalize='index') * 100
fig = px.bar(approval_by_request, 
             x=approval_by_request.index,
             y=['Appv.', 'Appv. Part', 'Prev. Exam'],
             title='Approval Status by Request Type (%)',
             labels={'x': 'Request Type', 'value': 'Percentage'},
             color_discrete_sequence=['#2ecc71', '#f39c12', '#3498db'])

fig.update_layout(height=400, width=600, barmode='stack', legend_title_text='Approval Status')
st.plotly_chart(fig, use_container_width=True)
