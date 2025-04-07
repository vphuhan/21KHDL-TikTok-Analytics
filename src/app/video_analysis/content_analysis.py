import pandas as pd
from itertools import chain
import streamlit as st
# from video_analysis.utils.preprocess import load_data
from video_analysis.utils.chart import *
from video_analysis.config import *
import numpy as np
from types import NoneType
# from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")


@st.cache_data
def load_data():
    features_df = pd.read_parquet(
        'data/content_analysis/content_analysis_data.parquet')

    def parse_list(x):
        if isinstance(x, np.ndarray):
            return list(x)
        if isinstance(x, NoneType):
            return []
    for col in features_df.columns:
        list_flag = features_df[col].apply(
            lambda x: isinstance(x, np.ndarray)).any()
        if list_flag:
            features_df[col] = features_df[col].apply(parse_list)
    return features_df


df = load_data()

print(df.info())

#################### SIDE BAR ####################
st.sidebar.header("Tùy chọn phân tích")

category_options = df['categories'].dropna().unique().tolist()
selected_category = st.sidebar.selectbox(
    "Chọn chủ đề:", options=category_options)


# Filter by categories
if selected_category:
    df = df[df['categories'] == selected_category]

#################### MAIN LAYOUT ####################

st.title("📊 TikTok Content Insight Dashboard")
st.markdown("## Về nội dung video")

# Field SelectBox
FIELDS_TO_ANALYZE = set(COLUMN_LABELS.keys()) - \
    set(['categories', 'has_cta', 'has_personal_story'])

selected_field = st.selectbox(
    "Chọn trường cần hiển thị biểu đồ:",
    options=FIELDS_TO_ANALYZE,
    format_func=lambda x: COLUMN_LABELS.get(x, x),

)

labels = df[selected_field].explode().dropna(
).unique().tolist()
color_map = generate_color_map(labels)


# Tạo hai cột
st.subheader(
    f"Hiệu suất tương tác theo {COLUMN_LABELS.get(selected_field, selected_field)}")
col1, col2 = st.columns(2)

with col1:
    selected_metric = st.selectbox(
        "Chỉ số hiệu suất:",
        options=list(COLUMN_METRICS.keys()),
        format_func=lambda x: COLUMN_METRICS.get(x, x))
    stat_type = st.radio(
        "Loại thống kê:",
        options=list(STAT_TYPES.keys()),
        format_func=lambda x: STAT_TYPES.get(x, x),
        horizontal=True
    )
    # st.subheader(
    #     f"{STAT_TYPES.get(stat_type, stat_type)} theo {COLUMN_LABELS.get(selected_field, selected_field)}")

    fig = plot_bar_chart(df, selected_field, selected_metric,
                         stat_type, color_map=color_map)
    if fig:
        st.plotly_chart(fig, use_container_width=True, key="bar_chart")
        # plotly_events(fig, select_event=True)

    # metrics = list(COLUMN_METRICS.keys())

    # exploded = df.copy().explode(
    #     selected_field).dropna(subset=[selected_field])

    # if stat_type == 'count':
    #     summary = exploded.groupby(selected_field).size(
    #     ).reset_index(name='Số lượng video')
    # else:
    #     summary = exploded.groupby(selected_field)[
    #         metrics].agg(stat_type).reset_index()

    # # Đổi tên cột cho đẹp:
    # summary = summary.rename(columns={
    #     m: COLUMN_METRICS[m] for m in metrics
    # })

    # # Hiển thị bảng:
    # st.dataframe(summary, use_container_width=True, hide_index=True)


with col2:
    exploded = df.copy()
    exploded = exploded.explode(selected_field).dropna(subset=[selected_field])
    labels = exploded[selected_field].unique()

    selected_labels = st.multiselect(
        "Chọn label để hiển thị radar chart:", labels, default=None
    )
    # st.write("")
    # st.write("")
    # st.write("")
    display_metrics = COLUMN_METRICS.copy()
    display_metrics.pop('engagement_rate', None)
    print(display_metrics)
    radar_fig = plot_radar_chart(df, selected_field, metrics=list(display_metrics.keys(
    )), selected_label=selected_labels, color_map=color_map)

    if radar_fig:
        st.plotly_chart(radar_fig, use_container_width=True, key="radar_chart")
