
import os
import json
import base64
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 NEON MUSIC",
    page_icon="🎧",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"}
SKIP_DIRS = {".git", "__pycache__", ".streamlit", ".venv", "venv"}

def find_files(extensions):
    result = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(root) / filename
            if path.suffix.lower() in extensions:
                result.append(path)
    return sorted(result, key=lambda p: p.name.lower())

def encode_file(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    with open(path, "rb") as file:
        data = base64.b64encode(file.read()).decode("ascii")
    return "data:" + mime + ";base64," + data

tracks = []
for path in find_files(AUDIO_EXTENSIONS):
    try:
        tracks.append({
            "name": path.stem,
            "src": encode_file(path),
        })
    except OSError:
        pass

logo_src = ""
for path in find_files({".jpg", ".jpeg", ".png", ".webp"}):
    if path.name.lower() in {
        "logo.jpg", "logo1.jpg", "logo.jpeg",
        "logo1.jpeg", "logo.png", "logo1.png",
        "logo.webp", "logo1.webp",
    }:
        try:
            logo_src = encode_file(path)
            break
        except OSError:
            pass

tracks_json = json.dumps(tracks, ensure_ascii=False).replace("<", "\\u003c")
logo_json = json.dumps(logo_src).replace("<", "\\u003c")

st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility:hidden;}
    .stApp {
        background: radial-gradient(ellipse at top, #291047, #090817 55%, #03040a);
        color: white;
    }
    .block-container {padding-top: 1rem; max-width: 1200px;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing:border-box}
body {
    margin:0;
    background:transparent;
    color:white;
    font-family:Arial,sans-serif;
}
.panel {
    background:linear-gradient(145deg,#120d27,#050711);
    border:1px solid #7936b6;
    border-radius:22px;
    padding:16px;
    box-shadow:0 0 28px #a13dff30;
    overflow:hidden;
}
.logo {
    display:block;
    max-width:130px;
    max-height:95px;
    object-fit:contain;
    margin:0 auto 12px;
    border-radius:12px;
    filter:drop-shadow(0 0 12px #c04bff);
}
h1 {
    text-align:center;
    font-size:clamp(25px,5vw,46px);
    letter-spacing:2px;
    background:linear-gradient(90deg,#00f5ff,#ff42d6,#ffffff,#a76aff,#00f5ff);
    background-size:300% auto;
    color:transparent;
    -webkit-background-clip:text;
    background-clip:text;
    animation:shine 4s linear infinite;
    filter:drop-shadow(0 0 10px #a63dff);
}
@keyframes shine {to{background-position:300% center}}
.tag {
    text-align:center;
    color:#c6aaff;
    letter-spacing:3px;
    font-size:11px;
    margin-bottom:18px;
}
canvas {
    display:block;
    width:100%;
    height:180px;
    background:#080817;
    border:1px solid #302052;
    border-radius:14px;
}
.speaker-area {
    height:185px;
    display:flex;
    align-items:center;
    justify-content:center;
}
.speaker {
    width:140px;
    height:140px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    border:3px solid #b44cff;
    background:radial-gradient(circle,#25203e,#080914 70%);
    box-shadow:0 0 24px #b64cff,inset 0 0 25px #00dfff55;
    transition:transform .06s linear;
}
.cone {
    width:75px;
    height:75px;
    border-radius:50%;
    border:4px solid #00eaff;
    background:radial-gradient(circle at 35% 30%,white,#c044ff 20%,#141326 65%,black);
    box-shadow:0 0 20px #00eaff;
}
.status {
    text-align:center;
    color:#00efff;
    font-size:12px;
    letter-spacing:2px;
    margin:8px 0;
}
.song {
    text-align:center;
    color:white;
    font-size:22px;
    font-weight:bold;
    overflow-wrap:anywhere;
    text-shadow:0 0 8px #ff39e9,0 0 18px #a43cff;
    margin:14px 0;
}
.time {
    text-align:center;
    color:#cbbbe9;
    font-size:12px;
    margin:8px;
}
input[type=range] {
    width:100%;
    accent-color:#ed43ff;
}
.controls {
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:8px;
    margin:12px 0;
}
button {
    border:1px solid #a95aff;
    border-radius:30px;
    background:linear-gradient(120deg,#6021a2,#b625a8);
    color:white;
    font-weight:bold;
    padding:11px 15px;
    cursor:pointer;
}
button:active {transform:scale(.97)}
.secondary {background:#101326;border-color:#00dff5}
.label {
    color:#61f6ff;
    margin:20px 0 10px;
    font-weight:bold;
    letter-spacing:2px;
}
.playlist {display:flex;flex-direction:column;gap:7px;max-height:240px;overflow:auto}
.track {
    width:100%;
    text-align:left;
    overflow-wrap:anywhere;
    background:#111026;
    border-color:#30204e;
    border-radius:10px;
    font-weight:normal;
}
.track.active {border-color:#ff4be6;background:#35144c}
.note {text-align:center;color:#c5b5e7;font-size:12px;line-height:1.8}
@media(max-width:500px) {
    .panel{padding:10px}
    canvas{height:145px}
    .speaker-area{height:160px}
    .speaker{width:120px;height:120px}
    .cone{width:65px;height:65px}
    button{padding:10px 12px}
}
</style>
</head>
<body>
<div class="panel">
    <div id="logoBox"></div>
    <h1>🎧 TA101 NEON MUSIC 🎧</h1>
    <div class="tag">FEEL THE BASS • SEE THE SOUND</div>

    <canvas id="visual"></canvas>

    <div class="speaker-area">
        <div class="speaker" id="speaker">
            <div class="cone"></div>
        </div>
    </div>

    <div class="status" id="status">READY TO PLAY</div>
    <div class="song" id="song">กำลังเตรียมเพลง...</div>
    <div class="time" id="time">00:00 / 00:00</div>
    <input id="seek" type="range" min="0" max="1000" value="0">

    <div class="controls">
        <button class="secondary" id="prev">⏮ ก่อนหน้า</button>
        <button id="toggle">▶ เริ่มเล่น</button>
        <button class="secondary" id="next">ถัดไป ⏭</button>
    </div>

    <div class="note">🔊 ระดับเสียง</div>
    <input id="volume" type="range" min="0" max="100" value="85">

    <audio id="audio" preload="metadata" playsinline></audio>

    <div class="label">✦ PLAYLIST ✦</div>
    <div class="playlist" id="playlist"></div>
    <div class="note">TA101 • NEON LIGHTS • MUSIC FOREVER 💜</div>
</div>

<script>
const TRACKS = __TRACKS__;
const LOGO = __LOGO__;

const audio = document.getElementById("audio");
const canvas = document.getElementById("visual");
const ctx = canvas.getContext("2d");
const speaker = document.getElementById("speaker");
const songEl = document.getElementById("song");
const statusEl = document.getElementById("status");
const toggle = document.getElementById("toggle");
const seek = document.getElementById("seek");
const timeEl = document.getElementById("time");
const playlist = document.getElementById("playlist");

let index = 0;
let audioCtx = null;
let analyser = null;
let source = null;
let freq = null;
let wave = null;
let frame = 0;
let buttons = [];

if (LOGO) {
    const img = document.createElement("img");
    img.src = LOGO;
    img.className = "logo";
    img.alt = "TA101 Logo";
    document.getElementById("logoBox").appendChild(img);
}

function clock(value) {
    if (!Number.isFinite(value) || value < 0) return "00:00";
    return String(Math.floor(value / 60)).padStart(2, "0") + ":" +
           String(Math.floor(value % 60)).padStart(2, "0");
}

function setupAudio() {
    if (audioCtx) {
        if (audioCtx.state === "suspended") audioCtx.resume();
        return;
    }
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) {
        statusEl.textContent = "BROWSER DOES NOT SUPPORT AUDIO ANALYSIS";
        return;
    }
    audioCtx = new AudioContextClass();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 1024;
    analyser.smoothingTimeConstant = 0.72;
    freq = new Uint8Array(analyser.frequencyBinCount);
    wave = new Uint8Array(analyser.fftSize);
    source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
}

function drawPlaylist() {
    playlist.innerHTML = "";
    buttons = [];
    TRACKS.forEach((track, i) => {
        const b = document.createElement("button");
        b.className = "track";
        b.textContent = (i + 1) + ". " + track.name;
        b.addEventListener("click", () => playTrack(i));
        playlist.appendChild(b);
        buttons.push(b);
    });
    markCurrent();
}

function markCurrent() {
    buttons.forEach((b, i) => b.classList.toggle("active", i === index));
}

function showSong() {
    songEl.textContent = TRACKS[index] ? TRACKS[index].name : "ยังไม่พบไฟล์เพลง";
    markCurrent();
}

async function playTrack(i) {
    if (!TRACKS.length) {
        statusEl.textContent = "กรุณาเพิ่มไฟล์เพลงในโปรเจกต์";
        return;
    }
    index = (i + TRACKS.length) % TRACKS.length;
    audio.pause();
    audio.src = TRACKS[index].src;
    audio.load();
    showSong();

    try {
        setupAudio();
        if (audioCtx && audioCtx.state === "suspended") await audioCtx.resume();
        await audio.play();
        statusEl.textContent = "♪ NOW PLAYING • NEON MODE ♪";
    } catch (e) {
        statusEl.textContent = "แตะปุ่มเล่นอีกครั้งเพื่อเริ่มเพลง";
    }
}

toggle.addEventListener("click", async () => {
    if (!TRACKS.length) {
        statusEl.textContent = "ไม่พบไฟล์เพลง";
        return;
    }
    if (audio.paused) {
        if (!audio.src) {
            await playTrack(index);
            return;
        }
        try {
            setupAudio();
            if (audioCtx && audioCtx.state === "suspended") await audioCtx.resume();
            await audio.play();
        } catch (e) {
            statusEl.textContent = "กดเล่นอีกครั้งเพื่อเริ่มเสียง";
        }
    } else {
        audio.pause();
    }
});

audio.addEventListener("play", () => {
    toggle.textContent = "⏸ หยุดชั่วคราว";
    statusEl.textContent = "♪ NOW PLAYING • NEON MODE ♪";
});
audio.addEventListener("pause", () => {
    toggle.textContent = "▶ เล่นเพลงต่อ";
    if (!audio.ended && audio.currentTime > 0) statusEl.textContent = "PAUSED";
});
audio.addEventListener("ended", () => {
    if (TRACKS.length > 1) playTrack(index + 1);
    else if (TRACKS.length === 1) playTrack(0);
});
audio.addEventListener("timeupdate", () => {
    if (audio.duration > 0) seek.value = audio.currentTime / audio.duration * 1000;
    timeEl.textContent = clock(audio.currentTime) + " / " + clock(audio.duration);
});
audio.addEventListener("loadedmetadata", () => {
    timeEl.textContent = clock(audio.currentTime) + " / " + clock(audio.duration);
});
audio.addEventListener("error", () => {
    statusEl.textContent = "ไฟล์เพลงนี้เล่นไม่ได้ โปรดตรวจสอบชนิดไฟล์";
});

seek.addEventListener("input", () => {
    if (audio.duration > 0) audio.currentTime = seek.value / 1000 * audio.duration;
});
document.getElementById("volume").addEventListener("input", e => {
    audio.volume = Number(e.target.value) / 100;
});
document.getElementById("prev").addEventListener("click", () => playTrack(index - 1));
document.getElementById("next").addEventListener("click", () => playTrack(index + 1));
audio.volume = 0.85;

function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.floor(rect.width * ratio));
    canvas.height = Math.max(1, Math.floor(rect.height * ratio));
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

function animate() {
    requestAnimationFrame(animate);
    frame++;
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, w, h);
    bg.addColorStop(0, "#080a1a");
    bg.addColorStop(0.5, "#1a0d2c");
    bg.addColorStop(1, "#050611");
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    let bass = 0;
    if (analyser && !audio.paused) {
        analyser.getByteFrequencyData(freq);
        analyser.getByteTimeDomainData(wave);
        const n = Math.min(24, freq.length);
        for (let i = 0; i < n; i++) bass += freq[i];
        bass = n ? bass / (n * 255) : 0;
    }

    const count = Math.max(32, Math.floor(w / 5));
    const gap = 2;
    const bw = (w - (count - 1) * gap) / count;
    const cy = h / 2;

    for (let i = 0; i < count; i++) {
        let value;
        if (analyser && !audio.paused) {
            const j = Math.floor(i / count * freq.length);
            value = freq[j] / 255;
        } else {
            value = 0.035 + Math.abs(Math.sin(frame * 0.025 + i * 0.2)) * 0.02;
        }

        const bh = Math.max(3, value * h * 0.88);
        const hue = (frame * 1.8 + i * 6) % 360;
        const x = i * (bw + gap);
        const grad = ctx.createLinearGradient(0, cy - bh / 2, 0, cy + bh / 2);
        grad.addColorStop(0, "hsla(" + hue + ",100%,70%,0.25)");
        grad.addColorStop(0.5, "hsl(" + hue + ",100%,65%)");
        grad.addColorStop(1, "hsl(" + ((hue + 70) % 360) + ",100%,55%)");

        ctx.fillStyle = grad;
        ctx.shadowBlur = 12;
        ctx.shadowColor = "hsl(" + hue + ",100%,60%)";
        ctx.fillRect(x, cy - bh / 2, bw, bh);
    }

    if (analyser && !audio.paused) {
        ctx.beginPath();
        for (let i = 0; i < wave.length; i++) {
            const x = i / (wave.length - 1) * w;
            const y = wave[i] / 255 * h;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.shadowBlur = 12;
        ctx.shadowColor = "#00eaff";
        ctx.stroke();
    }

    ctx.shadowBlur = 0;
    speaker.style.transform = "scale(" + (1 + bass * 0.23) + ")";
}

if (TRACKS.length) {
    drawPlaylist();
    showSong();
} else {
    songEl.textContent = "ยังไม่พบไฟล์เพลง";
    statusEl.textContent = "เพิ่มไฟล์ MP3 ในโฟลเดอร์โปรเจกต์";
    playlist.innerHTML =
        '<div class="note">วางไฟล์เพลงไว้ข้าง app.py หรือในโฟลเดอร์ย่อย แล้วรีเฟรชแอปครับ</div>';
}

animate();
</script>
</body>
</html>
"""

html = html.replace("__TRACKS__", tracks_json).replace("__LOGO__", logo_json)

st.caption("🎧 TA101 • NEON MUSIC")
components.html(html, height=1100, scrolling=True)
