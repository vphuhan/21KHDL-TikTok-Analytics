import streamlit as st
import pandas as pd
import plotly.express as px
import ast
# from wordcloud import WordCloud
import matplotlib.pyplot as plt

from config import COLUMN_LABELS


def render_chart(df, field, metric, stat_type):
    # đảm bảo cột tồn tại trước khi truy cập
    if metric not in df.columns or field not in df.columns:
        return None

    if field == 'cta_type':
        # df = df[df['has_cta'] == True]  # chỉ giữ video có CTA
        # df = df[df['cta_type'].notna()]  # loại bỏ NaN
        df = df[df['cta_type'] != "[nan]"]  # loại bỏ NaN
        # df['cta_type'] == "[nan]"
        df = df[df['cta_type'].apply(lambda x: isinstance(
            x, list) and len(x) > 0)]  # loại bỏ list rỗng

    if field not in df.columns:
        return None

    exploded = df[[metric, field]].copy()
    exploded = exploded.explode(field)
    exploded = exploded.dropna(subset=[field])  # loại bỏ nan trước khi group

    if stat_type == 'mean':
        grouped = (
            exploded.groupby(field)[metric]
            .mean()
            .reset_index(name=f'{stat_type}_{metric}')
            .sort_values(by=f'{stat_type}_{metric}', ascending=False)
        )
    elif stat_type == 'median':
        grouped = (
            exploded.groupby(field)[metric]
            .median()
            .reset_index(name=f'{stat_type}_{metric}')
            .sort_values(by=f'{stat_type}_{metric}', ascending=False)
        )
    elif stat_type == 'count':
        grouped = (
            exploded.groupby(field)[metric]
            .count()
            .reset_index(name='Số lượng video')
            .sort_values(by='Số lượng video', ascending=False)
        )
        metric = 'Số lượng video'
    else:
        return None

    fig = px.bar(
        grouped,
        x=grouped.columns[1],
        y=field,
        color=field,
        orientation='h',
        title=f'{COLUMN_LABELS.get(field, field)} vs {grouped.columns[1]}',
        labels={
            grouped.columns[1]: grouped.columns[1],
            field: COLUMN_LABELS.get(field, field)
        },
        height=600
    )
    fig.update_layout(showlegend=False)
    return fig


def render_wordcloud(df, field):
    from itertools import chain
    if field not in df.columns:
        return
    all_keywords = list(chain.from_iterable(df[field].dropna()))
    all_keywords = [str(word) for word in all_keywords if pd.notnull(word)]
    if not all_keywords:
        st.warning(
            f"Không có dữ liệu để hiển thị WordCloud cho {COLUMN_LABELS.get(field, field)}.")
        return
    text = " ".join(all_keywords)
    wc = WordCloud(width=1000, height=600, background_color='white',
                   collocations=False).generate(text)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)


def render_duration_chart(df, metric='views'):
    import numpy as np

    bins = [0, 10, 30, 60, 90, 120, 180, 300, 600, float("inf")]
    labels = ["<10s", "10-30s", "30-60s", "60-90s", "90-120s",
              "2 mins", "3-5 mins", "5-10 mins", ">10 mins"]

    if 'video.duration' not in df.columns or metric not in df.columns:
        st.warning("Thiếu cột 'video.duration' hoặc metric để phân tích.")
        return

    df = df.dropna(subset=['video.duration', metric])
    df['duration_bin'] = pd.cut(
        df['video.duration'], bins=bins, labels=labels, right=False)

    grouped = (
        df.groupby('duration_bin')[metric]
        .mean()
        .reset_index(name=f'avg_{metric}')
        .sort_values(by='duration_bin')
    )

    fig = px.bar(
        grouped,
        x='duration_bin',
        y=f'avg_{metric}',
        title=f'Trung bình {metric.capitalize()} theo độ dài video',
        labels={'duration_bin': 'Độ dài video',
                f'avg_{metric}': f'Trung bình {metric.capitalize()}'},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


def render_duration_chart(df, metric='views', stat_type='mean'):
    import numpy as np

    bins = [0, 10, 30, 60, 90, 120, 180, 300, 600, float("inf")]
    labels = ["<10s", "10-30s", "30-60s", "60-90s", "90-120s",
              "2 mins", "3-5 mins", "5-10 mins", ">10 mins"]

    if 'duration' not in df.columns or metric not in df.columns:
        st.warning("Thiếu cột 'duration' hoặc chỉ số để phân tích.")
        return

    df = df.dropna(subset=['duration', metric])
    df['duration_bin'] = pd.cut(
        df['duration'], bins=bins, labels=labels, right=False)

    if stat_type == 'mean':
        grouped = (
            df.groupby('duration_bin')[metric]
            .mean()
            .reset_index(name=f'{stat_type}_{metric}')
        )
    elif stat_type == 'median':
        grouped = (
            df.groupby('duration_bin')[metric]
            .median()
            .reset_index(name=f'{stat_type}_{metric}')
        )
    elif stat_type == 'count':
        grouped = (
            df.groupby('duration_bin')[metric]
            .count()
            .reset_index(name='Số lượng video')
        )
        metric = 'Số lượng video'
    else:
        st.warning("Loại thống kê không hợp lệ.")
        return

    y_col = grouped.columns[1]

    fig = px.bar(
        grouped,
        x='duration_bin',
        y=y_col,
        title=f'{y_col} theo độ dài video',
        labels={'duration_bin': 'Độ dài video', y_col: y_col},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
