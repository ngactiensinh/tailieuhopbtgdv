import streamlit as st
import pandas as pd
import re
import base64
import uuid
from datetime import datetime, timedelta
from supabase import create_client, Client
import urllib.parse

st.set_page_config(page_title="E-Cabinet TGDV - Tuyên Quang", page_icon="🏛️", layout="wide")

# ==========================================
# CẤU HÌNH SUPABASE
# ==========================================
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    pass

# --- MẬT KHẨU ---
PASS_ADMIN = "Admin@2026"
PASS_DAI_BIEU = "HopBan@2026"

# --- CSS GIAO DIỆN CÓ BACKGROUND VI MẠCH ---
st.markdown("""
<style>
    /* Hình nền vi mạch điện tử mờ 5% */
    .stApp { 
        background-color: #f4f6f9; 
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cpath d='M20 20 L40 20 L50 30 L50 50 M80 20 L60 20 L50 30 L50 50 M50 50 L50 70 L70 90 L90 90 M50 70 L30 90 L10 90' stroke='%2317a2b8' stroke-width='2' fill='none' opacity='0.05'/%3E%3Ccircle cx='20' cy='20' r='3' fill='%2317a2b8' opacity='0.05'/%3E%3Ccircle cx='80' cy='20' r='3' fill='%2317a2b8' opacity='0.05'/%3E%3Ccircle cx='10' cy='90' r='3' fill='%2317a2b8' opacity='0.05'/%3E%3Ccircle cx='90' cy='90' r='3' fill='%2317a2b8' opacity='0.05'/%3E%3Ccircle cx='50' cy='50' r='5' fill='%2317a2b8' opacity='0.08'/%3E%3C/svg%3E");
        background-repeat: repeat;
    }
    
    .header-box { background-color: #ffffff; border-top: 4px solid #17a2b8; border-radius: 8px; padding: 15px 30px; margin-bottom: 30px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;}
    .main-title { font-size: 24px; font-weight: 900; color: #2c3e50; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    
    /* Làm nền của các Form trắng tinh để nổi bật trên nền vi mạch */
    .featured-card { background-color: rgba(255, 255, 255, 0.95); border: 1px solid #e0e6ed; border-top: 4px solid #17a2b8; border-radius: 8px; padding: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.03); display: flex; flex-direction: column; transition: transform 0.2s ease, box-shadow 0.2s ease; margin-bottom: 8px;}
    .featured-card:hover { transform: translateY(-2px); box-shadow: 0px 6px 15px rgba(0,0,0,0.08); }
    .featured-title { color: #2c3e50; font-size: 16px; font-weight: bold; margin: 12px 0; line-height: 1.4; flex-grow: 1; text-align: left; }
    .featured-details { color: #6c757d; font-size: 13px; border-top: 1px dashed #dee2e6; padding-top: 12px; text-align: left; line-height: 1.6; }
    
    .tag-sap-dien-ra { background-color: #17a2b8; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block;}
    .tag-dang-dien-ra { background-color: #C8102E; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block; animation: blinker 1.5s linear infinite;}
    .tag-da-ket-thuc { background-color: #6c757d; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block;}
    @keyframes blinker { 50% { opacity: 0.6; } }
    
    div[data-testid="stForm"] { background-color: rgba(255, 255, 255, 0.95); border: 1px solid #e0e6ed; border-radius: 8px; padding: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.03);}
    div.stButton > button[kind="primary"], div.stButton > button[kind="formSubmit"] { background-color: #17a2b8; color: white; border: none; border-radius: 6px; font-weight: bold;}
    div.stButton > button[kind="secondary"] { background-color: #ffffff !important; color: #17a2b8 !important; border: 2px solid #17a2b8 !important; border-radius: 8px !important; padding: 8px 15px !important; font-size: 14px !important; font-weight: bold !important;}
    .section-title { color: #2c3e50; border-bottom: 2px solid #17a2b8; padding-bottom: 5px; margin-top: 20px; font-size: 16px; text-transform: uppercase; font-weight: bold;}
    .doc-card { background-color: rgba(255, 255, 255, 0.95); border-left: 4px solid #17a2b8; padding: 15px; border-radius: 6px; margin-bottom: 12px; border: 1px solid #e0e6ed; box-shadow: 0px 2px 5px rgba(0,0,0,0.02);}
</style>
""", unsafe_allow_html=True)

