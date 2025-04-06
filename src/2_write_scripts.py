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

# Tải dữ liệu với vòng quay chờ
with st.spinner("Đang tải dữ liệu TikTok..."):
    # Tải dữ liệu
    features_df = load_data()

# # Define the legacy prompt to be sent (default prompt)
# legacy_prompt = f"""
# Topic: %s

# Instructions: You are a powerful AI designed to create engaging and high-quality video scripts that can attract millions of views. I need a complete script for a video on the topic provided above. The script should include a catchy hook, an engaging introduction, informative and entertaining content, and a compelling call to action. Follow these detailed steps to create the script:

# ### Hook:

# - Start with an attention-grabbing hook that introduces the topic in an exciting way.
# - Use a surprising fact, a question, or a bold statement to draw viewers in.
# - Keep the hook under 30 seconds to ensure it's concise and impactful.

# ### Introduction:

# - Briefly introduce yourself and establish credibility.
# - Provide a quick overview of what the video will cover.
# - Highlight the value the viewer will get from watching the entire video.

# ### Main Content:

# - Break down the topic into clear, easy-to-follow sections.
# - Use a mix of informative content, personal anecdotes, and engaging storytelling.
# - Include at least three main points or subtopics to keep the content organized.
# - Use examples, statistics, and visuals (if applicable) to enhance the explanation.
# - Keep the tone conversational and relatable to maintain viewer interest.

# ### Engagement:

# - Ask rhetorical questions to keep viewers thinking and engaged.
# - Encourage viewers to leave comments, like the video, and subscribe to the channel.
# - Use phrases like “Let me know in the comments” or “What do you think about this?”

# ### Call to Action:

# - End with a strong call to action that tells viewers what to do next.
# - Suggest watching another related video, downloading a resource, or following on social media.
# - Thank the viewers for watching and remind them to subscribe for more content.

# Please give the answer in Vietnamese.

# Give the answer in format (add newline character after each section):

# ### Hook
# - [a paragraph]
# ### Introduction
# - [a paragraph]
# ### Main Content
# - [List of main content]
# ### Engagement
# - [List of engagement]
# ### Call to Action
# - [a paragraph]
# """.strip()


# # Available AI Models
# available_models = [
#     # Input token limit: 1,048,576
#     # Output token limit: 8,192
#     "gemini-2.0-flash",

#     # Input token limit 2,048,576
#     # Output token limit 8,192
#     "gemini-2.0-pro-exp",

#     "gemini-2.0-flash-thinking-exp",

#     # Input token limit 1,048,576
#     # Output token limit 8,192
#     "gemini-2.0-flash-lite",

#     # Input token limit 1,048,576
#     # Output token limit 8,192
#     "gemini-1.5-flash",

#     # Input token limit 1,048,576
#     # Output token limit 8,192
#     "gemini-1.5-flash-8b",

#     # Input token limit 2,097,152
#     # Output token limit 8,192
#     "gemini-1.5-pro",

#     "learnlm-1.5-pro-experimental",

#     "gemma-3-27b-it",
# ]


# def get_model():
#     # Function to get the selected model
#     return st.sidebar.selectbox(
#         "Select AI Model:",
#         available_models,
#         index=available_models.index("gemini-2.0-flash")
#     )


# # Get selected model
# model = get_model()
# print(f"Selected Model: {model}")

# # Title and description
# st.title('📝🔗 Write Scripts')
# st.markdown("Generate engaging video scripts with AI assistance")


# # Set start session time
# if 'start_time' not in st.session_state:
#     st.session_state.start_time = time.time()
# # Prompt customization section
# if 'prompt' not in st.session_state:
#     st.session_state.write_script_prompt = legacy_prompt


# with st.expander("View/Edit Research Prompt", expanded=False):
#     st.markdown("**You can customize the research prompt below:**")
#     st.markdown(
#         "_This is the instruction sent to the AI model. You can modify it to better suit your needs._")

#     # Text area for editing the prompt
#     custom_prompt = st.text_area(
#         "Customize Prompt Template:",
#         # Use the same key as the session state variable
#         key=f"2_write_scripts_custom_prompt_{st.session_state.start_time}",
#         value=st.session_state.write_script_prompt,
#         height=300
#     )

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("Update Prompt"):
#             st.session_state.write_script_prompt = custom_prompt
#             st.success("Prompt updated successfully!")

#     with col2:
#         if st.button("Reset to Default"):
#             st.success("Prompt reset to default!")
#             st.session_state.write_script_prompt = legacy_prompt
#             st.session_state.start_time = time.time()
#             st.rerun()

# prompt = st.session_state.write_script_prompt
# print("Prompt:", prompt)


# # Main content
# topic = st.text_area('Enter your video topic:', height=100,
#                      placeholder="For example: 'Street food for students'")
# print(f"Topic: {topic}")

