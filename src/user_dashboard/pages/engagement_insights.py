import streamlit as st
import plotly.express as px
from footer import display_footer
import pandas as pd

# Hàm tải dữ liệu được lưu trữ
@st.cache_data
def load_data():
    """Tải và lưu trữ dữ liệu người dùng đã được làm sạch từ tệp CSV"""
    cleaned_user_csv_file = "data/interim/cleaned_user_info.csv"
    cleaned_user_info_df = pd.read_csv(cleaned_user_csv_file)
    return cleaned_user_info_df

# Tải dữ liệu đã lưu trữ
cleaned_user_info_df = load_data()

# Tiêu đề trang
st.markdown(
    '<h2 style="text-align:center;">🏆 Phân tích mức độ tương tác</h2>', 
    unsafe_allow_html=True
)
st.write("Phân tích mối quan hệ giữa **người theo dõi** và **mức độ tương tác (lượt thích/trái tim)**.")

# Tạo các cột bố cục cho bộ chọn
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    follower_level = st.selectbox("📌 Chọn mức người theo dõi:", ["Thấp", "Trung bình", "Cao"])
with col2:
    engagement_level = st.selectbox("🔥 Chọn mức tương tác:", ["Thấp", "Trung bình", "Cao"])
with col3:
    plotly_theme = st.selectbox("🎨 Chọn chủ đề:", ["plotly_dark", "seaborn", "ggplot2", "plotly_white"])

# Tính tỷ lệ tương tác
cleaned_user_info_df['engagement_ratio'] = (
    cleaned_user_info_df['stats.heart'] / 
    cleaned_user_info_df['stats.followerCount'].replace(0, 1)
)

# Xác định các phân vị để lọc
percentiles = [0, 0.33, 0.66, 1]
low_followers = cleaned_user_info_df['stats.followerCount'].quantile(percentiles[1])
high_followers = cleaned_user_info_df['stats.followerCount'].quantile(percentiles[2])
low_engagement = cleaned_user_info_df['engagement_ratio'].quantile(percentiles[1])
high_engagement = cleaned_user_info_df['engagement_ratio'].quantile(percentiles[2])

# Lọc theo mức người theo dõi
if follower_level == "Thấp":
    filtered_df = cleaned_user_info_df[cleaned_user_info_df['stats.followerCount'] <= low_followers]
elif follower_level == "Trung bình":
    filtered_df = cleaned_user_info_df[
        (cleaned_user_info_df['stats.followerCount'] > low_followers) & 
        (cleaned_user_info_df['stats.followerCount'] <= high_followers)
    ]
else:
    filtered_df = cleaned_user_info_df[cleaned_user_info_df['stats.followerCount'] > high_followers]

# Lọc theo mức tương tác
if engagement_level == "Thấp":
    filtered_df = filtered_df[filtered_df['engagement_ratio'] <= low_engagement]
elif engagement_level == "Trung bình":
    filtered_df = filtered_df[
        (filtered_df['engagement_ratio'] > low_engagement) & 
        (filtered_df['engagement_ratio'] <= high_engagement)
    ]
else:
    filtered_df = filtered_df[filtered_df['engagement_ratio'] > high_engagement]

# Hiển thị trực quan với vòng quay chờ
with st.spinner("📊 Đang hiển thị phân tích mức độ tương tác..."):
    # Tạo biểu đồ phân tán
    fig = px.scatter(
        filtered_df,
        x='stats.followerCount',
        y='stats.heart',
        size='stats.followerCount',
        color='engagement_ratio',
        color_continuous_scale='viridis',
        hover_data=['user.uniqueId'],
        height=600,
        opacity=0.75
    )
    
    # Cập nhật bố cục biểu đồ
    fig.update_layout(
        xaxis_title="👥 Số lượng người theo dõi",
        yaxis_title="❤️ Tổng số lượt thích",
        template=plotly_theme,
        xaxis_type="log",
        yaxis_type="log",
        showlegend=True,
        coloraxis_colorbar_title="Tỷ lệ tương tác 🔥"
    )

    # Hiển thị kết quả
    st.markdown(
        f'<h3>📊 Thông tin chi tiết về tương tác: {follower_level} Người theo dõi & {engagement_level} Tương tác</h3>',
        unsafe_allow_html=True
    )
    
    # Hiển thị số liệu
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📌 Số lượng người dùng", f"{len(filtered_df):,}")
    with col2:
        st.metric("❤️ Trung bình lượt thích", f"{filtered_df['stats.heart'].mean():,.0f}")
    with col3:
        st.metric("👥 Trung bình người theo dõi", f"{filtered_df['stats.followerCount'].mean():,.0f}")
    
    # Hiển thị biểu đồ
    st.plotly_chart(fig, use_container_width=True)


# Latex string 
latex_string = filtered_df.to_latex()


# Những điểm chính
st.markdown(f"""
## Dataframe sau khi đưa qua latex
{latex_string}
""")