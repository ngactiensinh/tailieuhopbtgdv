import streamlit as st
import requests
import base64
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="E-Cabinet TGDV - Tuyên Quang", page_icon="🏛️", layout="wide")

# ---> LINK ỐNG NƯỚC <---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycby8XxSlcqExB6rW_Ymn3AGxkBcWQWqjJJbHM56Dd8oJfqfovogDVk_KqgnNDMbmmQo0/exec"

# --- MẬT KHẨU QUẢN TRỊ ---
PASS_ADMIN = "Admin@2026"
PASS_DAI_BIEU = "HopBan@2026"

# --- DANH SÁCH CHỨC VỤ & ĐƠN VỊ NỘI BỘ ---
DS_CHUC_VU = [
    "Chọn chức vụ...", "Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", 
    "Trưởng phòng", "Phó Trưởng phòng", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Chuyên viên", "Khác"
]

DS_DON_VI = [
    "Chọn đơn vị...", 
    "Ban Tuyên giáo và Dân vận Tỉnh ủy (Dành cho Lãnh đạo Ban)", 
    "Văn phòng Ban", 
    "Phòng Lý luận chính trị, Lịch sử Đảng", 
    "Phòng Tuyên truyền, Báo chí - Xuất bản", 
    "Phòng Khoa giáo, Văn hóa - Văn nghệ", 
    "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", 
    "Phòng Đoàn thể và các Hội"
]