# # Generate content when button is pressed
# if st.button('Generate Script') and topic:
#     try:
#         # Research on the topic
#         with st.spinner('Researching content...'):
#             print(prompt % topic)

#             client = genai.Client(
#                 api_key="AIzaSyBYqr4g63GOBTslf5xP0-AbIcSSlAuvMnM")
#             response = client.models.generate_content(
#                 model=model,
#                 contents=(prompt % topic).strip(),
#             )

#         # Display results
#         st.subheader("Generated Content:")
#         st.write(response.text)

#         # # Expandable sections for additional info
#         # with st.expander('Title History'):
#         #     st.info(title_memory.buffer)

#         # with st.expander('Script History'):
#         #     st.info(script_memory.buffer)

#         # with st.expander('Wikipedia Research'):
#         #     st.info(wiki_research)

#         # # Download options
#         # st.download_button(
#         #     label="Download Script",
#         #     data=f"TITLE: {title}\n\n{script}",
#         #     file_name="youtube_script.txt",
#         #     mime="text/plain"
#         # )

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# elif topic == "":
#     st.info("Please enter a topic to research.")
#     st.info("For example: Enter 'Street food for students' and click on the 'Generate Script' button.")


# --- PAGE: Tạo kịch bản từ mô tả người dùng ---


# def display_script_sections(script_data):
#     # --- THÔNG TIN CHUNG ---
#     st.markdown("### 📝 Tổng quan video")
#     st.markdown(
#         f"**🎬 Mô tả video:** {script_data.get('video_description', '')}")
#     st.markdown(f"**⏱️ Độ dài dự kiến:** {script_data.get('duration', '')}")
#     st.markdown(f"**📍 Bối cảnh:** {script_data.get('setting', '')}")
#     st.markdown(f"**👤 Nhân vật:** {script_data.get('characters', '')}")
#     st.markdown("---")

#     # --- DANH SÁCH CÁC ĐOẠN ---
#     st.markdown("### 🎬 Kịch bản theo từng phần")

#     for section in script_data.get("main_content", []):
#         time_title = f"#### **[{section['time_range']}] {section['title']}**"
#         # st.markdown(time_title)
#         st.markdown(
#             f"""
#             <div style="background-color: #f0f0f0; padding: 8px 16px; border-radius: 6px; margin-top: 10px; margin-bottom: 10px;">
#                 <strong>[{section['time_range']}] {section['title']}</strong>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         col1, col2 = st.columns([1, 2])
#         with col1:
#             st.markdown("🎥 **Cảnh quay**")
#             st.markdown(f"{section['visual_description']}")

#         with col2:
#             st.markdown("🗣️ **Lời thoại**")
#             st.markdown(f"\"{section['dialogue']}\"")

#         # st.markdown("---")

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
            # col_add, col_edit, col_delete = st.columns(3)
            # col_edit, col_delete = st.columns(2)
            # col_edit = st.columns(1)
            # with col_edit:
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
            # with col_delete:
            #     if st.button("🗑️ Xoá", key=f"{key_prefix}_delete_btn", help="Xoá", use_container_width=True):
            #         st.session_state[f"delete_section_{idx}"] = True
            #         st.rerun()

            # with col_add:
            #     if st.button("➕ Thêm", key=f"add_section_btn_{idx}", use_container_width=True):
            #         new_section = {
            #             "time_range": "0:00-0:15",
            #             "title": "Phần mới",
            #             "visual_description": "Mô tả cảnh quay mới",
            #             "dialogue": "Nội dung lời thoại mới"
            #         }
            #         st.session_state.updated_script_data["main_content"].insert(
            #             idx + 1, new_section)
            #         st.session_state[f"sec_{idx+1}_edit"] = True
            #         st.rerun()

        # Phần nội dung: xem hoặc chỉnh sửa
        col1, col2 = st.columns([1, 2])
        if edit_mode:
            with col1:
                st.markdown("🎥 **Cảnh quay**")
                st.text_area(
                    "🎥 Cảnh quay", section['visual_description'], key=f"{key_prefix}_visual", height=100, label_visibility="collapsed")
            with col2:
                st.markdown("🗣️ **Lời thoại**")
                st.text_area(
                    "🗣️ Lời thoại", section['dialogue'], key=f"{key_prefix}_dialogue", height=100, label_visibility="collapsed")
            # Sau khi chỉnh sửa, cập nhật nội dung mới vào section
            section["visual_description"] = st.session_state.get(
                f"{key_prefix}_visual", section["visual_description"])
            section["dialogue"] = st.session_state.get(
                f"{key_prefix}_dialogue", section["dialogue"])
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
        # st.markdown("---")

    #     # Giữa các phần, cho phép thêm phần mới
    #     col_add = st.columns(1)[0]
    #     if st.button("➕ Thêm phần mới", key=f"add_section_btn_{idx}", use_container_width=True):
    #         new_section = {
    #             "time_range": "0:00-0:15",
    #             "title": "Phần mới",
    #             "visual_description": "Mô tả cảnh quay mới",
    #             "dialogue": "Nội dung lời thoại mới"
    #         }
    #         st.session_state.updated_script_data["main_content"].insert(
    #             idx + 1, new_section)
    #         st.session_state[f"sec_{idx+1}_edit"] = True
    #         st.rerun()

    # # Nếu không có phần nào, hiển thị nút thêm đầu tiên
    # if len(st.session_state.updated_script_data.get("main_content", [])) == 0:
    #     if st.button("➕ Thêm phần đầu tiên", key="add_section_btn_first", use_container_width=True):
    #         new_section = {
    #             "time_range": "0:00-0:15",
    #             "title": "Phần mới",
    #             "visual_description": "Mô tả cảnh quay mới",
    #             "dialogue": "Nội dung lời thoại mới"
    #         }
    #         st.session_state.updated_script_data["main_content"].append(
    #             new_section)
    #         st.rerun()

    return st.session_state.updated_script_data


