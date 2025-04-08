# pages/hashtag_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from data_preprocessing import video_info_df as df
# from datetime import datetime

# Get the cached data from session state
if 'df' in st.session_state:
    df = st.session_state.df
else:
    st.error("Data not loaded. Please return to the main page.")
    st.stop()

# Constants
METRIC_LABELS = {
    "Lượt xem": "statsV2.playCount",
    "Lượt thích": "statsV2.diggCount",
    "Lượt bình luận": "statsV2.commentCount",
    "Lượt chia sẻ": "statsV2.shareCount"
}

METRIC_COLORS = {
    "statsV2.playCount": "Viridis",
    "statsV2.diggCount": "Blues",
    "statsV2.commentCount": "Greens",
    "statsV2.shareCount": "Reds"
}

def filter_data_by_hashtag(df, hashtag):
    """Filter dataframe to only include videos with the specified hashtag"""
    return df[df['hashtags'].apply(lambda x: hashtag in x if isinstance(x, list) else False)]

def get_hashtag_stats(df, hashtag, metric_col):
    """Calculate statistics for a specific hashtag"""
    hashtag_df = filter_data_by_hashtag(df, hashtag)
    
    if hashtag_df.empty:
        return None
    
    stats = {
        'total_videos': len(hashtag_df),
        'total_engagement': hashtag_df[metric_col].sum(),
        'avg_engagement': hashtag_df[metric_col].mean(),
        'median_engagement': hashtag_df[metric_col].median(),
        'max_engagement': hashtag_df[metric_col].max(),
        'min_engagement': hashtag_df[metric_col].min()
    }
    
    return stats

def plot_hashtag_performance_over_time(df, hashtag, metric_col, time_agg="Theo tháng"):
    """Plot performance of a hashtag over time"""
    metric_name = next(k for k, v in METRIC_LABELS.items() if v == metric_col)
    hashtag_df = filter_data_by_hashtag(df, hashtag)
    
    if time_agg == "Theo ngày":
        hashtag_df["time_group"] = hashtag_df["createTime"].dt.strftime("%Y-%m-%d")
    elif time_agg == "Theo tuần":
        hashtag_df["time_group"] = hashtag_df["createTime"].dt.to_period("W").dt.to_timestamp()
    else:  # Theo tháng
        hashtag_df["time_group"] = hashtag_df["createTime"].dt.to_period("M").dt.to_timestamp()
    
    grouped = hashtag_df.groupby("time_group")[metric_col].sum().reset_index()
    
    fig = px.line(
        grouped, 
        x="time_group", 
        y=metric_col,
        title=f"Hiệu suất của #{hashtag} theo thời gian ({time_agg})",
        labels={
            "time_group": "Ngày",
            metric_col: metric_name
        },
        line_shape="spline"
    )
    
    # fig.add_trace(line_color=METRIC_COLORS.get(metric_col, "Viridis"),
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Thời gian",
        yaxis_title=metric_name
    )
    
    return fig

def plot_hashtag_co_occurrence(df, hashtag, top_n=10):
    """Plot most common co-occurring hashtags"""
    # Get all videos containing the target hashtag
    target_videos = df[df['hashtags'].apply(lambda x: hashtag in x if isinstance(x, list) else False)]
    
    # Explode the hashtags and count co-occurrences
    co_occurring = target_videos.explode('hashtags')
    co_occurring_counts = co_occurring[co_occurring['hashtags'] != hashtag].groupby('hashtags').size().reset_index(name='count')
    top_co_occurring = co_occurring_counts.nlargest(top_n, 'count')
    
    fig = px.bar(
        top_co_occurring,
        x='hashtags',
        y='count',
        title=f"Hashtag thường xuất hiện cùng #{hashtag}",
        labels={'hashtags': 'Hashtag', 'count': 'Số lần xuất hiện'},
        color='count',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        xaxis_title="Hashtag",
        yaxis_title="Số lần xuất hiện cùng",
        coloraxis_showscale=False
    )
    
    return fig

