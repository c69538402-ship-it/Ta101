from pathlib import Path
import base64
import json
import mimetypes
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

songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            songs.append({
                "name": path.stem,
                "src": f"data:{mime};base64,{encoded}",
            })
        except OSError:
            continue

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")

logo_data = ""
for candidate in ("logo1.jpg", "logo1.jpeg", "logo1.png", "โลโก้.jpg", "logo.jpg"):
    logo_path = ROOT / candidate
    if logo_path.is_file():
        try:
            mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
            logo_data = f"data:{mime};base64,{base64.b64encode(logo_path.read_bytes()).decode('ascii')}"
            break
        except OSError:
            pass

logo_json = json.dumps(logo_data)

# โหลดไฟล์ player.html ที่สร้างขึ้นมา
html_path = ROOT / "player.html"
if html_path.is_file():
    player_html = html_path.read_text(encoding="utf-8")
else:
    player_html = "<h1>ไม่พบไฟล์ player.html กรุณาสร้างไฟล์ player.html ในโฟลเดอร์เดียวกัน</h1>"

# แทนที่ค่าตัวแปรเพลงและโลโก้เข้าไปในโค้ด HTML
player_html = (
    player_html
    .replace("__SONGS__", songs_json)
    .replace("__LOGO__", logo_json)
)

# บันทึก player_html ลงเป็นไฟล์ชั่วคราวสำหรับ iframe
html_file = ROOT / "index.html"
html_file.write_text(player_html, encoding="utf-8")

# ใช้ st.iframe แทนตามคำเตือนของ Streamlit
st.iframe(src="app/static/index.html" if (ROOT / "static").exists() else "index.html", height=900, scrolling=False)
