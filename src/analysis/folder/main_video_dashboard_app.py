import streamlit as st
from footer import display_footer
from data_load import load_data

# Set page configuration
st.set_page_config(
    layout="wide"
)

# Load data once when the app starts and cache it
df = load_data()

# Store the dataframe in session state so all pages can access it
if 'df' not in st.session_state:
    st.session_state.df = df

# Title of the main page
st.title("🎵 Bảng Điều Khiển Phân Tích TikTok")

# Introduction section
st.markdown("""
<div style="font-size: 18px; line-height: 1.6; color: #333;">
Chào mừng bạn đến với <b>Bảng Điều Khiển Phân Tích TikTok</b>, một công cụ mạnh mẽ sử dụng Streamlit để khám phá dữ liệu người dùng, chỉ số tương tác và xu hướng trên TikTok. 
Dù bạn là người đam mê dữ liệu, nhà tiếp thị hay người sáng tạo nội dung trên TikTok, bảng điều khiển này mang đến <span style="color: #FF5555;">hình ảnh trực quan tương tác</span> giúp bạn dễ dàng nắm bắt sự phát triển của nền tảng này.
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Features section
st.header("✨ Tính Năng")
st.markdown("""
<div style="font-size: 16px; line-height: 1.5;">
<ul style="list-style-type: none; padding-left: 0;">
    <li>📊 <a href="?page=correlation_analysis" style="color: #636EFA; text-decoration: none;">Phân Tích Tương Quan</a>: Khám phá mối quan hệ giữa số người theo dõi, lượt thích và số lượng video qua biểu đồ histogram, ma trận phân tán và bản đồ nhiệt.</li>
    <li>🏆 <a href="?page=top_users" style="color: #EF553B; text-decoration: none;">Người Dùng Hàng Đầu</a>: Xác định những người có ảnh hưởng nhất trên TikTok dựa trên lượt thích, người theo dõi hoặc tỷ lệ tương tác.</li>
    <li>📈 <a href="?page=engagement_insight" style="color: #00CC96; text-decoration: none;">Phân Tích Tương Tác</a>: Đánh giá cách mức độ tương tác thay đổi theo số lượng người theo dõi.</li>
    <li>👤 <a href="?page=personal_analysis" style="color: #AB63FA; text-decoration: none;">Phân Tích Cá Nhân</a>: Khám phá hồ sơ của từng TikToker, xu hướng video, việc sử dụng nhạc và mô hình hashtag.</li>
    <li>🎶 <a href="?page=hashtag_analysis" style="color: #FFA15A; text-decoration: none;">Phân Tích Hashtag & Bài Hát</a>: Tìm kiếm các hashtag và bài hát phổ biến trong một khoảng thời gian cụ thể.</li>
    <li>🖌️ <a href="?page=visual_interaction" style="color: #19D3F3; text-decoration: none;">Hình Ảnh Trực Quan Tương Tác</a>: Được xây dựng với Plotly để tạo biểu đồ động và có thể tùy chỉnh.</li>
    <li>📥 <a href="?page=top_users" style="color: #FF6692; text-decoration: none;">Xuất Dữ Liệu</a>: Tải xuống dữ liệu biểu đồ dưới dạng tệp CSV để phân tích sâu hơn.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Instructions section
st.header("🚀 Hướng Dẫn Sử Dụng")
st.markdown("""
<div style="font-size: 16px; line-height: 1.5;">
<ol style="padding-left: 20px;">
    <li><b>Điều Hướng</b>: Sử dụng thanh bên để chuyển đổi giữa các trang.</li>
    <li><b>Tương Tác</b>: Điều chỉnh thanh trượt, danh sách thả xuống và hộp kiểm để tùy chỉnh biểu đồ.</li>
    <li><b>Khám Phá</b>: Xem dữ liệu qua các biểu đồ trực quan tương tác và tải xuống thông tin chi tiết.</li>
    <li><b>Lọc</b>: Sử dụng bộ lọc thời gian trên các trang cụ thể để tập trung vào khoảng thời gian bạn quan tâm.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# # Divider
# st.markdown("---")

# # Getting the page selected from sidebar
# page = st.sidebar.radio("Select Analysis", ["Phân Tích Tương Quan", "Người Dùng Hàng Đầu", "Phân Tích Tương Tác", "Phân Tích Cá Nhân", "Phân Tích Hashtag & Bài Hát", "Hình Ảnh Trực Quan Tương Tác", "Xuất Dữ Liệu"])

# # Show the selected analysis page
# if page == "Phân Tích Tương Quan":
#     hashtag_engagement.display_hashtag_engagement()
# elif page == "Người Dùng Hàng Đầu":
#     video_performance.display_video_performance()
# elif page == "Phân Tích Tương Tác":
#     hashtag_insights.display_hashtag_insights()
# # elif page == "Phân Tích Cá Nhân":
# #     analysis4.show_analysis4()
# # elif page == "Phân Tích Hashtag & Bài Hát":
# #     analysis5.show_analysis5()
# # elif page == "Hình Ảnh Trực Quan Tương Tác":
# #     analysis6.show_analysis6()
# # elif page == "Xuất Dữ Liệu":
# #     analysis7.show_analysis7()
# etc...

# Footer with last updated timestamp
display_footer()

