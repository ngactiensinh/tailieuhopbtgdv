import streamlit as st
import pandas as pd
import re
import base64
import uuid
from datetime import datetime, timedelta
from supabase import create_client, Client
import urllib.parse

st.set_page_config(
    page_title="E-Cabinet TGDV - Tuyên Quang",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CẤU HÌNH SUPABASE
# ==========================================
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    pass

# ==========================================
# HÀM ĐẾM LƯỢT TRUY CẬP
# ==========================================
def log_access(app_name):
    key_name = f"da_dem_truy_cap_{app_name}"
    if key_name not in st.session_state:
        try:
            supabase.table("thong_ke_truy_cap").insert({"ten_app": app_name}).execute()
            st.session_state[key_name] = True
        except Exception:
            pass

log_access("E-Cabinet TGDV")

PASS_ADMIN = "Admin@2026"

# ==========================================
# CSS GIAO DIỆN PHONG CÁCH CHÍNH TRỊ - SANG TRỌNG
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&display=swap');

:root {
    --do-chinh:     #C8102E;
    --do-dam:       #9B0A20;
    --do-nhat:      #F9E8EB;
    --vang:         #C9A84C;
    --vang-nhat:    #FDF6E3;
    --xanh-dam:     #1A2557;
    --xanh-vua:     #243476;
    --xanh-nhat:    #EEF1FA;
    --trang:        #FFFFFF;
    --xam-nhat:     #F5F6FA;
    --xam-vien:     #E2E5EF;
    --xam-text:     #6B7280;
    --den-text:     #1C2237;
    --bong-nhe:     0 2px 12px rgba(26,37,87,0.08);
    --bong-vua:     0 4px 20px rgba(26,37,87,0.13);
    --bong-manh:    0 8px 32px rgba(26,37,87,0.18);
}

/* ---- NỀN ỨNG DỤNG ---- */
.stApp {
    background-color: #EEF1FA;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 39px,
            rgba(26,37,87,0.04) 39px,
            rgba(26,37,87,0.04) 40px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 39px,
            rgba(26,37,87,0.04) 39px,
            rgba(26,37,87,0.04) 40px
        );
    font-family: 'Source Sans 3', sans-serif;
}

/* ---- ĐẦU TRANG ---- */
.header-wrapper {
    background: linear-gradient(135deg, #1A2557 0%, #243476 60%, #1A2557 100%);
    border-bottom: 4px solid var(--vang);
    border-radius: 0 0 16px 16px;
    padding: 22px 36px;
    margin-bottom: 28px;
    box-shadow: var(--bong-manh);
    display: flex;
    align-items: center;
    gap: 24px;
    position: relative;
    overflow: hidden;
}
.header-wrapper::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23C9A84C' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
    pointer-events: none;
}
.header-logo-box {
    flex-shrink: 0;
    width: 72px; height: 72px;
    background: rgba(255,255,255,0.1);
    border: 2px solid rgba(201,168,76,0.5);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
}
.header-logo-box img {
    width: 64px; height: 64px;
    object-fit: contain;
}
.header-text-box { flex: 1; }
.header-subtitle {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--vang);
    margin-bottom: 4px;
}
.header-title {
    font-family: 'Merriweather', serif;
    font-size: 22px;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.25;
    text-shadow: 0 1px 4px rgba(0,0,0,0.3);
    margin: 0 0 6px 0;
}
.header-tagline {
    font-size: 12.5px;
    color: rgba(255,255,255,0.65);
    letter-spacing: 0.5px;
    font-style: italic;
}
.header-badge {
    background: linear-gradient(135deg, var(--do-chinh), var(--do-dam));
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 20px;
    letter-spacing: 1px;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 2px 8px rgba(200,16,46,0.4);
    white-space: nowrap;
    text-transform: uppercase;
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A2557 0%, #1E2B66 100%);
    border-right: 3px solid var(--vang);
}
section[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.88) !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: rgba(255,255,255,0.88) !important;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 8px;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 10px 14px !important;
    width: 100%;
    transition: all 0.2s ease;
    font-size: 13.5px !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(201,168,76,0.15);
    border-color: rgba(201,168,76,0.4);
}

/* ---- THẺ CUỘC HỌP (TRANG CHỦ) ---- */
.meeting-card {
    background: var(--trang);
    border-radius: 12px;
    border: 1px solid var(--xam-vien);
    border-top: 4px solid var(--xanh-vua);
    padding: 20px;
    box-shadow: var(--bong-nhe);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
    position: relative;
}
.meeting-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--bong-vua);
}
.meeting-card-title {
    font-family: 'Merriweather', serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--den-text);
    margin: 12px 0 14px 0;
    line-height: 1.45;
}
.meeting-card-meta {
    font-size: 13px;
    color: var(--xam-text);
    line-height: 1.8;
    border-top: 1px dashed var(--xam-vien);
    padding-top: 12px;
}
.meeting-card-meta strong {
    color: var(--xanh-dam);
}

