import streamlit as st
import pandas as pd
import plotly.express as px
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Bản dịch cột
COLUMN_LABELS = {
    'category': 'Chủ đề',
    'hook_type': 'Kiểu mở đầu',
    'structure_style': 'Cấu trúc nội dung',
    'tone_of_voice': 'Giọng điệu',
    'pacing': 'Nhịp độ',
    'has_cta': 'Có CTA',
    'cta_type': 'Kiểu CTA',
    'has_personal_story': 'Có kể chuyện cá nhân',
    'main_content_focus': 'Trọng tâm nội dung',
    'speaking_style': 'Cách nói',
    'emotion_keywords': 'Từ khoá cảm xúc',
    'hashtags': 'Hashtag'
}

# Load data


@st.cache_data
def load_data():
    df = pd.read_csv("content_analyse.csv")
    list_columns = list(COLUMN_LABELS.keys())

    def parse_list_column(value):
        try:
            parsed = ast.literal_eval(value) if isinstance(
                value, str) and value.startswith('[') else value
            return parsed if isinstance(parsed, list) else [parsed]
        except:
            return [value]

    for col in list_columns:
        if col in df.columns:
            df[col] = df[col].apply(parse_list_column)

    # Loại bỏ video không liên quan ẩm thực
    df = df[~df['category'].apply(lambda x: isinstance(
        x, list) and "Audio không liên quan ẩm thực" in x)]

    return df


def render_chart(df, field, metric, stat_type):
    # đảm bảo cột tồn tại trước khi truy cập
    if metric not in df.columns or field not in df.columns:
        return None

    if field == 'cta_type':
        df = df[df['has_cta'] == True]  # chỉ giữ video có CTA
        df = df[df['cta_type'].notna()]  # loại bỏ NaN
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


# Load data
df = load_data()

# Sidebar
st.sidebar.header("Tùy chọn phân tích")

category_options = sorted({
    cat for sublist in df['category'] if isinstance(sublist, list)
    for cat in sublist if isinstance(cat, str)
})

selected_category = st.sidebar.multiselect(
    "Chọn chủ đề:", options=category_options, default=None
)

# Lọc theo category nếu có chọn
if selected_category:
    df = df[df['category'].apply(lambda cats: any(
        cat in cats for cat in selected_category))]

selected_field = st.sidebar.selectbox("Chọn trường nội dung:", [
    'hook_type', 'structure_style', 'tone_of_voice', 'pacing',
    'has_cta', 'cta_type', 'has_personal_story', 'main_content_focus',
    'speaking_style'
], format_func=lambda x: COLUMN_LABELS.get(x, x))

selected_metric = st.sidebar.selectbox("Chỉ số hiệu suất:", [
    'views', 'likes', 'comments', 'shares', 'collects', 'engagement_rate'
], format_func=lambda x: {
    'views': 'Lượt xem',
    'likes': 'Lượt thích',
    'comments': 'Bình luận',
    'shares': 'Chia sẻ',
    'collects': 'Lưu',
    'engagement_rate': 'Tỷ lệ tương tác'
}.get(x, x))

stat_type = st.sidebar.radio("Loại thống kê:", options=['mean', 'median', 'count'], format_func=lambda x: {
    'mean': 'Trung bình',
    'median': 'Trung vị',
    'count': 'Số lượng video'
}.get(x, x))

# Main layout
st.title("📊 TikTok Content Insight Dashboard")

st.markdown("## 1. Biểu đồ hiệu suất theo trường nội dung")
fig = render_chart(df, selected_field, selected_metric, stat_type)
if fig:
    st.plotly_chart(fig, use_container_width=True)

st.markdown("## 2. Word Cloud cho Từ khoá Cảm xúc")
render_wordcloud(df, field='emotion_keywords')

st.markdown("## 3. Word Cloud cho Hashtag")
render_wordcloud(df, field='hashtags')

st.markdown("## 4. Hiệu suất theo độ dài video")
render_duration_chart(df, metric=selected_metric)