DS_CHUC_VU = ["Chọn chức vụ...", "Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", "Trưởng phòng", "Phó Trưởng phòng", "Chánh Văn phòng", "Phó Chánh Văn phòng", "Chuyên viên", "Khác"]
DS_DON_VI = ["Chọn đơn vị...", "Ban Tuyên giáo và Dân vận Tỉnh ủy (Lãnh đạo Ban)", "Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước, dân tộc và tôn giáo", "Phòng Đoàn thể và các Hội"]

def get_vn_now(): return datetime.utcnow() + timedelta(hours=7)

def get_logo_base64():
    try:
        with open("Logo TGDV.png", "rb") as f: return base64.b64encode(f.read()).decode("utf-8")
    except: return ""

def hien_thi_tieu_de(tieu_de_chinh):
    logo_data = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_data}" style="height: 65px; object-fit: contain;">' if logo_data else ""
    st.markdown(f'<div class="header-box"><div>{logo_html}</div><div><div class="main-title">{tieu_de_chinh}</div><div style="font-size: 13px; font-weight: bold; color: #6c757d; text-align: center; margin-top:3px;">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div></div>', unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        ch = supabase.table("cuoc_hop").select("*").order("id", desc=True).execute().data
        tl = supabase.table("tai_lieu").select("*").execute().data
        yk = supabase.table("y_kien").select("*").order("id", desc=True).execute().data
        
        df_ch = pd.DataFrame(ch).rename(columns={'ma_ch': 'Mã cuộc họp', 'ten_ch': 'Tên cuộc họp', 'thoi_gian': 'Thời gian', 'thoi_gian_ket_thuc': 'Thời gian kết thúc', 'dia_diem': 'Địa điểm'})
        df_tl = pd.DataFrame(tl).rename(columns={'ma_ch': 'Mã cuộc họp', 'ma_tl': 'Mã tài liệu', 'ten_tl': 'Tên tài liệu', 'link_file': 'Link Google Drive'})
        df_yk = pd.DataFrame(yk).rename(columns={'ma_ch': 'Mã cuộc họp', 'nguoi_gop_y': 'Tên đơn vị / Đại biểu', 'noi_dung': 'Nội dung góp ý', 'link_file': 'Link File sửa đổi', 'created_at': 'Thời gian gửi'})
        
        if not df_yk.empty: df_yk['Thời gian gửi'] = pd.to_datetime(df_yk['Thời gian gửi']).dt.tz_convert('Asia/Ho_Chi_Minh').dt.strftime("%H:%M %d/%m/%Y")
        return {"cuoc_hop": df_ch, "tai_lieu": df_tl, "y_kien": df_yk}
    except: return {"cuoc_hop": pd.DataFrame(), "tai_lieu": pd.DataFrame(), "y_kien": pd.DataFrame()}

def parse_meeting_time(t_str):
    try: return datetime.strptime(t_str.strip(), "%H:%M, %d/%m/%Y")
    except: return None

def get_realtime_status(start_str, end_str):
    start_time = parse_meeting_time(start_str)
    end_time = parse_meeting_time(end_str)
    now = get_vn_now()
    
    if not start_time: return "KHÔNG XÁC ĐỊNH", "tag-da-ket-thuc"
    if not end_time: end_time = start_time + timedelta(hours=4)
    
    if now < start_time: return "Sắp diễn ra", "tag-sap-dien-ra"
    elif start_time <= now <= end_time: return "Đang diễn ra", "tag-dang-dien-ra"
    else: return "Đã kết thúc", "tag-da-ket-thuc"

if "role" not in st.session_state: st.session_state["role"] = None
if "selected_meeting_id" not in st.session_state: st.session_state["selected_meeting_id"] = None

data_dict = load_data()
df_cuoc_hop = data_dict.get("cuoc_hop", pd.DataFrame())
df_tai_lieu = data_dict.get("tai_lieu", pd.DataFrame())
df_y_kien = data_dict.get("y_kien", pd.DataFrame())

if not df_cuoc_hop.empty:
    df_cuoc_hop['ParsedStart'] = df_cuoc_hop['Thời gian'].apply(parse_meeting_time)
    df_cuoc_hop[['RealtimeStatus', 'TagClass']] = df_cuoc_hop.apply(lambda r: pd.Series(get_realtime_status(r['Thời gian'], r.get('Thời gian kết thúc'))), axis=1)

# ==========================================
# MÀN HÌNH ĐĂNG NHẬP
# ==========================================
if st.session_state["role"] is None:
    hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY")
    if not df_cuoc_hop.empty:
        active_meetings = df_cuoc_hop[df_cuoc_hop['RealtimeStatus'].isin(["Sắp diễn ra", "Đang diễn ra"])]
        featured_df = active_meetings.sort_values(by='ParsedStart', ascending=True).head(3) if not active_meetings.empty else df_cuoc_hop.head(3)
        st.markdown('<div style="text-align:center; font-size: 16px; font-weight: bold; color: #6c757d; margin-bottom: 15px; text-transform: uppercase;">📌 Các hội nghị nổi bật</div>', unsafe_allow_html=True)
        n = len(featured_df)
        cols = st.columns([1, 2, 1]) if n == 1 else (st.columns([1, 4, 4, 1]) if n == 2 else st.columns(3))
        target_cols = [cols[1]] if n == 1 else ([cols[1], cols[2]] if n == 2 else cols)
        for i, (idx, row) in enumerate(featured_df.iterrows()):
            with target_cols[i]:
                st.markdown(f'<div class="featured-card"><div style="text-align: left;"><span class="{row["TagClass"]}">{row["RealtimeStatus"]}</span></div><div class="featured-title">{row["Tên cuộc họp"]}</div><div class="featured-details"><b>📍 Địa điểm:</b> {row["Địa điểm"]}<br><b>⏰ Bắt đầu:</b> {row["Thời gian"]}<br><b>🏁 Kết thúc:</b> {row.get("Thời gian kết thúc", "Chưa xác định")}</div></div>', unsafe_allow_html=True)
                if st.button("🚀 VÀO PHÒNG HỌP NÀY", key=f"btn_{row['Mã cuộc họp']}", type="secondary", use_container_width=True):
                    st.session_state["selected_meeting_id"] = row['Mã cuộc họp']; st.rerun()
    st.write("---")
    col_login1, col_login2, col_login3 = st.columns([1.5, 2.5, 1.5])
    with col_login2:
        if st.session_state.get("selected_meeting_id"):
            match_ch = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == st.session_state['selected_meeting_id']]
            if not match_ch.empty: st.success(f"✅ Bạn đang chọn: **{match_ch.iloc[0]['Tên cuộc họp']}**")
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span style="font-size: 28px;">🔐</span><br><b style="color: #2c3e50; font-size: 16px;">XÁC THỰC QUYỀN TRUY CẬP</b></div>', unsafe_allow_html=True)
            pwd = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...", label_visibility="collapsed")
            if st.form_submit_button("🚀 ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
                if pwd == PASS_ADMIN: st.session_state["role"] = "Admin"; st.rerun()
                elif pwd == PASS_DAI_BIEU: st.session_state["role"] = "DaiBieu"; st.rerun()
                else: st.error("❌ Sai mật khẩu!")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
logo_sidebar = get_logo_base64()
if logo_sidebar: st.sidebar.markdown(f'<div style="text-align: center; margin-bottom: 20px;"><img src="data:image/png;base64,{logo_sidebar}" width="100" style="object-fit: contain;"></div>', unsafe_allow_html=True)
if st.sidebar.button("🔄 Làm mới dữ liệu", use_container_width=True): st.cache_data.clear(); st.rerun()
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True, type="primary"): st.session_state["role"] = None; st.session_state["selected_meeting_id"] = None; st.rerun()

