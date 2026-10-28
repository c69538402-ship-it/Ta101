import base64
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC", page_icon="🌌", layout="centered"
)

# จัดการ State สำหรับเปลี่ยนธีมสีนีออน
if "theme_color" not in st.session_state:
  st.session_state.theme_color = "#00f5ff"
if "theme_glow" not in st.session_state:
  st.session_state.theme_glow = "#bd00ff"

# ฟังก์ชันเลือกธีม
col_t1, col_t2, col_t3, col_t4 = st.columns(4)
with col_t1:
  if st.button("🔵 ซียอน"):
    st.session_state.theme_color = "#00f5ff"
    st.session_state.theme_glow = "#bd00ff"
with col_t2:
  if st.button("🟢 เมทริกซ์"):
    st.session_state.theme_color = "#00ff82"
    st.session_state.theme_glow = "#0055ff"
with col_t3:
  if st.button("🟠 โซลาร์"):
    st.session_state.theme_color = "#ff7a00"
    st.session_state.theme_glow = "#ff006e"
with col_t4:
  if st.button("🟣 ไวโอเล็ต"):
    st.session_state.theme_color = "#e8f5ff"
    st.session_state.theme_glow = "#9900ff"

tc = st.session_state.theme_color
tg = st.session_state.theme_glow

# สไตล์ตกแต่งนีออนอวกาศพร้อมอนิเมชันกระพริบ
st.markdown(
    f"""
    <style>
    .stApp {{
        background: radial-gradient(ellipse at 50% 45%, #10133c 0%, #050615 48%, #010208 100%);
        color: #ffffff;
        font-family: 'Prompt', sans-serif;
    }
    h1 {{
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: {tc};
        text-shadow: 0 0 10px {tc}, 0 0 25px {tg};
        font-size: 1.8rem !important;
        margin-bottom: 0px;
        animation: flicker 3s infinite alternate;
    }}
    @keyframes flicker {{
        0% {{ opacity: 0.8; }}
        100% {{ opacity: 1; text-shadow: 0 0 15px {tc}, 0 0 35px {tg}; }}
    }}
    .subtitle {{
        text-align: center;
        font-size: 0.75rem;
        color: #aeb9dc;
        letter-spacing: 3px;
        margin-bottom: 15px;
    }}
    .logo-box {{
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }}
    .neon-card {{
        border: 2px solid {tc};
        border-radius: 20px;
        padding: 20px;
        background: rgba(5, 8, 25, 0.75);
        box-shadow: 0 0 20px {tc}44, inset 0 0 15px {tg}22;
        backdrop-filter: blur(10px);
        margin-top: 10px;
    }}
    .stSelectbox label {{
        color: {tc} !important;
        font-weight: bold;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("<h1>TA101 • NEON MUSIC</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>3D COSMIC AUDIO EXPERIENCE & VIBES</div>",
    unsafe_allow_html=True,
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# 1. ค้นหาไฟล์เพลง MP3 ทั้งหมด
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
  if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
    songs.append(path)

# 2. ค้นหารูปโลโก้
logo_path = None
for candidate in (
    "logo1.jpg",
    "logo1.jpeg",
    "logo1.png",
    "โลโก้.jpg",
    "logo.jpg",
):
  p = ROOT / candidate
  if p.is_file():
    logo_path = p
    break

# แสดงผลในกรอบการ์ดนีออน
with st.container():
  st.markdown("<div class='neon-card'>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    if logo_path:
      st.image(str(logo_path), use_container_width=True)
    else:
      st.markdown(
          f"<div style='text-align:center; color:{tc}; border:2px solid"
          f" {tc}; border-radius:50%; padding:35px; box-shadow:0 0 20px"
          f" {tc};'><b>TA101<br>NEON SPACE</b></div>",
          unsafe_allow_html=True,
      )

  st.write("")

  if not songs:
    st.warning(
        "⚠️ ไม่พบไฟล์เพลง .mp3 ในโฟลเดอร์หลัก กรุณานำไฟล์เพลงมาวางไว้หน้าเดียวกับ"
        " app.py"
    )
  else:
    # เลือกเพลง
    song_names = [s.stem for s in songs]
    selected_song_name = st.selectbox("🎵 เลือกเพลงในเพลย์ลิสต์", song_names)

    selected_index = song_names.index(selected_song_name)
    selected_file = songs[selected_index]

    st.write("")

    # เครื่องเล่นเพลง
    audio_bytes = selected_file.read_bytes()
    st.audio(audio_bytes, format="audio/mp3")

  st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.75rem; color:"
    " #7380b8;'>SPACE • LIGHT • SOUND • 1.618 ENERGY</div>",
    unsafe_allow_html=True,
)
