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

# ค้นหาไฟล์เพลงทั้งหมดในโฟลเดอร์
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

songs_json = json.dumps(songs, ensure_ascii=False)

# ค้นหาไฟล์โลโก้
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

# โค้ด HTML / CSS / JavaScript ตัวเล่นเพลงและเอฟเฟกต์อวกาศนีออน (ใช้ Canvas 2D ป้องกันจอดำ 100%)
player_html = f"""
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Prompt:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--a:#00f5ff;--b:#bd00ff;--panel:rgba(5,8,25,0.85)}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#02030b;color:#fff;font-family:Prompt,sans-serif}}
#stage{{position:relative;width:100%;height:100vh;overflow:hidden;background:radial-gradient(circle at center,#10133c 0%,#050615 50%,#010208 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}}
canvas{{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none}}
.hud{{position:relative;z-index:2;width:100%;max-width:440px;display:flex;flex-direction:column;align-items:center;gap:15px}}
.brand{{font-family:Orbitron,sans-serif;font-weight:900;letter-spacing:3px;font-size:22px;text-align:center;color:#eafcff;text-shadow:0 0 10px var(--a),0 0 20px var(--b)}}
.logo-box{{width:100px;height:100px;border-radius:50%;border:2px solid var(--a);box-shadow:0 0 20px var(--a),0 0 40px var(--b);overflow:hidden;background:#060817;display:grid;place-items:center}}
.logo-box img{{width:100%;height:100%;object-fit:cover}}
.panel{{width:100%;border:1px solid var(--a);border-radius:20px;padding:15px;background:var(--panel);backdrop-filter:blur(15px);box-shadow:0 0 25px rgba(0,255,255,0.25)}}
#track-title{{font-size:14px;font-weight:700;color:var(--a);text-align:center;margin-bottom:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
select{{width:100%;padding:8px;background:#060817;color:#fff;border:1px solid var(--a);border-radius:8px;margin-bottom:10px;font-family:Prompt,sans-serif}}
audio{{width:100%;margin-top:5px;filter:drop-shadow(0 0 5px var(--a))}}
.controls{{display:flex;justify-content:center;gap:12px;margin-top:10px}}
.neon-btn{{background:linear-gradient(45deg,var(--b),var(--a));border:none;color:white;padding:8px 18px;font-weight:bold;border-radius:20px;cursor:pointer;font-size:12px;box-shadow:0 0 10px var(--a)}}
#start-screen{{position:fixed;inset:0;background:#02030bf8;z-index:99;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}}
#start-screen h2{{font-family:Orbitron,sans-serif;color:var(--a);text-shadow:0 0 15px var(--a);margin-bottom:10px}}
#start-screen p{{color:#a5b4fc;font-size:13px;max-width:350px;line-height:1.6}}
#start-screen button{{margin-top:15px;padding:12px 28px;border:0;border-radius:25px;color:#fff;font-weight:bold;background:linear-gradient(90deg,var(--a),var(--b));cursor:pointer;box-shadow:0 0 20px var(--a);font-size:14px}}
</style>
</head>
<body>

<div id="start-screen">
  <h2>TA101 • NEON SPACE</h2>
  <p>ระบบเครื่องเล่นเพลงอวกาศนีออน พร้อมเอฟเฟกต์ดวงดาวเคลื่อนไหว รองรับทุกหน้าจอ</p>
  <button onclick="startApp()">✦ เริ่มต้นใช้งาน</button>
</div>

<div id="stage">
  <canvas id="space"></canvas>
  <div class="hud">
    <div class="brand">TA101 NEON MUSIC</div>
    <div class="logo-box">
      <img id="logo-img" style="display:none;" alt="Logo">
      <span id="logo-text" style="font-family:Orbitron;font-size:11px;color:var(--a);">TA101</span>
    </div>
    <div class="panel">
      <div id="track-title">กำลังเตรียมเพลง...</div>
      <select id="playlist"></select>
      <audio id="audio" controls></audio>
      <div class="controls">
        <button class="neon-btn" onclick="prevSong()">⏮ เพลงก่อนหน้า</button>
        <button class="neon-btn" onclick="nextSong()">⏭ เพลงถัดไป</button>
      </div>
    </div>
  </div>
</div>

<script>
const songs = {songs_json};
const logoData = {logo_json};
let currentIndex = 0;
const audio = document.getElementById('audio');

if(logoData) {{
    const img = document.getElementById('logo-img');
    img.src = logoData;
    img.style.display = 'block';
    document.getElementById('logo-text').style.display = 'none';
}}

function startApp(){
    document.getElementById('start-screen').style.display = 'none';
    if(songs.length > 0) playSong(0);
}

function initPlaylist(){
    const sel = document.getElementById('playlist');
    sel.innerHTML = '';
    if(songs.length === 0){
        let opt = document.createElement('option');
        opt.textContent = "ไม่พบไฟล์เพลงในโฟลเดอร์";
        sel.appendChild(opt);
        document.getElementById('track-title').textContent = "ไม่พบไฟล์เพลง (.mp3)";
        return;
    }
    songs.forEach((s, i) => {{
        let opt = document.createElement('option');
        opt.value = i;
        opt.textContent = (i+1) + ". " + s.name;
        sel.appendChild(opt);
    }});
    sel.onchange = (e) => playSong(Number(e.target.value));
}

function playSong(i){
    if(!songs.length) return;
    currentIndex = (i + songs.length) % songs.length;
    audio.src = songs[currentIndex].src;
    document.getElementById('track-title').textContent = "🎵 " + songs[currentIndex].name;
    document.getElementById('playlist').value = currentIndex;
    audio.play().catch(e => console.log(e));
}

audio.onended = () => nextSong();
function nextSong() { playSong(currentIndex + 1); }
function prevSong() { playSong(currentIndex - 1); }

initPlaylist();

// Canvas Starfield Background (เสถียร ไม่จอดำ รองรับมือถือและคอมพิวเตอร์ 100%)
const canvas = document.getElementById('space');
const ctx = canvas.getContext('2d');
let width, height, stars = [];

function resize(){
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}
window.onresize = resize;
resize();

for(let i=0; i<100; i++){{
    stars.push({{
        x: Math.random() * width,
        y: Math.random() * height,
        size: Math.random() * 2,
        speed: Math.random() * 0.4 + 0.1
    }});
}});

function animate(){
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#00f5ff";
    stars.forEach(s => {{
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        ctx.fill();
        s.y -= s.speed;
        if(s.y < 0) s.y = height;
    }});
    requestAnimationFrame(animate);
}
animate();
</script>
</body>
</html>
"""

components.html(player_html, height=720, scrolling=False)