menu_list = ["📚 Phòng họp & Tài liệu", "⚙️ Quản trị: Tạo mới", "📤 Quản trị: Đăng Tài liệu", "✏️ Quản trị: Chỉnh sửa / Xóa"] if st.session_state["role"] == "Admin" else ["📚 Phòng họp & Tài liệu"]
menu = st.sidebar.radio("📌 CHỨC NĂNG:", menu_list)

hien_thi_tieu_de("HỆ THỐNG PHÒNG HỌP KHÔNG GIẤY")

if menu == "📚 Phòng họp & Tài liệu":
    if df_cuoc_hop.empty: st.info("Chưa có cuộc họp.")
    else:
        ds_lua_chon = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
        idx_def = 0
        if st.session_state.get("selected_meeting_id"):
            for i, val in enumerate(ds_lua_chon):
                if val.startswith(st.session_state["selected_meeting_id"]): idx_def = i; break
        chon_hop = st.selectbox("📂 Lựa chọn Hội nghị:", ds_lua_chon, index=idx_def)
        
        if chon_hop:
            ma_ch = chon_hop.split(" - ")[0]; st.session_state["selected_meeting_id"] = ma_ch
            thong_tin = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch].iloc[0]
            
            st.markdown(f"<h3 style='color: #2c3e50; font-size: 20px; border-bottom: 2px solid #17a2b8; padding-bottom: 10px;'>📋 {thong_tin['Tên cuộc họp']}</h3>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f"**⏰ Bắt đầu:** {thong_tin['Thời gian']}")
            c2.write(f"**🏁 Kết thúc:** {thong_tin.get('Thời gian kết thúc', '---')}")
            c3.write(f"**📍 Địa điểm:** {thong_tin['Địa điểm']}")
            c4.markdown(f"**🟢 Trạng thái:** <span class='{thong_tin['TagClass']}' style='padding: 2px 8px;'>{thong_tin['RealtimeStatus']}</span>", unsafe_allow_html=True)
            
            st.write("---")

            col_doc, col_feedback = st.columns([5, 5], gap="large")
            with col_doc:
                st.markdown('<div class="section-title">📑 TÀI LIỆU KỲ HỌP</div>', unsafe_allow_html=True)
                tl_cua_hop = df_tai_lieu[df_tai_lieu['Mã cuộc họp'] == ma_ch] if not df_tai_lieu.empty else pd.DataFrame()
                if tl_cua_hop.empty: st.write("Chưa có tài liệu.")
                else:
                    for idx, row in tl_cua_hop.iterrows():
                        file_url = str(row.get("Link Google Drive", ""))
                        view_url = f"https://docs.google.com/viewer?url={urllib.parse.quote(file_url, safe='')}&embedded=true" if any(ext in file_url.lower() for ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']) else file_url
                        st.markdown(f'<div class="doc-card"><div class="doc-title" style="color: #2c3e50; font-size: 15px; margin-bottom: 12px;">📄 {row.get("Tên tài liệu")}</div><div style="display: flex; gap: 10px;"><a href="{view_url}" target="_blank" style="background: #e0f7fa; border: 1px solid #17a2b8; color: #17a2b8; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; text-decoration: none;">👁️ XEM TRỰC TIẾP</a><a href="{file_url}" target="_blank" style="background: #fff5f5; border: 1px solid #C8102E; color: #C8102E; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; text-decoration: none;">⬇️ TẢI VỀ</a></div></div>', unsafe_allow_html=True)
            with col_feedback:
                st.markdown('<div class="section-title">✍️ XIN Ý KIẾN / THAM LUẬN</div>', unsafe_allow_html=True)
                tab_gui, tab_xem = st.tabs(["💬 Gửi Ý kiến", "📂 Ý kiến đã thu nhận"])
                
                with tab_gui:
                    with st.form("form_gop_y", clear_on_submit=True):
                        h_t = st.text_input("👤 Họ và tên:"); c_v = st.selectbox("💼 Chức vụ:", DS_CHUC_VU); d_v = st.selectbox("🏢 Đơn vị:", DS_DON_VI); n_d = st.text_area("📝 Ý kiến đóng góp:"); f_u = st.file_uploader("📎 Đính kèm file văn bản đã sửa (Nếu có):", type=["docx", "pdf"])
                        if st.form_submit_button("🚀 GỬI Ý KIẾN"):
                            if not h_t or c_v=="Chọn chức vụ..." or d_v=="Chọn đơn vị...": st.error("⚠️ Điền đủ thông tin bắt buộc!")
                            else:
                                with st.spinner("Đang gửi..."):
                                    p_u = ""
                                    if f_u:
                                        s_n = f"YKien_{ma_ch}_{get_vn_now().strftime('%H%M%S')}_{uuid.uuid4().hex[:4]}.{f_u.name.split('.')[-1]}"
                                        supabase.storage.from_("kho-tai-lieu").upload(path=s_n, file=f_u.getvalue(), file_options={"content-type": f_u.type})
                                        p_u = supabase.storage.from_("kho-tai-lieu").get_public_url(s_n)
                                    supabase.table("y_kien").insert({"ma_ch": ma_ch, "nguoi_gop_y": f"{h_t} ({c_v} - {d_v})", "noi_dung": n_d, "link_file": p_u}).execute()
                                    st.success("✅ Gửi thành công!"); st.cache_data.clear(); st.rerun()

                with tab_xem:
                    yk_cua_hop = df_y_kien[df_y_kien['Mã cuộc họp'] == ma_ch] if not df_y_kien.empty else pd.DataFrame()
                    if yk_cua_hop.empty:
                        st.info("Chưa có ý kiến / tham luận nào được gửi.")
                    else:
                        for idx, row in yk_cua_hop.iterrows():
                            file_html = f'<div style="margin-top: 8px;"><a href="{row.get("Link File sửa đổi")}" target="_blank" style="font-size: 13px; color: #C8102E; text-decoration: none; font-weight: bold;">📎 Xem file đính kèm sửa đổi</a></div>' if pd.notna(row.get("Link File sửa đổi")) and row.get("Link File sửa đổi") != '' else ''
                            st.markdown(f"""
                            <div style="background-color: rgba(255, 255, 255, 0.95); border-left: 4px solid #17a2b8; padding: 12px 15px; margin-bottom: 12px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                <div style="font-weight: bold; color: #004B87; font-size: 15px;">👤 {row.get('Tên đơn vị / Đại biểu', 'Đại biểu')}</div>
                                <div style='color:#6c757d; font-size:12px; margin-bottom: 5px;'>🕒 Đã gửi lúc: {row.get('Thời gian gửi', '')}</div>
                                <div style="font-size: 14px; color: #333; line-height: 1.5;">{row.get('Nội dung góp ý', '')}</div>
                                {file_html}
                            </div>
                            """, unsafe_allow_html=True)

elif menu == "⚙️ Quản trị: Tạo mới":
    st.markdown('<div class="section-title">➕ TẠO CUỘC HỌP MỚI</div>', unsafe_allow_html=True)
    with st.form("form_tao_hop", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1: ma_ch = st.text_input("Mã Cuộc họp (VD: CH01)*:")
        with col2: ten_ch = st.text_input("Tên Cuộc họp / Hội nghị*:")
        col3, col4, col5 = st.columns(3)
        with col3: t_bd = st.text_input("Thời gian BẮT ĐẦU*", placeholder="HH:MM, DD/MM/YYYY")
        with col4: t_kt = st.text_input("Thời gian KẾT THÚC*", placeholder="HH:MM, DD/MM/YYYY")
        with col5: d_d = st.text_input("Địa điểm:")
        if st.form_submit_button("LƯU CUỘC HỌP MỚI"):
            pattern = r"^\d{2}:\d{2}, \d{2}/\d{2}/\d{4}$"
            if not ma_ch or not ten_ch: st.error("⚠️ Thiếu thông tin!")
            elif not re.match(pattern, t_bd) or not re.match(pattern, t_kt): st.error("⚠️ Sai định dạng thời gian!")
            else:
                supabase.table("cuoc_hop").insert({"ma_ch": ma_ch, "ten_ch": ten_ch, "thoi_gian": t_bd, "thoi_gian_ket_thuc": t_kt, "dia_diem": d_d}).execute()
                st.success("✅ Thành công!"); st.cache_data.clear()

elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-title">📤 UPLOAD TÀI LIỆU LÊN HỆ THỐNG</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty: st.warning("⚠️ Cần tạo cuộc họp trước.")
    else:
        with st.form("form_tai_lieu", clear_on_submit=True):
            ch_chon = st.selectbox("📌 Gắn vào Cuộc họp:", (df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']).tolist())
            u_fs = st.file_uploader("📂 Chọn file:", type=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"], accept_multiple_files=True)
            if st.form_submit_button("🚀 TẢI LÊN"):
                if not u_fs: st.error("⚠️ Chọn file!")
                else:
                    ma_ch = ch_chon.split(" - ")[0]; pg = st.progress(0)
                    for i, f in enumerate(u_fs):
                        s_n = f"{ma_ch}_{get_vn_now().strftime('%H%M%S')}_{uuid.uuid4().hex[:4]}.{f.name.split('.')[-1]}"
                        supabase.storage.from_("kho-tai-lieu").upload(path=s_n, file=f.getvalue(), file_options={"content-type": f.type})
                        p_u = supabase.storage.from_("kho-tai-lieu").get_public_url(s_n)
                        supabase.table("tai_lieu").insert({"ma_ch": ma_ch, "ma_tl": f"TL{i}", "ten_tl": f.name, "link_file": p_u}).execute()
                        pg.progress((i+1)/len(u_fs))
                    st.success("✅ Xong!"); st.cache_data.clear()

elif menu == "✏️ Quản trị: Chỉnh sửa / Xóa":
    st.markdown('<div class="section-title">✏️ CHỈNH SỬA THÔNG TIN CUỘC HỌP</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty: st.info("Không có dữ liệu.")
    else:
        ch_sua = st.selectbox("Chọn cuộc họp muốn sửa:", (df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']).tolist())
        ma_sua = ch_sua.split(" - ")[0]
        row_cu = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_sua].iloc[0]
        with st.form("form_sua_ch"):
            new_ten = st.text_input("Tên cuộc họp:", value=row_cu['Tên cuộc họp'])
            c1, c2 = st.columns(2)
            new_bd = c1.text_input("Thời gian bắt đầu:", value=row_cu['Thời gian'])
            new_kt = c2.text_input("Thời gian kết thúc:", value=row_cu.get('Thời gian kết thúc', ''))
            new_dd = st.text_input("Địa điểm:", value=row_cu['Địa điểm'])
            col_b1, col_b2 = st.columns([1, 1])
            if col_b1.form_submit_button("💾 CẬP NHẬT THÔNG TIN", use_container_width=True):
                supabase.table("cuoc_hop").update({"ten_ch": new_ten, "thoi_gian": new_bd, "thoi_gian_ket_thuc": new_kt, "dia_diem": new_dd}).eq("ma_ch", ma_sua).execute()
                st.success("✅ Đã cập nhật!"); st.cache_data.clear(); st.rerun()
            if col_b2.form_submit_button("🗑️ XÓA CUỘC HỌP NÀY", use_container_width=True):
                supabase.table("cuoc_hop").delete().eq("ma_ch", ma_sua).execute()
                st.warning("🔥 Đã xóa cuộc họp!"); st.cache_data.clear(); st.rerun()
