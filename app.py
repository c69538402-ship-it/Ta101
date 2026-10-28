import base64
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC", page_icon="🌌", layout="centered"
)

# สไตล์ตกแต่งธีมนีออนอวกาศดาร์กโหมด
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(ellipse at 50% 45%, #10133c 0%, #050615 48%, #010208 100%);
        color: #ffffff;
        font-family: 'Prompt', sans-serif;
    }
    h1 {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #00f5ff;
        text-shadow: 0 0 10px #00f5ff, 0 0 20px #bd00ff;
        font-size: 1.8rem !important;
        margin-bottom: 0px;
    .subtitle {
        text-align: center;
        font-size: 0.8rem;
        color: #aeb9dc;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    .stSelectbox label {
        color: #00f5ff !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("<h1>TA101 • NEON MUSIC</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>COSMIC AUDIO EXPERIENCE</div>", unsafe_allow_html=True
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# 1. ค้นหาไฟล์เพลง MP3 ทั้งหมดในโฟลเดอร์หลัก
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

# แสดงรูปโลโก้ตรงกลาง (ถ้ามี)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  if logo_path:
    st.image(str(logo_path), use_container_width=True)
  else:
    st.markdown(
        "<div style='text-align:center; color:#00f5ff; border:2px solid"
        " #00f5ff; border-radius:50%; padding:40px; box-shadow:0 0 20px"
        " #00f5ff;'><b>TA101<br>NEON SPACE</b></div>",
        unsafe_allow_html=True,
    )

st.write("")

# 3. ตรวจสอบว่ามีเพลงไหม
if not songs:
  st.warning(
      "⚠️ ไม่พบไฟล์เพลง .mp3 ในโฟลเดอร์หลัก กรุณานำไฟล์เพลงมาวางไว้หน้าเดียวกับ"
      " app.py"
  )
else:
  # ทำ Dropdown เลือกเพลง
  song_names = [s.stem for s in songs]
  selected_song_name = st.selectbox("🎵 เลือกเพลงในเพลย์ลิสต์", song_names)

  # หาไฟล์เพลงที่ถูกเลือก
  selected_index = song_names.index(selected_song_name)
  selected_file = songs[selected_index]

  st.write("")

  # เล่นเพลงด้วย Native Audio Player ของ Streamlit (รองรับมือถือและเบราว์เซอร์ทุกตัว 100%)
  audio_bytes = selected_file.read_bytes()
  st.audio(audio_bytes, format="audio/mp3")

  st.markdown("---")
  st.markdown(
      "<div style='text-align: center; font-size: 0.75rem; color:"
      " #7380b8;'>SPACE • LIGHT • SOUND • 1.618 ENERGY</div>",
      unsafe_allow_html=True,
  )
    
