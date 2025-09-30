import streamlit as st

def main_page():
    st.set_page_config(page_title="NTA Accommodations Dashboard", layout="wide")
    st.title("📊 NTA Accommodations Dashboard")
    st.markdown("""
    Welcome to the NTA Accommodations Dashboard! 
    Use the sidebar to navigate through various charts analyzing accommodation requests, 
    extended time distributions, diagnoses, and approval rates.

    This dashboard is currently refelctive of the 2025 Feb 'A - E' data.
    """)

# Define the main page
home_page = st.Page(main_page, title="Home")

# Navigation: Include the main page and let Streamlit auto-detect pages in the pages/ folder
pg = st.navigation({"Home": [home_page]})
pg.run()
