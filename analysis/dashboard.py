import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('C:/Users/nguye/OneDrive/Tài liệu/GitHub/21KHDL-TikTok-Analytics/data/interim/video_info.csv', sep='\t', encoding='utf-8')
    # Clean and preprocess data
    df['desc'] = df['desc'].fillna('').apply(lambda x: re.sub(r'[^\w\s]', '', x))
    return df

df = load_data()

# Helper functions
def categorize_content(desc):
    desc = desc.lower()
    if any(word in desc for word in ['hài', 'vui', 'meme', 'thử thách']):
        return 'Hài/Meme/Challenge'
    elif any(word in desc for word in ['mẹo', 'kiến thức', 'giáo dục', 'sức khỏe']):
        return 'Giáo dục/Sức khỏe'
    elif any(word in desc for word in ['tâm sự', 'confession', 'câu chuyện']):
        return 'Cá nhân/Storytime'
    elif any(word in desc for word in ['drama', 'tranh luận', 'tranh cãi']):
        return 'Drama/Tranh cãi'
    return 'Khác'

# Create new columns
df['content_type'] = df['desc'].apply(categorize_content)
df['viral_score'] = (df['stats.shareCount'] * 0.4 + 
                    df['stats.playCount'] * 0.3 + 
                    df['stats.diggCount'] * 0.3)

# Streamlit app
st.title('Phân Tích Khả Năng Viral & Tương Tác')

# Section 3: Viral Content Analysis
st.header('3. Phân Tích Nội Dung Viral')
col1, col2 = st.columns(2)

with col1:
    # Content Type Analysis
    fig = px.bar(df.groupby('content_type')['viral_score'].mean().reset_index(),
                 x='content_type', y='viral_score',
                 title='Điểm Viral Trung Bình Theo Thể Loại')
    st.plotly_chart(fig)

with col2:
    # Emotion Word Cloud
    emotion_words = ' '.join(df['desc'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(emotion_words)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud)
    plt.axis('off')
    st.pyplot(plt)

# Video Quality Analysis
st.subheader('Chất Lượng Hình Ảnh vs Viral Score')
fig = px.scatter(df, x='video.VQScore', y='viral_score',
                 color='content_type', hover_data=['desc'])
st.plotly_chart(fig)

# Section 4: Industry Analysis
st.header('4. Phân Tích Ngành Hàng')
industry_metrics = df.groupby('CategoryType').agg({
    'stats.playCount': 'mean',
    'stats.diggCount': 'mean',
    'stats.shareCount': 'mean'
}).reset_index()

fig = px.bar(industry_metrics.melt(id_vars='CategoryType'), 
             x='CategoryType', y='value', color='variable',
             title='Tương Tác Trung Bình Theo Ngành Hàng',
             labels={'value': 'Số lượt trung bình', 'variable': 'Loại tương tác'})
st.plotly_chart(fig)

# Interactive Filters
st.sidebar.header('Bộ Lọc')
min_plays = st.sidebar.slider('Lượt xem tối thiểu', 
                             min_value=0, 
                             max_value=int(df['stats.playCount'].max()),
                             value=1000)
filtered_df = df[df['stats.playCount'] >= min_plays]

# Time Analysis
st.subheader('Xu Hướng Theo Thời Gian')
fig = px.line(df.groupby(pd.to_datetime(df['createTime'], unit='s').dt.date)['viral_score'].mean(),
              title='Xu Hướng Viral Theo Thời Gian')
st.plotly_chart(fig)

# Advanced Analysis
st.header('Phân Tích Nâng Cao')
analysis_type = st.selectbox('Chọn loại phân tích', 
                            ['Tương Quan Giữa Các Chỉ Số', 
                             'Phân Bổ Thời Lượng Video'])

if analysis_type == 'Tương Quan Giữa Các Chỉ Số':
    fig = px.scatter_matrix(df[['stats.playCount', 'stats.diggCount', 
                              'stats.shareCount', 'video.duration']],
                          title='Ma Trận Tương Quan')
    st.plotly_chart(fig)
else:
    fig = px.histogram(df, x='video.duration', 
                     title='Phân Bổ Thời Lượng Video')
    st.plotly_chart(fig)