st.title("✍️ Tạo kịch bản TikTok từ mô tả")

user_description = st.text_area("Nhập mô tả video bạn muốn tạo:",
                                placeholder="Nhập mô tả video bạn muốn tạo:", height=150)

# if st.button("Tạo kịch bản") and user_description:
#     key = "AIzaSyBaT3UMomQUPjjpbRD2pCrE_sk3nT6P47w"  # vphacc096@gmail.com
#     client = genai.Client(api_key=key)

#     with st.spinner("Phân tích mô tả bằng Gemini..."):
#         label_dict = generate_labels_from_description(
#             user_description, client)

#     with st.spinner("Lọc video tương đồng..."):
#         if label_dict:
#             filtered_df = filter_by_multiple_labels_unified(
#                 features_df, label_dict, min_count=10)
#             filter_cat_df = features_df[features_df['categories']
#                                         == label_dict['categories']]
#         else:
#             filtered_df = features_df
#             filter_cat_df = features_df

#         mean_word_count = int(filtered_df['transcript_word_count'].mean())
#         mean_duration = int(filtered_df['video.duration'].mean())
#         mean_word_per_second = filtered_df['word_per_second'].mean()
#         mean_hashtag_count = int(filtered_df['hashtag_count'].mean())

#         top_10_hashtags = filter_cat_df['hashtags'].explode(
#         ).value_counts().head(10).index
#         top_10_hashtags_text = ', '.join(top_10_hashtags)

#         transcript_sample_text, desc_sample_text = format_transcript_desc_examples(
#             filtered_df)

#     with st.spinner("Tạo kịch bản thô..."):
#         plain_script = generate_plain_script(
#             user_description, transcript_sample_text, mean_word_count, client)

#     with st.spinner("Định dạng lại kịch bản..."):
#         formatted_script = format_script_with_gemini(
#             plain_script, desc_sample_text, mean_word_per_second, mean_hashtag_count, top_10_hashtags_text, client)

#     st.subheader("🎬 Kịch bản gợi ý")
#     # st.code(formatted_script, language="markdown")
#     # st.write(formatted_script)
#     if formatted_script:
#         display_script_sections(formatted_script)


