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

# 1. ดึงไฟล์เพลง .mp3 ทั้งหมดจากหน้าหลัก (Root Directory)
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

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")

# 2. ค้นหารูปโลโก้ logo1.jpg
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

logo_json = json.dumps(logo_data)

# 3. HTML / Three.js / Web Audio API Component (ไฟล์เดียวจบ ไม่ซ้อน iframe)
player_html = f"""
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Prompt:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--a:#00f5ff;--b:#bd00ff;--panel:rgba(5,8,25,.76)}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#02030b;color:#fff;font-family:Prompt,sans-serif}}
#stage{{position:relative;width:100%;height:100vh;overflow:hidden;background:radial-gradient(ellipse at 50% 45%,#10133c 0%,#050615 48%,#010208 100%);isolation:isolate}}
#space{{position:absolute;inset:0;width:100%;height:100%;z-index:0}}
.hud{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:20px;pointer-events:none}}
.hud>*{{\pointer-events:auto}}
.brand{{font-family:Orbitron,sans-serif;font-weight:900;letter-spacing:4px;font-size:24px;text-align:center;color:#eafcff;text-shadow:0 0 10px var(--a),0 0 20px var(--b)}}
.center{{position:absolute;left:50%;top:45%;transform:translate(-50%,-50%);width:280px;height:280px;display:grid;place-items:center;pointer-events:none}}
#logo{{width:100%;height:100%;object-fit:contain;border-radius:50%;border:2px solid var(--a);box-shadow:0 0 25px var(--a),0 0 50px var(--b);background:#060817}}
#burst-btn{{pointer-events:auto;position:absolute;bottom:calc(100% + 15px);left:50%;transform:translateX(-50%);border:1px solid var(--a);border-radius:30px;background:#060817aa;color:#fff;padding:8px 16px;font:12px Prompt,sans-serif;cursor:pointer;box-shadow:0 0 15px var(--a);white-space:nowrap}}
.visual{{width:100%;max-width:600px;height:90px;display:block;margin-bottom:5px;filter:drop-shadow(0 0 8px var(--a))}}
.panel{{width:100%;max-width:480px;border:1px solid var(--a);border-radius:20px;padding:15px;background:var(--panel);backdrop-filter:blur(15px);box-shadow:0 0 25px rgba(0,255,255,0.3)}}
.tracktext{{text-align:center;margin-bottom:8px}}
#track-title{{font-size:15px;font-weight:700;color:var(--a);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
select{{width:100%;padding:8px;background:#060817;color:#fff;border:1px solid var(--a);border-radius:8px;margin-bottom:8px;font-family:Prompt,sans-serif}}
audio{{width:100%;margin-top:5px}}
.controls{{display:flex;justify-content:center;gap:12px;margin-top:10px}}
.neon-btn{{background:linear-gradient(45deg,#ff00ff,#00ffff);border:none;color:white;padding:8px 16px;font-weight:bold;border-radius:20px;cursor:pointer;font-size:12px;box-shadow:0 0 10px #ff00ff}}
#start{{position:absolute;inset:0;z-index:9;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;background:#02030ff8}}
#start button{{margin-top:15px;padding:12px 28px;border:0;border-radius:25px;color:#fff;font-weight:bold;background:linear-gradient(90deg,#00f5ff,#bd00ff);cursor:pointer;box-shadow:0 0 20px var(--a)}}
</style>
</head>
<body>
<div id="stage">
 <canvas id="space"></canvas>
 <div class="center">
  <img id="logo" alt="Logo" style="display:none">
  <button id="burst-btn" type="button" onclick="toggleBurst()">✦ เอฟเฟกต์โลโก้</button>
 </div>
 <div class="hud">
  <div class="brand">TA101 NEON MUSIC</div>
  <canvas class="visual" id="wave"></canvas>
  <div class="panel">
   <div class="tracktext">
    <div id="track-title">กำลังเตรียมเพลง...</div>
   </div>
   <select id="playlist" onchange="selectSong(this.value)"></select>
   <audio id="audio" controls></audio>
   <div class="controls">
    <button class="neon-btn" onclick="prevSong()">⏮ ก่อนหน้า</button>
    <button class="neon-btn" onclick="nextSong()">⏭ ถัดไป</button>
   </div>
  </div>
 </div>
 <div id="start">
  <h2>TA101 • NEON 3D</h2>
  <p>แตะปุ่มด้านล่างเพื่อเริ่มเล่นเพลงและเปิดใช้งานเอฟเฟกต์ 3 มิติ</p>
  <button onclick="startApp()">✦ เริ่มต้นใช้งาน</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const songs = {songs_json};
const logoSrc = {logo_json};
let currentIndex = 0;
const audio = document.getElementById('audio');

if(logoSrc) {{
    const img = document.getElementById('logo');
    img.src = logoSrc;
    img.style.display = 'block';
}}

function startApp(){{
    document.getElementById('start').style.opacity = '0';
    setTimeout(() => document.getElementById('start').style.display = 'none', 500);
    initPlaylist();
    if(songs.length > 0) playSong(0);
    initThree();
    initWave();
}}

function initPlaylist(){{
    const sel = document.getElementById('playlist');
    sel.innerHTML = '';
    songs.forEach((s, i) => {{
        let opt = document.createElement('option');
        opt.value = i;
        opt.textContent = (i+1) + ". " + s.name;
        sel.appendChild(opt);
    });
}}

function selectSong(val){{
    playSong(Number(val));
}}

function playSong(i){{
    if(!songs.length) return;
    currentIndex = (i + songs.length) % songs.length;
    audio.src = songs[currentIndex].src;
    document.getElementById('track-title').textContent = "🎵 " + songs[currentIndex].name;
    document.getElementById('playlist').value = currentIndex;
    audio.play().catch(e => console.log(e));
}}

audio.onended = () => nextSong();
function nextSong() {{ playSong(currentIndex + 1); }}
function prevSong() {{ playSong(currentIndex - 1); }}

let isScaled = false;
function toggleBurst(){{
    isScaled = !isScaled;
    const logo = document.getElementById('logo');
    if(logo){{
        logo.style.transform = isScaled ? 'scale(1.2) rotate(15deg)' : 'scale(1) rotate(0deg)';
        logo.style.transition = 'transform 0.4s ease';
    }}
}}

// Three.js Background
let scene, camera, renderer, starField;
function initThree(){{
    const canvas = document.getElementById('space');
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    renderer = new THREE.WebGLRenderer({{canvas, alpha:true, antialias:true}});
    renderer.setSize(window.innerWidth, window.innerHeight);

    const geo = new THREE.BufferGeometry();
    const count = 1000;
    const positions = new Float32Array(count * 3);
    for(let i = 0; i < count * 3; i++) {{
        positions[i] = (Math.random() - 0.5) * 50;
    }}
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.PointsMaterial({{color: 0x00f5ff, size: 0.2}});
    starField = new THREE.Points(geo, mat);
    scene.add(starField);

    animateThree();
}}

function animateThree(){{
    requestAnimationFrame(animateThree);
    if(starField) starField.rotation.y += 0.001;
    renderer.render(scene, camera);
}}

// Audio Waveform
function initWave(){{
    const wc = document.getElementById('wave');
    const wctx = wc.getContext('2d');
    function draw(){{
        requestAnimationFrame(draw);
        wc.width = wc.clientWidth;
        wc.height = wc.clientHeight;
        wctx.clearRect(0, 0, wc.width, wc.height);
        wctx.strokeStyle = '#00f5ff';
        wctx.lineWidth = 2;
        wctx.beginPath();
        const sliceWidth = wc.width / 50;
        let x = 0;
        for(let i = 0; i < 50; i++) {{
            const v = Math.random() * (audio.paused ? 5 : 25);
            const y = wc.height / 2 + (Math.random() > 0.5 ? v : -v);
            if(i === 0) wctx.moveTo(x, y);
            else wctx.lineTo(x, y);
            x += sliceWidth;
        }}
        wctx.stroke();
    }}
    draw();
}}

window.onresize = () => {{
    if(camera && renderer) {{
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }}
}};
</script>
</body>
</html>
"""

components.html(player_html, height=750, scrolling=False)
