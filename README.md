<div align="center">
   <h1>🎬 Đồ án cuối kỳ: Phân tích dữ liệu TikTok và Xây dựng công cụ hỗ trợ viết kịch bản cho video TikTok</h1>
   <p><strong>Phân tích dữ liệu TikTok thông minh và hỗ trợ sáng tạo nội dung</strong></p>
   
   [![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://21khdl-tiktok-analytics.streamlit.app/)
   [![YouTube Demo](https://img.shields.io/badge/YouTube-Demo-FF0000?style=for-the-badge&logo=youtube)](https://www.youtube.com/playlist?list=PL3SfxVDJ_Zc6DvBKVd6xUc-exmt0AyA7x)
</div>

## 🧑‍🤝‍🧑 Sinh viên thực hiện

| STT |   MSSV   | Họ và tên                                 |
| :-: | :------: | ----------------------------------------- |
|  1  | 21127731 | Nguyễn Trọng Tín $^{\clubsuit}$           |
|  2  | 21127038 | Võ Phú Hãn $^{\clubsuit\heartsuit}$       |
|  3  | 21127351 | Hồ Đinh Duy Lực $^{\clubsuit}$            |
|  4  | 21127739 | Vũ Minh Phát $^{\clubsuit\heartsuit}$     |
|  5  | 21127742 | Nguyễn Minh Hiếu $^{\clubsuit\heartsuit}$ |
|  6  | 19127216 | Đặng Hoàn Mỹ $^{\clubsuit\diamondsuit}$   |

<details>
   <summary>📋 Thông tin nhóm</summary>
   
   ${\clubsuit}$: Nhóm 01 (Data Explorers) - Ứng dụng phân tích dữ liệu thông minh - 21KHDL  
   ${\heartsuit}$: Nhóm 05 - Khoa học dữ liệu ứng dụng - 21KHDL  
   ${\diamondsuit}$: Nhóm 09 - Khoa học dữ liệu ứng dụng - 21KHDL
</details>

## 🎥 Demo và Sản phẩm

### 📊 Sản phẩm

<div align="center">
   <a href="https://21khdl-tiktok-analytics.streamlit.app/">
      <img src="https://img.shields.io/badge/Truy_cập_ứng_dụng-00B2FF?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit App" />
   </a>
</div>

### 🎬 Video Demo

<div align="center">
   <a href="https://www.youtube.com/playlist?list=PL3SfxVDJ_Zc6DvBKVd6xUc-exmt0AyA7x">
      <img src="https://img.shields.io/badge/Xem_video_hướng_dẫn-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube Demo" />
   </a>
</div>

> Trong playlist sẽ có video hướng dẫn sử dụng bộ ba công cụ mà nhóm đã xây dựng, xoay quanh chủ đề trọng tâm của đồ án lần này là: "Xây dựng công cụ hỗ trợ viết kịch bản cho video TikTok".

## 📁 Cách tổ chức thư mục của đồ án

```
📦 21KHDL-TikTok-Analytics
 ┣ 📜 README.md              # Tài liệu giới thiệu và hướng dẫn sử dụng dự án
 ┣ 📜 Team-Plan-and-Work-Distribution.md  # Kế hoạch và phân công công việc
 ┣ 📜 requirements.txt       # Danh sách các thư viện cần thiết
 ┣ 📜 packages.txt           # Thông tin về các gói hoặc môi trường
 ┣ 📂 data                   # Dữ liệu thô, dữ liệu đã xử lý
 ┣ 📂 development            # Mã nguồn phát triển, tệp thử nghiệm
 ┣ 📂 docs                   # Tài liệu chi tiết về dự án, API
 ┣ 📂 models                 # Danh sách các mô hình được sử dụng trong dự án
 ┣ 📂 notebooks              # Jupyter Notebook phục vụ phân tích
 ┣ 📂 reports                # Các báo cáo, tài liệu liên quan đến dự án
 ┣ 📂 slides                 # Các slide thuyết trình, tài liệu trình bày
 ┗ 📂 src                    # Mã nguồn chính của ứng dụng
      ┗ 📂 app
          ┗ 📜 streamlit_app.py # Tệp chính của ứng dụng Streamlit
```

## 📝 Kế hoạch thực hiện đồ án và phân công công việc

Kế hoạch thực hiện đồ án và bảng phân công công việc chi tiết cho mỗi thành viên được trình bày trong file [**`Team-Plan-and-Work-Distribution.md`**](Team-Plan-and-Work-Distribution.md). Trong đó, nhóm đã phân chia công việc theo từng phần cụ thể và chỉ định nhiệm vụ cho từng thành viên.

## ⚙️ Hướng dẫn cài đặt và chạy ứng dụng

<details>
   <summary>Xem hướng dẫn chi tiết</summary>
   
   ### 1️⃣ Di chuyển đến thư mục gốc
   
   ```bash
   cd /đường/dẫn/đến/thư/mục/dự/án
   ```
   
   ### 2️⃣ Cài đặt thư viện cần thiết
   
   ```bash
   pip install -r requirements.txt
   ```
   
   ### 3️⃣ Khởi chạy ứng dụng
   
   ```bash
   streamlit run src/app/streamlit_app.py
   ```
   
   ### 4️⃣ Truy cập ứng dụng
   Mở trình duyệt web và truy cập địa chỉ: [http://localhost:8501/](http://localhost:8501/)
   
   ### 5️⃣ Dừng ứng dụng
   Nhấn `Ctrl + C` trong terminal để dừng ứng dụng.
</details>

---

<div align="center">
   <sub>Phát triển bởi nhóm sinh viên HCMUS - Đồ án Ứng dụng phân tích dữ liệu thông minh và Khoa học dữ liệu ứng dụng - 21KHDL</sub>
</div>
