import streamlit as st
import pandas as pd
from visualization import (
    load_data, 
    analyze_hashtag_engagement, 
    plot_improved_top_hashtags, 
    plot_hashtag_trends,
    analyze_hashtag_count_effect, 
    get_top_hashtags_by_group, 
    plot_interactive_hashtag_analysis
)

# Set Streamlit page config
st.set_page_config(page_title="TikTok Hashtag Insights", layout="wide")

# Title & Intro
st.title("📊 TikTok Hashtag Engagement Dashboard")
st.write("Analyze the top-performing hashtags based on different engagement metrics.")

# Load the dataset
DATA_PATH = "./data/processed/video_infor.csv"  
df = load_data(DATA_PATH)

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")

# Allow user to select analysis type
analysis_type = st.sidebar.radio("Select Analysis Type", 
                                 ["Hashtag Engagement", "Hashtag Trends", "Hashtag Count Effect"])

# 📌 Hashtag Engagement Analysis
if analysis_type == "Hashtag Engagement":
    top_n = st.slider("Select Top N Hashtags", min_value=3, max_value=10, value=5)
    top_hashtags = analyze_hashtag_engagement(df, top_n=top_n)
    fig = plot_improved_top_hashtags(top_hashtags)
    st.plotly_chart(fig, use_container_width=True)

# 📌 Hashtag Trends Analysis
elif analysis_type == "Hashtag Trends":
    st.sidebar.subheader("📅 Select Time Aggregation")
    time_agg = st.sidebar.radio("Choose time grouping:", ["Daily", "Weekly", "Monthly"])
    
    top_n_trends = st.slider("Select Top N Trending Hashtags", min_value=3, max_value=10, value=5)
    fig_trends = plot_hashtag_trends(df, time_agg=time_agg, top_n=top_n_trends)
    
    st.plotly_chart(fig_trends, use_container_width=True)

# 📌 Hashtag Count Effect Analysis
elif analysis_type == "Hashtag Count Effect":
    st.subheader("📊 Hashtag Count Effect on Engagement")

    # Compute hashtag count effect
    hashtag_effect_df = analyze_hashtag_count_effect(df)
    st.dataframe(hashtag_effect_df)

    # Compute top hashtags by group
    top_hashtags_df = get_top_hashtags_by_group(df)
    st.dataframe(top_hashtags_df)

    # Interactive visualization
    st.plotly_chart(plot_interactive_hashtag_analysis(hashtag_effect_df, top_hashtags_df), use_container_width=True)
