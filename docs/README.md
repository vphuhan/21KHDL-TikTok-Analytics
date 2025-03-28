# Khoa học dữ liệu ứng dụng - 21KHDL

# Báo cáo tiến độ đồ án cuối kỳ

## Sinh viên thực hiện: Nhóm 05

| STT |   MSSV   | Họ và tên        |
| :-: | :------: | ---------------- |
|  1  | 21127038 | Võ Phú Hãn       |
|  2  | 21127739 | Vũ Minh Phát     |
|  3  | 21127742 | Nguyễn Minh Hiếu |

## Danh sách các tài liệu liên quan đến đồ án cuối kỳ

- File "[TikTokApi_package](TikTokApi_package.url)": Chứa link đến website hướng dẫn sử dụng các module trong package `TikTokApi` để thu thập dữ liệu từ các video trên TikTok.

- File "[Video_to_audio](Video_to_audio.url)": Chứa link đến website hướng dẫn kết hợp 2 package `yt-dlp` và `FFmpeg` để trích xuất âm thanh từ video. Thay vì phải tải file video (thường có dung lượng lớn) về máy, chúng ta có thể trích xuất âm thanh từ video và lưu trữ dưới dạng file audio (thường có dung lượng nhỏ hơn) để tiết kiệm dung lượng lưu trữ. Điều này cũng giúp giảm thời gian xử lý dữ liệu.

- File "[Gemini_API_docs](Gemini_API_docs.url)": Chứa link đến website hướng dẫn sử dụng API của Gemini để thực hiện nhiều tác vụ khác nhau. Trong phạm vi đồ án lần này, nhóm đã sử dụng API của Gemini để:

  - Trích xuất transcript từ video.
  - Sử dụng transcript để trích xuất ra các đặc trưng giúp phân loại video.
  - Phân loại video dựa trên các đặc trưng đã trích xuất.
  - Tạo kịch bản cho video TikTok dựa trên chủ đề mà người dùng mong muốn.
  - v.v.

- File "[Streamlit_dashboard](Streamlit_dashboard.url)": Chứa link đến bài viết hướng dẫn cách tạo ra các dashboard cho phép người dùng _tương tác trực tiếp_ (dùng thư viện `Altair`, `Plotly`, v.v.) thông qua giao diện web (dùng thư viện `Streamlit`).

- File "[Deploy_Streamlit_app](Deploy_Streamlit_app.url)": Chứa link đến tài liệu hướng dẫn cách deploy 1 webapp sử dụng `Streamlit` lên nền tảng **Streamlit Community Cloud** (miễn phí). Thông qua đó, người dùng có thể truy cập đến webapp thông qua đường link mà không cần cài đặt thêm bất kỳ phần mềm nào khác.

- File "[Scriptwriting_prompts](Scriptwriting_prompts.url)": Chứa link đến website cung cấp các gợi ý về cách viết kịch bản cho video. Ta sẽ dựa vào khung kịch bản này để tạo ra các câu prompt phù hợp và gửi đến các AI agent (ví dụ như các model được cung cấp bởi `Gemini API`) để tạo ra kịch bản phù hợp với chủ đề mà người dùng mong muốn.
