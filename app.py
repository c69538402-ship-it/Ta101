import base64
import json
import mimetypes
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# ดึงเพลงทั้งหมด
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
  if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
    try:
      mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
      encoded = base64.b64encode(path.read_bytes()).decode("ascii")
      songs.append(
          {
              "name": path.stem,
              "src": f"data:{mime};base64,{encoded}",
          }
      )
    except OSError:
      continue

# ดึงโลโก้
logo_data = ""
for candidate in (
    "logo1.jpg",
    "logo1.jpeg",
    "logo1.png",
    "โลโก้.jpg",
    "logo.jpg",
):
  logo_path = ROOT / candidate
  if logo_path.is_file():
    try:
      mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
      logo_data = f"data:{mime};base64,{base64.b64encode(logo_path.read_bytes()).decode('ascii')}"
      break
    except OSError:
      pass

# โหลดไฟล์ player.html แยกส่วนออกมาเพื่อแก้ปัญหาจอดำ
html_file_path = ROOT / "player.html"
if html_file_path.is_file():
  html_content = html_file_path.read_text(encoding="utf-8")
  # ส่งข้อมูล JSON เข้าไปในคอมโพเนนต์
  components.html(
      f"""
        <div id="app-container"></div>
        <script>
            const songsData = {json.dumps(songs, ensure_ascii=False)};
            const logoData = "{logo_data}";
            
            // สร้าง iframe โหลด player.html เพื่อความเสถียร
            const iframe = document.createElement('iframe');
            iframe.style.width = '100%';
            iframe.style.height = '750px';
            iframe.style.border = 'none';
            iframe.srcdoc = {json.dumps(html_content)};
            
            document.getElementById('app-container').appendChild(iframe);
            
            iframe.onload = () => {{
                iframe.contentWindow.postMessage({{ songs: songsData, logo: logoData }}, '*');
            }};
        </script>
        """,
      height=780,
      scrolling=False,
  )
else:
  st.error(
      "⚠️ ไม่พบไฟล์ player.html กรุณาสร้างไฟล์ player.html ไว้ที่หน้าหลักของโปรเจกต์ครับ!"
    )
