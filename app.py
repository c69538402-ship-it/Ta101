import base64
from pathlib import Path
import mimetypes
import streamlit as st
import random

st.set_page_config(
    page_title="TA101 • NEON SPACE MP3",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# จัดการค่าเริ่มต้นใน Session State
if "neon_color" not in st.session_state:
    st.session_state.neon_color = "#00f5ff" # สีฟ้าไซเบอร์
if "song_index" not in st.session_state:
    st.session_state.song_index = 0
if "loop_mode" not in st.session_state:
    st.session_state.loop_mode = False
if "shuffle_mode" not in st.session_state:
    st.session_state.shuffle_mode = False

theme_color = st.session_state.neon_color

# CSS ออกแบบสไตล์ Hi-Fi MP3 Player นีออนล้ำๆ
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
        font-size: 20px !important;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }}
    .subtitle {{
        text-align: center;
        color: #a5b4fc;
        font-size: 10px;
        letter-spacing: 3px;
        margin-bottom: 15px;
    }}
    .mp3-player-card {{
        background: rgba(10, 15, 35, 0.9);
        border: 2px solid {theme_color};
        box-shadow: 0 0 25px {theme_color}55, inset 0 0 15px {theme_color}22;
        border-radius: 24px;
        padding: 20px;
        backdrop-filter: blur(15px);
        margin-top: 10px;
        margin-bottom: 15px;
    }}
    .lcd-screen {{
        background: #02040a;
        border: 1px solid {theme_color};
        box-shadow: inset 0 0 10px {theme_color}44;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin-bottom: 15px;
    }}
    .badge {{
        display: inline-block;
        padding: 3px 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {theme_color};
        color: {theme_color};
        border-radius: 20px;
        font-size: 11px;
    }}
    .stButton>button {{
        width: 100%;
        background: linear-gradient(45deg, #0f1026, #1e1b4b);
        color: {theme_color};
        border: 1px solid {theme_color};
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        box-shadow: 0 0 8px {theme_color}33;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: {theme_color};
        color: #000;
        box-shadow: 0 0 15px {theme_color};
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>TA101 • HI-FI MP3</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">✦ NEON SPACE AUDIO SYSTEM ✦</div>', unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# 1. ค้นหาโลโก้และแสดงผล
logo_path = None
for candidate in ("logo1.jpg", "logo1.jpeg", "logo1.png", "โลโก้.jpg", "logo.jpg"):
    candidate_path = ROOT / candidate
    if candidate_path.is_file():
        logo_path = candidate_path
        break

if logo_path:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(str(logo_path), width=140, use_column_width=False)

# 2. แผงควบคุมเลือกธีมสีนีออนแนวนอน
st.markdown("<p style='text-align: center; font-size: 11px; color: #94a3b8; margin-bottom: 8px;'>⚙️ ปรับแต่งธีมสีเครื่องเล่น</p>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    if st.button("💙 ไซเบอร์ฟ้า"):
        st.session_state.neon_color = "#00f5ff"
        st.rerun()
with col_b2:
    if st.button("💚 เมทริกซ์เขียว"):
        st.session_state.neon_color = "#00ff88"
        st.rerun()
with col_b3:
    if st.button("💜 เลเซอร์ชมพู"):
        st.session_state.neon_color = "#ff00d4"
        st.rerun()

# 3. ค้นหาไฟล์เพลงทั้งหมด
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        songs.append({"name": path.stem, "path": path})

if not songs:
    st.warning("⚠️ ไม่พบไฟล์เพลง (.mp3, .wav ฯลฯ) ในโฟลเดอร์โปรเจกต์ กรุณาอัปโหลดไฟล์เพลงไว้ข้างไฟล์ app.py")
else:
    st.markdown('<div class="mp3-player-card">', unsafe_allow_html=True)
    
    # แสดงสถิติเครื่องเล่น MP3
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f'<span class="badge">📂 แทร็ก {st.session_state.song_index + 1} / {len(songs)}</span>', unsafe_allow_html=True)
    with col_info2:
        mode_text = "🔁 วนซ้ำ: เปิด" if st.session_state.loop_mode else "🔁 วนซ้ำ: ปิด"
        st.markdown(f'<div style="text-align: right;"><span class="badge">{mode_text}</span></div>', unsafe_allow_html=True)

    # เลือกแทร็กเพลงผ่าน Dropdown
    song_names = [f"{i+1}. {s['name']}" for i, s in enumerate(songs)]
    
    selected_label = st.selectbox(
        "🎧 เลือกเพลงจากเพลย์ลิสต์:",
        song_names,
        index=st.session_state.song_index
    )

    selected_index = song_names.index(selected_label)
    if selected_index != st.session_state.song_index:
        st.session_state.song_index = selected_index
        st.rerun()

    current_song = songs[st.session_state.song_index]

    # หน้าจอ LCD จำลองแสดงเพลงที่กำลังเล่น
    st.markdown(f"""
        <div class="lcd-screen">
            <div style="font-size: 10px; color: #a5b4fc; letter-spacing: 2px; margin-bottom: 4px;">NOW PLAYING MP3</div>
            <div style="color: {theme_color}; font-weight: bold; font-size: 14px; text-shadow: 0 0 8px {theme_color};">🎵 {current_song['name']}</div>
        </div>
    """, unsafe_allow_html=True)

    # ตัวเล่นเสียง Streamlit MP3
    audio_bytes = current_song["path"].read_bytes()
    mime_type = mimetypes.guess_type(current_song["path"].name)[0] or "audio/mpeg"
    st.audio(audio_bytes, format=mime_type)

    # 4. แผงปุ่มควบคุมสไตล์เครื่องเล่น MP3 (ก่อนหน้า, สุ่ม, วนซ้ำ, ถัดไป)
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)
    
    with col_ctrl1:
        if st.button("⏮ ก่อนหน้า"):
            st
            
