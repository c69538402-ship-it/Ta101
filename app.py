import base64
from pathlib import Path
import mimetypes
import streamlit as st

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# จัดการธีมสีใน Session State
if "neon_color" not in st.session_state:
    st.session_state.neon_color = "#00f5ff" # ค่าเริ่มต้นสีฟ้า

theme_color = st.session_state.neon_color

# ตกแต่ง CSS นีออนแบบจัดเต็ม
st.markdown(f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at center, #0a0d24 0%, #03040c 60%, #010206 100%);
        color: #ffffff;
        font-family: 'Prompt', sans-serif;
    }}
    h1 {{
        font-family: 'Orbitron', sans-serif;
        color: {theme_color};
        text-shadow: 0 0 15px {theme_color}, 0 0 30px #7000ff;
        text-align: center;
        font-size: 22px !important;
        letter-spacing: 2px;
    }}
    .subtitle {{
        text-align: center;
        color: #a5b4fc;
        font-size: 11px;
        letter-spacing: 3px;
        margin-bottom: 20px;
    }}
    .neon-card {{
        background: rgba(10, 15, 35, 0.85);
        border: 2px solid {theme_color};
        box-shadow: 0 0 25px {theme_color}55, inset 0 0 15px {theme_color}33;
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(12px);
        margin-bottom: 15px;
    }}
    .stButton>button {{
        width: 100%;
        background: linear-gradient(45deg, #1e1b4b, #311042);
        color: {theme_color};
        border: 1px solid {theme_color};
        border-radius: 12px;
        font-weight: bold;
        box-shadow: 0 0 10px {theme_color}44;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: {theme_color};
        color: #000;
        box-shadow: 0 0 20px {theme_color};
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>TA101 • NEON SPACE</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">✦ ADVANCED COSMIC AUDIO EXPERIENCE ✦</div>', unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# 1. ค้นหาโลโก้และแสดงผลพร้อมกรอบนีออน
logo_path = None
for candidate in ("logo1.jpg", "logo1.jpeg", "logo1.png", "โลโก้.jpg", "logo.jpg"):
    candidate_path = ROOT / candidate
    if candidate_path.is_file():
        logo_path = candidate_path
        break

if logo_path:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(logo_path), width=160, use_column_width=False)

# 2. ลูกเล่น: ปุ่มเปลี่ยนธีมสีนีออนด้านบน
st.markdown("<p style='text-align: center; font-size: 12px; color: #94a3b8; margin-bottom: 5px;'>เลือกโทนสีนีออนอวกาศ</p>", unsafe_allow_html=True)
col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    if st.button("💙 ไซเบอร์ฟ้า"):
        st.session_state.neon_color = "#00f5ff"
        st.rerun()
with col_c2:
    if st.button("💚 เมทริกซ์เขียว"):
        st.session_state.neon_color = "#00ff88"
        st.rerun()
with col_c3:
    if st.button("💜 เลเซอร์ชมพู"):
        st.session_state.neon_color = "#ff00d4"
        st.rerun()

# 3. ค้นหาไฟล์เพลงทั้งหมดในโฟลเดอร์
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        songs.append({"name": path.stem, "path": path})

if not songs:
    st.warning("⚠️ ไม่พบไฟล์เพลง (.mp3, .wav ฯลฯ) ในโฟลเดอร์โปรเจกต์ กรุณาอัปโหลดไฟล์เพลงไว้ข้างไฟล์ app.py")
else:
    # จัดการ State เพลง
    if "song_index" not in st.session_state:
        st.session_state.song_index = 0

    st.markdown('<div class="neon-card">', unsafe_allow_html=True)

    # รายชื่อเพลงสำหรับ Selectbox
    song_names = [f"{i+1}. {s['name']}" for i, s in enumerate(songs)]
    
    selected_label = st.selectbox(
        "🎧 เลือกแทร็กเพลงในเพลย์ลิสต์:",
        song_names,
        index=st.session_state.song_index
    )

    # อัปเดต Index เมื่อผู้ใช้เลือกจาก Dropdown
    selected_index = song_names.index(selected_label)
    if selected_index != st.session_state.song_index:
        st.session_state.song_index = selected_index
        st.rerun()

    current_song = songs[st.session_state.song_index]

    st.markdown(f"<h4 style='color: {theme_color}; text-align: center; font-size: 15px;'>🎵 กำลังเล่น: {current_song['name']}</h4>", unsafe_allow_html=True)

    # ตัวเล่นเสียง
    audio_bytes = current_song["path"].read_bytes()
    mime_type = mimetypes.guess_type(current_song["path"].name)[0] or "audio/mpeg"
    st.audio(audio_bytes, format=mime_type)

    # 4. เพิ่มปุ่มควบคุมย้อนกลับ / ถัดไป แบบปลอดภัยไม่ติดบั๊ก DOM
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⏮ เพลงก่อนหน้า"):
            st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
            st.rerun()
    with col_next:
        if st.button("⏭ เพลงถัดไป"):
            st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ส่วนท้าย
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 10px; color: #64748b; letter-spacing: 2px;'>TA101 NEON SPACE • STABLE & IMMERSIVE</p>", unsafe_allow_html=True)
