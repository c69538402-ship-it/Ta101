import base64
import json
import mimetypes
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • NEON SPACE VISUALIZER",
    page_icon="🌌",
    layout="centered",
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

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")

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

# โค้ด HTML / JS พร้อมปุ่ม Start ป้องกันจอดำและปลดล็อก Audio API
player_html = """
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Prompt:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {
    --theme: #00f5ff;
    --glow: rgba(0, 245, 255, 0.4);
}
* { box-sizing: border-box; }
html, body {
    margin: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at center, #070a24 0%, #02030a 60%, #000104 100%);
    color: #fff; font-family: 'Prompt', sans-serif;
    overflow: hidden;
}
/* หน้าต่างเริ่มต้นเพื่อปลดล็อกจอดำและเสียง */
#splash {
    position: fixed; inset: 0; background: #02030bf8; z-index: 99;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center; padding: 20px;
}
#splash h2 {
    font-family: 'Orbitron', sans-serif; color: var(--theme);
    text-shadow: 0 0 15px var(--theme); margin-bottom: 10px; font-size: 20px;
}
#splash p { color: #a5b4fc; font-size: 12px; max-width: 320px; line-height: 1.5; margin-bottom: 20px; }
#splash button {
    padding: 12px 30px; border: 0; border-radius: 25px; color: #fff; font-weight: bold;
    background: linear-gradient(90deg, var(--theme), #7000ff); cursor: pointer;
    box-shadow: 0 0 20px var(--theme); font-size: 14px; font-family: Prompt, sans-serif;
}

.app-container {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    width: 100%; height: 100%; padding: 10px;
}
h1 {
    font-family: 'Orbitron', sans-serif; color: var(--theme);
    text-shadow: 0 0 15px var(--theme), 0 0 30px var(--theme);
    font-size: 18px; margin: 0 0 5px 0; letter-spacing: 2px; text-align: center;
}
.subtitle {
    font-size: 9px; color: #a5b4fc; letter-spacing: 3px; margin-bottom: 10px; text-align: center;
}
.logo-ring {
    width: 100px; height: 100px; border-radius: 50%;
    border: 2px solid var(--theme);
    box-shadow: 0 0 25px var(--theme), inset 0 0 15px var(--theme);
    overflow: hidden; margin-bottom: 10px; background: #010206;
    display: grid; place-items: center;
}
.logo-ring img { width: 100%; height: 100%; object-fit: cover; }

.card {
    width: 100%; max-width: 380px;
    background: rgba(6, 9, 26, 0.9);
    border: 2px solid var(--theme);
    box-shadow: 0 20px 40px rgba(0,0,0,0.9), 0 0 25px var(--glow);
    border-radius: 20px; padding: 15px; backdrop-filter: blur(15px);
}
.theme-selector {
    display: flex; justify-content: center; gap: 8px; margin-bottom: 8px;
}
.theme-btn {
    background: rgba(255,255,255,0.05); border: 1px solid var(--theme);
    color: var(--theme); padding: 4px 10px; border-radius: 10px; font-size: 10px;
    cursor: pointer; font-weight: bold; transition: 0.2s;
}
.theme-btn:hover { background: var(--theme); color: #000; }

select {
    width: 100%; padding: 7px; background: #02040a; color: #fff;
    border: 1px solid var(--theme); border-radius: 10px; font-family: Prompt, sans-serif;
    font-size: 12px; margin-bottom: 8px; outline: none;
}
.lcd {
    background: linear-gradient(135deg, #010206 0%, #0b102b 100%);
    border: 1px solid var(--theme); border-radius: 12px; padding: 10px;
    text-align: center; margin-bottom: 8px;
}
.track-title {
    color: var(--theme); font-weight: bold; font-size: 12px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    text-shadow: 0 0 8px var(--theme); margin-bottom: 6px;
}
canvas {
    display: block; width: 100%; height: 40px; background: rgba(0,0,0,0.4);
    border-radius: 6px; border: 1px solid rgba(255,255,255,0.1);
}
audio { width: 100%; margin: 6px 0; height: 30px; filter: drop-shadow(0 0 5px var(--theme)); }

.controls {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;
}
.ctrl-btn {
    background: linear-gradient(135deg, #0d1235, #040614);
    color: var(--theme); border: 1px solid var(--theme); border-radius: 10px;
    padding: 8px 2px; font-size: 10px; font-weight: bold; cursor: pointer; text-align: center;
    box-shadow: 0 3px 8px rgba(0,0,0,0.5); transition: 0.2s;
}
.ctrl-btn:hover { background: var(--theme); color: #000; }
</style>
</head>
<body>

<div id="splash">
    <h2>TA101 • NEON SPACE</h2>
    <p>แตะปุ่มด้านล่างเพื่อเปิดระบบเสียงและเริ่มต้นใช้งานเครื่องเล่นเพลง</p>
    <button onclick="startApp()">✦ เริ่มต้นใช้งานระบบ</button>
</div>

<div class="app-container">
    <h1>TA101 • VISUALIZER</h1>
    <div class="subtitle">✦ QUANTUM AUDIO SPECTRUM ✦</div>
    
    <div class="logo-ring">
        <img id="logo-img" style="display:none;" alt="Logo">
        <span id="logo-text" style="font-family:Orbitron;font-size:10px;color:var(--theme);">TA101</span>
    </div>

    <div class="card">
        <div class="theme-selector">
            <button class="theme-btn" onclick="setTheme('#00f5ff', 'rgba(0,245,255,0.4)')">💙 ฟ้า</button>
            <button class="theme-btn" onclick="setTheme('#00ff88', 'rgba(0,255,136,0.4)')">💚 เขียว</button>
            <button class="theme-btn" onclick="setTheme('#ff00d4', 'rgba(255,0,212,0.4)')">💜 ชมพู</button>
        </div>

        <select id="playlist" onchange="selectSong(this.value)"></select>

        <div class="lcd">
            <div id="track-title" class="track-title">พร้อมใช้งาน</div>
            <canvas id="visualizer"></canvas>
        </div>

        <audio id="audio" controls crossorigin="anonymous"></audio>

        <div class="controls">
            <button class="ctrl-btn" onclick="prevSong()">⏮ ก่อนหน้า</button>
            <button class="ctrl-btn" id="shuffle-btn" onclick="toggleShuffle()">🔀 สุ่ม: ปิด</button>
            <button class="ctrl-btn" id="loop-btn" onclick="toggleLoop()">🔁 วน: ปิด</button>
            <button class="ctrl-btn" onclick="nextSong()">ถัดไป ⏭</button>
        </div>
    </div>
</div>

<script>
const songs = __SONGS__;
const logoData = __LOGO__;
let currentIndex = 0;
let isShuffle = false;
let isLoop = false;
let audioCtx, analyser, source, canvasEl, canvasCtx;

const audio = document.getElementById('audio');
const titleEl = document.getElementById('track-title');
const playlistEl = document.getElementById('playlist');

if(logoData) {
    const img = document.getElementById('logo-img');
    img.src = logoData;
    img.style.display = 'block';
    document.getElementById('logo-text').style.display = 'none';
}

function startApp(){
    document.getElementById('splash').style.display = 'none';
    initAudioContext();
    initPlaylist();
    if(songs.length > 0) {
        loadSong(0);
        audio.play().catch(e => console.log(e));
    }
}

function setTheme(color, glow){
    document.documentElement.style.setProperty('--theme', color);
    document.documentElement.style.setProperty('--glow', glow);
}

function initAudioContext(){
    if(audioCtx) return;
    try {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        source = audioCtx.createMediaElementSource(audio);
        source.connect(analyser);
        analyser.connect(audioCtx.destination);
        analyser.fftSize = 64;

        canvasEl = document.getElementById('visualizer');
        canvasCtx = canvasEl.getContext('2d');
        
        function draw(){
            requestAnimationFrame(draw);
            let bufferLength = analyser.frequencyBinCount;
            let dataArray = new Uint8Array(bufferLength);
            analyser.getByteFrequencyData(dataArray);

            if(canvasEl.width !== canvasEl.offsetWidth || canvasEl.height !== canvasEl.offsetHeight) {
                canvasEl.width = canvasEl.offsetWidth;
                canvasEl.height = canvasEl.offsetHeight;
            }
            let width = canvasEl.width;
            let height = canvasEl.height;

            canvasCtx.fillStyle = 'rgba(2, 4, 10, 0.4)';
            canvasCtx.fillRect(0, 0, width, height);

            let barWidth = (width / bufferLength) * 2.2;
            let barHeight;
            let x = 0;

            let computedTheme = getComputedStyle(document.documentElement).getPropertyValue('--theme').trim();

            for(let i = 0; i < bufferLength; i++) {
                barHeight = (dataArray[i] / 255) * height;
                canvasCtx.fillStyle = computedTheme;
                canvasCtx.fillRect(x, height - barHeight, barWidth - 2, barHeight);
                x += barWidth + 2;
            }
        }
        draw();
    } catch(e) {
        console.log("Audio Context Error", e);
    }
}

function initPlaylist(){
    playlistEl.innerHTML = '';
    if(songs.length === 0){
        let opt = document.createElement('option');
        opt.textContent = "ไม่พบไฟล์เพลงในโฟลเดอร์";
        playlistEl.appendChild(opt);
        titleEl.textContent = "ไม่พบไฟล์เพลง (.mp3)";
        return;
    }
    songs.forEach((s, i) => {
        let opt = document.createElement('option');
        opt.value = i;
        opt.textContent = (i+1) + ". " + s.name;
        playlistEl.appendChild(opt);
    });
}

function loadSong(i){
    if(!songs.length) return;
    currentIndex = (i + songs.length) % songs.length;
    audio.src = songs[currentIndex].src;
    titleEl.textContent = "🎵 " + songs[currentIndex].name;
    playlistEl.value = currentIndex;
    if(audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
}

function selectSong(val){
    loadSong(Number(val));
    audio.play().catch(e => console.log(e));
}

function nextSong(){
    if(isShuffle){
        currentIndex = Math.floor(Math.random() * songs.length);
    } else {
        currentIndex = (currentIndex + 1) % songs.length;
    }
    loadSong(currentIndex);
    audio.play().catch(e => console.log(e));
}

function prevSong(){
    currentIndex = (currentIndex - 1 + songs.length) % songs.length;
    loadSong(currentIndex);
    audio.play().catch(e => console.log(e));
}

function toggleShuffle(){
    isShuffle = !isShuffle;
    document.getElementById('shuffle-btn').textContent = isShuffle ? "🔀 สุ่ม: เปิด" : "🔀 สุ่ม: ปิด";
}

function toggleLoop(){
    isLoop = !isLoop;
    audio.loop = isLoop;
    document.getElementById('loop-btn').textContent = isLoop ? "🔁 วน: เปิด" : "🔁 วน: ปิด";
}

audio.onended = () => {
    if(!isLoop) nextSong();
};
</script>
</body>
</html>
"""

# แทนที่ค่าตัวแปรลงใน HTML
player_html = (
    player_html
    .replace("__SONGS__", songs_json)
    .replace("__LOGO__", logo_json)
)

components.html(player_html, height=540, scrolling=False)
