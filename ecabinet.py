import streamlit as st
import pandas as pd
import re
import base64
import uuid
from datetime import datetime, timedelta
from supabase import create_client, Client

st.set_page_config(page_title="E-Cabinet TGDV - Tuyên Quang", page_icon="🏛️", layout="wide")

# ==========================================
# CẤU HÌNH SUPABASE (ĐỘNG CƠ TÊN LỬA)
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

# --- CSS NÂNG CẤP GIAO DIỆN ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .header-box { background-color: #ffffff; border-top: 4px solid #17a2b8; border-radius: 8px; padding: 15px 30px; margin-bottom: 30px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;}
    .main-title { font-size: 24px; font-weight: 900; color: #2c3e50; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    .featured-card { background-color: #ffffff; border: 1px solid #e0e6ed; border-top: 4px solid #17a2b8; border-radius: 8px; padding: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.03); display: flex; flex-direction: column; transition: transform 0.2s ease, box-shadow 0.2s ease; margin-bottom: 8px;}
    .featured-card:hover { transform: translateY(-2px); box-shadow: 0px 6px 15px rgba(0,0,0,0.08); }
    .featured-title { color: #2c3e50; font-size: 16px; font-weight: bold; margin: 12px 0; line-height: 1.4; flex-grow: 1; text-align: left; }
    .featured-details { color: #6c757d; font-size: 13px; border-top: 1px dashed #dee2e6; padding-top: 12px; text-align: left; line-height: 1.6; }
    .tag-sap-dien-ra { background-color: #17a2b8; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block;}
    .tag-dang-dien-ra { background-color: #C8102E; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block; animation: blinker 1.5s linear infinite;}
    .tag-da-ket-thuc { background-color: #6c757d; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; display: inline-block;}
    @keyframes blinker { 50% { opacity: 0.6; } }
    div[data-testid="stForm"] { background-color: #ffffff; border: 1px solid #e0e6ed; border-radius: 8px; padding: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.03);}
    div.stButton > button[kind="primary"], div.stButton > button[kind="formSubmit"] { background-color: #17a2b8; color: white; border: none; border-radius: 6px; font-weight: bold;}
    div.stButton > button[kind="primary"]:hover, div.stButton > button[kind="formSubmit"]:hover { background-color: #138496; color: white;}
    div.stButton > button[kind="secondary"] { background-color: #ffffff !important; color: #17a2b8 !important; border: 2px solid #17a2b8 !important; border-radius: 8px !important; padding: 8px 15px !important; font-size: 14px !important; font-weight: bold !important; transition: all 0.3s ease !important;}
    div.stButton > button[kind="secondary"]:hover { background-color: #17a2b8 !important; color: #ffffff !important;}
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

@st.cache_data(ttl=15)
def load_data():
    try:
        ch = supabase.table("cuoc_hop").select("*").execute().data
        tl = supabase.table("tai_lieu").select("*").execute().data
        yk = supabase.table("y_kien").select("*").execute().data
        
        df_ch = pd.DataFrame(ch).rename(columns={'ma_ch': 'Mã cuộc họp', 'ten_ch': 'Tên cuộc họp', 'thoi_gian': 'Thời gian', 'dia_diem': 'Địa điểm', 'trang_thai': 'Trạng thái'})
        df_tl = pd.DataFrame(tl).rename(columns={'ma_ch': 'Mã cuộc họp', 'ma_tl': 'Mã tài liệu', 'ten_tl': 'Tên tài liệu', 'loai_tl': 'Loại tài liệu', 'link_file': 'Link Google Drive'})
        df_yk = pd.DataFrame(yk).rename(columns={'ma_ch': 'Mã cuộc họp', 'nguoi_gop_y': 'Tên đơn vị / Đại biểu', 'noi_dung': 'Nội dung góp ý', 'link_file': 'Link File sửa đổi', 'created_at': 'Thời gian gửi'})
        
        if not df_yk.empty and 'Thời gian gửi' in df_yk.columns:
            df_yk['Thời gian gửi'] = pd.to_datetime(df_yk['Thời gian gửi']).dt.tz_convert('Asia/Ho_Chi_Minh').dt.strftime("%H:%M %d/%m/%Y")
            
        return {"cuoc_hop": df_ch, "tai_lieu": df_tl, "y_kien": df_yk}
    except Exception as e:
        return {"cuoc_hop": pd.DataFrame(), "tai_lieu": pd.DataFrame(), "y_kien": pd.DataFrame()}

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
if "meeting_name_temp" not in st.session_state: st.session_state["meeting_name_temp"] = None

data_dict = load_data()
df_cuoc_hop = data_dict.get("cuoc_hop", pd.DataFrame())
df_tai_lieu = data_dict.get("tai_lieu", pd.DataFrame())
df_y_kien = data_dict.get("y_kien", pd.DataFrame())

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
                
                if st.button("🚀 VÀO PHÒNG HỌP NÀY", key=f"btn_{row['Mã cuộc họp']}", type="secondary", use_container_width=True):
                    st.session_state["selected_meeting_id"] = row['Mã cuộc họp']
                    st.session_state["meeting_name_temp"] = row['Tên cuộc họp']
                    st.rerun()
    
    st.write("---")
    
    col_login1, col_login2, col_login3 = st.columns([1.5, 2.5, 1.5])
    with col_login2:
        if st.session_state.get("selected_meeting_id"):
            ten_ch_dang_chon = ""
            if not df_cuoc_hop.empty:
                match_ch = df_cuoc_hop[df_cuoc_hop['Mã cuộc họp'] == st.session_state['selected_meeting_id']]
                if not match_ch.empty: ten_ch_dang_chon = match_ch.iloc[0]['Tên cuộc họp']
            if ten_ch_dang_chon: st.success(f"✅ Bạn đang chọn: **{ten_ch_dang_chon}**. Vui lòng nhập mật khẩu để vào phòng họp!")
            
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span style="font-size: 28px;">🔐</span><br><b style="color: #2c3e50; font-size: 16px;">XÁC THỰC QUYỀN TRUY CẬP</b></div>', unsafe_allow_html=True)
            pwd = st.text_input("Nhập mật khẩu", type="password", placeholder="Nhập mật khẩu tại đây...", label_visibility="collapsed")
            
            if st.form_submit_button("🚀 ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
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

if st.sidebar.button("🔄 Làm mới Dữ liệu", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
    
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
                        # --- THUẬT TOÁN TÍCH HỢP BỘ ĐỌC VĂN BẢN TRỰC TUYẾN ---
                        file_url = str(row.get("Link Google Drive", ""))
                        view_url = file_url
                        
                        # Mượn bộ đọc của MS Office nếu là file Word, Excel, PPT
                        if any(ext in file_url.lower() for ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']):
                            view_url = f"https://view.officeapps.live.com/op/view.aspx?src={file_url}"
                            
                        st.markdown(f"""
                        <div class="doc-card">
                            <div class="doc-title" style="color: #2c3e50; font-size: 15px; margin-bottom: 12px;">📄 {row.get("Tên tài liệu")}</div>
                            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                                <a href="{view_url}" target="_blank" style="background: #e0f7fa; border: 1px solid #17a2b8; color: #17a2b8; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; text-decoration: none;">👁️ XEM TRỰC TIẾP</a>
                                <a href="{file_url}" target="_blank" style="background: #fff5f5; border: 1px solid #C8102E; color: #C8102E; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; text-decoration: none;">⬇️ TẢI VỀ</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

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
                                with st.spinner("Đang xử lý..."):
                                    nguoi_gui = f"{ho_ten} ({c_v} - {d_v})"
                                    public_url = ""
                                    if file_up is not None:
                                        try:
                                            file_ext = file_up.name.split('.')[-1] if '.' in file_up.name else 'bin'
                                            safe_name = f"YKien_{ma_ch}_{datetime.now().strftime('%H%M%S')}_{uuid.uuid4().hex[:6]}.{file_ext}"
                                            supabase.storage.from_("kho-tai-lieu").upload(path=safe_name, file=file_up.getvalue(), file_options={"content-type": file_up.type})
                                            public_url = supabase.storage.from_("kho-tai-lieu").get_public_url(safe_name)
                                        except Exception as e:
                                            st.error(f"⚠️ Lỗi tải file đính kèm: {e}"); st.stop()
                                    
                                    try:
                                        supabase.table("y_kien").insert({"ma_ch": ma_ch, "nguoi_gop_y": nguoi_gui, "noi_dung": noi_dung, "link_file": public_url}).execute()
                                        st.success("✅ Thành công!"); st.cache_data.clear()
                                    except Exception as e: st.error(f"⚠️ Lỗi lưu ý kiến: {e}")
                with tab_xem:
                    yk_cua_hop = df_y_kien[df_y_kien['Mã cuộc họp'] == ma_ch] if not df_y_kien.empty else pd.DataFrame()
                    if yk_cua_hop.empty: st.info("Chưa có ý kiến.")
                    else:
                        for _, row in yk_cua_hop.iterrows():
                            with st.expander(f"💬 {row.get('Tên đơn vị / Đại biểu')} - {row.get('Thời gian gửi')}"):
                                st.write(row.get('Nội dung góp ý'))
                                if row.get('Link File sửa đổi'): st.markdown(f"[📥 Xem file đính kèm]({row.get('Link File sửa đổi')})")

elif menu == "⚙️ Quản trị: Tạo Cuộc họp":
    st.markdown('<div class="section-title">➕ TẠO CUỘC HỌP MỚI</div>', unsafe_allow_html=True)
    st.info("💡 Bạn BẮT BUỘC phải nhập Thời gian đúng chuẩn định dạng: HH:MM, DD/MM/YYYY")
    
    with st.form("form_tao_hop", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1: ma_ch = st.text_input("Mã Cuộc họp (VD: CH01)*:")
        with col2: ten_ch = st.text_input("Tên Cuộc họp / Hội nghị*:")
        col3, col4 = st.columns(2)
        with col3: thoi_gian = st.text_input("Thời gian*", placeholder="Ví dụ: 08:30, 20/05/2026")
        with col4: dia_diem = st.text_input("Địa điểm:")
        
        if st.form_submit_button("LƯU CUỘC HỌP MỚI"):
            pattern = r"^\d{2}:\d{2}, \d{2}/\d{2}/\d{4}$"
            if not ma_ch or not ten_ch: st.error("⚠️ Vui lòng nhập Mã và Tên cuộc họp!")
            elif not re.match(pattern, thoi_gian.strip()): st.error("⚠️ Thời gian sai định dạng! Ví dụ đúng: 08:30, 20/05/2026")
            else:
                with st.spinner("Đang lưu vào Supabase..."):
                    try:
                        supabase.table("cuoc_hop").insert({"ma_ch": ma_ch, "ten_ch": ten_ch, "thoi_gian": thoi_gian, "dia_diem": dia_diem, "trang_thai": "Tự động"}).execute()
                        st.success("✅ Đã tạo cuộc họp thành công!"); st.cache_data.clear()
                    except Exception as e: st.error(f"⚠️ Lỗi lưu dữ liệu: {e}")

elif menu == "📤 Quản trị: Đăng Tài liệu":
    st.markdown('<div class="section-title">📤 UPLOAD TÀI LIỆU LÊN HỆ THỐNG</div>', unsafe_allow_html=True)
    if df_cuoc_hop.empty: st.warning("⚠️ Bạn cần tạo Cuộc họp trước.")
    else:
        with st.form("form_tai_lieu", clear_on_submit=True):
            ds_cuoc_hop_hien_thi = df_cuoc_hop['Mã cuộc họp'] + " - " + df_cuoc_hop['Tên cuộc họp']
            ch_chon = st.selectbox("📌 Gắn vào Cuộc họp:", ds_cuoc_hop_hien_thi.tolist())
            uploaded_files = st.file_uploader("📂 Chọn nhiều File cùng lúc:", type=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"], accept_multiple_files=True)
            
            if st.form_submit_button("🚀 TẢI LÊN VÀ PHÁT HÀNH TÀI LIỆU"):
                if not uploaded_files: st.error("⚠️ Chọn ít nhất 1 file!")
                else:
                    ma_ch = ch_chon.split(" - ")[0]
                    thanh_cong = 0
                    progress_bar = st.progress(0, text="Bắt đầu tải file...")
                    
                    for i, file_up in enumerate(uploaded_files):
                        try:
                            file_ext = file_up.name.split('.')[-1] if '.' in file_up.name else 'bin'
                            safe_name = f"{ma_ch}_{datetime.now().strftime('%H%M%S')}_{uuid.uuid4().hex[:6]}.{file_ext}"
                            
                            supabase.storage.from_("kho-tai-lieu").upload(path=safe_name, file=file_up.getvalue(), file_options={"content-type": file_up.type})
                            public_url = supabase.storage.from_("kho-tai-lieu").get_public_url(safe_name)
                            
                            supabase.table("tai_lieu").insert({"ma_ch": ma_ch, "ma_tl": f"TL{datetime.now().strftime('%H%M%S')}{i}", "ten_tl": file_up.name, "loai_tl": "", "link_file": public_url}).execute()
                            thanh_cong += 1
                        except Exception as e: st.error(f"⚠️ Lỗi khi tải file '{file_up.name}': {e}")
                            
                        progress_bar.progress(int(((i + 1) / len(uploaded_files)) * 100), text=f"Đang xử lý: {i+1}/{len(uploaded_files)} file...")
                    
                    if thanh_cong > 0:
                        st.success(f"✅ Tải lên hoàn tất ({thanh_cong}/{len(uploaded_files)} file)!"); st.cache_data.clear()
