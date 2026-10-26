from pathlib import Path
import base64
import mimetypes
import json
import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="TA101 • NEON MUSIC",
    page_icon="🎧",
    layout="centered"
)

# โฟลเดอร์ที่เก็บ app.py และไฟล์เพลง
ROOT = Path(__file__).resolve().parent

# ประเภทไฟล์เพลงที่รองรับ
AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".m4a",
    ".aac", ".opus", ".flac"
}

def encode_audio(path):
    """แปลงไฟล์เพลงเป็นข้อมูลสำหรับเครื่องเล่นบนหน้าเว็บ"""
    mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

# ค้นหาเพลงอัตโนมัติจากโฟลเดอร์เดียวกับ app.py
songs = []

for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            songs.append({
                "name": path.stem,
                "src": encode_audio(path)
            })
        except OSError:
            pass

st.write(f"🎵 พบเพลงทั้งหมด {len(songs)} เพลงในระบบ")

# แปลงข้อมูลเพลงเป็น JSON (ใช้ชื่อตัวแปร songs_json ให้ตรงกัน)
songs_json = json.dumps(
    songs, ensure_ascii=False
).replace("</", "<\\/")

player_html = r"""
<div style="background:#09091b;color:white;padding:20px;
border-radius:18px;border:1px solid #42f5ff;
font-family:Arial,sans-serif">
  <h2 style="color:#42f5ff">🎧 TA101 • NEON MUSIC</h2>
  <div id="songName">กำลังเตรียมเพลง...</div>
  <audio id="audio" controls style="width:100%;margin-top:15px"></audio>
  <div style="display:flex;gap:10px;margin-top:12px">
    <button id="prev" style="padding:8px 12px;cursor:pointer;">⏮ เพลงก่อนหน้า</button>
    <button id="play" style="padding:8px 12px;cursor:pointer;">▶ เล่น / หยุด</button>
    <button id="next" style="padding:8px 12px;cursor:pointer;">⏭ เพลงถัดไป</button>
  </div>
  <label style="display:block;margin-top:15px;cursor:pointer;">
    <input id="autoNext" type="checkbox" checked>
    เล่นเพลงถัดไปอัตโนมัติ
  </label>
  <label style="display:block;margin-top:10px;cursor:pointer;">
    <input id="repeatAll" type="checkbox" checked>
    เล่นวนตั้งแต่เพลงแรกเมื่อจบรายการ
  </label>
  <p id="count" style="color:#42f5ff;margin-top:10px;"></p>
</div>

<script>
const songs = __SONGS__;
const audio = document.getElementById("audio");
const songName = document.getElementById("songName");
const count = document.getElementById("count");
let index = 0;

function loadSong(i, autoplay = false) {
  if (!songs.length) {
    songName.textContent = "ไม่พบไฟล์เพลง";
    count.textContent = "กรุณาเพิ่มเพลงในโฟลเดอร์เดียวกัน";
    return;
  }

  index = (i + songs.length) % songs.length;
  audio.src = songs[index].src;
  songName.textContent = "🎵 " + songs[index].name;
  count.textContent =
    "เพลงที่ " + (index + 1) + " / " + songs.length;

  if (autoplay) {
    audio.play().catch(() => {
      songName.textContent =
        "กดปุ่มเล่นเพื่อเริ่มเพลง: " + songs[index].name;
    });
  }
}

document.getElementById("play").onclick = () => {
  if (audio.paused) {
    audio.play().catch(() => {});
  } else {
    audio.pause();
  }
};

document.getElementById("next").onclick = () => {
  loadSong(index + 1, true);
};

document.getElementById("prev").onclick = () => {
  loadSong(index - 1, true);
};

audio.addEventListener("ended", () => {
  if (!document.getElementById("autoNext").checked) return;

  if (index + 1 < songs.length) {
    loadSong(index + 1, true);
  } else if (document.getElementById("repeatAll").checked) {
    loadSong(0, true);
  }
});

if (songs.length) loadSong(0);
</script>
"""

player_html = player_html.replace("__SONGS__", songs_json)

components.html(player_html, height=360, scrolling=False)
