import streamlit as st
import requests
import base64
import pandas as pd
import re
from datetime import datetime, timedelta

st.set_page_config(page_title="E-Cabinet TGDV - Tuyên Quang", page_icon="🏛️", layout="wide")

# ---> LINK ỐNG NƯỚC <---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycby8XxSlcqExB6rW_Ymn3AGxkBcWQWqjJJbHM56Dd8oJfqfovogDVk_KqgnNDMbmmQo0/exec"

# --- MẬT KHẨU ---
PASS_ADMIN = "Admin@2026"
PASS_DAI_BIEU = "HopBan@2026"

# --- CSS NÂNG CẤP GIAO DIỆN & FIX LỖI NÚT DỌC ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    
    /* Header chính */
    .header-box {
        background-color: #ffffff; border-top: 4px solid #17a2b8; border-radius: 8px;
        padding: 15px 30px; margin-bottom: 30px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;
    }
    .main-title { font-size: 24px; font-weight: 900; color: #2c3e50; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    
    /* Thẻ cuộc họp nổi bật */
    .featured-card {
        background-color: #ffffff; border: 1px solid #e0e6ed; border-top: 4px solid #17a2b8;
        border-radius: 8px; padding: 20px 20px 50px 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.03); height: 100%;
        display: flex; flex-direction: column; transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .featured-card:hover { transform: translateY(-2px); box-shadow: 0px 6px 15px rgba(0,0,0,0.08); }
    .featured-title { color: #2c3e50; font-size: 16px; font-weight: bold; margin: 12px 0; line-height: 1.4; flex-grow: 1; text-align: left; }
    .featured-details { color: #6c757d; font-size: 13px; border-top: 1px dashed #dee2e6; padding-top: 12px; text-align: left; line-height: 1.6; }
    
    /* Mác Trạng thái */
    .tag-sap-dien-ra { background-color: #17a2b8; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block;}
    .tag-dang-dien-ra { background-color: #C8102E; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block; animation: blinker 1.5s linear infinite;}
    .tag-da-ket-thuc { background-color: #6c757d; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block;}
    @keyframes blinker { 50% { opacity: 0.6; } }
    
    /* Tùy chỉnh Form nói chung */
    div[data-testid="stForm"] {
        background-color: #ffffff; border: 1px solid #e0e6ed; border-radius: 8px;
        padding: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.03);
    }
    
    /* STYLE CHO CÁC NÚT BẤM CƠ BẢN TÀN HỆ THỐNG */
    div.stButton > button[kind="primary"], div.stButton > button[kind="formSubmit"] {
        background-color: #17a2b8; color: white; border: none; border-radius: 6px; font-weight: bold;
    }
    div.stButton > button[kind="primary"]:hover, div.stButton > button[kind="formSubmit"]:hover {
        background-color: #138496; color: white;
    }
    
    /* THỦ THUẬT ÉP NÚT THAM GIA (ĐÃ FIX LỖI RỚT CHỮ) */
    div.stButton { position: relative; }
    div.stButton > button[kind="secondary"] {
        position: absolute !important; right: 15px !important; top: -55px !important; 
        background-color: #ffffff !important; color: #17a2b8 !important; border: 2px solid #17a2b8 !important;
        border-radius: 20px !important; padding: 4px 20px !important; font-size: 14px !important; font-weight: bold !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1) !important; transition: all 0.3s ease !important; z-index: 10 !important;
        white-space: nowrap !important; /* Chống rớt chữ dọc */
        min-width: 130px !important; /* Ép cứng chiều rộng tối thiểu */
        width: auto !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #17a2b8 !important; color: #ffffff !important;
    }
    
    .section-title { color: #2c3e50; border-bottom: 2px solid #17a2b8; padding-bottom: 5px; margin-top: 20px; font-size: 16px; text-transform: uppercase; font-weight: bold;}
    .doc-card { background-color: #ffffff; border-left: 4px solid #17a2b8; padding: 15px; border-radius: 6px; margin-bottom: 12px; border: 1px solid #e0e6ed; box-shadow: 0px 2px 5px rgba(0,0,0,0.02);}
</style>
""", unsafe_allow_html=True)

DS_CHUC_VU = ["Chọn chức vụ...", "Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", "Trưởng phòng", "Phó Trưởng phòng", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Chuyên viên", "Khác"]
DS_DON_VI = ["Chọn đơn vị...", "Ban Tuyên giáo và Dân vận Tỉnh ủy (Lãnh đạo Ban)", "Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", "Phòng Đoàn thể và các Hội"]

def get_logo_base64():
    try:
        with open("Logo TGDV.png", "rb") as f: return base64.b64encode(f.read()).decode("utf-8")
    except: return ""

def hien_thi_tieu_de(tieu_de_chinh):
    logo_data = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height: 65px;">' if logo_data else ""
    st.markdown(f'<div class="header-box"><div>{logo_html}</div><div><div class="main-title">{tieu_de_chinh}</div><div style="font-size: 13px; font-weight: bold; color: #6c757d; text-align: center; margin-top:3px;">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div></div>', unsafe_allow_html=True)

@st.cache_data(ttl=30)
def load_data():
    try: return requests.get(WEB_APP_URL).json()
    except: return {"cuoc_hop": [], "tai_lieu": [], "y_kien": []}

def parse_meeting_time(t_str):
    try: return datetime.strptime(t_str.strip(), "%H:%M, %d/%m/%Y")
    except: return None

def get_realtime_status(t_str):
    meeting_time = parse_meeting_time(t_str)
    if not meeting_time: return "KHÔNG XÁC ĐỊNH", "tag-da-ket-thuc"
    now = datetime.now()
    end_time = meeting_time + timedelta(hours=4)
    if now < meeting_time: return "Sắp diễn ra", "tag-sap-dien-ra"
    elif meeting_time <= now <= end_time: return "Đang diễn ra", "tag-dang-dien-ra"
    else: return "Đã kết thúc", "tag-da-ket-thuc"

if "role" not in st.session_state: st.session_state["role"] = None
if "selected_meeting_id" not in st.session_state: st.session_state["selected_meeting_id"] = None

data = load_data()
df_cuoc_hop = pd.DataFrame(data.get("cuoc_hop", []))
df_tai_lieu = pd.DataFrame(data.get("tai_lieu", []))
df_y_kien = pd.DataFrame(data.get("y_kien", []))

if not df_cuoc_hop.empty:
    df_cuoc_hop['ParsedDate'] = df_cuoc_hop['Thời gian'].apply(parse_meeting_time)
    df_cuoc_hop[['RealtimeStatus', 'TagClass']] = df_cuoc_hop['Thời gian'].apply(lambda x: pd.Series(get_realtime_status(x)))

# ==========================================
# MÀN HÌNH ĐĂNG NHẬP
# ==========================================
if st.session_state["role"] is None:
    hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY")
    
    if not df_cuoc_hop.empty:
        active_meetings = df_cuoc_hop[df_cuoc_hop['RealtimeStatus'].isin(["Sắp diễn ra", "Đang diễn ra"])]
        if active_meetings.empty: featured_df = df_cuoc_hop.sort_values(by='ParsedDate', ascending=False).head(3)
        else: featured_df = active_meetings.sort_values(by='ParsedDate', ascending=True).head(3)
            
        st.markdown('<div style="text-align:center; font-size: 16px; font-weight: bold; color: #6c757d; margin-bottom: 15px; text-transform: uppercase;">📌 Các hội nghị nổi bật</div>', unsafe_allow_html=True)
        
        n = len(featured_df)
        if n == 1: cols = st.columns([1, 2, 1]); target_cols = [cols[1]]
        elif n == 2: cols = st.columns([1, 4, 4, 1]); target_cols = [cols[1], cols[2]]
        else: cols = st.columns(3); target_cols = cols

        for i, (idx, row) in enumerate(featured_df.iterrows()):
            with target_cols[i]:
                # Vẽ thẻ Giao diện
                st.markdown(f"""
                <div class="featured-card">
                    <div style="text-align: left;"><span class="{row['TagClass']}">{row['RealtimeStatus']}</span></div>
                    <div class="featured-title">{row['Tên cuộc họp']}</div>
                    <div class="featured-details">
                        <b>📍 Địa điểm:</b> {row['Địa điểm']}<br>
                        <b>⏰ Thời gian:</b> {row['Thời gian']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Nút bấm đã được khóa CSS chống rớt chữ
                if st.button("🚀 Tham gia", key=f"btn_{row['Mã cuộc họp']}", type="secondary"):
                    st.session_state["selected_meeting_id"] = row['Mã cuộc họp']
                    st.rerun()
    
    st.write("---")
    
    col_login1, col_login2, col_login3 = st.columns([1.5, 2.5, 1.5])
    with col_login2:
        # Đã Fix lỗi hiển thị tên "None"
        if st.session_state.get("selected_meeting_id"):
            ten_ch_dang_chon = ""
            if not df_cuoc_hop.empty:
                match_ch = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == st.session_state['selected_meeting_id']]
                if not match_ch.empty:
                    ten_ch_dang_chon = match_ch.iloc[0]['Tên cuộc họp']
            if ten_ch_dang_chon:
                st.success(f"✅ Bạn đang chọn: **{ten_ch_dang_chon}**. Vui lòng nhập mật khẩu để vào phòng họp!")
            
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span style="font-size: 28px;">🔐</span><br><b style="color: #2c3e50; font-size: 16px;">XÁC THỰC QUYỀN TRUY CẬP</b></div>', unsafe_allow_html=True)
            pwd = st.text_input("Nhập mật khẩu", type="password", placeholder="Nhập mật khẩu tại đây...", label_visibility="collapsed")
            
            if st.form_submit_button("🚀 VÀO HỆ THỐNG", use_container_width=True):
                if pwd == PASS_ADMIN: 
                    st.session_state["role"] = "Admin"
                    if not df_cuoc_hop.empty and not st.session_state.get("selected_meeting_id"): 
                        st.session_state["selected_meeting_id"] = featured_df.iloc[0]['Mã cuộc họp']
                    st.rerun()
                elif pwd == PASS_DAI_BIEU: 
                    st.session_state["role"] = "DaiBieu"
                    if not df_cuoc_hop.empty and not st.session_state.get("selected_meeting_id"): 
                        st.session_state["selected_meeting_id"] = featured_df.iloc[0]['Mã cuộc họp']
                    st.rerun()
                else: st.error("❌ Mật khẩu không chính xác!")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP)
# ==========================================
logo_sidebar = get_logo_base64()
if logo_sidebar: st.sidebar.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_sidebar}" width="100"></div>', unsafe_allow_html=True)
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True, type="primary"): st.session_state["role"] = None; st.session_state["selected_meeting_id"] = None; st.rerun()

menu = st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu", "⚙️ Quản trị: Tạo Cuộc họp", "📤 Quản trị: Đăng Tài liệu"]) if st.session_state["role"] == "Admin" else st.sidebar.radio("📌 CHỨC NĂNG:", ["📚 Phòng họp & Tài liệu"])

hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY")

if menu == "📚 Phòng họp & Tài liệu":
    if df_cuoc_hop.empty: st.info("Hiện chưa có cuộc họp nào.")
    else:
        ds_lua_chon = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
        danh_sach = ds_lua_chon.tolist()
        
        index_default = len(danh_sach) - 1
        if st.session_state.get("selected_meeting_id"):
            for i, val in enumerate(danh_sach):
                if val.startswith(st.session_state["selected_meeting_id"]):
                    index_default = i; break
                    
        chon_hop = st.selectbox("📂 Lựa chọn Hội nghị để xem tài liệu:", danh_sach, index=index_default)
        
        if chon_hop:
            ma_ch = chon_hop.split(" - ")[0]
            st.session_state["selected_meeting_id"] = ma_ch
            thong_tin = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch].iloc[0]
            
            st.markdown(f"<h3 style='color: #2c3e50; font-size: 20px;'>📋 {thong_tin['Tên cuộc họp']}</h3>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.write(f"**⏰ Thời gian:** {thong_tin['Thời gian']}")
            c2.write(f"**📍 Địa điểm:** {thong_tin['Địa điểm']}")
            c3.markdown(f"**🟢 Trạng thái:** <span class='{thong_tin['TagClass']}' style='padding: 2px 8px;'>{thong_tin['RealtimeStatus']}</span>", unsafe_allow_html=True)
            st.write("---")
            
            col_doc, col_feedback = st.columns([5, 5], gap="large")
            with col_doc:
                st.markdown('<div class="section-title">📑 TÀI LIỆU KỲ HỌP</div>', unsafe_allow_html=True)
                tl_cua_hop = df_tai_lieu[df_tai_lieu['Mã cuộc họp'] == ma_ch] if not df_tai_lieu.empty else pd.DataFrame()
                if tl_cua_hop.empty: st.write("Chưa có tài liệu.")
                else:
                    for idx, row in tl_cua_hop.iterrows():
                        st.markdown(f'<div class="doc-card"><div class="doc-title" style="color: #2c3e50;">📄 {row.get("Tên tài liệu")}</div><div style="margin-top: 8px;"><a href="{row.get("Link Google Drive")}" target="_blank" style="text-decoration: none; color: #17a2b8; font-weight: bold; font-size: 13px;">📥 XEM / TẢI VỀ</a></div></div>', unsafe_allow_html=True)

            with col_feedback:
                st.markdown('<div class="section-title">✍️ XIN Ý KIẾN / THAM LUẬN</div>', unsafe_allow_html=True)
                tab_gui, tab_xem = st.tabs(["💬 Gửi Ý kiến", "📂 Ý kiến đã thu nhận"])
                with tab_gui:
                    with st.form("form_gop_y", clear_on_submit=True):
                        ho_ten = st.text_input("👤 Họ và tên:")
                        c_v = st.selectbox("💼 Chức vụ:", DS_CHUC_VU)
                        d_v = st.selectbox("🏢 Đơn vị:", DS_DON_VI)
                        noi_dung = st.text_area("📝 Ý kiến đóng góp:")
                        file_up = st.file_uploader("📎 Đính kèm file văn bản đã sửa (Nếu có):", type=["docx", "pdf"])
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

elif menu == "⚙️ Quản trị: Tạo Cuộc họp":
    st.markdown('<div class="section-title">➕ TẠO CUỘC HỌP MỚI</div>', unsafe_allow_html=True)
    st.info("💡 Hệ thống tính toán trạng thái họp tự động. Bạn BẮT BUỘC phải nhập Thời gian đúng chuẩn định dạng bên dưới.")
    
    with st.form("form_tao_hop", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1: ma_ch = st.text_input("Mã Cuộc họp (VD: CH01)*:")
        with col2: ten_ch = st.text_input("Tên Cuộc họp / Hội nghị*:")
        col3, col4 = st.columns(2)
        with col3: thoi_gian = st.text_input("Thời gian (BẮT BUỘC NHẬP DẠNG: HH:MM, DD/MM/YYYY)*", placeholder="Ví dụ: 08:30, 20/05/2026")
        with col4: dia_diem = st.text_input("Địa điểm:")
        
        if st.form_submit_button("LƯU CUỘC HỌP MỚI"):
            pattern = r"^\d{2}:\d{2}, \d{2}/\d{2}/\d{4}$"
            if not ma_ch or not ten_ch: st.error("⚠️ Vui lòng nhập Mã và Tên cuộc họp!")
            elif not re.match(pattern, thoi_gian.strip()): st.error("⚠️ Thời gian sai định dạng! Vui lòng nhập đúng như mẫu: 08:30, 20/05/2026")
            else:
                with st.spinner("Đang lưu..."):
                    payload = {"action": "add_cuoc_hop", "ma_ch": ma_ch, "ten_ch": ten_ch, "thoi_gian": thoi_gian, "dia_diem": dia_diem, "trang_thai": "Tự động (Real-time)"}
                    if requests.post(WEB_APP_URL, json=payload).status_code == 200: st.success("✅ Đã tạo cuộc họp thành công!"); st.cache_data.clear()
                    else: st.error("Lỗi mạng.")

elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-title">📤 UPLOAD TÀI LIỆU LÊN HỆ THỐNG</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty: st.warning("⚠️ Bạn cần tạo Cuộc họp trước khi đăng tài liệu.")
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
