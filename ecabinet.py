import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="E-Cabinet TGDV - Tuyên Quang", page_icon="🏛️", layout="wide")

# ---> LINK ỐNG NƯỚC <---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycby8XxSlcqExB6rW_Ymn3AGxkBcWQWqjJJbHM56Dd8oJfqfovogDVk_KqgnNDMbmmQo0/exec"

# --- MẬT KHẨU QUẢN TRỊ ---
PASS_ADMIN = "Admin@2026"
PASS_DAI_BIEU = "HopBan@2026"

# --- CSS TÙY CHỈNH (GIAO DIỆN PHẲNG - MÀU EDOC+) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .header-box {
        background-color: #ffffff; border-top: 4px solid #17a2b8; border-radius: 5px;
        padding: 15px 30px; margin-bottom: 30px; box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;
    }
    .main-title { font-size: 26px; font-weight: 900; color: #2c3e50; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    .sub-title { font-size: 16px; font-weight: bold; color: #6c757d; margin-top: 5px; text-align: center;}
    .section-title { color: #2c3e50; border-bottom: 2px solid #17a2b8; padding-bottom: 5px; margin-top: 20px; font-size: 18px; text-transform: uppercase; font-weight: bold;}
    .doc-card { background-color: #ffffff; border-left: 4px solid #28a745; padding: 15px; border-radius: 4px; margin-bottom: 12px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05);}
    .doc-title { font-size: 15px; font-weight: bold; color: #343a40;}
    div[data-testid="stForm"] { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 5px; padding: 20px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05);}
    div.stButton > button:first-child { background-color: #17a2b8; color: white; border: none; border-radius: 4px; font-weight: bold; }
    div.stButton > button:first-child:hover { background-color: #138496; color: white; }
</style>
""", unsafe_allow_html=True)

# --- DANH SÁCH CHỨC VỤ & ĐƠN VỊ NỘI BỘ ---
DS_CHUC_VU = [
    "Chọn chức vụ...", "Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", 
    "Trưởng phòng", "Phó Trưởng phòng", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Chuyên viên", "Khác"
]

DS_DON_VI = [
    "Chọn đơn vị...", "Ban Tuyên giáo và Dân vận Tỉnh ủy (Dành cho Lãnh đạo Ban)", 
    "Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", 
    "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", "Phòng Đoàn thể và các Hội"
]

# --- HÀM LẤY LOGO ---
def get_logo_base64():
    try:
        with open("Logo TGDV.png", "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return ""

def hien_thi_tieu_de(tieu_de_chinh):
    logo_data = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height: 75px;">' if logo_data else ""
    st.markdown(f"""
    <div class="header-box">
        <div>{logo_html}</div>
        <div><div class="main-title">{tieu_de_chinh}</div><div class="sub-title">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=30)
def load_data():
    try: return requests.get(WEB_APP_URL).json()
    except: return {"cuoc_hop": [], "tai_lieu": [], "y_kien": []}

# ==========================================
# KHUNG ĐĂNG NHẬP
# ==========================================
if "role" not in st.session_state: st.session_state["role"] = None

if st.session_state["role"] is None:
    hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY (E-CABINET)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👋 Xin chào! Vui lòng nhập mật khẩu để vào Phòng họp trực tuyến.")
        pwd = st.text_input("🔑 Nhập mật khẩu truy cập:", type="password")
        if st.button("🚀 Đăng nhập", use_container_width=True):
            if pwd == PASS_ADMIN: st.session_state["role"] = "Admin"; st.rerun()
            elif pwd == PASS_DAI_BIEU: st.session_state["role"] = "DaiBieu"; st.rerun()
            else: st.error("❌ Mật khẩu không chính xác!")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
logo_sidebar = get_logo_base64()
if logo_sidebar: st.sidebar.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_sidebar}" width="110"></div>', unsafe_allow_html=True)

st.sidebar.markdown(f"<div style='text-align: center; margin-top: 15px; color: #2c3e50;'><b>👤 Quyền:</b> {'Quản trị viên' if st.session_state['role'] == 'Admin' else 'Đại biểu'}</div>", unsafe_allow_html=True)

if st.sidebar.button("🚪 Đăng xuất", use_container_width=True): st.session_state["role"] = None; st.rerun()
st.sidebar.write("---")

menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu", "⚙️ Quản trị: Tạo Cuộc họp", "📤 Quản trị: Đăng Tài liệu"]) if st.session_state["role"] == "Admin" else st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu"])

hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY (E-CABINET)")
data = load_data()
df_cuoc_hop = pd.DataFrame(data.get("cuoc_hop", []))
df_tai_lieu = pd.DataFrame(data.get("tai_lieu", []))
df_y_kien = pd.DataFrame(data.get("y_kien", []))

# ---------------------------------------------------------
# MODULE 1: PHÒNG HỌP & TÀI LIỆU
# ---------------------------------------------------------
if menu == "📚 Phòng họp & Tài liệu":
    if df_cuoc_hop.empty: st.info("Hiện chưa có cuộc họp nào được tạo trên hệ thống.")
    else:
        ds_cuoc_hop_hien_thi = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
        chon_hop = st.selectbox("📌 Lựa chọn Cuộc họp / Hội nghị:", ds_cuoc_hop_hien_thi.tolist())
        if chon_hop:
            ma_ch_dang_chon = chon_hop.split(" - ")[0]
            thong_tin_hop = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch_dang_chon].iloc[0]
            
            st.markdown(f"<h3 style='color: #2c3e50;'>📋 {thong_tin_hop['Tên cuộc họp']}</h3>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.write(f"**⏰ Thời gian:** {thong_tin_hop['Thời gian']}")
            c2.write(f"**📍 Địa điểm:** {thong_tin_hop['Địa điểm']}")
            c3.write(f"**🟢 Trạng thái:** {thong_tin_hop['Trạng thái']}")
            st.write("---")
            
            col_doc, col_feedback = st.columns([5, 5])
            with col_doc:
                st.markdown('<div class="section-title">📑 TÀI LIỆU KỲ HỌP</div>', unsafe_allow_html=True)
                if not df_tai_lieu.empty:
                    tl_cua_hop = df_tai_lieu[df_tai_lieu['Mã cuộc họp'] == ma_ch_dang_chon]
                    if tl_cua_hop.empty: st.write("Chưa có tài liệu nào được đăng tải.")
                    else:
                        for idx, row in tl_cua_hop.iterrows():
                            st.markdown(f"""
                            <div class="doc-card">
                                <div class="doc-title">📄 {row.get('Tên tài liệu', 'Không tên')}</div>
                                <div style="margin-top: 8px;">
                                    <a href="{row.get('Link Google Drive', '#')}" target="_blank" style="text-decoration: none; color: #17a2b8; font-weight: bold;">📥 Xem / Tải về</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else: st.write("Chưa có tài liệu nào được đăng tải.")

            with col_feedback:
                st.markdown('<div class="section-title">✍️ XIN Ý KIẾN / THAM LUẬN</div>', unsafe_allow_html=True)
                tab_gui, tab_xem = st.tabs(["💬 Gửi Ý kiến", "📂 Ý kiến đã thu nhận"])
                
                with tab_gui:
                    with st.form("form_gop_y", clear_on_submit=True):
                        ho_ten_gy = st.text_input("👤 Họ và tên người góp ý:")
                        col_f1, col_f2 = st.columns(2)
                        with col_f1: chuc_vu_gy = st.selectbox("💼 Chức vụ:", DS_CHUC_VU)
                        with col_f2: don_vi_gy = st.selectbox("🏢 Phòng/Ban/Đơn vị:", DS_DON_VI)
                        noi_dung_gy = st.text_area("📝 Nội dung tham gia ý kiến:")
                        file_sua_doi = st.file_uploader("📎 Tải lên File văn bản (Nếu có):", type=["docx", "doc", "pdf"])
                        if st.form_submit_button("🚀 GỬI Ý KIẾN LÊN HỆ THỐNG", use_container_width=True):
                            if not ho_ten_gy or chuc_vu_gy == "Chọn chức vụ..." or don_vi_gy == "Chọn đơn vị...": st.error("⚠️ Vui lòng điền đủ Họ tên, chọn Chức vụ và Đơn vị!")
                            elif not noi_dung_gy and file_sua_doi is None: st.error("⚠️ Vui lòng nhập nội dung góp ý hoặc tải lên file đính kèm!")
                            else:
                                with st.spinner("Đang gửi ý kiến về Ban Thư ký..."):
                                    nguoi_gui_tong_hop = f"{ho_ten_gy} ({chuc_vu_gy} - {don_vi_gy})"
                                    file_base64 = ""; file_name = ""; file_mimeType = ""
                                    if file_sua_doi is not None:
                                        file_base64 = base64.b64encode(file_sua_doi.getvalue()).decode('utf-8')
                                        file_name = f"YKien_{ma_ch_dang_chon}_{file_sua_doi.name}"
                                        file_mimeType = file_sua_doi.type
                                    payload = {"action": "add_y_kien", "ma_ch": ma_ch_dang_chon, "nguoi_gop_y": nguoi_gui_tong_hop, "noi_dung": noi_dung_gy, "file_base64": file_base64, "file_name": file_name, "file_mimeType": file_mimeType}
                                    try:
                                        res = requests.post(WEB_APP_URL, json=payload)
                                        if res.status_code == 200: st.success("✅ Đã ghi nhận ý kiến thành công!"); st.cache_data.clear()
                                        else: st.error("Lỗi máy chủ.")
                                    except Exception as e: st.error(f"Lỗi mạng: {e}")

                with tab_xem:
                    if not df_y_kien.empty:
                        yk_cua_hop = df_y_kien[df_y_kien['Mã cuộc họp'] == ma_ch_dang_chon]
                        if yk_cua_hop.empty: st.info("Chưa có ý kiến nào được gửi.")
                        else:
                            for idx, row in yk_cua_hop.iterrows():
                                with st.expander(f"💬 {row.get('Tên đơn vị / Đại biểu', 'Ẩn danh')} - {row.get('Thời gian gửi', '')}"):
                                    st.write(row.get('Nội dung góp ý', ''))
                                    link_file = row.get('Link File sửa đổi', '')
                                    if link_file and str(link_file) != "nan": st.markdown(f"[📥 Tải File đính kèm]({link_file})")
                    else: st.info("Chưa có ý kiến nào được gửi.")

# ---------------------------------------------------------
# MODULE 2: QUẢN TRỊ TẠO CUỘC HỌP
# ---------------------------------------------------------
elif menu == "⚙️ Quản trị: Tạo Cuộc họp":
    st.markdown('<div class="section-title">➕ TẠO CUỘC HỌP MỚI</div>', unsafe_allow_html=True)
    with st.form("form_tao_hop", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1: ma_ch = st.text_input("Mã Cuộc họp (VD: CH01)*:")
        with col2: ten_ch = st.text_input("Tên Cuộc họp / Hội nghị*:")
        col3, col4, col5 = st.columns(3)
        with col3: thoi_gian = st.text_input("Thời gian (VD: 08:00, 15/05/2026):")
        with col4: dia_diem = st.text_input("Địa điểm:")
        with col5: trang_thai = st.selectbox("Trạng thái:", ["Sắp diễn ra", "Đang diễn ra", "Đã kết thúc"])
        
        if st.form_submit_button("LƯU CUỘC HỌP MỚI"):
            if not ma_ch or not ten_ch: st.error("⚠️ Vui lòng nhập Mã và Tên cuộc họp!")
            else:
                with st.spinner("Đang lưu..."):
                    payload = {"action": "add_cuoc_hop", "ma_ch": ma_ch, "ten_ch": ten_ch, "thoi_gian": thoi_gian, "dia_diem": dia_diem, "trang_thai": trang_thai}
                    res = requests.post(WEB_APP_URL, json=payload)
                    if res.status_code == 200: st.success("✅ Đã tạo cuộc họp thành công!"); st.cache_data.clear()
                    else: st.error("Lỗi.")

# ---------------------------------------------------------
# MODULE 3: QUẢN TRỊ ĐĂNG TÀI LIỆU (ĐÃ NÂNG CẤP UPLOAD NHIỀU FILE)
# ---------------------------------------------------------
elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-title">📤 UPLOAD TÀI LIỆU LÊN HỆ THỐNG</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty:
        st.warning("⚠️ Bạn cần tạo Cuộc họp trước khi đăng tài liệu.")
    else:
        with st.form("form_tai_lieu", clear_on_submit=True):
            ds_cuoc_hop_hien_thi = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
            ch_chon = st.selectbox("📌 Gắn vào Cuộc họp:", ds_cuoc_hop_hien_thi.tolist())
            
            st.info("💡 **Mẹo:** Bạn có thể kéo thả hoặc chọn **nhiều file cùng lúc**. Hệ thống sẽ tự động dùng Tên file làm Tên tài liệu.")
            
            # Tính năng accept_multiple_files=True cho phép chọn nhiều file
            uploaded_files = st.file_uploader("📂 Chọn các File PDF/Word để đưa lên thư viện:", type=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"], accept_multiple_files=True)
            
            submit_tl = st.form_submit_button("🚀 TẢI LÊN VÀ PHÁT HÀNH TÀI LIỆU")
            
            if submit_tl:
                if not uploaded_files:
                    st.error("⚠️ Vui lòng chọn ít nhất 1 file để tải lên!")
                else:
                    ma_ch = ch_chon.split(" - ")[0]
                    thanh_cong = 0
                    loi = 0
                    
                    # Hiện thanh tiến trình
                    progress_bar = st.progress(0, text="Bắt đầu tải file lên hệ thống...")
                    
                    for i, file_up in enumerate(uploaded_files):
                        file_base64 = base64.b64encode(file_up.getvalue()).decode('utf-8')
                        ten_file_goc = file_up.name
                        
                        # Tự động sinh mã tài liệu ngẫu nhiên dựa trên thời gian
                        ma_tl_auto = f"TL{datetime.now().strftime('%H%M%S')}{i}"
                        
                        payload = {
                            "action": "add_tai_lieu",
                            "ma_ch": ma_ch, 
                            "ma_tl": ma_tl_auto,          # Mã tự động
                            "ten_tl": ten_file_goc,       # Lấy tên file gốc
                            "loai_tl": "",                # Bỏ trống phần loại tài liệu
                            "file_base64": file_base64, 
                            "file_name": ten_file_goc, 
                            "file_mimeType": file_up.type
                        }
                        
                        try:
                            res = requests.post(WEB_APP_URL, json=payload)
                            if res.status_code == 200: thanh_cong += 1
                            else: loi += 1
                        except: loi += 1
                        
                        # Cập nhật thanh tiến trình
                        percent_complete = int(((i + 1) / len(uploaded_files)) * 100)
                        progress_bar.progress(percent_complete, text=f"Đang xử lý: {i+1} / {len(uploaded_files)} file...")

                    if loi == 0:
                        st.success(f"✅ Đã tải lên và phát hành thành công {thanh_cong} tài liệu!")
                    else:
                        st.warning(f"⚠️ Hoàn tất tải lên: {thanh_cong} thành công, {loi} bị lỗi.")
                    
                    st.cache_data.clear()
