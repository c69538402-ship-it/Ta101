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

# 1. ดึงไฟล์เพลง .mp3 ทั้งหมดจากหน้าหลัก
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

# 2. ค้นหารูปโลโก้
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

# 3. HTML / Three.js / Web Audio API Component (ใช้ .replace เพื่อความปลอดภัย 100%)
player_html = (
    """<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Prompt:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--a:#00f5ff;--b:#bd00ff;--panel:rgba(5,8,25,.78)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02030b;color:#fff;font-family:Prompt,sans-serif}
#stage{position:relative;width:100%;height:100vh;overflow:hidden;background:radial-gradient(ellipse at 50% 45%,#10133c 0%,#050615 48%,#010208 100%);isolation:isolate}
#space{position:absolute;inset:0;width:100%;height:100%;z-index:0}
.hud{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:15px;pointer-events:none}
.hud>*{pointer-events:auto}
.top{width:100%;display:flex;flex-direction:column;align-items:center;gap:6px}
.brand{font-family:Orbitron,sans-serif;font-weight:900;letter-spacing:4px;font-size:clamp(20px,4vw,32px);text-align:center;color:#eafcff;text-shadow:0 0 10px var(--a),0 0 25px var(--b);animation:flicker 3s infinite alternate}
@keyframes flicker{0%{filter:brightness(0.9)}100%{filter:brightness(1.25);text-shadow:0 0 15px var(--a),0 0 35px var(--b)}}
.subtitle{font-size:9px;letter-spacing:3px;color:#c7d6ff;text-align:center}
.themes{display:flex;gap:8px;margin-top:2px}
.theme{width:20px;height:20px;border:2px solid #fff;border-radius:50%;cursor:pointer;box-shadow:0 0 10px currentColor}
#t1{background:linear-gradient(135deg,#00f5ff,#bd00ff);color:#00f5ff}
#t2{background:linear-gradient(135deg,#00ff82,#0055ff);color:#00ff82}
#t3{background:linear-gradient(135deg,#ff7a00,#ff006e);color:#ff7a00}
#t4{background:linear-gradient(135deg,#e8f5ff,#7777ff);color:#e8f5ff}

.center{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);width:min(60vw,280px);height:min(60vw,280px);display:grid;place-items:center;pointer-events:none}
.ring{position:absolute;border-radius:50%;border:1px dashed var(--a);box-shadow:0 0 15px var(--a);animation:orbit 20s linear infinite}
.r1{inset:0%;opacity:0.6}
.r2{inset:12%;border-style:solid;opacity:0.4;animation-direction:reverse;animation-duration:30s}
@keyframes orbit{to{transform:rotate(360deg)}}

#logo{width:42%;height:42%;object-fit:contain;border-radius:50%;border:2px solid var(--a);box-shadow:0 0 20px var(--a),0 0 45px var(--b);background:#060817;pointer-events:auto}
#burst-btn{pointer-events:auto;position:absolute;bottom:calc(100% + 12px);left:50%;transform:translateX(-50%);border:1px solid var(--a);border-radius:20px;background:#060817cc;color:#fff;padding:5px 12px;font:10px Prompt,sans-serif;white-space:nowrap;box-shadow:0 0 10px var(--a);cursor:pointer}

.visual{width:min(800px,100%);height:85px;display:block;filter:drop-shadow(0 0 6px var(--a));margin-bottom:6px}
.panel{width:min(500px,100%);border:1px solid var(--a);border-radius:18px;padding:12px;background:var(--panel);backdrop-filter:blur(15px);box-shadow:0 0 20px rgba(0,255,255,0.25)}
.track{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.thumb{width:42px;height:42px;border-radius:8px;border:1px solid var(--b);object-fit:cover;box-shadow:0 0 10px var(--b)}
.tracktext{flex:1;min-width:0}
#track-title{font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--a)}
#track-sub{font-size:10px;color:#aeb9dc}
#playlist{width:38%;background:#060817;color:#fff;border:1px solid var(--a);padding:5px;border-radius:6px;font:10px Prompt,sans-serif}
.progress{height:5px;background:rgba(255,255,255,0.2);border-radius:10px;overflow:hidden;cursor:pointer}
#fill{height:100%;width:0%;background:linear-gradient(90deg,var(--a),var(--b));box-shadow:0 0 10px var(--a)}
.times{display:flex;justify-content:space-between;font-size:9px;color:#aeb9dc;margin-top:3px}
.controls{display:flex;align-items:center;justify-content:center;gap:15px;margin-top:8px}
.ctrl{border:0;background:transparent;color:#fff;font-size:18px;cursor:pointer;text-shadow:0 0 8px var(--a)}
#play{width:45px;height:45px;border:0;border-radius:50%;font-size:16px;color:#fff;cursor:pointer;background:linear-gradient(135deg,var(--a),var(--b));box-shadow:0 0 15px var(--a)}
.options{display:flex;justify-content:center;gap:6px;margin-top:8px}
.pill{font:9px Prompt,sans-serif;color:#e7eaff;border:1px solid rgba(255,255,255,0.3);border-radius:15px;padding:4px 10px;background:rgba(255,255,255,0.05);cursor:pointer}
.pill.active{border-color:var(--a);box-shadow:0 0 8px var(--a);color:var(--a)}

#start{position:absolute;inset:0;z-index:9;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;background:radial-gradient(ellipse at center,#11143bf8,#010208f8);transition:opacity 0.5s}
#start h2{font:900 24px Orbitron,sans-serif;color:var(--a);text-shadow:0 0 15px var(--a);margin:0 0 8px}
#start p{color:#c8d4f4;font-size:11px;max-width:380px;line-height:1.6}
#start button{margin-top:12px;padding:10px 22px;border:0;border-radius:25px;color:#fff;font:700 12px Prompt,sans-serif;background:linear-gradient(90deg,var(--a),var(--b));box-shadow:0 0 20px var(--a);cursor:pointer}
.foot{font:8px Orbitron,sans-serif;letter-spacing:2px;color:#93a2d2;margin-top:5px;text-align:center}
</style>
</head>
<body>
<div id="stage">
 <canvas id="space"></canvas>
 <div class="center">
  <div class="ring r1"></div><div class="ring r2"></div>
  <img id="logo" alt="Logo" style="display:none">
  <button id="burst-btn" type="button" onclick="toggleLogoEffect()">✦ เอฟเฟกต์โลโก้</button>
 </div>
 <div class="hud">
  <div class="top">
   <div class="brand">TA101 • NEON MUSIC</div>
   <div class="subtitle">3D COSMIC AUDIO EXPERIENCE</div>
   <div class="themes">
    <button class="theme" id="t1" onclick="setTheme('#00f5ff','#bd00ff')"></button>
    <button class="theme" id="t2" onclick="setTheme('#00ff82','#0055ff')"></button>
    <button class="theme" id="t3" onclick="setTheme('#ff7a00','#ff006e')"></button>
    <button class="theme" id="t4" onclick="setTheme('#e8f5ff','#7777ff')"></button>
   </div>
  </div>
  <div style="flex:1"></div>
  <canvas class="visual" id="wave"></canvas>
  <div class="panel">
   <div class="track">
    <img class="thumb" id="thumb" alt="Thumb" style="display:none">
    <div class="tracktext">
     <div id="track-title">กำลังเตรียมเพลง...</div>
     <div id="track-sub">TA101 LOCAL PLAYLIST</div>
    </div>
    <select id="playlist" onchange="selectTrack(this.value)"></select>
   </div>
   <div class="progress" id="progress" onclick="seekAudio(event)"><div id="fill"></div></div>
   <div class="times"><span id="elapsed">0:00</span><span id="duration">0:00</span></div>
   <div class="controls">
    <button class="ctrl" onclick="prevTrack()">⏮</button>
    <button id="play" onclick="togglePlay()">▶</button>
    <button class="ctrl" onclick="nextTrack()">⏭</button>
   </div>
   <div class="options">
    <button class="pill active" id="loop-btn" onclick="toggleLoop()">↻ วนซ้ำ</button>
    <button class="pill" id="shuffle-btn" onclick="toggleShuffle()">⤨ สุ่ม</button>
   </div>
  </div>
  <div class="foot">SPACE • LIGHT • SOUND • 1.618 ENERGY</div>
 </div>
 <div id="start">
  <h2>ENTER THE COSMOS</h2>
  <p>ฉากอวกาศสามมิติ • ไฟนีออน • คลื่นเสียงตามเพลงจริง<br>แตะเพื่อเริ่มสัมผัสประสบการณ์เสียงและภาพ</p>
  <button onclick="startApp()">✦ เริ่มประสบการณ์ TA101</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const SONGS = __SONGS_REPLACE__;
const LOGO = __LOGO_REPLACE__;
const audio = new Audio();
audio.preload = "auto";
audio.crossOrigin = "anonymous";

let index = 0, playing = false, shuffle = false, loopList = true;
let ctx = null, analyser = null, source = null, freq = null, waveData = null;

if(LOGO) {
    document.getElementById('logo').src = LOGO;
    document.getElementById('logo').style.display = 'block';
    document.getElementById('thumb').src = LOGO;
    document.getElementById('thumb').style.display = 'block';
}

function setTheme(a, b){
    document.documentElement.style.setProperty('--a', a);
    document.documentElement.style.setProperty('--b', b);
}

function initAudio(){
    if(ctx) return;
    const AC = window.AudioContext || window.webkitAudioContext;
    if(!AC) return;
    ctx = new AC();
    analyser = ctx.createAnalyser();
    analyser.fftSize = 256;
    analyser.smoothingTimeConstant = 0.8;
    source = ctx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(ctx.destination);
    freq = new Uint8Array(analyser.frequencyBinCount);
    waveData = new Uint8Array(analyser.fftSize);
}

function fillPlaylist(){
    const sel = document.getElementById('playlist');
    sel.innerHTML = '';
    if(!SONGS.length){
        sel.innerHTML = '<option>ไม่พบเพลง</option>';
        document.getElementById('track-title').textContent = "ไม่พบไฟล์เพลง MP3";
        return;
    }
    SONGS.forEach((s, i) => {
        let op = document.createElement('option');
        op.value = i;
        op.textContent = (i+1) + ". " + s.name;
        sel.appendChild(op);
    });
    loadTrack(0);
}

function loadTrack(i){
    if(!SONGS.length) return;
    index = (i + SONGS.length) % SONGS.length;
    audio.src = SONGS[index].src;
    audio.load();
    document.getElementById('track-title').textContent = SONGS[index].name;
    document.getElementById('track-sub').textContent = "TRACK " + (index+1) + " / " + SONGS.length;
    document.getElementById('playlist').value = index;
}

async function startApp(){
    document.getElementById('start').style.opacity = '0';
    setTimeout(() => document.getElementById('start').style.display = 'none', 500);
    fillPlaylist();
    initAudio();
    if(ctx && ctx.state === "suspended") await ctx.resume();
    playAudio();
}

function togglePlay(){
    if(playing) pauseAudio();
    else playAudio();
}

async function playAudio(){
    initAudio();
    if(ctx && ctx.state === "suspended") await ctx.resume();
    try {
        await audio.play();
        playing = true;
        document.getElementById('play').textContent = "Ⅱ";
    } catch(e) {
        playing = false;
        document.getElementById('play').textContent = "▶";
    }
}

function pauseAudio(){
    audio.pause();
    playing = false;
    document.getElementById('play').textContent = "▶";
}

function nextTrack(){
    if(!SONGS.length) return;
    if(shuffle && SONGS.length > 1
    
