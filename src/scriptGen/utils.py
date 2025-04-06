import pandas as pd
import json
import numpy as np
from types import NoneType
import re
from IPython.display import display, Markdown
from itertools import product  # Nếu dùng, nhưng ở đây không cần dùng product

# !pip install mlxtend
# from mlxtend.preprocessing import TransactionEncoder
# from mlxtend.frequent_patterns import apriori, association_rules
import ast
import json
from collections import defaultdict
from itertools import combinations, chain, product

from google import genai
from google.genai import types


def filter_by_multiple_labels_unified(df, conditions, soft_fields=None, min_count=10):
    """
    Lọc dataframe dựa trên điều kiện ban đầu (conditions) với quy trình "nới lỏng":
      - Bắt đầu với full điều kiện.
      - Duyệt theo thứ tự ưu tiên: các trường soft theo thứ tự ưu tiên, sau đó strict fields.
      - Với mỗi trường (trừ 'categories'), thử giảm dần số label (bỏ từ cuối về) cho đến khi đủ số video (>= min_count).
      - Nếu không đủ, loại bỏ luôn trường đó (trừ trường 'categories').
    """
    print(conditions)
    if conditions is None:
        return df

    if soft_fields is None:
        soft_fields = ["pacing", "audience_target",
                       "content_style", "tone_of_voice", "cta_type"]

    # Chuẩn hóa conditions: đảm bảo mỗi giá trị là list
    fixed_conditions = {}
    for f, val in conditions.items():
        fixed_conditions[f] = val if isinstance(val, list) else [val]

    # Xác định strict fields là những trường không nằm trong soft_fields
    strict_fields = [f for f in fixed_conditions.keys()
                     if f not in soft_fields]
    # Combined order: các trường soft theo thứ tự ưu tiên, sau đó strict fields (nhưng luôn giữ 'categories')
    combined_order = [
        f for f in soft_fields if f in fixed_conditions] + strict_fields

    def apply_filters(dataframe, conds):
        for field, target_labels in conds.items():
            dataframe = dataframe[dataframe[field].apply(
                lambda labels: all(lbl in labels for lbl in target_labels))]
        return dataframe

    # Bắt đầu với điều kiện đầy đủ
    test_conditions = fixed_conditions.copy()
    best_df = apply_filters(df.copy(), test_conditions)
    if len(best_df) >= min_count:
        print("Final condition (full):", test_conditions)
        return best_df

    # Duyệt qua các trường theo thứ tự ưu tiên
    for field in combined_order:
        # Không nới lỏng trường 'categories'
        if field == "categories":
            continue
        if field not in test_conditions:
            continue
        original_labels = test_conditions[field]
        # Thử giảm dần số label (bỏ từ cuối về) cho trường đó
        for i in range(1, len(original_labels) + 1):
            candidate = original_labels[:-i]
            test_conditions[field] = candidate
            df_filtered = apply_filters(df.copy(), test_conditions)
            print(
                f"Trying {field} with candidate {candidate}: {len(df_filtered)} results")
            if len(df_filtered) >= min_count:
                print("Final condition:", test_conditions)
                return df_filtered
            best_df = df_filtered
        # Nếu đã thử hết các candidate của field mà vẫn chưa đủ, loại bỏ luôn field đó (trừ 'categories')
        if field in test_conditions and field != "categories":
            del test_conditions[field]
        df_filtered = apply_filters(df.copy(), test_conditions)
        print(f"Removed field {field}: {len(df_filtered)} results")
        if len(df_filtered) >= min_count:
            print("Final condition:", test_conditions)
            return df_filtered
        best_df = df_filtered

    return best_df  # Trả về kết quả tốt nhất tìm được, dù có thể ít hơn min_count


