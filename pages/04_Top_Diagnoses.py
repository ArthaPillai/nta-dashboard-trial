import streamlit as st
import pandas as pd
import plotly.express as px
from ..utils import extract_diagnoses

# Load data
file_path = "../Master_NTA_KeyDetails.xlsx"
df = pd.read_excel(file_path)

st.set_page_config(page_title="Top Diagnoses", layout="wide")
st.title("Top 10 Most Common Diagnoses")

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
