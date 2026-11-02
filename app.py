
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

# ตกแต่งธีมหน้าเว็บด้วย CSS เบาๆ ให้เป็นแนวอวกาศนีออน
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
        font-size: 24px !important;
    }
    .subtitle {
        text-align: center;
        color: #a5b4fc;
        font-size: 12px;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1>TA101 • NEON SPACE MUSIC</h1>", unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">3D COSMIC AUDIO EXPERIENCE (STABLE MODE)</div>',
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

# 2. ค้นหาไฟล์เพลงทั้งหมด
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
  if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
    songs.append({"name": path.stem, "path": path})

if not songs:
  st.warning(
      "⚠️ ไม่พบไฟล์เพลง (.mp3, .wav ฯลฯ) ในโฟลเดอร์โปรเจกต์ กรุณาอัปโหลดไฟล์เพลงไว้ข้างไฟล์ app.py"
  )
else:
  # 3. เลือกเพลงผ่าน Selectbox (ใช้งานง่าย ไม่หลุด ไม่จอดำ)
  song_names = [f"{i+1}. {s['name']}" for i, s in enumerate(songs)]
  selected_song_label = st.selectbox("เลือกเพลง:", song_names)

  # หา index ของเพลงที่เลือก
  selected_index = song_names.index(selected_song_label)
  current_song = songs[selected_index]

  st.markdown(f"### 🎵 กำลังเล่น: {current_song['name']}")

  # 4. ตัวเล่นเสียงมาตรฐานของ Streamlit รองรับมือถือและคอมพิวเตอร์สมบูรณ์แบบ
  audio_bytes = current_song["path"].read_bytes()
  mime_type = mimetypes.guess_type(current_song["path"].name)[0] or "audio/mpeg"
  st.audio(audio_bytes, format=mime_type)

  # ปุ่มเปลี่ยนเพลงแบบง่าย
  col_prev, col_next = st.columns(2)
  with col_prev:
    if st.button("⏮ เพลงก่อนหน้า", use_container_width=True):
      new_index = (selected_index - 1) % len(songs)
      st.rerun()
  with col_next:
    if st.button("⏭ เพลงถัดไป", use_container_width=True):
      new_index = (selected_index + 1) % len(songs)
      st.rerun()

st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 10px; color: #64748b;'>SPACE"
    " • LIGHT • SOUND • 1.618 ENERGY</p>",
    unsafe_allow_html=True,
)
