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

# ธีมและการตกแต่ง CSS นีออน
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at center, #10133c 0%, #050615 50%, #010208 100%);
        color: #ffffff;
        font-family: 'Prompt', sans-serif;
    }
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #00f5ff;
        text-shadow: 0 0 10px #00f5ff, 0 0 20px #bd00ff;
        text-align: center;
        font-size: 22px !important;
    }
    .subtitle {
        text-align: center;
        color: #a5b4fc;
        font-size: 11px;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    .neon-card {
        background: rgba(10, 14, 35, 0.75);
        border: 1px solid rgba(0, 245, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.15);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1>TA101 • NEON SPACE MUSIC</h1>", unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">✦ COSMIC AUDIO EXPERIENCE WITH STABLE MODE ✦</div>',
    unsafe_allow_html=True,
)

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
  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.image(str(logo_path), width=180, use_column_width=False)

# 2. ค้นหาไฟล์เพลงทั้งหมดในโฟลเดอร์
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
  if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
    songs.append({"name": path.stem, "path": path})

if not songs:
  st.warning(
      "⚠️ ไม่พบไฟล์เพลง (.mp3, .wav ฯลฯ) ในโฟลเดอร์โปรเจกต์ กรุณาอัปโหลดไฟล์เพลง"
      " ไว้ข้างไฟล์ app.py"
  )
else:
  # กำหนดค่าเริ่มต้นให้กับ Session State
  if "song_index" not in st.session_state:
    st.session_state.song_index = 0

  st.markdown('<div class="neon-card">', unsafe_allow_html=True)

  # เลือกเพลงผ่าน Selectbox โดยผูกกับ index ใน session_state โดยตรง
  song_names = [f"{i+1}. {s['name']}" for i, s in enumerate(songs)]
  
  def update_song():
    st.session_state.song_index = song_names.index(st.session_state.selectbox_key)

  selected_label = st.selectbox(
      "🎧 เลือกแทร็กเพลงในเพลย์ลิสต์:",
      song_names,
      index=st.session_state.song_index,
      key="selectbox_key",
      on_change=update_song
  )

  current_song = songs[st.session_state.song_index]

  st.markdown(f"### 🎵 กำลังเล่น: {current_song['name']}")

  # ตัวเล่นเสียงมาตรฐานแบบปลอดภัย (ไม่ใช้ st.rerun ที่ทำให้ DOM พัง)
  audio_bytes = current_song["path"].read_bytes()
  mime_type = mimetypes.guess_type(current_song["path"].name)[0] or "audio/mpeg"
  st.audio(audio_bytes, format=mime_type)

  st.markdown("</div>", unsafe_allow_html=True)

# ส่วนท้ายสไตล์อวกาศ
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 10px; color: #94a3b8; "
    "letter-spacing: 2px;'>SPACE • LIGHT • SOUND • 1.618 ENERGY</p>",
    unsafe_allow_html=True,
)
