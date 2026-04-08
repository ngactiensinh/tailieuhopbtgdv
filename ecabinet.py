import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="E-Cabinet TGDV - Tuyên Quang", page_icon="🏛️", layout="wide")

# ---> LINK ỐNG NƯỚC <---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycby8XxSlcqExB6rW_Ymn3AGxkBcWQWqjJJbHM56Dd8oJfqfovogDVk_KqgnNDMbmmQo0/exec"

# --- MẬT KHẨU ---
PASS_ADMIN = "Admin@2026"
PASS_DAI_BIEU = "HopBan@2026"

# --- CSS NÂNG CẤP GIAO DIỆN ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .header-box {
        background-color: #ffffff; border-top: 4px solid #17a2b8; border-radius: 5px;
        padding: 15px 30px; margin-bottom: 25px; box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;
    }
    .main-title { font-size: 26px; font-weight: 900; color: #2c3e50; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    
    /* Thẻ cuộc họp nổi bật ngoài màn hình đăng nhập */
    .featured-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0faff 100%);
        border: 2px solid #17a2b8;
        border-radius: 10px;
        padding: 25px;
        margin: 0 auto 30px auto;
        max-width: 800px;
        box-shadow: 0px 4px 15px rgba(23, 162, 184, 0.2);
        text-align: center;
    }
    .featured-tag {
        background-color: #C8102E; color: white; padding: 4px 12px; 
        border-radius: 4px; font-size: 13px; font-weight: bold; text-transform: uppercase;
    }
    
    .section-title { color: #2c3e50; border-bottom: 2px solid #17a2b8; padding-bottom: 5px; margin-top: 20px; font-size: 18px; text-transform: uppercase; font-weight: bold;}
    .doc-card { background-color: #ffffff; border-left: 4px solid #28a745; padding: 15px; border-radius: 4px; margin-bottom: 12px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05);}
</style>
""", unsafe_allow_html=True)

# --- DANH SÁCH ĐƠN VỊ NỘI BỘ ---
DS_CHUC_VU = ["Chọn chức vụ...", "Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", "Trưởng phòng", "Phó Trưởng phòng", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Chuyên viên", "Khác"]
DS_DON_VI = ["Chọn đơn vị...", "Ban Tuyên giáo và Dân vận Tỉnh ủy (Lãnh đạo Ban)", "Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", "Phòng Đoàn thể và các Hội"]

def get_logo_base64():
    try:
        with open("Logo TGDV.png", "rb") as f: return base64.b64encode(f.read()).decode("utf-8")
    except: return ""

def hien_thi_tieu_de(tieu_de_chinh):
    logo_data = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height: 75px;">' if logo_data else ""
    st.markdown(f'<div class="header-box"><div>{logo_html}</div><div><div class="main-title">{tieu_de_chinh}</div><div style="font-size: 14px; font-weight: bold; color: #6c757d; text-align: center;">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div></div>', unsafe_allow_html=True)

@st.cache_data(ttl=30)
def load_data():
    try: return requests.get(WEB_APP_URL).json()
    except: return {"cuoc_hop": [], "tai_lieu": [], "y_kien": []}

# --- KHỞI TẠO BIẾN TRẠNG THÁI ---
if "role" not in st.session_state: st.session_state["role"] = None
if "selected_meeting_id" not in st.session_state: st.session_state["selected_meeting_id"] = None

# --- LẤY DỮ LIỆU SỚM ĐỂ HIỂN THỊ TRƯỚC ĐĂNG NHẬP ---
data = load_data()
df_cuoc_hop = pd.DataFrame(data.get("cuoc_hop", []))
df_tai_lieu = pd.DataFrame(data.get("tai_lieu", []))
df_y_kien = pd.DataFrame(data.get("y_kien", []))

# ==========================================
# MÀN HÌNH ĐĂNG NHẬP
# ==========================================
if st.session_state["role"] is None:
    hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY (E-CABINET)")
    
    # 🌟 HIỂN THỊ CUỘC HỌP NỔI BẬT NGAY TẠI ĐÂY
    latest_ch_id = None
    if not df_cuoc_hop.empty:
        latest_ch = df_cuoc_hop.iloc[-1]
        latest_ch_id = latest_ch['Mã cuộc họp']
        st.markdown(f"""
        <div class="featured-card">
            <span class="featured-tag">Sắp diễn ra / Mới nhất</span>
            <h2 style="color: #004B87; margin-top: 15px; margin-bottom: 10px;">{latest_ch['Tên cuộc họp']}</h2>
            <p style="margin: 0; color: #495057; font-size: 16px;">📍 <b>Địa điểm:</b> {latest_ch['Địa điểm']} &nbsp;|&nbsp; ⏰ <b>Thời gian:</b> {latest_ch['Thời gian']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🔐 Vui lòng nhập mật khẩu để vào phòng họp hoặc truy cập kho tài liệu.")
        pwd = st.text_input("🔑 Nhập mật khẩu:", type="password")
        if st.button("🚀 Vào phòng họp", use_container_width=True):
            if pwd == PASS_ADMIN: 
                st.session_state["role"] = "Admin"
                if latest_ch_id: st.session_state["selected_meeting_id"] = latest_ch_id
                st.rerun()
            elif pwd == PASS_DAI_BIEU: 
                st.session_state["role"] = "DaiBieu"
                if latest_ch_id: st.session_state["selected_meeting_id"] = latest_ch_id
                st.rerun()
            else: 
                st.error("❌ Mật khẩu không chính xác!")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP)
# ==========================================
logo_sidebar = get_logo_base64()
if logo_sidebar: st.sidebar.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_sidebar}" width="110"></div>', unsafe_allow_html=True)
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True): st.session_state["role"] = None; st.rerun()

menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu", "⚙️ Quản trị: Tạo Cuộc họp", "📤 Quản trị: Đăng Tài liệu"]) if st.session_state["role"] == "Admin" else st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu"])

hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY (E-CABINET)")

# ---------------------------------------------------------
# MODULE 1: PHÒNG HỌP & TÀI LIỆU
# ---------------------------------------------------------
if menu == "📚 Phòng họp & Tài liệu":
    if df_cuoc_hop.empty:
        st.info("Hiện chưa có cuộc họp nào.")
    else:
        # Xử lý tự động chọn cuộc họp mới nhất hoặc do người dùng chọn
        ds_lua_chon = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
        danh_sach = ds_lua_chon.tolist()
        
        index_default = len(danh_sach) - 1 # Mặc định chọn cái cuối cùng (mới nhất)
        if st.session_state.get("selected_meeting_id"):
            for i, val in enumerate(danh_sach):
                if val.startswith(st.session_state["selected_meeting_id"]):
                    index_default = i
                    break
                    
        chon_hop = st.selectbox("📂 Lựa chọn Cuộc họp / Hội nghị để xem tài liệu:", danh_sach, index=index_default)
        
        if chon_hop:
            ma_ch = chon_hop.split(" - ")[0]
            st.session_state["selected_meeting_id"] = ma_ch # Lưu lại lựa chọn
            thong_tin = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch].iloc[0]
            
            st.markdown(f"<h3 style='color: #2c3e50;'>📋 {thong_tin['Tên cuộc họp']}</h3>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.write(f"**⏰ Thời gian:** {thong_tin['Thời gian']}")
            c2.write(f"**📍 Địa điểm:** {thong_tin['Địa điểm']}")
            c3.write(f"**🟢 Trạng thái:** {thong_tin['Trạng thái']}")
            st.write("---")
            
            col_doc, col_feedback = st.columns([5, 5])
            with col_doc:
                st.markdown('<div class="section-title">📑 TÀI LIỆU KỲ HỌP</div>', unsafe_allow_html=True)
                tl_cua_hop = df_tai_lieu[df_tai_lieu['Mã cuộc họp'] == ma_ch] if not df_tai_lieu.empty else pd.DataFrame()
                if tl_cua_hop.empty: st.write("Chưa có tài liệu.")
                else:
                    for idx, row in tl_cua_hop.iterrows():
                        st.markdown(f'<div class="doc-card"><div class="doc-title">📄 {row.get("Tên tài liệu")}</div><div style="margin-top: 8px;"><a href="{row.get("Link Google Drive")}" target="_blank" style="text-decoration: none; color: #17a2b8; font-weight: bold;">📥 Xem tài liệu</a></div></div>', unsafe_allow_html=True)

            with col_feedback:
                st.markdown('<div class="section-title">✍️ XIN Ý KIẾN / THAM LUẬN</div>', unsafe_allow_html=True)
                tab_gui, tab_xem = st.tabs(["💬 Gửi Ý kiến", "📂 Ý kiến đã thu nhận"])
                with tab_gui:
                    with st.form("form_gop_y", clear_on_submit=True):
                        ho_ten = st.text_input("👤 Họ và tên:")
                        c_v = st.selectbox("💼 Chức vụ:", DS_CHUC_VU)
                        d_v = st.selectbox("🏢 Đơn vị:", DS_DON_VI)
                        noi_dung = st.text_area("📝 Ý kiến đóng góp:")
                        file_up = st.file_uploader("📎 Đính kèm file (Nếu có):", type=["docx", "pdf"])
                        if st.form_submit_button("🚀 GỬI Ý KIẾN", use_container_width=True):
                            if not ho_ten or c_v == "Chọn chức vụ..." or d_v == "Chọn đơn vị...": st.error("⚠️ Điền đủ thông tin!")
                            else:
                                with st.spinner("Đang gửi..."):
                                    f_b64 = base64.b64encode(file_up.getvalue()).decode('utf-8') if file_up else ""
                                    payload = {"action": "add_y_kien", "ma_ch": ma_ch, "nguoi_gop_y": f"{ho_ten} ({c_v} - {d_v})", "noi_dung": noi_dung, "file_base64": f_b64, "file_name": file_up.name if file_up else "", "file_mimeType": file_up.type if file_up else ""}
                                    if requests.post(WEB_APP_URL, json=payload).status_code == 200: st.success("✅ Thành công!"); st.cache_data.clear()
                with tab_xem:
                    yk_cua_hop = df_y_kien[df_y_kien['Mã cuộc họp'] == ma_ch] if not df_y_kien.empty else pd.DataFrame()
                    if yk_cua_hop.empty: st.info("Chưa có ý kiến.")
                    else:
                        for _, row in yk_cua_hop.iterrows():
                            with st.expander(f"💬 {row.get('Tên đơn vị / Đại biểu')} - {row.get('Thời gian gửi')}"):
                                st.write(row.get('Nội dung góp ý'))
                                if str(row.get('Link File sửa đổi')) != "nan": st.markdown(f"[📥 Xem file đính kèm]({row.get('Link File sửa đổi')})")

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
# MODULE 3: QUẢN TRỊ ĐĂNG TÀI LIỆU
# ---------------------------------------------------------
elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-title">📤 UPLOAD TÀI LIỆU LÊN HỆ THỐNG</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty:
        st.warning("⚠️ Bạn cần tạo Cuộc họp trước khi đăng tài liệu.")
    else:
        with st.form("form_tai_lieu", clear_on_submit=True):
            ds_cuoc_hop_hien_thi = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
            ch_chon = st.selectbox("📌 Gắn vào Cuộc họp:", ds_cuoc_hop_hien_thi.tolist())
            st.info("💡 **Mẹo:** Kéo thả hoặc chọn **nhiều file cùng lúc**. Hệ thống tự động dùng Tên file làm Tên tài liệu.")
            uploaded_files = st.file_uploader("📂 Chọn các File để đưa lên thư viện:", type=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"], accept_multiple_files=True)
            
            if st.form_submit_button("🚀 TẢI LÊN VÀ PHÁT HÀNH TÀI LIỆU"):
                if not uploaded_files: st.error("⚠️ Vui lòng chọn ít nhất 1 file để tải lên!")
                else:
                    ma_ch = ch_chon.split(" - ")[0]
                    thanh_cong = 0
                    progress_bar = st.progress(0, text="Bắt đầu tải file...")
                    for i, file_up in enumerate(uploaded_files):
                        payload = {"action": "add_tai_lieu", "ma_ch": ma_ch, "ma_tl": f"TL{datetime.now().strftime('%H%M%S')}{i}", "ten_tl": file_up.name, "loai_tl": "", "file_base64": base64.b64encode(file_up.getvalue()).decode('utf-8'), "file_name": file_up.name, "file_mimeType": file_up.type}
                        try:
                            if requests.post(WEB_APP_URL, json=payload).status_code == 200: thanh_cong += 1
                        except: pass
                        progress_bar.progress(int(((i + 1) / len(uploaded_files)) * 100), text=f"Đang xử lý: {i+1}/{len(uploaded_files)} file...")
                    st.success(f"✅ Tải lên hoàn tất ({thanh_cong}/{len(uploaded_files)} file)!"); st.cache_data.clear()
