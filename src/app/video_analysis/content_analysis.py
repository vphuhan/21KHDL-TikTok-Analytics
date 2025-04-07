import pandas as pd
import numpy as np
import streamlit as st
from itertools import chain
from types import NoneType
from video_analysis.utils.chart import plot_bar_chart, plot_radar_chart, generate_color_map
from video_analysis.config import COLUMN_LABELS, COLUMN_METRICS, STAT_TYPES


@st.cache_data
def load_data():
    """Load data from parquet file and preprocess numpy arrays to lists"""

    def _parse_list(x):
        """Convert numpy arrays to Python lists, handle None values"""
        if isinstance(x, np.ndarray):
            return list(x)
        if isinstance(x, NoneType):
            return []
        return x

    features_df = pd.read_parquet(
        'data/content_analysis/content_analysis_data.parquet')

    # Convert numpy arrays to Python lists for better compatibility
    for col in features_df.columns:
        if features_df[col].apply(lambda x: isinstance(x, np.ndarray)).any():
            features_df[col] = features_df[col].apply(_parse_list)

    return features_df


class TikTokContentAnalysis:
    """Class for TikTok content analysis dashboard"""

    def __init__(self):
        # Configure page layout
        st.set_page_config(layout="wide")

        # Load and prepare data
        self.df = load_data()
        self.df = self.df[self.df['categories'] != 'Không liên quan ẩm thực']

        # Set up fields to analyze
        self.fields_to_analyze = set(COLUMN_LABELS.keys()) - \
            set(['categories', 'has_cta', 'has_personal_story'])

        # Initialize state
        self.selected_category = None
        self.selected_field = None
        self.filtered_df = self.df
        self.color_map = {}

    def _parse_list(self, x):
        """Convert numpy arrays to Python lists, handle None values"""
        if isinstance(x, np.ndarray):
            return list(x)
        if isinstance(x, NoneType):
            return []
        return x

    def setup_sidebar(self):
        """Configure sidebar filters"""
        st.sidebar.header("Tùy chọn phân tích")

        # Category filter
        category_options = self.df['categories'].dropna().unique().tolist()
        self.selected_category = st.sidebar.selectbox(
            "Chọn chủ đề:",
            options=category_options,
            index=None
        )

        # Apply filters
        self.apply_filters()

    def apply_filters(self):
        """Apply selected filters to the dataframe"""
        self.filtered_df = self.df.copy()

        if self.selected_category:
            self.filtered_df = self.filtered_df[self.filtered_df['categories']
                                                == self.selected_category]

    def setup_main_layout(self):
        """Setup main page layout and components"""
        st.title("📊 TikTok Content Insight Dashboard")
        st.markdown("## Về nội dung video")

        # Field selection
        self.selected_field = st.selectbox(
            "Chọn trường cần hiển thị biểu đồ:",
            options=self.fields_to_analyze,
            format_func=lambda x: COLUMN_LABELS.get(x, x),
        )

        # Generate color map for consistency across charts
        labels = self.filtered_df[self.selected_field].explode(
        ).dropna().unique().tolist()
        self.color_map = generate_color_map(labels)

        # Display performance metrics section
        self.display_performance_metrics()

    def display_performance_metrics(self):
        """Display performance metrics section with charts"""
        st.subheader(
            f"Hiệu suất tương tác theo {COLUMN_LABELS.get(self.selected_field, self.selected_field)}")

        # Create two columns for charts
        col1, col2 = st.columns(2)

        with col1:
            self.display_bar_chart(col1)

        with col2:
            self.display_radar_chart(col2)

    def display_bar_chart(self, container):
        """Display bar chart with controls"""
        # Performance metric selection
        selected_metric = st.selectbox(
            "Chỉ số hiệu suất:",
            options=list(COLUMN_METRICS.keys()),
            format_func=lambda x: COLUMN_METRICS.get(x, x)
        )

        # Statistic type selection
        stat_type = st.radio(
            "Loại thống kê:",
            options=list(STAT_TYPES.keys()),
            format_func=lambda x: STAT_TYPES.get(x, x),
            horizontal=True
        )

        # Generate and display bar chart
        fig = plot_bar_chart(
            self.filtered_df,
            self.selected_field,
            selected_metric,
            stat_type,
            color_map=self.color_map
        )

        if fig:
            st.plotly_chart(fig, use_container_width=True, key="bar_chart")

    def display_radar_chart(self, container):
        """Display radar chart with controls"""
        # Prepare data for radar chart
        exploded = self.filtered_df.copy()
        exploded = exploded.explode(self.selected_field).dropna(
            subset=[self.selected_field])
        labels = exploded[self.selected_field].unique()

        # Label selection for radar chart
        selected_labels = st.multiselect(
            "Chọn label để hiển thị radar chart:",
            labels,
            default=None
        )

        # Prepare metrics for radar chart (exclude engagement_rate)
        display_metrics = COLUMN_METRICS.copy()
        display_metrics.pop('engagement_rate', None)

        # Generate and display radar chart
        radar_fig = plot_radar_chart(
            self.filtered_df,
            self.selected_field,
            metrics=list(display_metrics.keys()),
            selected_label=selected_labels,
            color_map=self.color_map
        )

        if radar_fig:
            st.plotly_chart(radar_fig, use_container_width=True,
                            key="radar_chart")

    def run(self):
        """Main application flow"""
        # Set up sidebar filters
        self.setup_sidebar()

        # Set up main layout
        self.setup_main_layout()


# Run the application when script is executed
# if __name__ == "__main__":
app = TikTokContentAnalysis()
app.run()
