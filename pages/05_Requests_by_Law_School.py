import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = get_data_path()
try:
    df = pd.read_excel(file_path)
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