# --- HÀM ĐỌC ẢNH TỪ GITHUB (TRÁNH LỖI KHI KHÔNG CÓ FILE) ---
def get_image_base64(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

# --- HÀM TẠO TIÊU ĐỀ Banner (Cho giao diện bên trong) ---
def hien_thi_tieu_de(tieu_de_chinh):
    logo_data = get_image_base64("Logo TGDV.png")
    if logo_data:
        logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height: 85px;">'
    else:
        logo_html = '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png" style="height: 85px;">'
    
    st.markdown(f"""
    <div class="header-oval">
        <div>{logo_html}</div>
        <div>
            <div class="main-title">{tieu_de_chinh}</div>
            <div class="sub-title">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- HÀM LẤY DỮ LIỆU TỪ GOOGLE SHEETS ---
@st.cache_data(ttl=30)
def load_data():
    try:
        res = requests.get(WEB_APP_URL)
        return res.json()
    except:
        return {"cuoc_hop": [], "tai_lieu": [], "y_kien": []}

# ==========================================
# KHUNG ĐĂNG NHẬP (GIAO DIỆN iCPV CABINET)
# ==========================================
if "role" not in st.session_state:
    st.session_state["role"] = None

if st.session_state["role"] is None:
    # --- CSS SIÊU CẤP CHO MÀN HÌNH ĐĂNG NHẬP ---
    st.markdown("""
    <style>
        /* Nền toàn bộ màn hình màu đỏ cờ */
        .stApp {
            background: linear-gradient(135deg, #B30000, #800000, #4d0000) !important;
        }
        /* Ẩn Header mặc định */
        header {visibility: hidden;}
        
        /* Căn chỉnh lại padding của Streamlit */
        .block-container {
            padding-top: 5vh !important;
            padding-bottom: 2rem !important;
            max-width: 1000px !important;
        }
        
        /* Box trắng bao bọc form đăng nhập */
        .login-box {
            background-color: white;
            padding: 30px 40px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.6);
            height: 100%;
        }
        .main-text {
            color: #004B87;
            font-size: 20px;
            font-weight: 900;
            text-align: center;
            line-height: 1.3;
            margin-top: 10px;
            margin-bottom: 5px;
            font-family: Arial, sans-serif;
        }
        .sub-text {
            color: #004B87;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 25px;
        }
        .label-text {
            font-size: 14px;
            color: #C8102E;
            font-weight: bold;
            margin-bottom: -10px;
        }
        /* Chỉnh nút bấm màu đỏ */
        div.stButton > button:first-child {
            background-color: #C8102E !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            padding: 10px !important;
            margin-top: 15px !important;
        }
        div.stButton > button:first-child:hover {
            background-color: #8b0000 !important;
        }
        .link-text {
            font-size: 13px;
            color: #C8102E;
            text-align: right;
            cursor: pointer;
            margin-top: -15px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Khung layout chính (Gộp cả ảnh và form vào chung một hàng)
    st.markdown('<div style="background-color: white; border-radius: 15px; overflow: hidden; box-shadow: 0px 15px 40px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
    
    col_img, col_form = st.columns([1.2, 1], gap="small")
    
    # Cột trái: Ảnh phòng họp
    with col_img:
        img_phonghop = get_image_base64("phonghop.jpg")
        if img_phonghop:
            st.markdown(f'<img src="data:image/jpeg;base64,{img_phonghop}" style="width: 100%; height: 500px; object-fit: cover; display: block; border-right: 2px solid #f0f0f0;">', unsafe_allow_html=True)
        else:
            # Ảnh mặc định nếu chưa up phonghop.jpg
            st.markdown(f'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Vietnam_National_Assembly_Hall.jpg/800px-Vietnam_National_Assembly_Hall.jpg" style="width: 100%; height: 500px; object-fit: cover; display: block; border-right: 2px solid #f0f0f0;">', unsafe_allow_html=True)
    
    # Cột phải: Form đăng nhập
    with col_form:
        st.markdown('<div style="padding: 30px 40px 30px 20px;">', unsafe_allow_html=True)
        
        # Logo
        logo_data = get_image_base64("Logo TGDV.png")
        if logo_data:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_data}" style="height:50px;"></div>', unsafe_allow_html=True)
        
        # Text
        st.markdown('<div class="main-text">HỆ THỐNG THÔNG TIN PHỤC VỤ HỌP<br>VÀ XỬ LÝ CÔNG VIỆC</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-text">Đăng nhập</div>', unsafe_allow_html=True)
        
        # Form nhập liệu
        st.markdown('<p class="label-text">Tên tài khoản *</p>', unsafe_allow_html=True)
        tk = st.text_input("Tên tài khoản", value="Đại biểu dự họp", label_visibility="collapsed", disabled=True)
        
        st.markdown('<p class="label-text">Mật khẩu *</p>', unsafe_allow_html=True)
        pwd = st.text_input("Mật khẩu", type="password", label_visibility="collapsed")
        
        st.markdown('<div class="link-text">Quên mật khẩu?</div>', unsafe_allow_html=True)
        
        if st.button("Đăng nhập", use_container_width=True):
            if pwd == PASS_ADMIN:
                st.session_state["role"] = "Admin"
                st.rerun()
            elif pwd == PASS_DAI_BIEU:
                st.session_state["role"] = "DaiBieu"
                st.rerun()
            else:
                st.error("❌ Mật khẩu không chính xác!")
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP)
# ==========================================
# --- TRẢ LẠI CSS NỀN TRẮNG VÀ GIAO DIỆN TRUYỀN THỐNG ---
st.markdown("""
<style>
    .stApp { background: #FFFFFF !important; }
    .header-oval {
        background-color: #ffffff;
        border: 4px solid #C8102E;
        border-radius: 60px;
        padding: 15px 30px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 25px;
        flex-wrap: wrap;
    }
    .main-title { font-size: 32px; font-weight: 900; color: #C8102E; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    .sub-title { font-size: 18px; font-weight: bold; color: #004B87; margin-top: 5px; text-align: center;}
    .section-title { color: #C8102E; border-bottom: 2px solid #C8102E; padding-bottom: 5px; margin-top: 20px;}
    .doc-card { background-color: #f8f9fa; border-left: 5px solid #C8102E; padding: 15px; border-radius: 5px; margin-bottom: 10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05);}
    .doc-title { font-size: 16px; font-weight: bold; color: #004B87;}
    .doc-type { font-size: 13px; background-color: #e9ecef; padding: 2px 8px; border-radius: 10px; color: #495057;}
</style>
""", unsafe_allow_html=True)

# Hiển thị Logo lên Sidebar
logo_sidebar = get_image_base64("Logo TGDV.png")
if logo_sidebar:
    st.sidebar.markdown(f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_sidebar}" width="120">
        </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png", width=80)

st.sidebar.markdown(f"<div style='text-align: center; margin-top: 10px;'><b>👤 Quyền:</b> {'Quản trị viên (Admin)' if st.session_state['role'] == 'Admin' else 'Đại biểu'}</div>", unsafe_allow_html=True)

if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state["role"] = None
    st.rerun()

st.sidebar.write("---")

# Menu điều hướng
if st.session_state["role"] == "Admin":
    menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu", "⚙️ Quản trị: Tạo Cuộc họp", "📤 Quản trị: Đăng Tài liệu"])
else:
    menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu"])

hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY (E-CABINET)")

data = load_data()
df_cuoc_hop = pd.DataFrame(data.get("cuoc_hop", []))
df_tai_lieu = pd.DataFrame(data.get("tai_lieu", []))
df_y_kien = pd.DataFrame(data.get("y_kien", []))

# ---------------------------------------------------------
# MODULE 1: PHÒNG HỌP & TÀI LIỆU
# ---------------------------------------------------------
if menu == "📚 Phòng họp & Tài liệu":
    if df_cuoc_hop.empty:
        st.info("Hiện chưa có cuộc họp nào được tạo trên hệ thống.")
    else:
        ds_cuoc_hop_hien_thi = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
        chon_hop = st.selectbox("📌 Lựa chọn Cuộc họp / Hội nghị:", ds_cuoc_hop_hien_thi.tolist())
        
        if chon_hop:
            ma_ch_dang_chon = chon_hop.split(" - ")[0]
            thong_tin_hop = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch_dang_chon].iloc[0]
            
            st.markdown(f"### 📋 {thong_tin_hop['Tên cuộc họp']}")
            c1, c2, c3 = st.columns(3)
            c1.write(f"**⏰ Thời gian:** {thong_tin_hop['Thời gian']}")
            c2.write(f"**📍 Địa điểm:** {thong_tin_hop['Địa điểm']}")
            c3.write(f"**🟢 Trạng thái:** {thong_tin_hop['Trạng thái']}")
            
            st.write("---")
            
            col_doc, col_feedback = st.columns([5, 5])
            
            with col_doc:
                st.markdown('<h3 class="section-title">📑 TÀI LIỆU KỲ HỌP</h3>', unsafe_allow_html=True)
                if not df_tai_lieu.empty:
                    tl_cua_hop = df_tai_lieu[df_tai_lieu['Mã cuộc họp'] == ma_ch_dang_chon]
                    if tl_cua_hop.empty:
                        st.write("Chưa có tài liệu nào được đăng tải.")
                    else:
                        for idx, row in tl_cua_hop.iterrows():
                            st.markdown(f"""
                            <div class="doc-card">
                                <div class="doc-title">📄 {row.get('Tên tài liệu', 'Không tên')}</div>
                                <div style="margin-top: 5px;">
                                    <span class="doc-type">{row.get('Loại tài liệu', 'Tài liệu')}</span>
                                    <a href="{row.get('Link Google Drive', '#')}" target="_blank" style="margin-left: 15px; text-decoration: none; color: #C8102E; font-weight: bold;">📥 Xem / Tải về</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.write("Chưa có tài liệu nào được đăng tải.")

            with col_feedback:
                st.markdown('<h3 class="section-title">✍️ XIN Ý KIẾN / THAM LUẬN</h3>', unsafe_allow_html=True)
                
                tab_gui, tab_xem = st.tabs(["💬 Gửi Ý kiến", "📂 Ý kiến đã thu nhận"])
                
                with tab_gui:
                    with st.form("form_gop_y", clear_on_submit=True):
                        ho_ten_gy = st.text_input("👤 Họ và tên người góp ý:")
                        
                        col_f1, col_f2 = st.columns(2)
                        with col_f1: 
                            chuc_vu_gy = st.selectbox("💼 Chức vụ:", DS_CHUC_VU)
                        with col_f2: 
                            don_vi_gy = st.selectbox("🏢 Phòng/Ban/Đơn vị:", DS_DON_VI)
                        
                        noi_dung_gy = st.text_area("📝 Nội dung tham gia ý kiến:")
                        file_sua_doi = st.file_uploader("📎 Tải lên File văn bản đã sửa / File tham luận (Nếu có):", type=["docx", "doc", "pdf"])
                        
                        btn_gui = st.form_submit_button("🚀 GỬI Ý KIẾN LÊN HỆ THỐNG", use_container_width=True)
                        
                        if btn_gui:
                            if not ho_ten_gy or chuc_vu_gy == "Chọn chức vụ..." or don_vi_gy == "Chọn đơn vị...":
                                st.error("⚠️ Vui lòng điền đủ Họ tên, chọn Chức vụ và Đơn vị!")
                            elif not noi_dung_gy and file_sua_doi is None:
                                st.error("⚠️ Vui lòng nhập nội dung góp ý hoặc tải lên file đính kèm!")
                            else:
                                with st.spinner("Đang gửi ý kiến về Ban Thư ký..."):
                                    nguoi_gui_tong_hop = f"{ho_ten_gy} ({chuc_vu_gy} - {don_vi_gy})"
                                    
                                    file_base64 = ""; file_name = ""; file_mimeType = ""
                                    if file_sua_doi is not None:
                                        file_base64 = base64.b64encode(file_sua_doi.getvalue()).decode('utf-8')
                                        file_name = f"YKien_{ma_ch_dang_chon}_{file_sua_doi.name}"
                                        file_mimeType = file_sua_doi.type
                                    
                                    payload = {
                                        "action": "add_y_kien",
                                        "ma_ch": ma_ch_dang_chon, "nguoi_gop_y": nguoi_gui_tong_hop, "noi_dung": noi_dung_gy,
                                        "file_base64": file_base64, "file_name": file_name, "file_mimeType": file_mimeType
                                    }
                                    try:
                                        res = requests.post(WEB_APP_URL, json=payload)
                                        if res.status_code == 200:
                                            st.success("✅ Đã ghi nhận ý kiến thành công!")
                                            st.cache_data.clear()
                                        else: st.error("Lỗi máy chủ.")
                                    except Exception as e: st.error(f"Lỗi mạng: {e}")

                with tab_xem:
                    if not df_y_kien.empty:
                        yk_cua_hop = df_y_kien[df_y_kien['Mã cuộc họp'] == ma_ch_dang_chon]
                        if yk_cua_hop.empty:
                            st.info("Chưa có ý kiến nào được gửi.")
                        else:
                            for idx, row in yk_cua_hop.iterrows():
                                with st.expander(f"💬 {row.get('Tên đơn vị / Đại biểu', 'Ẩn danh')} - {row.get('Thời gian gửi', '')}"):
                                    st.write(row.get('Nội dung góp ý', ''))
                                    link_file = row.get('Link File sửa đổi', '')
                                    if link_file and str(link_file) != "nan":
                                        st.markdown(f"[📥 Tải File đính kèm]({link_file})")
                    else:
                        st.info("Chưa có ý kiến nào được gửi.")

# ---------------------------------------------------------
# MODULE 2: QUẢN TRỊ TẠO CUỘC HỌP
# ---------------------------------------------------------
elif menu == "⚙️ Quản trị: Tạo Cuộc họp":
    st.markdown('<h3 class="section-title">➕ TẠO CUỘC HỌP MỚI</h3>', unsafe_allow_html=True)
    with st.form("form_tao_hop", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1: ma_ch = st.text_input("Mã Cuộc họp (VD: CH01)*:")
        with col2: ten_ch = st.text_input("Tên Cuộc họp / Hội nghị*:")
        
        col3, col4, col5 = st.columns(3)
        with col3: thoi_gian = st.text_input("Thời gian (VD: 08:00, 15/05/2026):")
        with col4: dia_diem = st.text_input("Địa điểm:")
        with col5: trang_thai = st.selectbox("Trạng thái:", ["Sắp diễn ra", "Đang diễn ra", "Đã kết thúc"])
        
        submit_hop = st.form_submit_button("LƯU CUỘC HỌP MỚI")
        
        if submit_hop:
            if not ma_ch or not ten_ch:
                st.error("⚠️ Vui lòng nhập Mã và Tên cuộc họp!")
            else:
                with st.spinner("Đang lưu..."):
                    payload = {"action": "add_cuoc_hop", "ma_ch": ma_ch, "ten_ch": ten_ch, "thoi_gian": thoi_gian, "dia_diem": dia_diem, "trang_thai": trang_thai}
                    res = requests.post(WEB_APP_URL, json=payload)
                    if res.status_code == 200:
                        st.success("✅ Đã tạo cuộc họp thành công!")
                        st.cache_data.clear()
                    else: st.error("Lỗi.")

# ---------------------------------------------------------
# MODULE 3: QUẢN TRỊ ĐĂNG TÀI LIỆU
# ---------------------------------------------------------
elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<h3 class="section-title">📤 UPLOAD TÀI LIỆU LÊN HỆ THỐNG</h3>', unsafe_allow_html=True)
    if df_cuoc_hop.empty:
        st.warning("⚠️ Bạn cần tạo Cuộc họp trước khi đăng tài liệu.")
    else:
        with st.form("form_tai_lieu", clear_on_submit=True):
            ds_cuoc_hop_hien_thi = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
            ch_chon = st.selectbox("Gắn vào Cuộc họp:", ds_cuoc_hop_hien_thi.tolist())
            
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1: ma_tl = st.text_input("Mã Tài liệu (VD: TL01)*:")
            with c2: ten_tl = st.text_input("Tên Tài liệu*:")
            with c3: loai_tl = st.selectbox("Loại Tài liệu:", ["Báo cáo", "Tờ trình", "Nghị quyết", "Dự thảo", "Tài liệu tham khảo"])
            
            file_up = st.file_uploader("📂 Chọn File PDF/Word để đưa lên thư viện:", type=["pdf", "doc", "docx", "xls", "xlsx"])
            
            submit_tl = st.form_submit_button("🚀 TẢI LÊN VÀ PHÁT HÀNH TÀI LIỆU")
            
            if submit_tl:
                if not ma_tl or not ten_tl or file_up is None:
                    st.error("⚠️ Vui lòng điền đủ Mã, Tên và chọn File tải lên!")
                else:
                    with st.spinner("Đang đẩy file lên kho Google Drive và mã hóa (vui lòng chờ)..."):
                        file_base64 = base64.b64encode(file_up.getvalue()).decode('utf-8')
                        ma_ch = ch_chon.split(" - ")[0]
                        payload = {
                            "action": "add_tai_lieu",
                            "ma_ch": ma_ch, "ma_tl": ma_tl, "ten_tl": ten_tl, "loai_tl": loai_tl,
                            "file_base64": file_base64, "file_name": file_up.name, "file_mimeType": file_up.type
                        }
                        res = requests.post(WEB_APP_URL, json=payload)
                        if res.status_code == 200:
                            st.success("✅ Đã tải lên và phát hành tài liệu thành công!")
                            st.cache_data.clear()
                        else: st.error("Lỗi.")