/* ---- STATUS TAGS ---- */
.tag {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.tag-sap-dien-ra  { background: #EEF1FA; color: var(--xanh-vua); border: 1px solid var(--xanh-vua); }
.tag-dang-dien-ra { background: var(--do-chinh); color: white; animation: pulse 2s infinite; }
.tag-da-ket-thuc  { background: #F3F4F6; color: #6B7280; border: 1px solid #D1D5DB; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.75} }

/* ---- PANEL NỘI DUNG ---- */
.content-panel {
    background: var(--trang);
    border-radius: 12px;
    border: 1px solid var(--xam-vien);
    padding: 24px 28px;
    box-shadow: var(--bong-nhe);
    margin-bottom: 16px;
}
.section-heading {
    font-family: 'Merriweather', serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--xanh-dam);
    text-transform: uppercase;
    letter-spacing: 1px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--vang);
    margin-bottom: 18px;
    display: flex; align-items: center; gap: 8px;
}

/* ---- THẺ TÀI LIỆU ---- */
.doc-card {
    background: var(--xam-nhat);
    border: 1px solid var(--xam-vien);
    border-left: 4px solid var(--xanh-vua);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    transition: background 0.2s;
}
.doc-card:hover { background: var(--xanh-nhat); }
.doc-name {
    font-size: 14px;
    font-weight: 600;
    color: var(--den-text);
    flex: 1;
}
.doc-btn-group { display: flex; gap: 8px; flex-shrink: 0; }
.btn-view {
    background: var(--xanh-nhat);
    border: 1px solid var(--xanh-vua);
    color: var(--xanh-vua);
    padding: 5px 14px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
    white-space: nowrap;
    transition: all 0.15s;
}
.btn-view:hover { background: var(--xanh-vua); color: white; }
.btn-dl {
    background: var(--do-nhat);
    border: 1px solid var(--do-chinh);
    color: var(--do-chinh);
    padding: 5px 14px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
    white-space: nowrap;
    transition: all 0.15s;
}
.btn-dl:hover { background: var(--do-chinh); color: white; }

/* ---- THẺ Ý KIẾN ---- */
.yk-card {
    background: var(--trang);
    border: 1px solid var(--xam-vien);
    border-left: 4px solid var(--do-chinh);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: var(--bong-nhe);
}
.yk-name { font-size: 14.5px; font-weight: 700; color: var(--xanh-dam); margin-bottom: 3px; }
.yk-time { font-size: 12px; color: var(--xam-text); margin-bottom: 8px; }
.yk-content { font-size: 14px; color: var(--den-text); line-height: 1.6; }

/* ---- THÔNG TIN HỘI NGHỊ (META ROW) ---- */
.meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    background: var(--xanh-nhat);
    border: 1px solid var(--xam-vien);
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 20px;
}
.meta-item {
    display: flex; align-items: center; gap: 8px;
    font-size: 13.5px;
    color: var(--den-text);
    flex: 1;
    min-width: 180px;
}
.meta-item span.label { color: var(--xam-text); font-size: 12px; display: block; margin-bottom: 1px; }
.meta-item span.value { font-weight: 600; color: var(--xanh-dam); }

/* ---- TIÊU ĐỀ TRANG ĐĂNG NHẬP ---- */
.login-section-title {
    text-align: center;
    color: var(--xam-text);
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 20px 0 10px 0;
    display: flex; align-items: center; gap: 12px;
}
.login-section-title::before, .login-section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--xam-vien);
}
.meetings-section-title {
    font-family: 'Merriweather', serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--xanh-dam);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    text-align: center;
    margin-bottom: 20px;
    display: flex; align-items: center; justify-content: center; gap: 10px;
}
.meetings-section-title::before, .meetings-section-title::after {
    content: '';
    width: 40px; height: 2px;
    background: linear-gradient(to right, transparent, var(--vang));
}
.meetings-section-title::after {
    background: linear-gradient(to left, transparent, var(--vang));
}

/* ---- FORM CÁ NHÂN HOÁ ---- */
div[data-testid="stForm"] {
    background: var(--trang);
    border: 1px solid var(--xam-vien);
    border-radius: 12px;
    padding: 24px !important;
    box-shadow: var(--bong-nhe);
}

