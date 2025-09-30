import streamlit as st
from pathlib import Path

def main_page():
    st.set_page_config(page_title="NTA Accommodations Dashboard", layout="wide")
    st.title("📊 NTA Accommodations Dashboard")
    st.markdown("""
    Welcome to the NTA Accommodations Dashboard! 
    
    Use the sidebar to navigate through various charts analyzing accommodation requests, 
    extended time distributions, diagnoses, and approval rates.

    This dashboard is currently refelctive of the 2025 Feb 'A - E' data.
    """)

# Define the main page with title "Home" for the sidebar
home_page = st.Page(main_page, title="Home")

# Collect all pages from the pages/ folder
pages_dir = Path(__file__).parent / "pages"
page_files = sorted(pages_dir.glob("*.py")) 

# Create a list of st.Page objects for pages in the pages/ folder
other_pages = [st.Page(str(page_file)) for page_file in page_files]

# Combine main page and other pages for navigation
all_pages = [home_page] + other_pages

# Set up navigation with all pages
pg = st.navigation(all_pages)
pg.run()
