import streamlit as st
import os
import functools
from pathlib import Path
from google import genai


# Cache function to read prompt files
@st.cache_data
def read_prompt_file(file_path):
    """Read and cache prompt content from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


# Function to generate suggestions using Gemini API
@st.cache_data
def generate_suggestion(system_prompt: str, user_description: str):
    """Generate video suggestions using Google's Gemini API."""

    # Generate content
    try:
        client = genai.Client(
            api_key="AIzaSyBYqr4g63GOBTslf5xP0-AbIcSSlAuvMnM")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                system_prompt,
                user_description,
            ],
        )
        return response.text
    except Exception as e:
        st.error(f"Lỗi khi tạo nội dung: {e}")
        return None


st.set_page_config(
    page_title="Hệ thống gợi ý nội dung video ẩm thực",
    page_icon="🍜",
    layout="wide",
)

st.title("Hệ thống gợi ý nội dung video ẩm thực")


# Video direction selection
st.header("Chọn hướng thực hiện video")
video_type = st.radio(
    "Chọn loại video bạn muốn thực hiện:",
    ["Video review món ăn hoặc quán ăn", "Video mukbang", "Video hướng dẫn nấu ăn"]
)
st.write(
    f"Bạn đã chọn: **{video_type}**. Hệ thống sẽ gợi ý nội dung cho video này."
)


# Map the selection to prompt files
prompt_file_mapping = {
    "Video review món ăn hoặc quán ăn": "data/prompts/food_review_template.md",
    "Video mukbang": "data/prompts/mukbang_template.md",
    "Video hướng dẫn nấu ăn": "data/prompts/cooking_template.md"
}

selected_prompt_file = prompt_file_mapping[video_type]
system_prompt = read_prompt_file(selected_prompt_file)

# User input
st.header("Mô tả video của bạn")
user_description = st.text_area(
    "Hãy mô tả chi tiết về video ẩm thực bạn muốn thực hiện:",
    height=150
)

# Generate suggestions
if st.button("Tạo gợi ý"):
    if not user_description.strip():
        st.warning(
            "Vui lòng nhập mô tả về video của bạn trước khi tạo gợi ý.")
    else:
        with st.spinner("Đang tạo gợi ý..."):
            suggestion = generate_suggestion(
                system_prompt, user_description)
            if suggestion:
                st.header("Gợi ý cho video của bạn")
                st.markdown(suggestion)