/* ---- NÚT BẤM ---- */
div.stButton > button {
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 700;
    border-radius: 8px;
    transition: all 0.2s ease;
    letter-spacing: 0.3px;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--do-chinh), var(--do-dam));
    color: white;
    border: none;
    box-shadow: 0 3px 10px rgba(200,16,46,0.35);
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 5px 16px rgba(200,16,46,0.5);
    transform: translateY(-1px);
}
div.stButton > button[kind="secondary"] {
    background: white !important;
    color: var(--xanh-vua) !important;
    border: 2px solid var(--xanh-vua) !important;
}
div.stButton > button[kind="formSubmit"] {
    background: linear-gradient(135deg, var(--xanh-vua), var(--xanh-dam));
    color: white;
    border: none;
    box-shadow: 0 3px 10px rgba(26,37,87,0.3);
}

/* ---- TABS ---- */
div[data-testid="stTabs"] button {
    font-weight: 600 !important;
    font-size: 13.5px !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--xanh-vua) !important;
    border-bottom-color: var(--xanh-vua) !important;
}

/* ---- SELECT BOX ---- */
div[data-testid="stSelectbox"] label {
    font-weight: 600;
    color: var(--xanh-dam);
}

/* ---- INPUT ---- */
div.stTextInput input, div.stTextArea textarea {
    border-radius: 8px;
    border: 1.5px solid var(--xam-vien);
    font-family: 'Source Sans 3', sans-serif;
}
div.stTextInput input:focus, div.stTextArea textarea:focus {
    border-color: var(--xanh-vua);
    box-shadow: 0 0 0 3px rgba(36,52,118,0.1);
}

/* ---- THÔNG BÁO ---- */
div[data-testid="stSuccess"] {
    background: #F0FDF4; border-color: #22C55E; border-radius: 8px;
}
div[data-testid="stError"] {
    background: #FFF5F5; border-color: var(--do-chinh); border-radius: 8px;
}
div[data-testid="stWarning"] {
    background: var(--vang-nhat); border-radius: 8px;
}
div[data-testid="stInfo"] {
    background: var(--xanh-nhat); border-color: var(--xanh-vua); border-radius: 8px;
}

