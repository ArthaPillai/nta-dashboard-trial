import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = "../Master_NTA_KeyDetails.xlsx"
df = pd.read_excel(file_path)

st.set_page_config(page_title="Request Types", layout="wide")
st.title("Distribution of Request Types")

request_type_counts = df['Request_Type'].value_counts()
fig = px.pie(values=request_type_counts.values, 
             names=request_type_counts.index,
             title='Distribution of Request Types',
             color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])

fig.update_layout(height=400, width=500, legend_title_text='Request Type')
st.plotly_chart(fig, use_container_width=True)
