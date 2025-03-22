import streamlit as st
from utils.preprocess import load_data
from utils.chart import render_chart, render_wordcloud, render_duration_chart
from config import COLUMN_LABELS

st.set_page_config(layout="wide")

# Load data
df = load_data("data/content_analyse.csv")

# Sidebar filters
st.sidebar.header("Tùy chọn phân tích")

category_options = sorted({
    cat for sublist in df['category'] if isinstance(sublist, list)
    for cat in sublist if isinstance(cat, str)
})

selected_category = st.sidebar.multiselect(
    "Chọn chủ đề:", options=category_options, default=None
)

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

# st.markdown("## 2. Word Cloud cho Từ khoá Cảm xúc")
# render_wordcloud(df, field='emotion_keywords')

# st.markdown("## 3. Word Cloud cho Hashtag")
# render_wordcloud(df, field='hashtags')

st.markdown("## 4. Hiệu suất theo độ dài video")
render_duration_chart(df, metric=selected_metric, stat_type=stat_type)
