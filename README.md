# Cách chạy app

- Đứng ở root folder:

```bash
pip install -r requirements.txt
streamlit run src/app/streamlit_app.py
```

# 21KHDL-TikTok-Analytics

- Lịch họp cố định:
  - 14h T3 hàng tuần
  - 14h T6 hàng tuần

# TODO: 14h T6, 18/04/2025

- Viết báo cáo cuối kỳ trên Overleaf
  - Link: https://www.overleaf.com/project/68078b37211771149621ef34

```
Danh sách thành viên và Bảng mức độ đóng góp

Chương 1: Giới thiệu chung
- Giới thiệu chung về đồ án
- Tóm tắt về công nghệ được sử dụng trong đồ án
  - TikTok-API (unofficial), Gemini API, Plotly, Streamlit, Streamlit Community Cloud, v.v.
  - AI để phân tích dữ liệu
  - st.Page để merge các page
  - st.cache để cache dữ liệu
  - File parquet để keep datatype
  - Dùng Gemini API để tạo báo cáo
  - v.v.


[Hãn]
Chương 2: Thu thập dữ liệu
- Nhấn mạnh rằng dùng TikTok-API (unofficial) để thu thập dữ liệu
- Có 2 tập dữ liệu chính: video-data + user-data


[Phát]
Chương 3: Tiền xử lý dữ liệu
- Trình bày giống trong file notebook
- Rút trích transcript
- Rút trích món ăn và địa điểm


[Hãn]
Chương 4: Webapp tạo kịch bản (dashboard + tools)
- Rút trích ... của Hãn
- Trình bày webapp


[Lực]
Chương 5: Dashboard phân tích user
- Filter + Loại biểu đồ + Nhận xét + v.v.


[C.Mỹ]
Chương 6: Dashboard phân tích video
- Câu hỏi: Vào thời điểm nào trong tuần/tháng/năm thì video được đăng tải nhiều? Có lượt tương tác nhiều không?
- Filter + Loại biểu đồ + Nhận xét + v.v.


[Tín]
Chương 7: Dashboard phân tích xu hướng
- Filter + Loại biểu đồ + Nhận xét + v.v.


[Phát]
Chương 8: Một vài công cụ bổ sung
- Một vài webapp hỗ trợ nghiên cứu


[Phát]
Chương 9: Hướng phát triển trong tương lai
- Dùng airflow để tự động hóa pipeline (ưu điểm: vì chỉ dùng API nên đảm bảo thời gian xử lý nhanh hơn)
- Tập trung vào các chart để trả lời các câu hỏi người dùng muốn nghe

```

## Tiền xử lý dữ liệu

- Viết mô tả cho các bước tiền xử lý dữ liệu
- Có thể chèn code nếu cần
- Trình bày kết quả sau bước tiền xử lý dữ liệu

## Trực quan hóa và phân tích dữ liệu

- Có thể viết mô tả ngắn gọn cho các bước code để trực quan hóa dữ liệu
- Giới thiệu các tính năng mà người dùng có thể thực hiện trên dashboard
- Chụp hình chart, dashboard và chèn vào báo cáo
- Viết nhận xét cho các chart, dashboard
