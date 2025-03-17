import streamlit as st

def generate_script(description):
    # Ví dụ đơn giản: tạo ra kịch bản dựa trên mô tả người dùng nhập vào.
    # Bạn có thể mở rộng logic này để tạo nhiều màn hình khác nhau.
    script = f"Screen 1: Giới thiệu về món ăn\n{description}\n"
    return script

def main():
    st.title("Tạo Kịch Bản Video Tự Động")
    
    # Nhận mô tả từ người dùng
    description = st.text_area("Nhập mô tả nội dung:", height=150)
    
    # Khi người dùng nhấn nút, tạo ra kịch bản
    if st.button("Tạo Kịch Bản"):
        script = generate_script(description)
        st.subheader("Kịch Bản Tạo Ra:")
        st.text(script)

if __name__ == "__main__":
    main()
