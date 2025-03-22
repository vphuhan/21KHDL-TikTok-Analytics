import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from preprocess import load_data
from config import COLUMN_LABELS
# Import custom functions from `visualization.py`
from visualization import (
    analyze_hashtag_engagement,
    plot_video_duration_vs_views,
    plot_video_duration_vs_engagement,
    plot_improved_top_hashtags,
    plot_hashtag_trends,
    analyze_hashtag_count_effect,
    get_top_hashtags_by_group,
    plot_interactive_hashtag_analysis,
    plot_posting_time_vs_views,
    plot_posting_day_vs_engagement,
    render_chart
)

# 📂 Import preprocessed data from `data_preprocessing.py`
# from data_preprocessing import video_info_df as df
df = load_data("notebooks/preprocess/content_analyse.csv")


# 🎨 Set Streamlit page configuration
st.set_page_config(page_title="TikTok Insights Dashboard", layout="wide")

# 🎯 Dashboard Title
st.title("📊 TikTok Insights Dashboard")
st.write("Analyze TikTok video performance and hashtag engagement.")

# 🔄 Sidebar Navigation
st.sidebar.header("Tùy chọn phân tích")

category_options = sorted({
    cat for sublist in df['category'] if isinstance(sublist, list)
    for cat in sublist if isinstance(cat, str)
})

selected_category = st.sidebar.multiselect(
    "Chọn chủ đề:", options=category_options, default=None
)

stat_type = st.sidebar.radio("Loại thống kê:", options=['mean', 'median', 'count'], format_func=lambda x: {
    'mean': 'Trung bình',
    'median': 'Trung vị',
    'count': 'Số lượng video'
}.get(x, x))

# Filter by category
if selected_category:
    df = df[df['category'].apply(lambda cats: any(
        cat in cats for cat in selected_category))]

# 📌 Tabs for different insights
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 Video Performance",
    "📈 Hashtag Engagement",
    "📊",
    "📌"
])

with tab1:
    st.subheader("🎬 Video Performance Insights")

    # 📌 Metric Selector
    metric_options = {
        "Views": "statsV2.playCount",
        "Likes": "statsV2.diggCount",
        "Comments": "statsV2.commentCount",
        "Shares": "statsV2.shareCount",
        "Collects": "statsV2.collectCount",
        "Engagement Rate": "engagement_rate",
    }
    selected_metric = st.radio("📊 Select Metric:", list(
        metric_options.keys()), horizontal=True)

    # Get the column name based on selection
    metric_col = metric_options[selected_metric]

    st.markdown("## 1. Hiệu suất theo trường nội dung")

    FIELDS_TO_ANALYZE = [
        'hook_type', 'structure_style', 'tone_of_voice', 'pacing',
        'has_cta', 'cta_type', 'has_personal_story', 'main_content_focus',
        'speaking_style'
    ]

    selected_field = st.selectbox(
        "Chọn trường cần hiển thị biểu đồ:",
        options=FIELDS_TO_ANALYZE,
        format_func=lambda x: COLUMN_LABELS.get(x, x)
    )

    fig = render_chart(df, selected_field, metric_col, stat_type)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    # Organize into 2 columns
    col1, col2 = st.columns(2)

    # 📊 Video Duration vs. Selected Metric
    with col1:
        # st.write(f"📌 **Video Duration vs. {selected_metric}**")
        fig1 = plot_video_duration_vs_views(df, metric_col)
        st.plotly_chart(fig1, use_container_width=True)

    # 🎨 Video Duration vs. Engagement (Alternative Metric View)
    with col2:
        # st.write(f"📌 **Video Duration vs. Engagement ({selected_metric})**")
        fig2 = plot_video_duration_vs_engagement(df, metric_col)
        st.plotly_chart(fig2, use_container_width=True)

    # 📅 Posting Time Analysis
    st.markdown("---")
    st.subheader("⏰ Best Time to Post for Higher Views & Engagement")

    # Organize into 2 columns
    col3, col4 = st.columns(2)

    # 🕒 Posting Hour vs. Selected Metric
    with col3:
        st.write(f"📌 **Posting Time (19h-22h) vs. {selected_metric}**")
        fig3 = plot_posting_time_vs_views(df, metric_col)
        st.plotly_chart(fig3, use_container_width=True)

    # 📅 Weekday vs. Selected Metric
    with col4:
        st.write(f"📌 **Weekend (Fri-Sun) vs. {selected_metric}**")
        fig4 = plot_posting_day_vs_engagement(df, metric_col)
        st.plotly_chart(fig4, use_container_width=True)


# 📌 HASHTAG ANALYSIS TAB
# with tab2:  # Rename this tab to "Hashtag Analysis"
#     st.title("🔍 Hashtag Analysis Dashboard")

#     # Sidebar Filters
#     st.sidebar.subheader("🔧 Hashtag Analysis Settings")

#     # Select Top N Hashtags for Engagement & Trends
#     top_n = st.sidebar.slider("Select Top N Hashtags",
#                               min_value=3, max_value=10, value=5)

#     # Select Time Aggregation for Trends
#     time_agg = st.sidebar.radio("Choose Time Grouping:", [
#                                 "Daily", "Weekly", "Monthly"])

#     # Layout: Two-Column Structure for Engagement & Trends
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("📈 Hashtag Engagement Insights")
#         fig3 = plot_improved_top_hashtags(
#             analyze_hashtag_engagement(df, top_n))
#         st.plotly_chart(fig3, use_container_width=True)

#     with col2:
#         st.subheader("📊 Hashtag Trends Over Time")
#         fig4 = plot_hashtag_trends(df, time_agg, top_n)
#         st.plotly_chart(fig4, use_container_width=True)

#     # Full-Width Section: Hashtag Count Analysis
#     st.markdown("---")
#     st.subheader("📌 Hashtag Count Effect on Engagement")

#     # Show DataFrames
#     hashtag_effect_df = analyze_hashtag_count_effect(df)
#     top_hashtags_df = get_top_hashtags_by_group(df)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.dataframe(hashtag_effect_df, use_container_width=True)
#     with col2:
#         st.dataframe(top_hashtags_df, use_container_width=True)

#     # Interactive Visualization
#     fig5 = plot_interactive_hashtag_analysis(
#         hashtag_effect_df, top_hashtags_df)
#     st.plotly_chart(fig5, use_container_width=True)
