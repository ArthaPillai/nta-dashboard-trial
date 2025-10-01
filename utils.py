import re
import pandas as pd
from pathlib import Path

def get_data_path():
    """Return the absolute path to the Excel file in the project root."""
    current_dir = Path(__file__).parent
    data_path = current_dir / "Master_NTA_Anonymized.xlsx"
    if not data_path.exists():
        raise FileNotFoundError(f"Excel file not found at: {data_path}")
    return data_path

def extract_extended_time(accommodations):
    if pd.isna(accommodations):
        return None
    match = re.search(r'(\d+)%\s+Extended Time', str(accommodations))
    if match:
        return int(match.group(1))
    return None

def extract_extended_time_numeric(accommodations):
    if pd.isna(accommodations):
        return 0
    match = re.search(r'(\d+)%\s+Extended Time', str(accommodations))
    if match:
        return int(match.group(1))
    return 0

def count_accommodations(accommodations):
    if pd.isna(accommodations):
        return 0
    return len(str(accommodations).split(','))

def extract_diagnoses(diagnosis_text):
    if pd.isna(diagnosis_text):
        return []
    diagnoses = [d.strip() for d in str(diagnosis_text).split(',')]
    return diagnoses
