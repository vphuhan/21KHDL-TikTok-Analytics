import os
import sys
from data_loader import load_data
from utils import *

try:
    import streamlit as st
    from google import genai
    import time
except ImportError as e:
    import traceback
    print(f"Error importing required packages: {e}")
    print(traceback.format_exc())
    try:
        # If streamlit is successfully imported, show error in UI
        if 'st' in globals():
            st.error(
                f"Failed to import required packages. Please install them using: pip install -r requirements.txt\n\nError: {e}")
            st.stop()
    except:
        # If we can't even use streamlit, exit the program
        sys.exit(1)


# App configuration
st.set_page_config(page_title="Write Scripts", page_icon="📝")


# Available AI Models
available_models = [
    # Input token limit: 1,048,576
    # Output token limit: 8,192
    "gemini-2.0-flash",

    # Input token limit 2,048,576
    # Output token limit 8,192
    "gemini-2.0-pro-exp",

    # "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-flash-thinking-exp-1219",

    # Input token limit 1,048,576
    # Output token limit 8,192
    "gemini-2.0-flash-lite",

    # Input token limit 1,048,576
    # Output token limit 8,192
    "gemini-1.5-flash",

    # Input token limit 1,048,576
    # Output token limit 8,192
    "gemini-1.5-flash-8b",

    # Input token limit 2,097,152
    # Output token limit 8,192
    "gemini-1.5-pro",

    "learnlm-1.5-pro-experimental",

    "gemma-3-27b-it",
]


def get_model():
    # Function to get the selected model
    return st.sidebar.selectbox(
        "Select AI Model:",
        available_models,
        index=available_models.index("gemini-2.0-flash")
    )


# Get selected model
model = get_model()
print(f"Selected Model: {model}")


# Initialize session state variables
if 'formatted_script' not in st.session_state:
    st.session_state.formatted_script = None

# Tải dữ liệu với vòng quay chờ
with st.spinner("Đang tải dữ liệu TikTok..."):
    # Tải dữ liệu
    features_df = load_data()