/* ---- ẨN STREAMLIT MẶCĐỊNH ---- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HÀM TIỆN ÍCH
# ==========================================
def get_vn_now():
    return datetime.utcnow() + timedelta(hours=7)

def get_logo_base64():
    try:
        with open("Logo TGDV.png", "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""

def hien_thi_tieu_de():
    logo_data = get_logo_base64()
    logo_html = f'<div class="header-logo-box"><img src="data:image/png;base64,{logo_data}"></div>' if logo_data else '<div class="header-logo-box" style="font-size:32px;">🏛️</div>'
    role_label = '<span class="header-badge">⚙️ QUẢN TRỊ VIÊN</span>' if st.session_state.get("role") == "Admin" else '<span class="header-badge" style="background:linear-gradient(135deg,#1A6B3A,#145530);">👤 ĐẠI BIỂU</span>' if st.session_state.get("role") == "DaiBieu" else ''
    st.markdown(f"""
    <div class="header-wrapper">
        {logo_html}
        <div class="header-text-box">
            <div class="header-subtitle">Ban Tuyên giáo và Dân vận Tỉnh ủy Tuyên Quang</div>
            <div class="header-title">🏛️ Hệ thống Phòng họp Không giấy</div>
            <div class="header-tagline">E-Cabinet — Chuyển đổi số trong hoạt động hội nghị</div>
        </div>
        {role_label}
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        ch = supabase.table("cuoc_hop").select("*").order("id", desc=True).execute().data
        tl = supabase.table("tai_lieu").select("*").execute().data
        yk = supabase.table("y_kien").select("*").order("id", desc=True).execute().data

        df_ch = pd.DataFrame(ch).rename(columns={
            'ma_ch': 'Mã cuộc họp', 'ten_ch': 'Tên cuộc họp',
            'thoi_gian': 'Thời gian', 'thoi_gian_ket_thuc': 'Thời gian kết thúc',
            'dia_diem': 'Địa điểm'
        })
        df_tl = pd.DataFrame(tl).rename(columns={
            'ma_ch': 'Mã cuộc họp', 'ma_tl': 'Mã tài liệu',
            'ten_tl': 'Tên tài liệu', 'link_file': 'Link Google Drive'
        })
        df_yk = pd.DataFrame(yk).rename(columns={
            'ma_ch': 'Mã cuộc họp', 'nguoi_gop_y': 'Tên đơn vị / Đại biểu',
            'noi_dung': 'Nội dung góp ý', 'link_file': 'Link File sửa đổi',
            'created_at': 'Thời gian gửi'
        })

        if not df_yk.empty:
            df_yk['Thời gian gửi'] = pd.to_datetime(df_yk['Thời gian gửi']).dt.tz_convert('Asia/Ho_Chi_Minh').dt.strftime("%H:%M — %d/%m/%Y")
        return {"cuoc_hop": df_ch, "tai_lieu": df_tl, "y_kien": df_yk}
    except Exception:
        return {"cuoc_hop": pd.DataFrame(), "tai_lieu": pd.DataFrame(), "y_kien": pd.DataFrame()}

def parse_meeting_time(t_str):
    try:
        return datetime.strptime(t_str.strip(), "%H:%M, %d/%m/%Y")
    except Exception:
        return None

def get_realtime_status(start_str, end_str):
    start_time = parse_meeting_time(start_str)
    end_time = parse_meeting_time(end_str)
    now = get_vn_now()

    if not start_time:
        return "Không xác định", "tag-da-ket-thuc"
    if not end_time:
        end_time = start_time + timedelta(hours=4)

    if now < start_time:
        return "Sắp diễn ra", "tag-sap-dien-ra"
    elif start_time <= now <= end_time:
        return "Đang diễn ra", "tag-dang-dien-ra"
    else:
        return "Đã kết thúc", "tag-da-ket-thuc"

# ==========================================
# KHỞI TẠO SESSION STATE
# ==========================================
if "role" not in st.session_state:
    st.session_state["role"] = None
if "selected_meeting_id" not in st.session_state:
    st.session_state["selected_meeting_id"] = None

# ==========================================
# TẢI DỮ LIỆU
# ==========================================
data_dict = load_data()
df_cuoc_hop = data_dict.get("cuoc_hop", pd.DataFrame())
df_tai_lieu = data_dict.get("tai_lieu", pd.DataFrame())
df_y_kien   = data_dict.get("y_kien", pd.DataFrame())

if not df_cuoc_hop.empty:
    df_cuoc_hop['ParsedStart'] = df_cuoc_hop['Thời gian'].apply(parse_meeting_time)
    df_cuoc_hop[['RealtimeStatus', 'TagClass']] = df_cuoc_hop.apply(
        lambda r: pd.Series(get_realtime_status(r['Thời gian'], r.get('Thời gian kết thúc'))), axis=1
    )

# ==========================================
# MÀN HÌNH ĐĂNG NHẬP
# ==========================================
if st.session_state["role"] is None:
    hien_thi_tieu_de()

    if not df_cuoc_hop.empty:
        active = df_cuoc_hop[df_cuoc_hop['RealtimeStatus'].isin(["Sắp diễn ra", "Đang diễn ra"])]
        featured_df = active.sort_values('ParsedStart').head(3) if not active.empty else df_cuoc_hop.head(3)

        st.markdown('<div class="meetings-section-title">📌 Chọn Hội nghị để Tham gia</div>', unsafe_allow_html=True)

        n = len(featured_df)
        if n == 1:
            cols_outer = st.columns([1, 2, 1])
            target_cols = [cols_outer[1]]
        elif n == 2:
            cols_outer = st.columns([1, 3, 3, 1])
            target_cols = [cols_outer[1], cols_outer[2]]
        else:
            target_cols = st.columns(3)

        for i, (idx, row) in enumerate(featured_df.iterrows()):
            with target_cols[i]:
                kt_str = row.get("Thời gian kết thúc", "")
                kt_display = kt_str if kt_str and str(kt_str) != 'nan' else "Chưa xác định"
                st.markdown(f"""
                <div class="meeting-card">
                    <span class="tag {row['TagClass']}">
                        {'🔴' if row['RealtimeStatus']=='Đang diễn ra' else '🔵' if row['RealtimeStatus']=='Sắp diễn ra' else '⚫'}
                        {row['RealtimeStatus']}
                    </span>
                    <div class="meeting-card-title">{row['Tên cuộc họp']}</div>
                    <div class="meeting-card-meta">
                        <strong>📍 Địa điểm:</strong> {row['Địa điểm']}<br>
                        <strong>⏰ Bắt đầu:</strong> {row['Thời gian']}<br>
                        <strong>🏁 Kết thúc:</strong> {kt_display}<br>
                        <strong>🔖 Mã:</strong> {row['Mã cuộc họp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("🚀 VÀO PHÒNG HỌP NÀY", key=f"btn_{row['Mã cuộc họp']}", type="primary", use_container_width=True):
                    st.session_state["selected_meeting_id"] = row['Mã cuộc họp']
                    st.session_state["role"] = "DaiBieu"
                    st.rerun()

    # ---- Đăng nhập Admin ----
    st.markdown('<div class="login-section-title">Dành cho Quản trị viên</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.5, 2.5, 1.5])
    with col2:
        with st.form("login_form", clear_on_submit=True):
            st.markdown("""
            <div style="text-align:center; padding: 4px 0 16px 0;">
                <div style="font-size: 36px; margin-bottom: 6px;">🔐</div>
                <div style="font-family:'Merriweather',serif; font-size:15px; font-weight:700; color:#1A2557;">
                    Đăng nhập Quản trị viên
                </div>
                <div style="font-size:12.5px; color:#6B7280; margin-top: 4px;">
                    Đại biểu không cần đăng nhập, bấm trực tiếp vào phòng họp phía trên
                </div>
            </div>
            """, unsafe_allow_html=True)
            pwd = st.text_input("Mật khẩu quản trị:", type="password", placeholder="Nhập mật khẩu...")
            if st.form_submit_button("🚪 ĐĂNG NHẬP", use_container_width=True):
                if pwd == PASS_ADMIN:
                    st.session_state["role"] = "Admin"
                    st.rerun()
                else:
                    st.error("❌ Sai mật khẩu! Vui lòng thử lại.")
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH (SAU KHI VÀO)
# ==========================================
hien_thi_tieu_de()

# ---- Sidebar ----
logo_data = get_logo_base64()
if logo_data:
    st.sidebar.markdown(
        f'<div style="text-align:center; padding: 16px 0 20px 0;">'
        f'<img src="data:image/png;base64,{logo_data}" width="90" style="object-fit:contain; border-radius:50%; border:2px solid rgba(201,168,76,0.5);">'
        f'</div>',
        unsafe_allow_html=True
    )

st.sidebar.markdown(
    '<div style="font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; '
    'color:rgba(201,168,76,0.9); padding: 0 8px 12px 8px; border-bottom: 1px solid rgba(255,255,255,0.1); '
    'margin-bottom: 14px;">📌 Điều hướng</div>',
    unsafe_allow_html=True
)

menu_list = (
    ["📚 Phòng họp & Tài liệu", "⚙️ Quản trị: Tạo mới", "📤 Quản trị: Đăng Tài liệu", "✏️ Quản trị: Chỉnh sửa / Xóa"]
    if st.session_state["role"] == "Admin"
    else ["📚 Phòng họp & Tài liệu"]
)
menu = st.sidebar.radio("", menu_list)

st.sidebar.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
if st.sidebar.button("🔄 Làm mới dữ liệu", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
st.sidebar.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
if st.sidebar.button("🚪 Thoát khỏi phòng họp", use_container_width=True, type="primary"):
    st.session_state["role"] = None
    st.session_state["selected_meeting_id"] = None
    st.rerun()

st.sidebar.markdown(
    f'<div style="position:fixed; bottom:20px; font-size:11px; color:rgba(255,255,255,0.35); padding:0 16px; line-height:1.6;">'
    f'⏰ {get_vn_now().strftime("%H:%M — %d/%m/%Y")}<br>'
    f'📍 E-Cabinet TGDV v2.0</div>',
    unsafe_allow_html=True
)

# ==========================================
# TRANG: PHÒNG HỌP & TÀI LIỆU
# ==========================================
if menu == "📚 Phòng họp & Tài liệu":
    if df_cuoc_hop.empty:
        st.info("ℹ️ Chưa có cuộc họp nào trong hệ thống.")
    else:
        ds_lua_chon = df_cuoc_hop['Mã cuộc họp'] + " — " + df_cuoc_hop['Tên cuộc họp']
        idx_def = 0
        if st.session_state.get("selected_meeting_id"):
            for i, val in enumerate(ds_lua_chon):
                if val.startswith(st.session_state["selected_meeting_id"]):
                    idx_def = i
                    break

        chon_hop = st.selectbox("📂 Lựa chọn Hội nghị:", ds_lua_chon, index=idx_def)

        if chon_hop:
            ma_ch = chon_hop.split(" — ")[0]
            st.session_state["selected_meeting_id"] = ma_ch
            thong_tin = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_ch].iloc[0]
            cho_phep_yk = True if pd.isna(thong_tin.get('cho_phep_gop_y')) else bool(thong_tin.get('cho_phep_gop_y'))
            kt_str = thong_tin.get('Thời gian kết thúc', '')
            kt_display = kt_str if kt_str and str(kt_str) != 'nan' else "Chưa xác định"

            # Tên hội nghị
            st.markdown(
                f'<div style="font-family:Merriweather,serif; font-size:19px; font-weight:700; '
                f'color:#1A2557; border-left:4px solid #C9A84C; padding-left:14px; margin: 10px 0 16px 0; line-height:1.4;">'
                f'{thong_tin["Tên cuộc họp"]}</div>',
                unsafe_allow_html=True
            )

            # Thông tin meta
            st.markdown(f"""
            <div class="meta-row">
                <div class="meta-item">
                    <span>⏰</span>
                    <div><span class="label">Thời gian bắt đầu</span><span class="value">{thong_tin['Thời gian']}</span></div>
                </div>
                <div class="meta-item">
                    <span>🏁</span>
                    <div><span class="label">Thời gian kết thúc</span><span class="value">{kt_display}</span></div>
                </div>
                <div class="meta-item">
                    <span>📍</span>
                    <div><span class="label">Địa điểm</span><span class="value">{thong_tin['Địa điểm']}</span></div>
                </div>
                <div class="meta-item">
                    <span>🔖</span>
                    <div><span class="label">Trạng thái</span>
                    <span class="tag {thong_tin['TagClass']}" style="font-size:11px; padding:2px 10px;">
                        {thong_tin['RealtimeStatus']}
                    </span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Layout tài liệu + góp ý
            if cho_phep_yk:
                col_doc, col_yk = st.columns([5, 5], gap="large")
            else:
                col_doc = st.container()

            # ---- CỘT TÀI LIỆU ----
            with col_doc:
                st.markdown('<div class="section-heading">📑 Tài liệu Kỳ họp</div>', unsafe_allow_html=True)
                tl_cua_hop = df_tai_lieu[df_tai_lieu['Mã cuộc họp'] == ma_ch] if not df_tai_lieu.empty else pd.DataFrame()

                if tl_cua_hop.empty:
                    st.info("Chưa có tài liệu nào được đăng tải.")
                else:
                    for _, row in tl_cua_hop.iterrows():
                        file_url = str(row.get("Link Google Drive", ""))
                        is_office = any(ext in file_url.lower() for ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'])
                        view_url = f"https://docs.google.com/viewer?url={urllib.parse.quote(file_url, safe='')}&embedded=true" if is_office else file_url
                        st.markdown(f"""
                        <div class="doc-card">
                            <span style="font-size:20px; flex-shrink:0;">📄</span>
                            <div class="doc-name">{row.get('Tên tài liệu')}</div>
                            <div class="doc-btn-group">
                                <a href="{view_url}" target="_blank" class="btn-view">👁️ Xem</a>
                                <a href="{file_url}" target="_blank" class="btn-dl">⬇️ Tải</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # ---- CỘT GÓP Ý ----
            if cho_phep_yk:
                with col_yk:
                    st.markdown('<div class="section-heading">✍️ Ý kiến / Tham luận</div>', unsafe_allow_html=True)
                    tab_gui, tab_xem = st.tabs(["💬 Gửi ý kiến mới", f"📂 Ý kiến đã thu nhận"])

                    with tab_gui:
                        with st.form("form_gop_y", clear_on_submit=True):
                            h_t = st.text_input("👤 Họ và tên Đại biểu *")
                            c_v = st.text_input("💼 Chức vụ *", placeholder="VD: Phó Giám đốc, Trưởng phòng...")
                            d_v = st.text_input("🏢 Cơ quan / Đơn vị *")
                            n_d = st.text_area("📝 Nội dung ý kiến đóng góp", height=130)
                            f_u = st.file_uploader("📎 Đính kèm file văn bản đã sửa (nếu có):", type=["docx", "pdf"])

                            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                            if st.form_submit_button("🚀 GỬI Ý KIẾN", use_container_width=True):
                                if not h_t or not c_v or not d_v:
                                    st.error("⚠️ Vui lòng điền đầy đủ Họ tên, Chức vụ và Đơn vị!")
                                else:
                                    with st.spinner("Đang gửi ý kiến..."):
                                        p_u = ""
                                        if f_u:
                                            s_n = f"YKien_{ma_ch}_{get_vn_now().strftime('%H%M%S')}_{uuid.uuid4().hex[:4]}.{f_u.name.split('.')[-1]}"
                                            supabase.storage.from_("kho-tai-lieu").upload(
                                                path=s_n, file=f_u.getvalue(),
                                                file_options={"content-type": f_u.type}
                                            )
                                            p_u = supabase.storage.from_("kho-tai-lieu").get_public_url(s_n)
                                        supabase.table("y_kien").insert({
                                            "ma_ch": ma_ch,
                                            "nguoi_gop_y": f"{h_t} ({c_v} — {d_v})",
                                            "noi_dung": n_d,
                                            "link_file": p_u
                                        }).execute()
                                        st.success("✅ Gửi ý kiến thành công!")
                                        st.cache_data.clear()
                                        st.rerun()

                    with tab_xem:
                        yk_cua_hop = df_y_kien[df_y_kien['Mã cuộc họp'] == ma_ch] if not df_y_kien.empty else pd.DataFrame()
                        if yk_cua_hop.empty:
                            st.info("Chưa có ý kiến / tham luận nào được gửi.")
                        else:
                            st.markdown(f'<div style="font-size:13px; color:#6B7280; margin-bottom:12px;">Tổng cộng: <strong>{len(yk_cua_hop)}</strong> ý kiến</div>', unsafe_allow_html=True)
                            for _, row in yk_cua_hop.iterrows():
                                file_html = (
                                    f'<div style="margin-top:8px;">'
                                    f'<a href="{row.get("Link File sửa đổi")}" target="_blank" '
                                    f'style="font-size:12.5px; color:#C8102E; font-weight:700; text-decoration:none;">'
                                    f'📎 Xem file đính kèm</a></div>'
                                ) if pd.notna(row.get("Link File sửa đổi")) and row.get("Link File sửa đổi") != '' else ''
                                st.markdown(f"""
                                <div class="yk-card">
                                    <div class="yk-name">👤 {row.get('Tên đơn vị / Đại biểu', 'Đại biểu')}</div>
                                    <div class="yk-time">🕒 {row.get('Thời gian gửi', '')}</div>
                                    <div class="yk-content">{row.get('Nội dung góp ý', '')}</div>
                                    {file_html}
                                </div>
                                """, unsafe_allow_html=True)

# ==========================================
# TRANG: QUẢN TRỊ - TẠO MỚI
# ==========================================
elif menu == "⚙️ Quản trị: Tạo mới":
    st.markdown('<div class="section-heading">➕ Tạo Cuộc họp / Hội nghị mới</div>', unsafe_allow_html=True)
    with st.form("form_tao_hop", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            ma_ch = st.text_input("Mã Cuộc họp *", placeholder="VD: CH01")
        with col2:
            ten_ch = st.text_input("Tên Cuộc họp / Hội nghị *")

        col3, col4, col5 = st.columns(3)
        with col3:
            t_bd = st.text_input("Thời gian bắt đầu *", placeholder="HH:MM, DD/MM/YYYY")
        with col4:
            t_kt = st.text_input("Thời gian kết thúc *", placeholder="HH:MM, DD/MM/YYYY")
        with col5:
            d_d = st.text_input("Địa điểm tổ chức")

        cp_gy = st.checkbox("✅ Cho phép Đại biểu gửi Ý kiến / Tham luận trực tuyến", value=True)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.form_submit_button("💾 LƯU CUỘC HỌP MỚI", use_container_width=True):
            pattern = r"^\d{2}:\d{2}, \d{2}/\d{2}/\d{4}$"
            if not ma_ch or not ten_ch:
                st.error("⚠️ Vui lòng điền đầy đủ Mã và Tên cuộc họp!")
            elif not re.match(pattern, t_bd) or not re.match(pattern, t_kt):
                st.error("⚠️ Sai định dạng thời gian! Vui lòng nhập theo mẫu: HH:MM, DD/MM/YYYY")
            else:
                supabase.table("cuoc_hop").insert({
                    "ma_ch": ma_ch, "ten_ch": ten_ch,
                    "thoi_gian": t_bd, "thoi_gian_ket_thuc": t_kt,
                    "dia_diem": d_d, "cho_phep_gop_y": cp_gy
                }).execute()
                st.success(f"✅ Đã tạo thành công cuộc họp: {ten_ch}")
                st.cache_data.clear()

# ==========================================
# TRANG: QUẢN TRỊ - ĐĂNG TÀI LIỆU
# ==========================================
elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-heading">📤 Upload Tài liệu lên Hệ thống</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty:
        st.warning("⚠️ Cần tạo ít nhất một cuộc họp trước khi đăng tài liệu.")
    else:
        with st.form("form_tai_lieu", clear_on_submit=True):
            ch_chon = st.selectbox(
                "📌 Gắn tài liệu vào Cuộc họp:",
                (df_cuoc_hop['Mã cuộc họp'] + " — " + df_cuoc_hop['Tên cuộc họp']).tolist()
            )
            u_fs = st.file_uploader(
                "📂 Chọn file tài liệu:",
                type=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
                accept_multiple_files=True
            )
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.form_submit_button("🚀 TẢI LÊN HỆ THỐNG", use_container_width=True):
                if not u_fs:
                    st.error("⚠️ Vui lòng chọn ít nhất một file!")
                else:
                    ma_ch = ch_chon.split(" — ")[0]
                    pg = st.progress(0, text="Đang tải lên...")
                    for i, f in enumerate(u_fs):
                        s_n = f"{ma_ch}_{get_vn_now().strftime('%H%M%S')}_{uuid.uuid4().hex[:4]}.{f.name.split('.')[-1]}"
                        supabase.storage.from_("kho-tai-lieu").upload(
                            path=s_n, file=f.getvalue(),
                            file_options={"content-type": f.type}
                        )
                        p_u = supabase.storage.from_("kho-tai-lieu").get_public_url(s_n)
                        supabase.table("tai_lieu").insert({
                            "ma_ch": ma_ch, "ma_tl": f"TL{i}",
                            "ten_tl": f.name, "link_file": p_u
                        }).execute()
                        pg.progress((i + 1) / len(u_fs), text=f"Đang tải: {f.name}")
                    st.success(f"✅ Đã tải lên thành công {len(u_fs)} tài liệu!")
                    st.cache_data.clear()

# ==========================================
# TRANG: QUẢN TRỊ - CHỈNH SỬA / XÓA
# ==========================================
elif menu == "✏️ Quản trị: Chỉnh sửa / Xóa":
    st.markdown('<div class="section-heading">✏️ Chỉnh sửa / Xóa Cuộc họp</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty:
        st.info("Không có dữ liệu cuộc họp nào.")
    else:
        ch_sua = st.selectbox(
            "Chọn cuộc họp cần chỉnh sửa:",
            (df_cuoc_hop['Mã cuộc họp'] + " — " + df_cuoc_hop['Tên cuộc họp']).tolist()
        )
        ma_sua = ch_sua.split(" — ")[0]
        row_cu = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == ma_sua].iloc[0]

        with st.form("form_sua_ch"):
            new_ten = st.text_input("Tên cuộc họp:", value=row_cu['Tên cuộc họp'])
            c1, c2 = st.columns(2)
            new_bd = c1.text_input("Thời gian bắt đầu:", value=row_cu['Thời gian'])
            new_kt = c2.text_input("Thời gian kết thúc:", value=str(row_cu.get('Thời gian kết thúc', '')))
            new_dd = st.text_input("Địa điểm:", value=row_cu['Địa điểm'])

            cp_gy_cu = True if pd.isna(row_cu.get('cho_phep_gop_y')) else bool(row_cu.get('cho_phep_gop_y'))
            new_cp_gy = st.checkbox("✅ Cho phép Đại biểu gửi Ý kiến / Tham luận trực tuyến", value=cp_gy_cu)

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            col_b1, col_b2 = st.columns(2)

            submitted_update = col_b1.form_submit_button("💾 CẬP NHẬT THÔNG TIN", use_container_width=True)
            submitted_delete = col_b2.form_submit_button("🗑️ XÓA CUỘC HỌP NÀY", use_container_width=True)

            if submitted_update:
                supabase.table("cuoc_hop").update({
                    "ten_ch": new_ten, "thoi_gian": new_bd,
                    "thoi_gian_ket_thuc": new_kt, "dia_diem": new_dd,
                    "cho_phep_gop_y": new_cp_gy
                }).eq("ma_ch", ma_sua).execute()
                st.success("✅ Đã cập nhật thông tin cuộc họp thành công!")
                st.cache_data.clear()
                st.rerun()

            if submitted_delete:
                try:
                    # 1. Xóa các ý kiến liên quan trong DB
                    supabase.table("y_kien").delete().eq("ma_ch", ma_sua).execute()
                    
                    # 2. Lấy danh sách tài liệu để xóa file vật lý trên Cloud
                    tl_cu = supabase.table("tai_lieu").select("link_file").eq("ma_ch", ma_sua).execute().data
                    for tl in tl_cu:
                        url = tl.get("link_file", "")
                        if url:
                            # Lấy tên file từ url
                            ten_file_tren_cloud = url.split('/')[-1]
                            supabase.storage.from_("kho-tai-lieu").remove([ten_file_tren_cloud])
                    
                    # 3. Xóa thông tin tài liệu và cuộc họp trong DB
                    supabase.table("tai_lieu").delete().eq("ma_ch", ma_sua).execute()
                    supabase.table("cuoc_hop").delete().eq("ma_ch", ma_sua).execute()
                    
                    st.warning(f"🗑️ Đã xóa cuộc họp '{row_cu['Tên cuộc họp']}' và dọn sạch toàn bộ tài liệu/ý kiến liên quan.")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi khi xóa: {e}")

# XIN LƯU Ý: LUÔN GIỮ DÒNG TRỐNG NÀY Ở CUỐI FILE ĐỂ TRÁNH LỖI TOKENIZER
