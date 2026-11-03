import base64
from pathlib import Path
import mimetypes
import streamlit as st
import random

st.set_page_config(
    page_title="TA101 • MULTI-DIMENSIONAL NEON SPACE",
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

# CSS ออกแบบหน้าแอปให้มีหลายมิติ (Multi-Dimensional Depth & 3D Hologram Effect)
st.markdown(f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at center, #0f133a 0%, #050716 50%, #010208 100%);
        color: #ffffff;
        font-family: 'Prompt', sans-serif;
    }}
    h1 {{
        font-family: 'Orbitron', sans-serif;
        color: {theme_color};
        text-shadow: 0 0 10px {theme_color}, 0 0 25px {theme_color}, 0 0 40px #7000ff;
        text-align: center;
        font-size: 21px !important;
        letter-spacing: 3px;
        margin-bottom: 0px;
    }}
    .subtitle {{
        text-align: center;
        color: #a5b4fc;
        font-size: 10px;
        letter-spacing: 4px;
        margin-bottom: 15px;
        text-shadow: 0 0 5px rgba(165,180,252,0.5);
    }}
    /* เอฟเฟกต์โฮโลแกรมโลโก้ลอยตัว (Floating Animation) */
    .hologram-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }}
    .hologram-box {{
        width: 130px;
        height: 130px;
        border-radius: 50%;
        border: 2px solid {theme_color};
        box-shadow: 0 0 20px {theme_color}, inset 0 0 15px {theme_color}, 0 15px 25px rgba(0,0,0,0.8);
        overflow: hidden;
        animation: float 3s ease-in-out infinite;
        background: #02040a;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0px) scale(1); box-shadow: 0 0 15px {theme_color}, inset 0 0 15px {theme_color}; }}
        50% {{ transform: translateY(-8px) scale(1.02); box-shadow: 0 0 30px {theme_color}, inset 0 0 25px {theme_color}; }}
        100% {{ transform: translateY(0px) scale(1); box-shadow: 0 0 15px {theme_color}, inset 0 0 15px {theme_color}; }}
    }}
    .hologram-box img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    /* กล่องเครื่องเล่นมิติซ้อน (Multi-Layer Card) */
    .mp3-player-card {{
        background: rgba(8, 12, 30, 0.85);
        border: 2px solid {theme_color};
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9), 0 0 25px {theme_color}66, inset 0 0 20px {theme_color}33;
        border-radius: 24px;
        padding: 20px;
        backdrop-filter: blur(15px);
        margin-top: 5px;
        margin-bottom: 15px;
    }}
    /* หน้าจอ LCD มิติเชิงลึก */
    .lcd-screen {{
        background: linear-gradient(135deg, #010308 0%, #0a0f24 100%);
        border: 1px solid {theme_color};
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9), 0 0 10px {theme_color}44;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        margin-bottom: 15px;
    }}
    /* แถบคลื่นเสียง 3 มิติ */
    .equalizer {{
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 5px;
        height: 28px;
        margin-top: 10px;
    }}
    .bar {{
        width: 5px;
        background: linear-gradient(to top, #02040a, {theme_color});
        box-shadow: 0 0 10px {theme_color};
        border-radius: 3px;
        animation: bounce 0.8s infinite ease-in-out alternate;
    }}
    .bar:nth-child(1) {{ animation-delay: 0.1s; height: 12px; }}
    .bar:nth-child(2) {{ animation-delay: 0.3s; height: 22px; }}
    .bar:nth-child(3) {{ animation-delay: 0.2s; height: 16px; }}
    .bar:nth-child(4) {{ animation-delay: 0.5s; height: 26px; }}
    .bar:nth-child(5) {{ animation-delay: 0.2s; height: 20px; }}
    .bar:nth-child(6) {{ animation-delay: 0.4s; height: 14px; }}
    .bar:nth-child(7) {{ animation-delay: 0.1s; height: 24px; }}
    
    @keyframes bounce {{
        0% {{ transform: scaleY(0.3); opacity: 0.4; }}
        100% {{ transform: scaleY(1.25); opacity: 1; filter: drop-shadow(0 0 8px {theme_color}); }}
    }}

    .badge {{
        display: inline-block;
        padding: 4px 12px;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid {theme_color};
        color: {theme_color};
        border-radius: 20px;
        font-size: 11px;
        box-shadow: inset 0 0 5px {theme_color}44;
    }}
    /* ปุ่มกดสไตล์ 3D นูนต่ำ */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #101535 0%, #070a1a 100%);
        color: {theme_color};
        border: 1px solid {theme_color};
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.6), 0 0 8px {theme_color}44;
        transition: 0.2s;
    }}
    .stButton>button:hover {{
        background: {theme_color};
        color: #000;
        box-shadow: 0 6px 15px rgba(0,0,0,0.8), 0 0 20px {theme_color};
        transform: translateY(-2px);
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>TA101 • MULTI-DIMENSION</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">✦ HOLOGRAPHIC SPACE AUDIO SYSTEM ✦</div>', unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# 1. ค้นหาโลโก้และแสดงผลด้วยเอฟเฟกต์โฮโลแกรมลอยตัว
logo_path = None
for candidate in ("logo1.jpg", "logo1.jpeg", "logo1.png", "โลโก้.jpg", "logo.jpg"):
    candidate_path = ROOT / candidate
    if candidate_path.is_file():
        logo_path = candidate_path
        break

if logo_path:
    encoded_logo = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    mime_logo = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
    st.markdown(f"""
        <div class="hologram-container">
            <div class="hologram-box">
                <img src="data:{mime_logo};base64,{encoded_logo}" alt="Logo">
            </div>
        </div>
    """, unsafe_allow_html=True)

# 2. แผงเปลี่ยนธีมสีนีออนแนวนอน
st.markdown("<p style='text-align: center; font-size: 11px; color: #94a3b8; margin-bottom: 8px;'>🌌 เลือกระบบมิติแสงสี</p>", unsafe_allow_html=True)
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
    
    # สถิติแทร็ก
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f'<span class="badge">📂 แทร็ก {st.session_state.song_index + 1} / {len(songs)}</span>', unsafe_allow_html=True)
    with col_info2:
        mode_text = "🔁 วนซ้ำ: เปิด" if st.session_state.loop_mode else "🔁 วนซ้ำ: ปิด"
        st.markdown(f'<div style="text-align: right;"><span class="badge">{mode_text}</span></div>', unsafe_allow_html=True)

    # เลือกเพลงผ่าน Dropdown
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

    # หน้าจอ LCD มิติเชิงลึก + คลื่นเสียง 3 มิติ
    st.markdown(f"""
        <div class="lcd-screen">
            <div style="font-size: 9px; color: #a5b4fc; letter-spacing: 3px; margin-bottom: 4px;">HOLOGRAPHIC STREAM</div>
            <div style="color: {theme_color}; font-weight: bold; font-size: 14px; text-shadow: 0 0 10px {theme_color};">🎵 {current_song['name']}</div>
            
            <div class="equalizer">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ตัวเล่นเสียง Streamlit
    audio_bytes = current_song["path"].read_bytes()
    mime_type = mimetypes.guess_type(current_song["path"].name)[0] or "audio/mpeg"
    st.audio(audio_bytes, format=mime_type)

    # 4. ปุ่มควบคุม 3 มิติ (ก่อนหน้า, สุ่ม, วนซ้ำ, ถัดไป)
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)
    
    with col_ctrl1:
        if st.button("⏮ ก่อนหน้า"):
            st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
            st.rerun()
            
    with col_ctrl2:
        shuffle_label = "🔀 สุ่ม: เปิด" if st.session_state.shuffle_mode else "🔀 สุ่ม: ปิด"
        if st.button(shuffle_label):
            st.session_state.shuffle_mode = not st.session_state.shuffle_mode
            if st.session_state.shuffle_mode:
                st.session_state.song_index = random.randint(0, len(songs) - 1)
            st.rerun()
            
    with col_ctrl3:
        loop_label = "🔁 วนซ้ำ" if not st.session_state.loop_mode else "⏹ หยุดวน"
        if st.button(loop_label):
            st.session_state.loop_mode = not st.session_state.loop_mode
            st.rerun()
            
    with col_ctrl4:
        if st.button("ถัดไป ⏭"):
            if st.session_state.shuffle_mode:
                st.session_state.song_index = random.randint(0, len(songs) - 1)
            else:
                st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ส่วนท้าย
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 9px; color: #64748b; letter-spacing: 2px;'>TA101 3D MULTI-DIMENSIONAL AUDIO ENGINE • STABLE</p>", unsafe_allow_html=True)
