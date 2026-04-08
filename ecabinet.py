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
    
    /* Thẻ cuộc họp nổi bật */
    .featured-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0faff 100%);
        border: 2px solid #17a2b8;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(23, 162, 184, 0.2);
    }
    .featured-tag {
        background-color: #C8102E; color: white; padding: 3px 10px; 
        border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase;
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

# ==========================================
# ĐĂNG NHẬP
# ==========================================
if st.session_state["role"] is None:
    hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY (E-CABINET)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True): st.session_state["role"] = None; st.rerun()

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
    if df_cuoc_hop.empty:
        st.info("Hiện chưa có cuộc họp nào.")
    else:
        # 🌟 PHẦN NỔI BẬT: CUỘC HỌP MỚI NHẤT
        latest_ch = df_cuoc_hop.iloc[-1]
        
        st.markdown(f"""
        <div class="featured-card">
            <span class="featured-tag">Mới nhất / Đang diễn ra</span>
            <h2 style="color: #004B87; margin-top: 10px;">{latest_ch['Tên cuộc họp']}</h2>
            <p style="margin: 0;">📍 <b>Địa điểm:</b> {latest_ch['Địa điểm']} | ⏰ <b>Thời gian:</b> {latest_ch['Thời gian']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2, _ = st.columns([2, 2, 4])
        if col_btn1.button("🔥 VÀO HỌP NGAY", use_container_width=True):
            st.session_state["selected_meeting_id"] = latest_ch['Mã cuộc họp']
        
        st.write("---")
        
        # Danh sách chọn cuộc họp khác (Dành cho việc tra cứu tài liệu cũ)
        ds_lua_chon = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
        # Tự động chọn cuộc họp nếu đã bấm nút "Vào họp ngay"
        index_default = 0
        if st.session_state["selected_meeting_id"]:
            try:
                index_default = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == st.session_state["selected_meeting_id"]].index[0]
            except: pass
            
        chon_hop = st.selectbox("📂 Hoặc chọn cuộc họp khác để tra cứu tài liệu:", ds_lua_chon.tolist(), index=int(index_default))
        
        if chon_hop:
            ma_ch = chon_hop.split(" - ")[0]
            st.session_state["selected_meeting_id"] = ma_ch
            thong_tin = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch].iloc[0]
            
            st.markdown(f"<h3 style='color: #2c3e50;'>📋 {thong_tin['Tên cuộc họp']}</h3>", unsafe_allow_html=True)
            
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
# MODULE 2 & 3: GIỮ NGUYÊN NHƯ BẢN TRƯỚC
# ---------------------------------------------------------
elif menu == "⚙️ Quản trị: Tạo Cuộc họp":
    st.markdown('<div class="section-title">➕ TẠO CUỘC HỌP MỚI</div>', unsafe_allow_html=True)
    with st.form("form_tao_hop"):
        c1, c2 = st.columns([1, 3])
        m_ch = c1.text_input("Mã CH (VD: CH01):")
        t_ch = c2.text_input("Tên Cuộc họp:")
        c3, c4, c5 = st.columns(3)
        t_g = c3.text_input("Thời gian:")
        d_d = c4.text_input("Địa điểm:")
        t_t = c5.selectbox("Trạng thái:", ["Sắp diễn ra", "Đang diễn ra", "Đã kết thúc"])
        if st.form_submit_button("LƯU CUỘC HỌP"):
            res = requests.post(WEB_APP_URL, json={"action": "add_cuoc_hop", "ma_ch": m_ch, "ten_ch": t_ch, "thoi_gian": t_g, "dia_diem": d_d, "trang_thai": t_t})
            if res.status_code == 200: st.success("✅ Xong!"); st.cache_data.clear()

elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-title">📤 UPLOAD TÀI LIỆU NHIỀU FILE</div>', unsafe_allow_html=True)
    if not df_cuoc_hop.empty:
        with st.form("form_up_nhieu"):
            ch_chon = st.selectbox("Chọn cuộc họp:", (df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']).tolist())
            files = st.file_uploader("Chọn nhiều file cùng lúc:", accept_multiple_files=True)
            if st.form_submit_button("🚀 TẢI LÊN TẤT CẢ"):
                for f in files:
                    payload = {"action": "add_tai_lieu", "ma_ch": ch_chon.split(" - ")[0], "ma_tl": f"TL{datetime.now().strftime('%S%f')}", "ten_tl": f.name, "loai_tl": "", "file_base64": base64.b64encode(f.getvalue()).decode('utf-8'), "file_name": f.name, "file_mimeType": f.type}
                    requests.post(WEB_APP_URL, json=payload)
                st.success("✅ Đã tải lên xong!"); st.cache_data.clear()
