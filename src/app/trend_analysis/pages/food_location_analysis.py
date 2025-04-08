import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
from collections import defaultdict
import os
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Phân Tích Xu Hướng Ẩm Thực Việt Nam",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 500;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .description {
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .highlight {
        color: #1E40AF;
        font-weight: 500;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #6B7280;
        font-size: 0.8rem;
    }
    .metric-container {
        background-color: #F3F4F6;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)
    
# Function to load and cache data
@st.cache_data(ttl=3600)
def load_data():
    # file_path = "C:/Users/nguye/OneDrive/Tài liệu/GitHub/21KHDL-TikTok-Analytics/notebooks/extract_food_location/final.parquet"
    file_path = "src/app/trend_analysis/final.parquet"
    df = pd.read_parquet(file_path)
    return df

# Load data
try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
    data_loaded = False

# Define functions for each section
@st.cache_data
def get_data_overview_info(df):
    """Prepare data overview information without widgets"""
    # Calculate time range and metrics
    min_date = df['date'].min().strftime('%d/%m/%Y')
    max_date = df['date'].max().strftime('%d/%m/%Y')
    total_records = len(df)
    unique_weeks = df['year_week'].nunique()
    
    # Format year_week for display (Y2023_W47 format)
    df['year_week_formatted'] = df['year_week'].apply(
        lambda x: f"Y{x.split('-')[0]}_W{int(x.split('-')[1]):02d}" if '-' in str(x) else x
    )
    
    # Get formatted min and max year_week for display
    min_year_week = df['year_week'].min()
    max_year_week = df['year_week'].max()
    min_year_week_display = f"Y{min_year_week.split('-')[0]}_W{int(min_year_week.split('-')[1]):02d}" if '-' in str(min_year_week) else min_year_week
    max_year_week_display = f"Y{max_year_week.split('-')[0]}_W{int(max_year_week.split('-')[1]):02d}" if '-' in str(max_year_week) else max_year_week
    
    # Count records by week
    weekly_counts = df.groupby('year_week').size().reset_index(name='count')
    
    # Add the formatted display version
    weekly_counts['year_week_display'] = weekly_counts['year_week'].apply(
        lambda x: f"Y{x.split('-')[0]}_W{int(x.split('-')[1]):02d}" if '-' in str(x) else x
    )
    
    return {
        'min_date': min_date,
        'max_date': max_date,
        'total_records': total_records,
        'unique_weeks': unique_weeks,
        'min_year_week_display': min_year_week_display,
        'max_year_week_display': max_year_week_display,
        'weekly_counts': weekly_counts,
    }

def display_data_overview(df):
    """Display general overview and statistics about the dataset"""
    st.markdown("<h2 class='sub-header'>Tổng Quan Dữ Liệu</h2>", unsafe_allow_html=True)
    
    overview_info = get_data_overview_info(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng số bản ghi", f"{overview_info['total_records']:,}")
    with col2:
        st.metric("Thời gian bắt đầu", overview_info['min_year_week_display'])
    with col3:
        st.metric("Thời gian kết thúc", overview_info['max_year_week_display'])
    with col4:
        st.metric("Số tuần dữ liệu", overview_info['unique_weeks'])
    
    st.markdown("##### Phân bố dữ liệu theo thời gian")
    
    fig = px.bar(
        overview_info['weekly_counts'], 
        x='year_week', 
        y='count',
        labels={'count': 'Số lượng bản ghi'},
        title='Số lượng bản ghi theo tuần'
    )
    
    fig.update_layout(
        xaxis_title="Tuần",
        yaxis_title="Số lượng",
        height=500,
        hovermode="x unified",
        yaxis=dict(range=[0, 300]),
        margin=dict(b=120)
    )
    
    fig.update_xaxes(
        tickmode='array',
        tickvals=overview_info['weekly_counts']['year_week'].tolist(),
        ticktext=overview_info['weekly_counts']['year_week_display'].tolist(),
        tickangle=90,
        tickfont=dict(size=10)
    )
    
    # Add custom hover template
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Số lượng: %{y:,.0f}<extra></extra>',
    )
    
    st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------
@st.cache_data
def get_food_category_data(df):
    all_foods = df['foods'].explode().dropna()
    food_counts = all_foods.value_counts()
    
    def identify_food_groups(food_counts):
        # Dictionary to store tokens for each food
        food_tokens = {}
        for food in food_counts.index:
            tokens = food.lower().split()
            food_tokens[food] = tokens
        
        # Common Vietnamese food prefixes that typically come first
        prefixes = {"mì", "bún", "cơm", "bánh", "chả", "chân gà", "thịt", "cá", "hải", "phở", "phô"}
        
        # Track which foods have been processed and mappings
        food_to_group = {}
        food_groups = defaultdict(list)
        processed_foods = set()
        
        # Process each food
        for food in food_counts.index:
            if food in processed_foods:
                continue
                
            base_tokens = food_tokens[food]
            current_group = []
            
            # Find similar foods based on common words
            for other_food in food_counts.index:
                if other_food in processed_foods:
                    continue
                    
                other_tokens = food_tokens[other_food]
                common_words = set(base_tokens) & set(other_tokens)
                
                # If at least 2 words are common, group these foods
                if len(common_words) >= 2:
                    current_group.append(other_food)
                    processed_foods.add(other_food)
            
            # Create a meaningful group name
            if current_group:
                # Collect all words from the foods in this group
                all_words = []
                original_phrases = []
                
                for group_food in current_group:
                    all_words.extend(food_tokens[group_food])
                    # Store original words with their order
                    for i in range(len(food_tokens[group_food]) - 1):
                        original_phrases.append(f"{food_tokens[group_food][i]} {food_tokens[group_food][i+1]}")
                
                # Find most common words
                word_counts = pd.Series(all_words).value_counts()
                top_words = word_counts.head(2).index.tolist()
                
                # Determine correct word order
                if len(top_words) >= 2:
                    # Check if the two words appear together in original phrases
                    word_pair = f"{top_words[0]} {top_words[1]}"
                    reversed_pair = f"{top_words[1]} {top_words[0]}"
                    
                    pair_count = sum(1 for phrase in original_phrases if phrase == word_pair)
                    reversed_count = sum(1 for phrase in original_phrases if phrase == reversed_pair)
                    
                    # If prefix word is second, swap the order
                    if top_words[1] in prefixes and top_words[0] not in prefixes:
                        group_name = f"{top_words[1]} {top_words[0]}"
                    # Use the order that appears most in original phrases
                    elif reversed_count > pair_count:
                        group_name = reversed_pair
                    else:
                        group_name = word_pair
                else:
                    group_name = " ".join(top_words)
                
                # Map foods to group
                for group_food in current_group:
                    food_to_group[group_food] = group_name
                    food_groups[group_name].append(group_food)
        
        return food_groups, food_to_group
    
    # Generate food groups
    food_groups, food_to_group = identify_food_groups(food_counts)
    
    # Count occurrences for each group
    group_counts = {}
    for group_name, variants in food_groups.items():
        total_count = sum(food_counts[variant] for variant in variants)
        group_counts[group_name] = {
            'total_count': total_count,
            'variants': variants,
            'variant_counts': {variant: food_counts[variant] for variant in variants}
        }
    
    # Sort groups by total count
    sorted_groups = sorted(group_counts.items(), key=lambda x: x[1]['total_count'], reverse=True)
    
    return {
        'food_groups': food_groups,
        'food_to_group': food_to_group,
        'group_counts': group_counts,
        'sorted_groups': sorted_groups,
        'food_counts': food_counts
    }

@st.cache_data
def prepare_category_details(category_name, category_data, food_counts):
    variants = sorted(
        category_data['variant_counts'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    variant_df = pd.DataFrame(variants, columns=['variant', 'count'])
    total = variant_df['count'].sum()
    variant_df['percentage'] = variant_df['count'] / total * 100
    
    main_variants = variant_df[variant_df['percentage'] >= 5]
    other_variants = variant_df[variant_df['percentage'] < 5]
    
    if len(main_variants) > 10:
        main_variants = main_variants.head(10)
        other_variants = pd.concat([
            variant_df.iloc[10:], 
            other_variants
        ])
    
    plot_data = main_variants.copy()
    
    if not other_variants.empty:
        other_sum = other_variants['count'].sum()
        other_row = pd.DataFrame({
            'variant': ['Các phân loại khác'],
            'count': [other_sum],
            'percentage': [other_sum / total * 100]
        })
        plot_data = pd.concat([plot_data, other_row])
    
    # Format the data for table view
    all_variants_df = pd.DataFrame(variants, columns=['Biến Thể', 'Số Lượng'])
    all_variants_df['Tỉ Lệ'] = all_variants_df['Số Lượng'] / all_variants_df['Số Lượng'].sum() * 100
    all_variants_df['Tỉ Lệ'] = all_variants_df['Tỉ Lệ'].round(2).astype(str) + '%'
    
    return {
        'category_name': category_name,
        'total_count': category_data['total_count'],
        'num_variants': len(category_data['variants']),
        'plot_data': plot_data,
        'all_variants_df': all_variants_df
    }

#---------------------------------------------- 


def analyze_food_categories(df):
    """Analyze and visualize food categories and their variants"""
    st.markdown("<h2 class='sub-header'>Phân Tích Món Ăn Theo Danh Mục</h2>", unsafe_allow_html=True)
    
    # Get processed food category data
    category_data = get_food_category_data(df)
    sorted_groups = category_data['sorted_groups']
    
    # Let user select how many top categories to view
    top_k = st.slider(
        "Chọn số lượng danh mục món ăn",
        min_value=5,
        max_value=min(20, len(sorted_groups)),
        value=10
    )
    
    # Get top K categories
    top_categories = sorted_groups[:top_k]
    
    # Create overview bar chart of categories
    category_names = [group[0].upper() for group in top_categories]
    category_values = [group[1]['total_count'] for group in top_categories]
    
    fig = px.bar(
        x=category_values,
        y=category_names,
        orientation='h',
        labels={'x': 'Số lượng đề cập', 'y': 'Danh mục món ăn'},
        title=f'Top {top_k} Danh Mục Món Ăn Được Đề Cập Nhiều Nhất'
    )
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Create detailed view for selected category
    st.markdown("##### Chi tiết danh mục món ăn")
    st.write("Chọn một danh mục để xem chi tiết của từng loại món ăn:")
    
    # Convert category names to a more readable format for the selectbox
    readable_categories = [f"{cat[0].upper()} ({cat[1]['total_count']} đề cập)" for cat in top_categories]
    selected_category_index = st.selectbox(
        "Danh sách món ăn",
        range(len(readable_categories)),
        format_func=lambda i: readable_categories[i]
    )
    
    # Get the selected category details
    selected_category = top_categories[selected_category_index]
    category_name = selected_category[0]
    category_details = prepare_category_details(
        category_name, 
        selected_category[1],
        category_data['food_counts']
    )
    
    # Display category information
    st.markdown(f"**Loại món: {category_details['category_name'].upper()}**")
    st.markdown(f"Tổng số đề cập: {category_details['total_count']}")
    st.markdown(f"Số lượng phân loại: {category_details['num_variants']}")
    
    # Create pie chart
    fig = px.pie(
        category_details['plot_data'], 
        values='count', 
        names='variant',
        title=f'Phân bố thức ăn trong món {category_details["category_name"].upper()}',
        hover_data=['percentage']
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<br>Tỉ lệ: %{percent}<extra></extra>'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show table of all variants
    with st.expander("Xem chi tiết từng phân loại"):
        st.dataframe(category_details['all_variants_df'], use_container_width=True)

#------------------------------------------------------------- 
@st.cache_data
def prepare_weekly_trend_data(df, food_to_group):
    """Prepare weekly trend data without widgets"""
    # Make sure createTime is processed properly
    if 'year_week' not in df.columns:
        df['year_week'] = pd.to_datetime(df['createTime'], unit='s').dt.strftime('%Y-%U')
        
    # Get all unique weeks
    weeks = sorted(df['year_week'].unique())
    
    # Process weekly trends
    category_counts = defaultdict(lambda: defaultdict(int))
    
    # Group by week and category
    for _, row in df.iterrows():
        if not isinstance(row['foods'], list) or not row['foods']:
            continue
            
        week = row['year_week']
        for food in row['foods']:
            if food in food_to_group:  # Check if food exists in the mapping
                category = food_to_group.get(food, "Khác")
                category_counts[week][category] += 1
    
    # Transform to DataFrame format
    trend_data = []
    for week, categories in category_counts.items():
        for category, count in categories.items():
            trend_data.append({
                'week': week,
                'category': category,
                'count': count
            })
    
    # Create a DataFrame and check if it's empty or missing the required columns
    result_df = pd.DataFrame(trend_data)
    
    # If the DataFrame is empty, create a default one with the required columns
    if result_df.empty or 'category' not in result_df.columns:
        result_df = pd.DataFrame(columns=['week', 'category', 'count'])
        
    return result_df

@st.cache_data
def get_location_data(df, city_list=None):
    """Process location data for visualization with optional city filtering"""
    # Define default city list if none provided
    city_list = [
        "hà nội", "hồ chí minh", "sài gòn", "nha trang", "đà nẵng", 
        "huế", "cần thơ", "hải phòng", "đà lạt", "vũng tàu",
        "biên hòa", "quy nhơn", "buôn ma thuột", "thái nguyên", "vinh",
        "hạ long", "phan thiết", "long xuyên", "việt trì", "thanh hóa",
        "hòa bình", "mỹ tho", "rạch giá", "cam ranh", "đồng hới",
        "tuy hòa", "hà tĩnh", "pleiku", "nam định", "bắc ninh",
        "thái bình", "ninh bình", "cao bằng", "lạng sơn", "tuyên quang",
        "yên bái", "lào cai", "điện biên phủ", "sơn la", "hải dương",
        "hưng yên", "phủ lý", "bắc giang", "lạng sơn", "móng cái",
        "uông bí", "cẩm phả", "bắc kạn", "sapa", "tam đảo",
        "hà giang", "lai châu", "quảng ninh", "hà nam", "quảng ngãi",
        "tam kỳ", "hội an", "kon tum", "gia nghĩa", "buôn hồ",
        "bảo lộc", "bến tre", "trà vinh", "cao lãnh", "sa đéc",
        "vĩnh long", "sóc trăng", "bạc liêu", "cà mau", "hà tiên",
        "tân an", "gò công", "châu đốc", "tây ninh", "thủ dầu một",
        "đồng xoài", "phan rang-tháp chàm", "bà rịa", "thuận an", "dĩ an"
    ]
    
    # Convert city list to lowercase for case-insensitive matching
    city_list = [city.lower() for city in city_list]
    
    # Standardize city data with filtering
    city_counts = df['city_std'].explode().dropna().str.lower()
    filtered_cities = city_counts[city_counts.isin(city_list)]
    city_data = filtered_cities.value_counts().reset_index()
    city_data.columns = ['city', 'count']
    
    # Create district data with city information - filter out null districts
    district_city_data = df[['city_std', 'district_std']].explode('district_std').dropna()
    
    # Additional filter to ensure both city and district are non-null
    district_city_data = district_city_data[
        (district_city_data['city_std'].notna()) & 
        (district_city_data['district_std'].notna()) &
        (district_city_data['district_std'] != 'null') &
        (district_city_data['district_std'] != '')
    ]
    
    # Filter to only include districts from our selected cities
    district_city_data = district_city_data[
        district_city_data['city_std'].str.lower().isin(city_list)
    ]
    
    # Create district data with city hierarchy for treemap
    district_data_with_city = district_city_data.groupby(
        ['city_std', 'district_std']
    ).size().reset_index(name='count')
    
    # Make sure city names are properly capitalized for display
    city_data['city'] = city_data['city'].str.title()
    district_data_with_city['city_std'] = district_data_with_city['city_std'].str.title()
    
    return {
        'city_data': city_data,
        'district_data_with_city': district_data_with_city
    }

def analyze_geospatial_distribution(df):
    """Analyze and visualize geographical distribution of food mentions with predefined cities"""
    st.markdown("<h2 class='sub-header'>Phân Bố Địa Lý</h2>", unsafe_allow_html=True)
    
    # Define list of cities to include
    predefined_cities = [
        "hà nội", "hồ chí minh", "sài gòn", "nha trang", "đà nẵng", 
        "huế", "cần thơ", "hải phòng", "đà lạt", "vũng tàu",
        "biên hòa", "quy nhơn", "buôn ma thuột", "thái nguyên", "vinh",
        "hạ long", "phan thiết", "long xuyên", "việt trì", "thanh hóa",
        "hòa bình", "mỹ tho", "rạch giá", "cam ranh", "đồng hới",
        "tuy hòa", "hà tĩnh", "pleiku", "nam định", "bắc ninh",
        "thái bình", "ninh bình", "cao bằng", "lạng sơn", "tuyên quang",
        "yên bái", "lào cai", "điện biên phủ", "sơn la", "hải dương",
        "hưng yên", "phủ lý", "bắc giang", "lạng sơn", "móng cái",
        "uông bí", "cẩm phả", "bắc kạn", "sapa", "tam đảo",
        "hà giang", "lai châu", "quảng ninh", "hà nam", "quảng ngãi",
        "tam kỳ", "hội an", "kon tum", "gia nghĩa", "buôn hồ",
        "bảo lộc", "bến tre", "trà vinh", "cao lãnh", "sa đéc",
        "vĩnh long", "sóc trăng", "bạc liêu", "cà mau", "hà tiên",
        "tân an", "gò công", "châu đốc", "tây ninh", "thủ dầu một",
        "đồng xoài", "phan rang-tháp chàm", "bà rịa", "thuận an", "dĩ an"
    ]
    
    # Get location data with custom city filtering
    location_data = get_location_data(df, city_list=predefined_cities)
    city_data = location_data['city_data']
    district_data_with_city = location_data['district_data_with_city']
    
    if city_data.empty:
        st.warning("Không tìm thấy dữ liệu cho các thành phố đã chọn!")
        return
    
    # Display city-based visualization - LIMIT TO TOP 10
    st.markdown("##### Phân bố đề cập theo thành phố/tỉnh đã chọn")
    
    # Sort by count (descending) then take only top 10
    sorted_city_data = city_data.sort_values('count', ascending=False).head(10)
    # Re-sort for display (ascending for horizontal bar chart)
    sorted_city_data = sorted_city_data.sort_values('count', ascending=True)
    
    # Create visualization
    fig = px.bar(
        sorted_city_data,
        x='count',
        y='city',
        orientation='h',
        labels={'count': 'Số lượng đề cập', 'city': 'Thành phố/Tỉnh'},
        title='Top 10 thành phố/tỉnh có nhiều đề cập nhất'
    )
    
    fig.update_layout(
        xaxis_title="Số lượng đề cập",
        yaxis_title="Thành phố/Tỉnh",
        height=400  # Fixed height for top 10
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create enhanced treemap with city and district hierarchy (also limit to top 10 cities)
    st.markdown("##### Bản đồ phân bố địa lý (Top 10 thành phố và Quận/Huyện)")
    
    # Prepare data for hierarchical treemap
    if not district_data_with_city.empty:
        # Get only districts for the top 10 cities
        top_10_cities = sorted_city_data['city'].tolist()
        filtered_district_data = district_data_with_city[
            district_data_with_city['city_std'].isin(top_10_cities)
        ]
        
        # Create treemap with city -> district hierarchy
        fig = px.treemap(
            filtered_district_data,
            path=['city_std', 'district_std'],  # Hierarchical path
            values='count',
            title='Phân bố địa lý theo Top 10 thành phố và quận/huyện',
            color='count',
            color_continuous_scale=[[0, 'rgb(0,68,137)'], [0.5, 'rgb(0,142,171)'], [1, 'rgb(0,204,150)']]
        )
        
        # Improve treemap appearance
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<extra></extra>',
            textinfo="label+value"
        )
        
        fig.update_layout(
            height=700,  # Larger height for better visibility
            margin=dict(t=50, l=25, r=25, b=25)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Không có dữ liệu quận/huyện cho các thành phố đã chọn.")

@st.cache_data
def find_unique_weekly_foods(df, threshold_pct=60, min_mentions=2, comparison_weeks=3):
    """
    Identifies foods that are uniquely trending in specific weeks with lower thresholds
    to ensure more weeks have data.
    """
    # Ensure we have a date column with proper week formatting
    if 'date' not in df.columns and 'createTime' in df.columns:
        df['date'] = pd.to_datetime(df['createTime'], unit='s')
    
    # Use the standardized year_week column if it exists, otherwise create it
    if 'year_week' not in df.columns:
        df['year_week'] = df['date'].dt.strftime('%Y-%U')
    
    # Explode foods list to get individual food items
    exploded_df = df.explode('foods')[['year_week', 'foods']].dropna()
    
    # Get all weeks in chronological order
    all_weeks = sorted(exploded_df['year_week'].unique())
    
    # Create a lookup for formatted week display
    week_display = {}
    for week in all_weeks:
        if '-' in str(week):
            year, w_num = week.split('-')
            week_display[week] = f"Y{year}_W{int(w_num):02d}"
        else:
            week_display[week] = week
    
    # Calculate food counts for all weeks
    all_food_counts = exploded_df.groupby(['year_week', 'foods']).size().reset_index(name='count')
    
    # Get a list of consistently popular foods (appear in most weeks)
    popular_threshold = len(all_weeks) * 0.7  # Foods that appear in 70% or more of all weeks
    common_foods = exploded_df.groupby('foods')['year_week'].nunique()
    consistently_popular = common_foods[common_foods >= popular_threshold].index.tolist()
    
    # Dictionary to store unique foods by week
    unique_weekly_foods = {}
    
    # Process each week
    for i, current_week in enumerate(all_weeks):
        # Skip the first weeks since we need previous weeks for comparison
        if i < comparison_weeks:
            unique_weekly_foods[current_week] = []
            continue
        
        # Get previous weeks for comparison
        previous_weeks = all_weeks[max(0, i-comparison_weeks):i]
        
        # Get foods for current week
        current_week_foods = all_food_counts[all_food_counts['year_week'] == current_week]
        
        # Filter out foods that don't meet minimum mention threshold
        current_week_foods = current_week_foods[current_week_foods['count'] >= min_mentions]
        
        # Skip consistently popular foods
        current_week_foods = current_week_foods[~current_week_foods['foods'].isin(consistently_popular)]
        
        # If no foods meet the criteria, try a lower threshold temporarily for this week
        if current_week_foods.empty:
            current_week_foods = all_food_counts[
                (all_food_counts['year_week'] == current_week) & 
                (all_food_counts['count'] >= 1)
            ]
            current_week_foods = current_week_foods[~current_week_foods['foods'].isin(consistently_popular)]
        
        # For each food in current week, check if it's unique to this week
        unique_foods = []
        for _, row in current_week_foods.iterrows():
            food = row['foods']
            current_count = row['count']
            
            # Get counts for this food in previous weeks
            previous_counts = all_food_counts[
                (all_food_counts['foods'] == food) & 
                (all_food_counts['year_week'].isin(previous_weeks))
            ]['count'].sum()
            
            # Calculate what percentage of mentions are in current week vs previous weeks
            total_mentions = current_count + previous_counts
            if total_mentions == 0:
                continue
                
            current_percentage = (current_count / total_mentions) * 100
            
            # Lower the threshold for weeks with little data to ensure some results
            week_threshold = threshold_pct
            if len(current_week_foods) < 5:
                week_threshold = max(40, threshold_pct - 20)
                
            # If current week accounts for at least threshold_pct% of mentions, consider it uniquely trending
            if current_percentage >= week_threshold:
                unique_foods.append((food, current_count, current_percentage))
        
        # Sort unique foods by count and store in dictionary
        unique_foods.sort(key=lambda x: x[1], reverse=True)
        unique_weekly_foods[current_week] = unique_foods
    
    return unique_weekly_foods, week_display

#----------------------
@st.cache_data
def prepare_unique_food_visualization_data(unique_foods_by_week, week_display, top_n=5):
    """Prepare visualization data for unique foods without widgets"""
    viz_data = []
    for week, foods in unique_foods_by_week.items():
        formatted_week = week_display[week]
        for i, (food, count, percentage) in enumerate(foods[:top_n]):
            viz_data.append({
                'week': week,
                'week_display': formatted_week,
                'food': food,
                'count': count,
                'percentage': percentage,
                'rank': i + 1
            })
    
    if not viz_data:
        return None
    
    viz_df = pd.DataFrame(viz_data)
    
    # Create a proper sort key for weeks to ensure chronological order
    if 'week' in viz_df.columns and not viz_df.empty:
        viz_df['week_sort'] = viz_df['week'].apply(
            lambda w: int(w.replace('-', '')) if '-' in w else w
        )
        viz_df = viz_df.sort_values('week_sort')
    
    weeks_with_data = [week for week, foods in unique_foods_by_week.items() if foods]
    
    return {
        'viz_df': viz_df,
        'weeks_with_data': weeks_with_data
    }

def analyze_unique_weekly_foods(df):
    """Visualize uniquely trending foods by week with simpler display"""
    st.markdown("<h2 class='sub-header'>Các Món Ăn Nổi Bật Theo Tuần</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        threshold_pct = st.slider(
            "Ngưỡng phần trăm (%):",
            min_value=40,
            max_value=80,
            value=60,  # Lower default threshold to get more results
            help="Phần trăm tối thiểu của đề cập xuất hiện trong tuần hiện tại so với các tuần trước đó"
        )
    
    with col2:
        min_mentions = st.slider(
            "Số lượng đề cập tối thiểu:",
            min_value=1,
            max_value=10,
            value=2,  # Lower default threshold
            help="Số lượng đề cập tối thiểu để được xem xét"
        )
    
    with col3:
        comparison_weeks = st.slider(
            "Số tuần so sánh:",
            min_value=1,
            max_value=8,
            value=3,
            help="Số tuần trước đó để so sánh"
        )
    
    with st.spinner("Đang phân tích dữ liệu..."):
        # Get cached unique foods data with formatted week display
        unique_foods_by_week, week_display = find_unique_weekly_foods(
            df,
            threshold_pct=threshold_pct,
            min_mentions=min_mentions,
            comparison_weeks=comparison_weeks
        )
        
        # Prepare visualization data
        viz_data_container = prepare_unique_food_visualization_data(
            unique_foods_by_week, 
            week_display,
            top_n=10  # Increase to get more foods per week
        )
        
        if viz_data_container is None or viz_data_container['viz_df'].empty:
            st.warning("Không có đủ dữ liệu để hiển thị món ăn nổi bật với các tham số đã chọn.")
            return
        
        viz_df = viz_data_container['viz_df']
        weeks_with_data = viz_data_container['weeks_with_data']

    # Show week selector
    if not weeks_with_data:
        st.warning("Không tìm thấy tuần nào có món ăn nổi bật với các tham số đã chọn.")
        return

    # Format all weeks for display in the dropdown
    all_formatted_weeks = []
    for week in sorted(df['year_week'].unique()):
        if '-' in str(week):
            year, w_num = week.split('-')
            all_formatted_weeks.append((week, f"Y{year}_W{int(w_num):02d}"))
        else:
            all_formatted_weeks.append((week, week))
            
    # Create a dictionary for lookup
    week_to_display = {k: v for k, v in all_formatted_weeks}
    display_to_week = {v: k for k, v in all_formatted_weeks}
    
    # Show dropdown with formatted week values
    formatted_weeks = [week_to_display[w] for w in sorted(df['year_week'].unique())]
    selected_display = st.selectbox(
        "Chọn tuần để phân tích:",
        formatted_weeks,
        index=min(len(formatted_weeks)-1, 0)  # Default to most recent week
    )
    
    # Convert display format back to the actual week value
    selected_year_week = display_to_week.get(selected_display)
    
    # Create two columns - one for selected week, one for overview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Create a formatted header for the week
        week_header = f"Món ăn nổi bật trong Tuần {week_to_display[selected_year_week]}"
        st.markdown(f"##### {week_header}")
        
        # Get foods for selected week
        week_foods = []
        if selected_year_week in unique_foods_by_week:
            week_foods = unique_foods_by_week[selected_year_week]
        
        if not week_foods:
            st.info("Không có món ăn nổi bật nào trong tuần này với các tham số đã chọn.")
        else:
            # Create a simple list of foods with count and percentage
            for i, (food, count, percentage) in enumerate(week_foods[:15], 1):
                st.markdown(
                    f"**{i}. {food}** - {count} đề cập ({percentage:.1f}%)"
                )
    
    with col2:
        # Show a preview of other weeks' unique foods
        st.markdown("##### Xem trước các tuần khác")
        
        # Create tabs for nearby weeks
        all_weeks = sorted(unique_foods_by_week.keys())
        if selected_year_week in all_weeks:
            current_idx = all_weeks.index(selected_year_week)
            
            # Get a range of 5 weeks centered on selected week if possible
            start_idx = max(0, current_idx - 2)
            end_idx = min(len(all_weeks), current_idx + 3)
            nearby_weeks = all_weeks[start_idx:end_idx]
            
            # Create a tab for each nearby week
            if nearby_weeks:
                tabs = st.tabs([week_to_display.get(w, w) for w in nearby_weeks])
                
                for i, week in enumerate(nearby_weeks):
                    with tabs[i]:
                        week_foods = unique_foods_by_week[week]
                        if week_foods:
                            # Show top 5 foods for each week in preview
                            for j, (food, count, percentage) in enumerate(week_foods[:5], 1):
                                st.markdown(
                                    f"**{j}. {food}** - {count} đề cập ({percentage:.1f}%)"
                                )
                        else:
                            st.info("Không có món ăn nổi bật.")
    
    # Improved heatmap visualization for weekly food trends
    if len(weeks_with_data) > 1:
        st.markdown("##### Món ăn nổi bật theo tuần")
        
        # Create heatmap data
        if not viz_df.empty:
            # Create tabs for different visualization options
            heat_tabs = st.tabs(["Heatmap Tối Ưu", "Heatmap Đầy Đủ", "Biểu Đồ Bubble", "Bảng Dữ Liệu"])
            
            with heat_tabs[0]:
                # ENHANCED HEATMAP - Optimized for visualization
                
                # 1. Filter foods that appear in at least 2 weeks for more meaningful trends
                food_week_counts = viz_df.groupby('food')['week'].nunique()
                multi_week_foods = food_week_counts[food_week_counts >= 1].index.tolist()
                
                # 2. Get top foods by total mentions across all weeks
                top_foods_overall = viz_df.groupby('food')['count'].sum().nlargest(15).index.tolist()
                
                # 3. Combine multi-week and top foods, prioritizing multi-week foods
                target_foods = list(set(multi_week_foods + top_foods_overall))[:15]
                
                # Create optimized heatmap data
                opt_viz_df = viz_df[viz_df['food'].isin(target_foods)]
                
                if not opt_viz_df.empty:
                    # Pivot and handle column naming
                    opt_heatmap = opt_viz_df.pivot_table(
                        index='food',
                        columns='week',
                        values='count',
                        aggfunc='sum',
                        fill_value=0
                    )
                    
                    # Format column names 
                    column_mapping = {col: week_to_display.get(col, col) for col in opt_heatmap.columns}
                    opt_heatmap = opt_heatmap.rename(columns=column_mapping)
                    
                    # Add sorting for more intuitive display
                    row_totals = opt_heatmap.sum(axis=1)
                    opt_heatmap = opt_heatmap.loc[row_totals.sort_values(ascending=False).index]
                    
                    # Create enhanced heatmap
                    fig = px.imshow(
                        opt_heatmap,
                        labels=dict(x="Tuần", y="Món ăn", color="Số lượng đề cập"),
                        title="Heatmap món ăn nổi bật theo tuần (Được tối ưu cho khả năng hiển thị)",
                        color_continuous_scale="RdBu_r",  # Better color scale
                        aspect="auto"  # Better aspect ratio
                    )
                    
                    # Better axis formatting
                    fig.update_xaxes(
                        title="Tuần",
                        tickangle=45,  # Less extreme angle
                        tickmode='array',
                        tickvals=list(range(len(opt_heatmap.columns))),
                        ticktext=opt_heatmap.columns
                    )
                    
                    # Show values in cells
                    fig.update_traces(
                        text=opt_heatmap.values,
                        texttemplate="%{text}",
                        textfont={"size": 12}
                    )
                    
                    fig.update_layout(
                        height=500,
                        margin=dict(l=100, r=20, t=50, b=80)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add interpretation guidance
                    st.info("💡 Màu càng đậm thể hiện món ăn được đề cập nhiều hơn. Heatmap này chỉ hiển thị các món nổi bật nhất và được đề cập trong nhiều tuần.")
                else:
                    st.warning("Không đủ dữ liệu để tạo biểu đồ heatmap tối ưu.")
            
            with heat_tabs[1]:
                # ORIGINAL FULL HEATMAP (with minor improvements)
                # Pivot for heatmap
                heatmap_data = viz_df.pivot_table(
                    index='food',
                    columns='week',
                    values='count',
                    aggfunc='sum',
                    fill_value=0
                )
                
                # Create a mapping for pretty column names (formatted weeks)
                column_mapping = {col: week_to_display.get(col, col) for col in heatmap_data.columns}
                heatmap_data = heatmap_data.rename(columns=column_mapping)
                
                # Get top foods overall for better visualization
                top_foods = viz_df.groupby('food')['count'].sum().nlargest(20).index
                if len(top_foods) > 0:
                    heatmap_data = heatmap_data.loc[heatmap_data.index.isin(top_foods)]
                    
                    # Create heatmap visualization using plotly
                    fig = px.imshow(
                        heatmap_data,
                        labels=dict(x="Tuần", y="Món ăn", color="Số lượng đề cập"),
                        title="Heatmap đầy đủ các món ăn nổi bật theo tuần",
                        color_continuous_scale="Blues"
                    )
                    
                    fig.update_xaxes(
                        title="Tuần",
                        tickangle=90,
                        tickmode='array',
                        tickvals=list(range(len(heatmap_data.columns))),
                        ticktext=heatmap_data.columns
                    )
                    
                    fig.update_layout(height=600)
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Không đủ dữ liệu để tạo biểu đồ heatmap.")
            
            with heat_tabs[2]:
                # BUBBLE CHART - Alternative visualization better for sparse data
                # Prepare data
                bubble_data = viz_df.copy()
                
                # Add formatted week display
                bubble_data['week_display'] = bubble_data['week'].map(week_to_display)
                
                # Sort by count for better display
                bubble_data = bubble_data.sort_values('count', ascending=False)
                
                # Limit to top 12 foods by total mentions
                top_bubble_foods = bubble_data.groupby('food')['count'].sum().nlargest(12).index.tolist()
                bubble_data = bubble_data[bubble_data['food'].isin(top_bubble_foods)]
                
                # Create bubble chart
                fig = px.scatter(
                    bubble_data,
                    x='week_display',
                    y='food',
                    size='count',
                    color='percentage',  # Use percentage for color
                    size_max=40,  # Maximum bubble size
                    hover_name='food',
                    hover_data={
                        'count': True,
                        'percentage': ':.1f%',
                        'week_display': False,
                        'food': False
                    },
                    labels={
                        'week_display': 'Tuần',
                        'food': 'Món ăn',
                        'count': 'Số lượng đề cập',
                        'percentage': 'Phần trăm (%)'
                    },
                    color_continuous_scale='Viridis',
                    title='Biểu đồ bubble thể hiện món ăn nổi bật theo tuần'
                )
                
                # Adjust layout
                fig.update_layout(
                    xaxis=dict(title='Tuần'),
                    yaxis=dict(title='Món ăn'),
                    height=500,
                    coloraxis_colorbar=dict(title='Phần trăm (%)')
                )
                
                # Customize hover template
                fig.update_traces(
                    hovertemplate='<b>%{hovertext}</b><br>Tuần: %{x}<br>Số lượng: %{customdata[0]}<br>Phần trăm: %{customdata[1]}%<extra></extra>'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.info("💡 Kích thước bong bóng thể hiện số lượng đề cập, màu sắc thể hiện phần trăm tập trung trong tuần đó. Biểu đồ này hiển thị tốt hơn với dữ liệu thưa.")
            
            with heat_tabs[3]:
                # DATA TABLE VIEW - For those who prefer raw data
                st.subheader("Bảng dữ liệu món ăn theo tuần")
                
                # Create a pivot table with formatted values
                pivot_table = viz_df.pivot_table(
                    index='food',
                    columns='week',
                    values='count',
                    aggfunc='sum',
                    fill_value=0
                )
                
                # Format column names
                pivot_table = pivot_table.rename(columns=week_to_display)
                
                # Add total column
                pivot_table['Tổng đề cập'] = pivot_table.sum(axis=1)
                
                # Sort by total mentions
                pivot_table = pivot_table.sort_values('Tổng đề cập', ascending=False)
                
                # Format for display
                display_table = pivot_table.copy()
                
                # Display the table
                st.dataframe(display_table, use_container_width=True)
                
                # Add download option
                csv = pivot_table.to_csv().encode('utf-8')
                st.download_button(
                    label="Tải xuống dữ liệu dưới dạng CSV",
                    data=csv,
                    file_name="food_trends_by_week.csv",
                    mime="text/csv",
                )
        else:
            st.warning("Không có đủ dữ liệu để tạo biểu đồ với các tham số đã chọn.")
# Main app
def main():
    """Main application function"""
    
    # Header
    st.markdown("<h1 class='main-header'>Phân Tích Xu Hướng Ẩm Thực Việt Nam</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Phân tích dữ liệu xu hướng đề cập đến món ăn Việt Nam trên mạng xã hội dựa trên dữ liệu TikTok.</p>", unsafe_allow_html=True)
    
    # Check if data loaded successfully
    if not data_loaded:
        st.warning("Không thể tiếp tục vì dữ liệu không được tải thành công.")
        return
        
    # Application sections
    display_data_overview(df)
    analyze_food_categories(df)
    analyze_geospatial_distribution(df)
    analyze_unique_weekly_foods(df)

# Run the app
if __name__ == "__main__":
    main()
