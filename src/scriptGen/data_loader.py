import pandas as pd
import streamlit as st
import numpy as np
from types import NoneType


@st.cache_data
def load_data():
    features_df = pd.read_parquet('data/ScriptGen-data/script_gendata.parquet')

    def parse_list(x):
        if isinstance(x, np.ndarray):
            return list(x)
        if isinstance(x, NoneType):
            return []

    for col in features_df.columns:
        str_flag = features_df[col].apply(
            lambda x: isinstance(x, np.ndarray)).any()
        if str_flag:
            features_df[col] = features_df[col].apply(parse_list)
    return features_df
