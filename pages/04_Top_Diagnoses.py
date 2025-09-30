import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from utils import extract_diagnoses, get_data_path

# Load data
try:
    df = pd.read_excel(get_data_path())
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

all_diagnoses = []
for diagnosis in df['Diagnosis']:
    all_diagnoses.extend(extract_diagnoses(diagnosis))

diagnosis_counts = pd.Series(all_diagnoses).value_counts().head(10)

fig = px.bar(y=diagnosis_counts.index, 
             x=diagnosis_counts.values,
             orientation='h',
             title='Top 10 Most Common Diagnoses',
             labels={'x': 'Number of Cases', 'y': 'Diagnosis'},
             color=diagnosis_counts.values,
             color_continuous_scale='Reds')

fig.update_layout(height=500, width=600, coloraxis_colorbar_title="No. of Cases")
st.plotly_chart(fig, use_container_width=True)