def plot_hashtag_author_performance(df, hashtag, metric_col, top_n=10):
    """Plot top authors using this hashtag"""
    metric_name = next(k for k, v in METRIC_LABELS.items() if v == metric_col)
    hashtag_df = filter_data_by_hashtag(df, hashtag)
    
    author_stats = hashtag_df.groupby('author.uniqueId').agg(
        total_engagement=(metric_col, 'sum'),
        video_count=('id', 'count'),
        avg_engagement=(metric_col, 'mean')
    ).reset_index().nlargest(top_n, 'total_engagement')
    
    fig = px.bar(
        author_stats,
        x='author.uniqueId',
        y='total_engagement',
        title=f"Tác giả sử dụng #{hashtag} hiệu quả nhất",
        labels={
            'author.uniqueId': 'Tác giả',
            'total_engagement': f'Tổng {metric_name}',
            'video_count': 'Số video'
        },
        hover_data=['video_count', 'avg_engagement'],
        color='total_engagement',
        color_continuous_scale=METRIC_COLORS.get(metric_col, "Viridis")
    )
    
    fig.update_layout(
        xaxis_title="Tác giả",
        yaxis_title=f"Tổng {metric_name}",
        coloraxis_showscale=False
    )
    
    return fig

def display_hashtag_analysis(df):
    """Main function to display the hashtag analysis page"""
    st.set_page_config(
        page_title="🔍 Phân Tích Hashtag Đơn Lẻ",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Phân Tích Hashtag Đơn Lẻ")
    
    # Get list of all unique hashtags
    all_hashtags = sorted(list(set([tag for sublist in df['hashtags'].dropna() for tag in sublist])))
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Cài Đặt Phân Tích")
        selected_hashtag = st.selectbox(
            "Chọn hashtag để phân tích",
            all_hashtags,
            index=all_hashtags.index('1phutsaigon') if '1phutsaigon' in all_hashtags else 0
        )
        
        selected_metric = st.selectbox(
            "Chỉ số phân tích",
            list(METRIC_LABELS.keys()),
            index=0
        )
        metric_col = METRIC_LABELS[selected_metric]
        
        time_agg = st.selectbox(
            "Nhóm theo thời gian",
            ["Theo ngày", "Theo tuần", "Theo tháng"],
            index=2
        )
        
        top_n = st.slider(
            "Số lượng kết quả hiển thị",
            5, 20, 10
        )
    
    # Main content
    st.header(f"Phân tích hiệu suất của #{selected_hashtag}")
    
    # Hashtag statistics cards
    stats = get_hashtag_stats(df, selected_hashtag, metric_col)
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tổng video", f"{stats['total_videos']:,}")
        col2.metric(f"Tổng {selected_metric}", f"{stats['total_engagement']:,}")
        col3.metric(f"Trung bình {selected_metric}", f"{stats['avg_engagement']:,.0f}")
        col4.metric(f"Trung vị {selected_metric}", f"{stats['median_engagement']:,.0f}")
        
        # Performance over time
        st.subheader(f"Hiệu suất #{selected_hashtag} theo thời gian")
        st.plotly_chart(
            plot_hashtag_performance_over_time(df, selected_hashtag, metric_col, time_agg),
            use_container_width=True
        )
        
        # Co-occurring hashtags
        st.subheader(f"Hashtag thường đi cùng #{selected_hashtag}")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.plotly_chart(
                plot_hashtag_co_occurrence(df, selected_hashtag, top_n),
                use_container_width=True
            )
        
        with col2:
            st.markdown("### Nhận xét")
            st.markdown(f"""
            - Phân tích các hashtag thường xuất hiện cùng #{selected_hashtag}
            - Giúp phát hiện các chủ đề liên quan
            - Có thể dùng để tìm ý tưởng cho chiến dịch tiếp theo
            """)
        
        # Top authors using this hashtag
        st.subheader(f"Tác giả sử dụng #{selected_hashtag} hiệu quả nhất")
        st.plotly_chart(
            plot_hashtag_author_performance(df, selected_hashtag, metric_col, top_n),
            use_container_width=True
        )
        
        # Raw data
        with st.expander("Xem dữ liệu thô"):
            hashtag_data = filter_data_by_hashtag(df, selected_hashtag)
            st.dataframe(
                hashtag_data[['createTime', 'desc', metric_col, 'author.uniqueId', 'hashtags']].sort_values(metric_col, ascending=False),
                use_container_width=True
            )
    else:
        st.warning(f"Không tìm thấy dữ liệu cho hashtag #{selected_hashtag}")

if __name__ == "__main__":
    display_hashtag_analysis(df)