formatted_script = {'characters': 'Người làm nội trợ yêu thích nấu ăn và chia sẻ công thức.',
                    'duration': '2 phút 18 giây',
                    'main_content': [{'time_range': '0:00-0:15',
                                      'title': 'Mở đầu',
                                      'visual_description': 'Cận cảnh đĩa mì Ý sốt kem nấm truffle hấp dẫn.',
                                      'dialogue': 'Trời ơi tin được không, mì Ý sốt kem nấm truffle làm tại nhà mà ngon như nhà hàng 5 sao luôn á! Tui thề là tui làm xong tui còn bất ngờ á, sao mà nó dễ mà nó ngon dữ vậy trời.'},
                                     {'time_range': '0:15-0:25',
                                      'title': 'Giới thiệu công thức',
                                      'visual_description': 'Người nói giới thiệu và hướng dẫn cách làm.',
                                      'dialogue': 'Hôm nay tui chỉ cho mấy bà cách làm mì Ý sốt kem nấm truffle siêu dễ, ai cũng làm được, mà đảm bảo ngon nhức nách luôn. Mấy bà nào mà ghiền mì Ý sốt kem mà lại mê cái mùi truffle sang chảnh á thì nhất định phải coi hết video này nha.'},
                                     {'time_range': '0:25-0:40',
                                      'title': 'Liệt kê nguyên liệu',
                                      'visual_description': 'Hiển thị các nguyên liệu cần thiết.',
                                      'dialogue': 'Nguyên liệu thì siêu đơn giản luôn nè: mì Ý, nấm các loại, tui ở đây dùng nấm mỡ với nấm đùi gà cho nó dễ kiếm, kem tươi, phô mai parmesan bào sợi sợi á, tỏi, hành tây, rồi thêm một xíu truffle oil hoặc là truffle paste cho nó thơm nức mũi. Nếu có truffle tươi bào lên trên thì càng ngon nữa, nhưng mà không có thì truffle oil cũng okila rồi.'},
                                     {'time_range': '0:40-0:50',
                                      'title': 'Luộc mì',
                                      'visual_description': 'Quá trình luộc mì.',
                                      'dialogue': 'Cách làm thì còn dễ hơn nữa nè. Đầu tiên là luộc mì trước nha, nhớ cho chút muối với dầu ăn vô cho mì nó khỏi dính. Luộc vừa tới thôi nha mấy bà, đừng có luộc mềm quá ăn nó dở ẹc à.'},
                                     {'time_range': '0:50-1:10',
                                      'title': 'Làm sốt kem nấm truffle',
                                      'visual_description': 'Các bước làm sốt kem nấm truffle.',
                                      'dialogue': 'Trong lúc chờ luộc mì á thì mình đi làm sốt kem nấm truffle nè. Bắt cái chảo lên, cho xíu bơ lạt vô cho nó thơm, rồi phi thơm tỏi băm với hành tây băm. Phi cho nó vàng vàng thơm thơm lên là được rồi. Xong rồi cho nấm vô xào, xào cho nấm nó ra hết nước với lại nó hơi săn lại á.'},
                                     {'time_range': '1:10-1:35',
                                      'title': 'Hoàn thiện sốt',
                                      'visual_description': 'Đổ kem tươi và nêm nếm gia vị.',
                                      'dialogue': 'Tiếp theo là đổ kem tươi vô, cái này tui dùng whipping cream cho nó béo ngậy. Nêm nếm gia vị cho vừa ăn nha, muối, tiêu, chút xíu hạt nêm nếu thích. Rồi cái quan trọng nhất nè, cho truffle oil hoặc truffle paste vô, cái này là bí quyết tạo nên cái mùi vị sang chảnh của món này đó. Mấy bà cứ nêm nếm từ từ thôi nha, cho vừa đủ thơm là được, đừng có cho nhiều quá nó bị nồng á.'},
                                     {'time_range': '1:35-1:45',
                                      'title': 'Trộn mì với sốt',
                                      'visual_description': 'Trộn mì đã luộc vào sốt kem nấm.',
                                      'dialogue': 'Để lửa nhỏ riu riu cho sốt nó hơi sánh lại là ok rồi đó. Lúc này mì cũng vừa chín tới rồi, vớt mì ra cho vô chảo sốt kem nấm luôn. Trộn đều lên cho mì nó áo đều sốt kem nấm là xong.'},
                                     {'time_range': '1:45-1:55',
                                      'title': 'Trình bày',
                                      'visual_description': 'Gắp mì ra đĩa và rắc phô mai parmesan.',
                                      'dialogue': 'Cuối cùng là gắp mì ra dĩa, rắc thêm phô mai parmesan bào sợi lên trên cho nó đẹp mắt với lại nó béo nữa. Ai mà thích ăn cay thì rắc thêm chút xíu tiêu xay hoặc là ớt bột lên trên nha.'},
                                     {'time_range': '1:55-2:10',
                                      'title': 'Cảm nhận',
                                      'visual_description': 'Ăn thử và thể hiện cảm xúc.',
                                      'dialogue': 'Trời ơi ngon gì đâu luôn á! Cái sợi mì nó dai dai, sốt kem nấm thì béo ngậy thơm lừng mùi truffle, ăn một miếng là muốn ăn thêm miếng nữa luôn á. Mấy bà phải thử làm ngay nha. Đảm bảo là ai ăn cũng ghiền cho coi.'},
                                     {'time_range': '2:10-2:18',
                                      'title': 'Kêu gọi hành động',
                                      'visual_description': 'Hướng dẫn xem công thức và follow.',
                                      'dialogue': 'Công thức tui để hết trên màn hình rồi đó, mấy bà cứ làm theo là y chang luôn. Lưu video này lại, share cho bạn bè cùng làm. Follow tui để xem thêm nhiều món ngon dễ làm nữa nha!'}],
                    'setting': 'Bếp tại nhà.',
                    'video_description': 'Mì Ý sốt kem nấm truffle ngon chuẩn nhà hàng 5 sao ngay tại nhà! Xem ngay công thức siêu dễ này và trổ tài thôi nào! #Ancungtiktok #learnontiktok #anngonnaugon #miy'}

if formatted_script:
    display_script_sections(formatted_script)
