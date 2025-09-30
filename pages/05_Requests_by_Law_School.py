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
    
st.set_page_config(page_title="Requests by Law School", layout="wide")
st.title("Accommodation Requests by Law School")

law_school_counts = df['Law_School'].value_counts()
fig = px.bar(y=law_school_counts.index, 
             x=law_school_counts.values,
             orientation='h',
             title='Accommodation Requests by Law School',
             labels={'x': 'Number of Requests', 'y': 'Law School'},
             color=law_school_counts.values,
             color_continuous_scale='Blues')

fig.update_layout(height=400, width=700, coloraxis_colorbar_title="No. of Requests")
st.plotly_chart(fig, use_container_width=True)