def display_script_sections(script_data):
    # --- THÔNG TIN CHUNG ---
    st.markdown("### 📝 Tổng quan video")
    st.markdown(
        f"**🎬 Mô tả video:** {script_data.get('video_description', '')}")
    st.markdown(f"**⏱️ Độ dài dự kiến:** {script_data.get('duration', '')}")
    st.markdown(f"**📍 Bối cảnh:** {script_data.get('setting', '')}")
    st.markdown(f"**👤 Nhân vật:** {script_data.get('characters', '')}")
    st.markdown("---")

    st.markdown("### 🎬 Kịch bản theo từng phần")
    updated_sections = []

    # Khởi tạo session state cho dữ liệu chỉnh sửa nếu chưa có
    if 'updated_script_data' not in st.session_state:
        st.session_state.updated_script_data = script_data.copy()

    # Xử lý xoá phần nếu có
    sections_to_delete = []
    for idx in range(len(st.session_state.updated_script_data.get("main_content", []))):
        if st.session_state.get(f"delete_section_{idx}", False):
            sections_to_delete.append(idx)
            st.session_state[f"delete_section_{idx}"] = False
    for idx in sorted(sections_to_delete, reverse=True):
        st.session_state.updated_script_data["main_content"].pop(idx)

    # Hiển thị từng đoạn
    for idx, section in enumerate(st.session_state.updated_script_data.get("main_content", [])):
        key_prefix = f"sec_{idx}"
        # Nếu chưa có, khởi tạo edit mode
        if f"{key_prefix}_edit" not in st.session_state:
            st.session_state[f"{key_prefix}_edit"] = False
        edit_mode = st.session_state[f"{key_prefix}_edit"]

        default_text = f"[{section['time_range']}] {section['title']}"
        # Dòng tiêu đề với nút sửa và xoá
        col_title, col_btns = st.columns([8, 2])
        with col_title:
            if edit_mode:
                time_title_input = st.text_input(
                    "⏱️ Thời gian & tiêu đề", default_text, key=f"{key_prefix}_time_title", label_visibility="collapsed")
            else:
                st.markdown(
                    f"""
                    <div style="background-color: #f0f0f0; padding: 8px 16px; border-radius: 6px;">
                        <strong>{default_text}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with col_btns:
            if not edit_mode:
                if st.button("✏️ Sửa", key=f"{key_prefix}_edit_btn", help="Sửa", use_container_width=True):
                    st.session_state[f"{key_prefix}_edit"] = True
                    st.rerun()
            else:
                if st.button("✅ Lưu", key=f"{key_prefix}_save_btn", help="Lưu", use_container_width=True):
                    # Lấy giá trị chỉnh sửa cho tiêu đề
                    time_title_raw = st.session_state.get(
                        f"{key_prefix}_time_title", default_text)
                    if "]" in time_title_raw:
                        time_part, title_part = time_title_raw.split(
                            "]", 1)
                        section["time_range"] = time_part.strip(" [")
                        section["title"] = title_part.strip()
                    st.session_state[f"{key_prefix}_edit"] = False
                    st.rerun()

        # Phần nội dung: xem hoặc chỉnh sửa
        col1, col2 = st.columns([1, 2])
        if edit_mode:
            with col1:
                st.markdown("🎥 **Cảnh quay**")
                visual_input = st.text_area(
                    "🎥 Cảnh quay", section['visual_description'], key=f"{key_prefix}_visual", height=100, label_visibility="collapsed")
            with col2:
                st.markdown("🗣️ **Lời thoại**")
                dialogue_input = st.text_area(
                    "🗣️ Lời thoại", section['dialogue'], key=f"{key_prefix}_dialogue", height=100, label_visibility="collapsed")
            # Cập nhật giá trị trong session state để không bị mất khi rerun
            if f"{key_prefix}_visual" in st.session_state:
                section["visual_description"] = visual_input
            if f"{key_prefix}_dialogue" in st.session_state:
                section["dialogue"] = dialogue_input
        else:
            with col1:
                st.markdown("🎥 **Cảnh quay**")
                st.markdown(section['visual_description'])
            with col2:
                st.markdown("🗣️ **Lời thoại**")
                st.markdown(f"\"{section['dialogue']}\"")

        updated_sections.append({
            "time_range": section["time_range"],
            "title": section["title"],
            "visual_description": section["visual_description"],
            "dialogue": section["dialogue"]
        })

    return st.session_state.updated_script_data


st.title("✍️ Tạo kịch bản TikTok từ mô tả")

user_description = st.text_area("Nhập mô tả video bạn muốn tạo:",
                                placeholder="Làm video TikTok hướng dẫn nấu mì tôm trứng siêu nhanh, siêu dễ cho sinh viên.", height=150)

if st.button("Tạo kịch bản") and user_description:
    key = "AIzaSyBaT3UMomQUPjjpbRD2pCrE_sk3nT6P47w"  # vphacc096@gmail.com
    client = genai.Client(api_key=key)

    with st.spinner("Phân tích mô tả bằng Gemini..."):
        label_dict = generate_labels_from_description(
            user_description, client, model)

        duration = None
        if label_dict is None:
            filtered_df = features_df
            filter_cat_df = features_df
        elif label_dict and label_dict['categories'] == 'Không liên quan ẩm thực':
            st.error(
                "Yêu cầu của bạn không liên quan đến ẩm thực! Vui lòng thử lại với một mô tả khác.")
        else:
            if label_dict.get("duration") is not None:
                duration = int(label_dict.pop("duration", None))

            filtered_df = filter_by_multiple_labels_unified(
                features_df, label_dict, min_count=10)
            filter_cat_df = features_df[features_df['categories']
                                        == label_dict['categories']]

        mean_word_count = int(filtered_df['transcript_word_count'].mean())
        mean_duration = int(filtered_df['video.duration'].mean())
        mean_word_per_second = filtered_df['word_per_second'].mean()
        mean_hashtag_count = int(filtered_df['hashtag_count'].mean())
        top_10_hashtags = filter_cat_df['hashtags'].explode(
        ).value_counts().head(10).index
        top_10_hashtags_text = ', '.join(top_10_hashtags)
        transcript_sample_text, desc_sample_text = format_transcript_desc_examples(
            filtered_df)

        if duration is None:
            duration = mean_duration

        word_count = int(mean_word_per_second * duration)
        print(f"Duration: {duration}")
        print(f"Word Count: {word_count}")

    with st.spinner("Tạo kịch bản thô..."):
        plain_script = generate_plain_script(
            user_description, transcript_sample_text, word_count, client, model)

    with st.spinner("Định dạng lại kịch bản..."):
        formatted_script = format_script_with_gemini(
            plain_script, desc_sample_text, mean_word_per_second, mean_hashtag_count, top_10_hashtags_text, client, model)

        # Save to session state
        st.session_state.formatted_script = formatted_script
        # Initialize the updated_script_data in session state
        st.session_state.updated_script_data = formatted_script.copy()

    st.header("🎬 Kịch bản gợi ý")

# Always check if formatted_script exists in session state, not just the local variable
if st.session_state.formatted_script:
    display_script_sections(st.session_state.formatted_script)
