# data_loader.py
import streamlit as st
import pandas as pd
from data_preprocessing import video_info_df  # assuming you have this function

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """Load and cache the preprocessed data"""
    return video_info_df  # This should return your video_info_df