def generate_labels_from_description(user_description, client, model):

    with open('src/scriptGen/label_schema.json', 'r', encoding='utf-8') as f:
        label_schema = json.load(f)

    annotate_user_desc_function = {
        "name": "filter_by_multiple_labels",
        # "description": "Dựa trên miêu tả của người dùng về video họ muốn thực hiện, tiến hành gán nhãn cho các trường được định trước.",
        "description": "Dựa trên miêu tả của người dùng về video họ muốn thực hiện, tiến hành lọc ra các video phù hợp với mô tả của người dùng.",
        "parameters": label_schema
    }

    system_instruction = """
    Bạn là một hệ thống gán nhãn nội dung video TikTok ẩm thực dựa trên mô tả tự do của người dùng. Nhiệm vụ của bạn là trích xuất các nhãn (label) tương ứng với schema đã định nghĩa.

    Xác định xem nội dung có thuộc chủ đề ẩm thực hay không. Chọn một trong các chủ đề ẩm thực như sau:
    - Review quán ăn: Tập trung vào đánh giá, giới thiệu quán ăn, nhà hàng, xe đẩy, tiệm nhỏ,... nơi có thể đến ăn trực tiếp.
    - Review sản phẩm ăn uống: Đánh giá các loại thực phẩm đóng gói, bánh kẹo, gia vị, đồ dùng nhà bếp, v.v.
    - Review món ăn: Tập trung vào đánh giá hương vị, chất lượng của một món ăn hoặc đồ uống cụ thể (có thể là tự làm hoặc mua nhưng không phải sản phẩm đóng gói). Ít hoặc hoàn toàn không đề cập đến quán ăn.
    - Mukbang: Video tập trung vào việc ăn số lượng lớn, ăn to, ăn gần mic hoặc ăn nhiều món cùng lúc, thường ít lời thoại.
    - Nấu ăn: Video hướng dẫn hoặc ghi lại quá trình nấu ăn, có thể ở nhà, ngoài trời hoặc trong bếp chuyên nghiệp.
    - Không liên quan ẩm thực: Video không thuộc bất kỳ chủ đề nào liên quan đến ăn uống, món ăn, quán ăn hoặc trải nghiệm ẩm thực.

    Yêu cầu nghiêm ngặt:

    1. Chỉ sử dụng đúng các trường và nhãn (label) được liệt kê trong schema. Không được tạo nhãn mới.
    2. Chỉ gán nhãn cho những trường được đề cập rõ ràng hoặc có thể suy luận trực tiếp, hợp lý từ mô tả của người dùng.
    3. Tuyệt đối không được suy diễn chủ quan hoặc gán nhãn theo cảm tính. Nếu người dùng không đề cập hoặc không gợi ý rõ ràng, thì không trả về trường đó. (Ví dụ không suy luận ra cách tone_of_voice dựa trên tông giọng của người dùng mà chỉ trích ra khi người dùng có đề cập cụ thể)
    4. Nếu chỉ có một vài trường được đề cập, chỉ trả về các trường đó.
    5. Sử dụng tool được định nghĩa để cho ra kết quả
    """

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


def format_transcript_desc_examples(user_desc_filter_df):
    today = pd.Timestamp.now(tz='Asia/Ho_Chi_Minh')

    # Tính số ngày kể từ khi tạo video
    user_desc_filter_df['days_since'] = (
        today - user_desc_filter_df['createTime']).dt.days
    alpha = 0.7
    user_desc_filter_df['score'] = user_desc_filter_df['statsV2.playCount'] / \
        ((user_desc_filter_df['days_since'] + 1) ** alpha)
    sorted_df = user_desc_filter_df.sort_values(by='score', ascending=False)
    example_df = sorted_df.head(30)

    def create_examples(df, col):
        return "\n\n".join(
            [f"{i}. {t}" for i, t in enumerate(df[col], 1)]
        )

    transcript_sample_text = create_examples(example_df, 'transcript')
    desc_sample_text = create_examples(example_df, 'desc')
    return transcript_sample_text, desc_sample_text


