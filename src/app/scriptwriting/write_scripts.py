import sys
import os

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

try:
    import streamlit as st
    from google import genai
    import time

    import pandas as pd
    import numpy as np
    from types import NoneType

    import json
    from google import genai
    from google.genai import types


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
# st.set_page_config(page_title="Write Scripts", page_icon="📝")


@st.cache_data
def load_data():
    features_df = pd.read_parquet('data/ScriptGen-data/script_gendata.parquet')

    def parse_list(x):
        if isinstance(x, np.ndarray):
            return list(x)
        if isinstance(x, NoneType):
            return []
    for col in features_df.columns:
        str_flag = features_df[col].apply(
            lambda x: isinstance(x, np.ndarray)).any()
        if str_flag:
            features_df[col] = features_df[col].apply(parse_list)
    return features_df


# st.title("Viết kịch bản video TikTok")
# st.write("[Empty for now]")

# Constants
API_KEY = "AIzaSyBaT3UMomQUPjjpbRD2pCrE_sk3nT6P47w"  # vphacc096@gmail.com
DEFAULT_MODEL = "gemini-2.0-flash"
PAGE_TITLE = "Write Scripts"
PAGE_ICON = "📝"
CONFIG_DIR = "src/app/scriptwriting/config"

# Available AI Models
AVAILABLE_MODELS = [
    "gemini-2.0-flash",         # Input: 1,048,576 tokens, Output: 8,192 tokens
    "gemini-2.0-pro-exp",       # Input: 2,048,576 tokens, Output: 8,192 tokens
    "gemini-2.0-flash-thinking-exp-1219",
    "gemini-2.0-flash-lite",    # Input: 1,048,576 tokens, Output: 8,192 tokens
    "gemini-1.5-flash",         # Input: 1,048,576 tokens, Output: 8,192 tokens
    "gemini-1.5-flash-8b",      # Input: 1,048,576 tokens, Output: 8,192 tokens
    "gemini-1.5-pro",           # Input: 2,097,152 tokens, Output: 8,192 tokens
    "learnlm-1.5-pro-experimental",
    "gemma-3-27b-it",
]


def filter_by_multiple_labels_unified(df, conditions, soft_fields=None, min_count=10):
    """
    Filter a dataframe based on initial conditions with a "relaxation" process:
    - Start with full conditions
    - Process fields in priority order: soft fields first, then strict fields
    - For each field (except 'categories'), gradually reduce labels until we have enough videos (>= min_count)
    - If still not enough, remove the field completely (except 'categories')

    Parameters:
    - df: pandas DataFrame to filter
    - conditions: dict of field -> list of labels to filter on
    - soft_fields: list of field names that can be relaxed first (default priority order)
    - min_count: minimum number of rows required in result

    Returns:
    - Filtered DataFrame with relaxed conditions if necessary
    """
    print(conditions)
    # Input validation
    if df is None or df.empty:
        print("DataFrame is empty or None")
        return df

    if conditions is None or not conditions:
        return df

    # Default soft fields if none provided
    if soft_fields is None:
        soft_fields = ["pacing", "audience_target",
                       "content_style", "tone_of_voice", "cta_type"]

    # Ensure all condition values are lists
    fixed_conditions = {k: v if isinstance(
        v, list) else [v] for k, v in conditions.items()}

    # Determine strict fields (those not in soft_fields)
    strict_fields = [f for f in fixed_conditions.keys()
                     if f not in soft_fields]

    # Processing order: soft fields first in their priority order, then strict fields
    field_order = [
        f for f in soft_fields if f in fixed_conditions] + strict_fields

    def apply_filters(dataframe, filter_conditions):
        """Apply all filter conditions to the dataframe"""
        result = dataframe.copy()
        for field, target_labels in filter_conditions.items():
            if field in result.columns and target_labels:  # Check if field exists and labels are not empty
                result = result[result[field].apply(
                    lambda labels: all(lbl in labels for lbl in target_labels))]
        return result

    # First try with all conditions
    test_conditions = fixed_conditions.copy()
    filtered_df = apply_filters(df, test_conditions)

    if len(filtered_df) >= min_count:
        print("Final condition (full):", test_conditions)
        print(filtered_df.shape)
        return filtered_df

    best_df = filtered_df  # Track the best result so far

    # Process fields in priority order
    for field in field_order:
        # Never relax 'categories' field
        if field == "categories" or field not in test_conditions:
            continue

        original_labels = test_conditions[field].copy()
        if not original_labels:  # Skip if empty list
            continue

        # Try removing labels one by one from the end
        for i in range(1, len(original_labels) + 1):
            candidate_labels = original_labels[:-i]

            # Skip if we'd end up with empty list (will be handled in the field removal step)
            if not candidate_labels:
                continue

            test_conditions[field] = candidate_labels
            filtered_df = apply_filters(df, test_conditions)

            print(
                f"Trying {field} with labels {candidate_labels}: {len(filtered_df)} results")

            if len(filtered_df) >= min_count:
                print("Final condition:", test_conditions)
                print(filtered_df.shape)
                return filtered_df

            # Keep track of best result
            if len(filtered_df) > len(best_df):
                best_df = filtered_df

        # If relaxing labels didn't help enough, try removing the field completely
        if field != "categories":
            del test_conditions[field]
            filtered_df = apply_filters(df, test_conditions)
            print(f"Removed field {field}: {len(filtered_df)} results")

            if len(filtered_df) >= min_count:
                print("Final condition:", test_conditions)
                print(filtered_df.shape)
                return filtered_df

            # Keep track of best result
            if len(filtered_df) > len(best_df):
                best_df = filtered_df

    print("Couldn't meet minimum count requirement. Returning best result with", len(
        best_df), "rows")
    print(best_df.shape)
    return best_df


