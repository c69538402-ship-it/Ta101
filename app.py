import base64
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# จัดการ State ธีมสีนีออน
if "theme_color" not in st.session_state:
  st.session_state.theme_color = "#00f5ff"
if "theme_glow" not in st.session_state:
  st.session_state.theme_glow = "#bd00ff"
if "cyber_mode" not in st.session_state:
  st.session_state.cyber_mode = "HYPER DRIVE"

# แผงควบคุมเลือกธีมสีสไตล์ไซเบอร์
cols = st.columns(4)
with cols[0]:
  if st.button("🔵 CYAN", use_container_width=True):
    st.session_state.theme_color = "#00f5ff"
    st.session_state.theme_glow = "#bd00ff"
with cols[1]:
  if st.button("🟢 MATRIX", use_container_width=True):
    st.session_state.theme_color = "#00ff82"
    st.session_state.theme_glow = "#0055ff"
with cols[2]:
  if st.button("🟠 SOLAR", use_container_width=True):
    st.session_state.theme_color = "#ff7a00"
    st.session_state.theme_glow = "#ff006e"
with cols[3]:
  if st.button("🟣 VIOLET", use_container_width=True):
    st.session_state.theme_color = "#e8f5ff"
    st.session_state.theme_glow = "#9900ff"

tc = st.session_state.theme_color
tg = st.session_state.theme_glow

# ตกแต่ง CSS นีออนอวกาศขั้นเทพ
css_code = f"""
    <style>
    .stApp {{
        background: radial-gradient(ellipse at 50% 30%, #13183f 0%, #060817 55%, #010208 100%);
        color: #ffffff;
        font-family: 'Prompt', sans-serif;
    }
    h1 {{
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: {tc};
        text-shadow: 0 0 12px {tc}, 0 0 30px {tg};
        font-size: 1.7rem !important;
        margin-bottom: 0px;
        animation: flicker 3s infinite alternate;
    }}
    @keyframes flicker {{
        0% {{ opacity: 0.85; filter: brightness(0.9); }}
        100% {{ opacity: 1; filter: brightness(1.2); text-shadow: 0 0 20px {tc}, 0 0 40px {tg}; }}
    }}
    .sub-title {{
        text-align: center;
        font-size: 0.7rem;
        color: #aeb9dc;
        letter-spacing: 4px;
        margin-bottom: 15px;
        font-family: 'Orbitron', sans-serif;
    }}
    .cyber-card {{
        border: 2px solid {tc};
        border-radius: 24px;
        padding: 22px;
        background: rgba(8, 12, 32, 0.82);
        box-shadow: 0 0 25px {tc}44, inset 0 0 20px {tg}33;
        backdrop-filter: blur(16px);
        margin-top: 10px;
    }}
    .status-badge {{
        display: inline-block;
        background: {tc}22;
        border: 1px solid {tc};
        color: {tc};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 0 10px {tc}66;
        margin-bottom: 12px;
    }}
    .stSelectbox label {{
        color: {tc} !important;
        font-weight: 600;
    }}
    .stAudio {{
        filter: drop-shadow(0 0 8px {tc});
    }}
    </style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# หัวข้อหลัก
st.markdown("<h1>TA101 • NEON SPACE</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>COSMIC AUDIO ENGINE • V.1.618</div>",
    unsafe_allow_html=True,
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# ค้นหาเพลง
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
  if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
    songs.append(path)

# ค้นหาโลโก้
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

# แสดงผลในกรอบไซเบอร์การ์ด
with st.container():
  st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)

  # สถานะระบบจำลองแบบล้ำๆ
  st.markdown(
      "<div style='text-align:center;'><span class='status-badge'>⚡ SPACE"
      " ENGINE: ONLINE • AUDIO REACTIVE READY</span></div>",
      unsafe_allow_html=True,
  )

  # แสดงโลโก้ตรงกลางพร้อมกรอบเรืองแสง
  col1, col2, col3 = st.columns([1, 2.2, 1])
  with col2:
    if logo_path:
      st.image(str(logo_path), use_container_width=True)
    else:
      st.markdown(
          f"<div style='text-align:center; color:{tc}; border:2px dashed"
          f" {tc}; border-radius:50%; padding:45px; box-shadow:0 0 25px"
          f" {tc}; background:rgba(0,0,0,0.5);'><b>TA101<br>COSMIC</b></div>",
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
    selected_song_name = st.selectbox("🎵 เลือกแทร็กเสียงในเพลย์ลิสต์", song_names)

    selected_index = song_names.index(selected_song_name)
    selected_file = songs[selected_index]

    st.write("")

    # เครื่องเล่นเพลงแบบเนทีฟ (ลื่นไหล ไม่จอดำ รองรับทุกมือถือ)
    audio_bytes = selected_file.read_bytes()
    st.audio(audio_bytes, format="audio/mp3")

  st.markdown("</div>", unsafe_allow_html=True)

# ฟุตเตอร์เท่ๆ
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.7rem; color:"
    " #8a9bbd; font-family: Orbitron, sans-serif; letter-spacing: 2px;'>SPACE •"
    " LIGHT • SOUND • 1.618 ENERGY</div>",
    unsafe_allow_html=True,
)