def generate_plain_script(
        user_input, transcript_sample_text, mean_word_count, client, model):
    prompt_plain_script = f"""
    Bạn là chuyên gia viết kịch bản video TikTok trong lĩnh vực ẩm thực.

    Hãy viết một kịch bản video TikTok dạng **lời thoại tự nhiên** dựa trên **các transcript mẫu bên dưới** và **mô tả món ăn từ người dùng**.

    **Yêu cầu:**
    - Kịch bản có độ dài khoảng **{mean_word_count} từ**, không được chênh lệch quá 100 từ.
    - Viết theo dạng **lời thoại tự nhiên**, như thể đang nói trong video TikTok.
    - **Không chia phần**, **không thêm tiêu đề**, **không mở ngoặc giải thích** hoặc mô tả bối cảnh.
    - **Không chèn chú thích** như (cảnh quay), (hình ảnh), (âm thanh).
    - Sử dụng **giọng điệu, cách nói, tốc độ, hook và CTA** tương tự các transcript mẫu.
    - Ưu tiên sử dụng cụm từ đời thường, dễ viral như \"Trời ơi ngon gì đâu luôn á\", \"ăn là ghiền\", v.v.

    ---

    **Mô tả từ người dùng:**
    {user_input}

    **Các transcript mẫu để tham khảo phong cách viết:**
    {transcript_sample_text}
    """
    response_plain_script = client.models.generate_content(
        # model="gemini-2.0-flash-thinking-exp-1219",
        # model="gemini-2.0-flash",
        model=model,
        contents=[prompt_plain_script],
        # config=config,
    )
    return response_plain_script.text


def format_script_with_gemini(plain_script, desc_sample_text, mean_word_per_second, mean_hashtag_count, top_10_cat_hashtags_text, client, model):
    script_seconds = len(plain_script.split()) / int(mean_word_per_second)
    print("output script words:",  len(plain_script.split()))
    print("output script seconds:",  script_seconds)
    response_structured_script_schema = {
        "type": "object",
        "properties": {
            "video_description": {
                "type": "string",
                "description": f"Mô tả video kèm theo {mean_hashtag_count} hashtag, viết dựa trên nội dung kịch bản, các đoạn mô tả mẫu và top 10 hashtag được dùng nhiều nhất."
            },
            "duration": {
                "type": "string",
                "description": "Độ dài dự kiến của video, định dạng là '<x> phút <y> giây'."
            },
            "setting": {
                "type": "string",
                "description": "Bối cảnh hoặc địa điểm ghi hình, mô tả ngắn gọn."
            },
            "characters": {
                "type": "string",
                "description": "Nhân vật xuất hiện trong video, mô tả ngắn gọn."
            },
            "main_content": {
                "type": "array",
                "description": "Danh sách các bước/nội dung chính của video đã được chia nhỏ.",
                "items": {
                    "type": "object",
                    "required": ["time_range", "title", "visual_description", "dialogue"],
                    "properties": {
                        "time_range": {
                            "type": "string",
                            "description": "Khoảng thời gian của đoạn, ví dụ: '0:00-0:15'"
                        },
                        "title": {
                            "type": "string",
                            "description": "Tên bước/phần, ví dụ: 'Giới thiệu món ăn'"
                        },
                        "visual_description": {
                            "type": "string",
                            "description": "Mô tả ngắn gọn về hình ảnh cần quay."
                        },
                        "dialogue": {
                            "type": "string",
                            "description": "Lời thoại gốc từ kịch bản plain, được giữ nguyên."
                        }
                    }
                }
            }
        },
        "required": ["video_description", "duration", "setting", "characters", "main_content"]
    }

    prompt_structured_script = f"""
    Bạn là chuyên gia viết kịch bản TikTok ẩm thực.

    Hãy chuyển kịch bản dạng plain dưới đây thành format theo schema JSON sau, giữ nguyên lời thoại gốc, chia nhỏ theo từng bước nội dung như mở đầu, mô tả món, cảm nhận, CTA,...

    Thông tin thêm:
    - duration: {int(script_seconds // 60)} phút {int(script_seconds % 60)} giây

    Top 10 hashtag được sử dụng nhiều nhất: {top_10_cat_hashtags_text}

    Các đoạn mô tả video mẫu:

    {desc_sample_text}

    Kịch bản plain:

    {plain_script}
    """
    # - Lồng ghép cảm xúc mạnh (sốc, tiếc, mê mẩn, chill...) để tăng tính cuốn hút
    # - Giữ nhịp điệu tự nhiên, mang phong cách văn nói, không viết theo kiểu văn viết

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
    return response_dict
