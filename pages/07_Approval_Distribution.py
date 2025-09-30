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

st.set_page_config(page_title="Approval Distribution", layout="wide")
st.title("Approval Status Distribution")

approval_counts = df['Approved?'].value_counts()
fig = px.bar(x=approval_counts.index, 
             y=approval_counts.values,
             title='Approval Status Distribution',
             labels={'x': 'Approval Status', 'y': 'Count'},
             color=approval_counts.values,
             color_continuous_scale='Blues')

fig.update_layout(height=400, width=500, coloraxis_colorbar_title="Approval Count")
st.plotly_chart(fig, use_container_width=True)