def load_prompt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def load_schema(path: str) -> dict:
    """Load JSON schema from given file path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_labels_from_description(user_description, client, model):

    label_schema = load_schema(CONFIG_DIR+'/label_schema.json')

    annotate_user_desc_function = {
        "name": "filter_by_multiple_labels",
        # "description": "Dựa trên miêu tả của người dùng về video họ muốn thực hiện, tiến hành gán nhãn cho các trường được định trước.",
        "description": "Dựa trên miêu tả của người dùng về video họ muốn thực hiện, tiến hành lọc ra các video phù hợp với mô tả của người dùng.",
        "parameters": label_schema
    }

    system_instruction = load_prompt(CONFIG_DIR+'/label_instruction.md')

    prompt = "Dựa trên miêu tả của người dùng về video họ muốn thực hiện, tiến hành gán nhãn cho các trường được định trước.\n\n" + \
        f"Miêu tả: {user_description}"

    # Configure the client and tools

    tools = types.Tool(function_declarations=[annotate_user_desc_function])
    config = types.GenerateContentConfig(
        tools=[tools],
        # system_instruction=system_instruction,
        temperature=0.1,
        top_k=15,
        top_p=0.9
    )
    # Send request with function declarations
    response_filter = client.models.generate_content(
        model="gemini-2.0-flash",
        # model=model,
        contents=[system_instruction, prompt],
        config=config,
    )

    tool_call = response_filter.candidates[0].content.parts[0].function_call

    return tool_call.args if tool_call else None


def format_transcript_desc_examples(user_desc_filter_df, min_count=20):
    today = pd.Timestamp.now(tz='Asia/Ho_Chi_Minh')

    # Tính số ngày kể từ khi tạo video
    user_desc_filter_df['days_since'] = (
        today - user_desc_filter_df['createTime']).dt.days
    alpha = 0.7
    user_desc_filter_df['score'] = user_desc_filter_df['statsV2.playCount'] / \
        ((user_desc_filter_df['days_since'] + 1) ** alpha)
    sorted_df = user_desc_filter_df.sort_values(by='score', ascending=False)
    example_df = sorted_df.head(min_count)

    def create_examples(df, col):
        return "\n\n".join(
            [f"{i}. {t}" for i, t in enumerate(df[col], 1)]
        )

    transcript_sample_text = create_examples(example_df, 'transcript')
    desc_sample_text = create_examples(example_df, 'desc')
    return transcript_sample_text, desc_sample_text


def generate_plain_script(
        user_input, transcript_sample_text, word_count, client, model, max_output_tokens=2000):

    prompt_input = {'user_input': user_input,
                    'transcript_sample_text': transcript_sample_text,
                    'word_count': word_count}

    prompt_plain_script = load_prompt(
        CONFIG_DIR+'/plain_script_prompt.md').format(**prompt_input)

    response_plain_script = client.models.generate_content(
        # model="gemini-2.0-flash-thinking-exp-1219",
        # model="gemini-2.0-flash",
        model=model,
        contents=[prompt_plain_script],
        config={'maxOutputTokens': max_output_tokens},
    )

    print(response_plain_script.usage_metadata)
    return response_plain_script.text


def format_script_with_gemini(plain_script, desc_sample_text, mean_word_per_second, mean_hashtag_count, top_10_cat_hashtags_text, client, model):
    script_seconds = len(plain_script.split()) / (mean_word_per_second)
    print("output script words:",  len(plain_script.split()))
    print("output script seconds:",  script_seconds)

    raw_schema = load_schema(
        CONFIG_DIR+'/structured_script_schema.json')
    schema_str = json.dumps(raw_schema)
    schema_str = schema_str.replace(
        "{mean_hashtag_count}", str(mean_hashtag_count))
    response_structured_script_schema = json.loads(schema_str)

    duration_text = f"{int(script_seconds // 60)} phút {int(script_seconds % 60)} giây"
    prompt_input = {'duration_text': duration_text,
                    'top_10_cat_hashtags_text': top_10_cat_hashtags_text,
                    'desc_sample_text': desc_sample_text,
                    'plain_script': plain_script}

    prompt_structured_script = load_prompt(
        CONFIG_DIR+'/structured_script_prompt.md').format(**prompt_input)

    response_structured_script = client.models.generate_content(
        model="gemini-2.0-flash",
        # model=model,
        contents=[prompt_structured_script],
        config={
            'response_mime_type': "application/json",
            'response_schema': response_structured_script_schema,
            # 'system_instruction': system_instruction,
            # 'temperature': 0.1

        }
    )

    try:
        response_dict = json.loads(response_structured_script.text)
    except json.decoder.JSONDecodeError as e:
        print("JSON decode error:", e)
        return None

    # script_seconds = len(response_plain_script.text.split()) / int(mean_word_per_second)
    # response_dict['duration'] = f"{int(script_seconds // 60)} phút {int(script_seconds % 60)} giây"
    # === Tính lại time_range cho từng đoạn main_content ===

    def seconds_to_mmss(sec):
        minutes = int(sec // 60)
        seconds = int(sec % 60)
        return f"{minutes}:{seconds:02d}"

    current_time = 0.0
    for step in response_dict.get("main_content", []):
        dialogue = step.get("dialogue", "")
        word_count = len(dialogue.split())
        duration = duration = round(word_count / mean_word_per_second, 2)

        start = seconds_to_mmss(current_time)
        end = seconds_to_mmss(current_time + duration)
        step["time_range"] = f"{start}-{end}"

        current_time += duration
    return response_dict


class ScriptGenerator:
    def __init__(self):
        self.init_page_config()
        self.init_session_state()
        self.model = self.get_model()
        self.features_df = self.load_data()
        self.client = genai.Client(api_key=API_KEY)

    def init_page_config(self):
        """Initialize Streamlit page configuration"""
        st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide",
                           initial_sidebar_state="expanded",)

    def init_session_state(self):
        """Initialize session state variables"""
        if 'formatted_script' not in st.session_state:
            st.session_state.formatted_script = None
        if 'updated_script_data' not in st.session_state:
            st.session_state.updated_script_data = None

    def get_model(self):
        """Get the selected AI model from sidebar"""
        return st.sidebar.selectbox(
            "Select AI Model:",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL)
        )

    def load_data(self):
        """Load TikTok data with spinner"""
        with st.spinner("Đang tải dữ liệu TikTok..."):
            features_df = load_data()

        if features_df is None:
            st.error("Không thể tải dữ liệu TikTok. Vui lòng thử lại sau.")
            st.stop()

        return features_df

    def generate_script(self, user_description):
        """Generate script based on user description"""
        with st.spinner("Phân tích mô tả..."):
            # Generate labels from description
            label_dict = generate_labels_from_description(
                user_description, self.client, self.model)

            # Handle non-food content
            if label_dict is None:
                filtered_df = self.features_df
                filter_cat_df = self.features_df
            elif label_dict and label_dict['categories'] == 'Không liên quan ẩm thực':
                st.error(
                    "Yêu cầu của bạn không liên quan đến ẩm thực! Vui lòng thử lại với một mô tả khác.")
                return None
            else:
                # Extract duration if available
                duration = int(label_dict.pop("duration", None)) if label_dict.get(
                    "duration") is not None else None

                # Filter data based on labels
                filtered_df = filter_by_multiple_labels_unified(
                    self.features_df, label_dict, min_count=20)
                filter_cat_df = self.features_df[self.features_df['categories']
                                                 == label_dict['categories']]

            # Calculate statistics
            stats = self._calculate_statistics(filtered_df, filter_cat_df)

            # Use mean duration if not specified
            if duration is None:
                duration = stats['mean_duration']

            word_count = int(stats['mean_word_per_second'] * duration)
            max_output_tokens = int(word_count * 1.5)
            # max_output_tokens = 2000

            # Adjusted for better performance
            print(f"Duration: {duration}")
            print(f"Max Word Count: {word_count}")
            print(f"Max Output Token: {max_output_tokens}")

        # Generate and format script
        with st.spinner("Tạo kịch bản thô..."):
            plain_script = generate_plain_script(
                user_description, stats['transcript_sample_text'], word_count, self.client, self.model, max_output_tokens)

        with st.spinner("Định dạng lại kịch bản..."):
            formatted_script = format_script_with_gemini(
                plain_script,
                stats['desc_sample_text'],
                stats['mean_word_per_second'],
                stats['mean_hashtag_count'],
                stats['top_10_hashtags_text'],
                self.client,
                self.model
            )

            # Save to session state
            st.session_state.formatted_script = formatted_script
            st.session_state.updated_script_data = formatted_script.copy()

        return formatted_script

    def _calculate_statistics(self, filtered_df, filter_cat_df):
        """Calculate statistics from filtered dataframes"""
        stats = {
            'mean_word_count': int(filtered_df['transcript_word_count'].mean()),
            'mean_duration': int(filtered_df['video.duration'].mean()),
            'mean_word_per_second': filtered_df['word_per_second'].mean(),
            'mean_hashtag_count': int(filtered_df['hashtag_count'].mean()),
        }

        # Get top hashtags
        top_10_hashtags = filter_cat_df['hashtags'].explode(
        ).value_counts().head(10).index
        stats['top_10_hashtags_text'] = ', '.join(top_10_hashtags)

        # Get sample texts
        stats['transcript_sample_text'], stats['desc_sample_text'] = format_transcript_desc_examples(
            filtered_df, min_count=20)

        return stats

    def display_script_overview(self, script_data):
        """Display the script overview section"""
        st.markdown("### 📝 Tổng quan video")
        st.markdown(
            f"**🎬 Mô tả video:** {script_data.get('video_description', '')}")
        st.markdown(
            f"**⏱️ Độ dài dự kiến:** {script_data.get('duration', '')}")
        st.markdown(f"**📍 Bối cảnh:** {script_data.get('setting', '')}")
        st.markdown(f"**👤 Nhân vật:** {script_data.get('characters', '')}")
        st.markdown("---")

    def display_script_sections(self, script_data):
        """Display all script sections with edit functionality"""
        # Display overview
        self.display_script_overview(script_data)

        st.markdown("### 🎬 Kịch bản theo từng phần")

        # Process section deletions
        self._process_section_deletions()

        # Display each section
        for idx, section in enumerate(st.session_state.updated_script_data.get("main_content", [])):
            self._display_single_section(idx, section)

        return st.session_state.updated_script_data

    def _process_section_deletions(self):
        """Process any pending section deletions"""
        sections_to_delete = []
        for idx in range(len(st.session_state.updated_script_data.get("main_content", []))):
            if st.session_state.get(f"delete_section_{idx}", False):
                sections_to_delete.append(idx)
                st.session_state[f"delete_section_{idx}"] = False

        for idx in sorted(sections_to_delete, reverse=True):
            st.session_state.updated_script_data["main_content"].pop(idx)

    def _display_single_section(self, idx, section):
        """Display a single script section with edit functionality"""
        key_prefix = f"sec_{idx}"

        # Initialize edit mode state if not exists
        if f"{key_prefix}_edit" not in st.session_state:
            st.session_state[f"{key_prefix}_edit"] = False

        edit_mode = st.session_state[f"{key_prefix}_edit"]
        default_text = f"[{section['time_range']}] {section['title']}"

        # Title row with edit/save buttons
        self._display_section_header(
            key_prefix, section, default_text, edit_mode)

        # Content section (visual and dialogue)
        self._display_section_content(key_prefix, section, edit_mode)

    def _display_section_header(self, key_prefix, section, default_text, edit_mode):
        """Display the section header with edit/save buttons"""
        col_title, col_btns = st.columns([9, 1])

        with col_title:
            if edit_mode:
                time_title_input = st.text_input(
                    "⏱️ Thời gian & tiêu đề", default_text,
                    key=f"{key_prefix}_time_title",
                    label_visibility="collapsed"
                )
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
                if st.button("✏️", key=f"{key_prefix}_edit_btn", help="Sửa", use_container_width=True):
                    st.session_state[f"{key_prefix}_edit"] = True
                    st.rerun()
            else:
                if st.button("✅", key=f"{key_prefix}_save_btn", help="Lưu", use_container_width=True):
                    self._save_section_edits(key_prefix, section, default_text)
                    st.session_state[f"{key_prefix}_edit"] = False
                    st.rerun()

    def _save_section_edits(self, key_prefix, section, default_text):
        """Save edits made to a section"""
        time_title_raw = st.session_state.get(
            f"{key_prefix}_time_title", default_text)
        if "]" in time_title_raw:
            time_part, title_part = time_title_raw.split("]", 1)
            section["time_range"] = time_part.strip(" [")
            section["title"] = title_part.strip()

    def _display_section_content(self, key_prefix, section, edit_mode):
        """Display the content (visual and dialogue) of a section"""
        col1, col2 = st.columns([1, 2])

        if edit_mode:
            with col1:
                st.markdown("🎥 **Cảnh quay**")
                visual_input = st.text_area(
                    "🎥 Cảnh quay", section['visual_description'],
                    key=f"{key_prefix}_visual", height=100,
                    label_visibility="collapsed"
                )
            with col2:
                st.markdown("🗣️ **Lời thoại**")
                dialogue_input = st.text_area(
                    "🗣️ Lời thoại", section['dialogue'],
                    key=f"{key_prefix}_dialogue", height=100,
                    label_visibility="collapsed"
                )

            # Update section values
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

    def run(self):
        """Main application flow"""
        st.title("✍️ Tạo kịch bản TikTok")

        # Expandable section for description input
        with st.expander("📝 Nhập mô tả video", expanded=True):
            user_description = st.text_area(
                "Mô tả chi tiết về video TikTok bạn muốn tạo:",
                placeholder="Làm video TikTok hướng dẫn nấu mì tôm trứng siêu nhanh, siêu dễ cho sinh viên. Cần nhấn mạnh vào sự tiện lợi và hướng dẫn từng bước...",
                height=250  # Increased height for more space
            )

            # Add some example suggestions
            st.markdown("""
            **Một số chi tiết có thể gợi ý cho hệ thống:**
            - **Món ăn** và **mục tiêu video** (review, nấu, chia sẻ...)
            - **Cách triển khai** (kể chuyện, hướng dẫn, review...)
            - **Cách mở đầu, giọng điệu, tốc độ video**
            - Có **CTA** gì không (comment, chia sẻ, ghé quán...)
            - Ai là **người xem** chính (học sinh, dân văn phòng, nội trợ...)
            
            **Ví dụ**: Tôi muốn làm video quảng bá cho sản phẩm bánh tráng chấm phô mai của nhà tôi, cách nói chuyện gần gũi, có hướng dẫn cách ăn, giọng điệu từ tốn.
            """)

            generate_button = st.button(
                "✨ Tạo kịch bản", use_container_width=False)

        if generate_button and user_description:
            self.generate_script(user_description)
            st.header("🎬 Kịch bản gợi ý")

        # Display script if available
        if st.session_state.formatted_script:
            self.display_script_sections(st.session_state.formatted_script)


# Main execution
# if __name__ == "__main__":
app = ScriptGenerator()
app.run()
