import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np


@st.cache_data  # 👈 Add the caching decorator
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


csv_file = os.getcwd() + "/data/processed/merged_data.csv"
df = load_data(file_path=csv_file)


# Title of dashboard
# st.title("TikTok data analysis")


# add checkbox to sidebar
checkbox = st.sidebar.checkbox(label="Display dataset")
if checkbox:
    # Display the dataframe
    st.dataframe(df)

# Give sidebar a title
st.sidebar.title("Analysis settings")
feature_selection = st.sidebar.multiselect(
    label="Select the features to plot",
    options=df.select_dtypes(include=np.number).columns,
)


st.button("Rerun")
