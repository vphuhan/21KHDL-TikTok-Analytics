# Đồ án cuối kỳ - Khoa học dữ liệu ứng dụng - 21KHDL

## Sinh viên thực hiện: Nhóm 05

| STT | MSSV     | Họ và tên        |
| :-: | -------- | ---------------- |
|  1  | 21127038 | Võ Phú Hãn       |
|  2  | 21127739 | Vũ Minh Phát     |
|  3  | 21127742 | Nguyễn Minh Hiếu |

## Link đến playlist chứa video demo của đồ án

- Link đến playlist chứa video demo của đồ án: https://www.youtube.com/playlist?list=PLY_ov3yMCYsdSNYektjNKpKpVDOnbqabk
- Trong playlist sẽ có video trình bày đầy đủ cả 3 công cụ hỗ trợ mà nhóm đã xây dựng, xoay quanh chủ đề trọng tâm của đồ án lần này là: "Xây dựng công cụ hỗ trợ viết kịch bản dành cho các video trên TikTok".

## Link đến trang web chứa sản phẩm của đồ án

- Link đến trang web chứa sản phẩm của đồ án: https://21khdl-tiktok-analytics.streamlit.app/

<!-- ## Cách tổ chức thư mục chứa mã nguồn ("./src")

- Thư mục "**`src`**" chứa tất cả mã nguồn của đồ án:
  - Thư mục con "All-in-one": chứa mã nguồn được sử dụng trong quá trình phát triển tất cả 6 mô hình (tuần tự và song song).
  - Thư mục con "Host-V1": chứa mã nguồn được sử dụng trong quá trình phát triển mô hình tuần tự lần 1.
  - Thư mục con "Host-V2": chứa mã nguồn được sử dụng trong quá trình phát triển mô hình tuần tự lần 2.
  - Thư mục con "Parallel-V1": chứa mã nguồn được sử dụng trong quá trình phát triển mô hình song song lần 1.
  - Thư mục con "Parallel-V2": chứa mã nguồn được sử dụng trong quá trình phát triển mô hình song song lần 2.
  - Thư mục con "Parallel-V3": chứa mã nguồn được sử dụng trong quá trình phát triển mô hình song song lần 3.
  - Thư mục con "Parallel-V4": chứa mã nguồn được sử dụng trong quá trình phát triển mô hình song song lần 4.
  - Thư mục con "Test-kernel-functions": chứa 1 file notebook và các file code để kiểm tra tính đúng đắn của các hàm kernel được sử dụng trong quá trình phát triển mô hình song song.
  - Thư mục con "Live-Demo": chứa 1 file notebook và các file code để chạy chương trình minh họa trong video "Live - Demo". -->

## Kế hoạch thực hiện đồ án và phân công công việc

- Tài liệu về kế hoạch thực hiện đồ án của nhóm 05 và bảng phân công công việc chi tiết cho mỗi thành viên đã được đính kèm trong file "**`Team-Plan-and-Work-Distribution.md`**" của bài nộp.

## Hướng dẫn chạy webapp trên máy cá nhân

- Di chuyển môi trường lập trình đến thư mục gốc của dự án (root folder), hay còn gọi là thư mục chứa file "**`requirements.txt`**".
- Chạy các lệnh sau trong terminal để cài đặt các thư viện cần thiết và chạy ứng dụng Streamlit:

```bash
pip install -r requirements.txt
streamlit run src/app/streamlit_app.py
```
