import os
import json
import base64
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
page_title="TA101 | NEON MUSIC",
page_icon="🎧",
layout="wide",
initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent

AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"}
LOGO_NAMES = {"logo.jpg", "logo.jpeg", "logo.png", "logo1.jpg", "logo1.jpeg", "logo1.png"}

def find_audio_files():

def find_audio_files():
    files = []

    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [
            d for d in dirs
            if d not in {".git", "__pycache__", ".streamlit", "venv", ".venv"}
        ]

        for filename in filenames:
            path = Path(root) / filename
            if path.suffix.lower() in AUDIO_EXTENSIONS:
                files.append(path)

    return sorted(
        files,
        key=lambda p: (str(p.parent).lower(), p.name.lower())
    )

def encode_file(path):
mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
with open(path, "rb") as file:
encoded = base64.b64encode(file.read()).decode("ascii")
return f"data:{mime};base64,{encoded}"

def find_logo():
for name in ["logo.jpg", "logo1.jpg", "logo.jpeg", "logo1.jpeg",
"logo.png", "logo1.png"]:
path = BASE_DIR / name
if path.exists():
return encode_file(path)

```
for root, dirs, filenames in os.walk(BASE_DIR):
    dirs[:] = [
        d for d in dirs
        if d not in {".git", "__pycache__", ".streamlit", "venv", ".venv"}
    ]
    for filename in filenames:
        if filename.lower() in LOGO_NAMES:
            return encode_file(Path(root) / filename)

return ""
```

tracks = []
for path in find_audio_files():
try:
tracks.append({
"name": path.stem,
"src": encode_file(path),
})
except OSError:
pass

logo_src = find_logo()

tracks_json = json.dumps(
tracks, ensure_ascii=False, separators=(",", ":")
).replace("<", "\u003c")

logo_json = json.dumps(logo_src).replace("<", "\u003c")

st.markdown(
""" <style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {
background:
radial-gradient(ellipse at 50% 0%, #28104b 0%, #100b22 45%, #03040b 100%);
color: white;
}
.block-container {
padding-top: 0.6rem;
padding-bottom: 1rem;
max-width: 1500px;
} </style>
""",
unsafe_allow_html=True,
)

html_template = r"""

<!DOCTYPE html>

<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
html, body {
    margin: 0;
    width: 100%;
    min-height: 100%;
    background: transparent;
    color: #fff;
    font-family: Arial, sans-serif;
}
body { overflow-x: hidden; }
.app {
    position: relative;
    overflow: hidden;
    padding: 18px;
    border: 1px solid #693baf;
    border-radius: 24px;
    background: linear-gradient(150deg, #100b23f5, #050711f8 70%);
    box-shadow: 0 0 24px #8c35ff30, inset 0 0 28px #25205c50;
}
.glow {
    text-align: center;
    font-weight: 900;
    letter-spacing: 3px;
    font-size: clamp(27px, 5vw, 49px);
    background: linear-gradient(90deg, #00f5ff, #ff40da, #fff, #a45cff, #00f5ff);
    background-size: 300% 100%;
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    animation: shimmer 4s linear infinite;
    filter: drop-shadow(0 0 12px #a946ff);
}
@keyframes shimmer { to { background-position: 300% 0; } }
.tagline {
    text-align: center;
    color: #d4b9ff;
    font-size: 12px;
    letter-spacing: 4px;
    margin: 8px 0 18px;
}
.logo-wrap {
    text-align: center;
    min-height: 0;
}
.logo {
    max-width: 125px;
    max-height: 100px;
    object-fit: contain;
    border-radius: 15px;
    filter: drop-shadow(0 0 12px #9b4dff);
    margin: 0 auto 12px;
}
.visualizer {
    display: block;
    width: 100%;
    height: 190px;
    border-radius: 16px;
    background: radial-gradient(ellipse at center, #191139, #060712 75%);
    border: 1px solid #34205c;
}
.speaker-area {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0 12px;
    min-height: 205px;
}
.speaker {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: radial-gradient(circle, #20213b 0%, #0a0b15 63%, #21103d 100%);
    border: 3px solid #a54bff;
    box-shadow: 0 0 20px #b33cffaa, inset 0 0 25px #00eaff40;
    transition: transform .06s linear, box-shadow .06s linear;
}
.speaker:before {
    content: "";
    position: absolute;
    inset: 10px;
    border: 2px solid #18eaff;
    border-radius: 50%;
    box-shadow: 0 0 12px #18eaff;
}
.speaker:after {
    content: "";
    position: absolute;
    inset: 25px;
    border: 5px dashed #f344de;
    border-radius: 50%;
    animation: spin 10s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.cone {
    width: 78px;
    height: 78px;
    border-radius: 50%;
    z-index: 1;
    background: radial-gradient(circle at 35% 30%, #fcfcff, #bd4bff 17%, #17162d 45%, #03040a 70%);
    border: 3px solid #00f5ff;
    box-shadow: 0 0 18px #00dfff, inset 0 0 15px #e44dff;
}
.status {
    text-align: center;
    color: #3bf6ff;
    font-size: 12px;
    letter-spacing: 2px;
    margin: 3px 0 14px;
}
.song-name {
    text-align: center;
    font-size: clamp(17px, 3vw, 24px);
    font-weight: 800;
    color: #fff;
    text-shadow: 0 0 7px #fff, 0 0 16px #fa3bff, 0 0 25px #814dff;
    overflow-wrap: anywhere;
    margin: 10px 0;
}
.time {
    text-align: center;
    color: #b9b4d8;
    font-size: 12px;
    margin: 8px 0;
}
.controls {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 12px 0;
}
button {
    cursor: pointer;
    border: 1px solid #9f62ff;
    border-radius: 999px;
    padding: 11px 18px;
    color: white;
    font-weight: 800;
    background: linear-gradient(120deg, #6527a8, #b326a9);
    box-shadow: 0 0 12px #8c35ff65;
}
button:hover { filter: brightness(1.25); }
button:active { transform: scale(.97); }
button.secondary {
    background: #111629;
    border-color: #16dff5;
}
.progress {
    width: 100%;
    accent-color: #ed49ff;
    cursor: pointer;
}
.volume-row {
    display: flex;
    gap: 12px;
    align-items: center;
    color: #bdefff;
    font-size: 12px;
    margin: 12px 0;
}
.volume-row input { width: 100%; accent-color: #00eaff; }
.playlist-title {
    color: #54f7ff;
    letter-spacing: 2px;
    font-weight: 800;
    margin: 20px 0 10px;
    text-shadow: 0 0 10px #00cfff;
}
.playlist {
    display: flex;
    flex-direction: column;
    gap: 7px;
    max-height: 250px;
    overflow-y: auto;
}
.track {
    text-align: left;
    border-radius: 10px;
    background: #121126;
    border: 1px solid #30214f;
    padding: 10px 12px;
    font-weight: 500;
    overflow-wrap: anywhere;
}
.track.active {
    border-color: #ff48e8;
    background: linear-gradient(90deg, #3b1459, #17112d);
    box-shadow: 0 0 12px #e63fff40;
    color: #fff;
}
.footer {
    text-align: center;
    color: #b7a4e8;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 22px;
}
.empty {
    text-align: center;
    color: #ffc5ee;
    padding: 24px 8px;
    line-height: 1.8;
}
@media (max-width: 520px) {
    .app { padding: 12px; border-radius: 17px; }
    .visualizer { height: 150px; }
    .speaker { width: 130px; height: 130px; }
    .cone { width: 62px; height: 62px; }
    .speaker-area { min-height: 165px; }
    button { padding: 10px 14px; }
}
</style>
</head>
<body>
<div class="app">
    <div class="logo-wrap" id="logoWrap"></div>
    <div class="glow">🎧 TA101 NEON MUSIC 🎧</div>
    <div class="tagline">FEEL THE BASS • SEE THE SOUND</div>

```
<canvas class="visualizer" id="visualizer"></canvas>

<div class="speaker-area">
    <div class="speaker" id="speaker"><div class="cone"></div></div>
</div>
<div class="status" id="status">READY TO PLAY</div>
<div class="song-name" id="songName">กำลังเตรียมเพลง...</div>

<div class="time" id="timeLabel">00:00 / 00:00</div>
<input class="progress" id="progress" type="range" min="0" max="1000" value="0">

<div class="controls">
    <button class="secondary" id="prevBtn">⏮ ก่อนหน้า</button>
    <button id="playBtn">▶ เริ่มเล่นเพลง</button>
    <button class="secondary" id="nextBtn">ถัดไป ⏭</button>
</div>

<div class="volume-row">
    <span>🔉 เสียง</span>
    <input id="volume" type="range" min="0" max="100" value="85">
    <span id="volumeLabel">85%</span>
</div>

<audio id="audio" preload="metadata" playsinline></audio>

<div class="playlist-title">✦ PLAYLIST ✦</div>
<div class="playlist" id="playlist"></div>
<div class="footer">TA101 • NEON LIGHTS • MUSIC FOREVER 💜</div>
```

</div>

<script>
const TRACKS = __TRACKS_JSON__;
const LOGO = __LOGO_JSON__;

const audio = document.getElementById("audio");
const canvas = document.getElementById("visualizer");
const ctx = canvas.getContext("2d");
const speaker = document.getElementById("speaker");
const playBtn = document.getElementById("playBtn");
const statusEl = document.getElementById("status");
const songName = document.getElementById("songName");
const timeLabel = document.getElementById("timeLabel");
const progress = document.getElementById("progress");
const playlist = document.getElementById("playlist");
const volume = document.getElementById("volume");
const volumeLabel = document.getElementById("volumeLabel");

let current = 0;
let audioContext = null;
let analyser = null;
let sourceNode = null;
let frequencyData = null;
let timeData = null;
let playing = false;
let frame = 0;
let playlistButtons = [];

if (LOGO) {
    const img = document.createElement("img");
    img.className = "logo";
    img.src = LOGO;
    img.alt = "TA101 logo";
    document.getElementById("logoWrap").appendChild(img);
}

function formatTime(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) return "00:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
}

function setupAudioGraph() {
    if (audioContext) {
        if (audioContext.state === "suspended") audioContext.resume();
        return;
    }

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) {
        statusEl.textContent = "BROWSER AUDIO ANALYSIS UNAVAILABLE";
        return;
    }

    audioContext = new AudioCtx();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 1024;
    analyser.smoothingTimeConstant = 0.72;
    frequencyData = new Uint8Array(analyser.frequencyBinCount);
    timeData = new Uint8Array(analyser.fftSize);

    sourceNode = audioContext.createMediaElementSource(audio);
    sourceNode.connect(analyser);
    analyser.connect(audioContext.destination);
}

function renderPlaylist() {
    playlist.innerHTML = "";
    playlistButtons = [];

    TRACKS.forEach((track, index) => {
        const button = document.createElement("button");
        button.className = "track";
        button.textContent = (index + 1) + ". " + track.name;
        button.addEventListener("click", () => playTrack(index));
        playlist.appendChild(button);
        playlistButtons.push(button);
    });

    updatePlaylist();
}

function updatePlaylist() {
    playlistButtons.forEach((button, index) => {
        button.classList.toggle("active", index === current);
    });
}

function setTrackName() {
    if (!TRACKS.length) {
        songName.textContent = "ยังไม่พบไฟล์เพลง";
        return;
    }
    songName.textContent = TRACKS[current].name;
    updatePlaylist();
}

async function playTrack(index) {
    if (!TRACKS.length) {
        statusEl.textContent = "ไม่พบไฟล์เพลงในโปรเจกต์";
        return;
    }

    current = (index + TRACKS.length) % TRACKS.length;
    audio.pause();
    audio.src = TRACKS[current].src;
    audio.load();
    setTrackName();

    try {
        setupAudioGraph();
        if (audioContext && audioContext.state === "suspended") {
            await audioContext.resume();
        }
        await audio.play();
        playing = true;
        playBtn.textContent = "⏸ หยุดชั่วคราว";
        statusEl.textContent = "♪ NOW PLAYING • NEON MODE ♪";
    } catch (error) {
        playing = false;
        playBtn.textContent = "▶ เริ่มเล่นเพลง";
        statusEl.textContent = "กดปุ่มเล่นอีกครั้งเพื่อเริ่มเพลง";
    }
}

playBtn.addEventListener("click", async () => {
    if (!TRACKS.length) {
        statusEl.textContent = "กรุณาเพิ่มไฟล์เพลง MP3 ในโปรเจกต์";
        return;
    }

    if (audio.paused) {
        if (!audio.src) {
            await playTrack(current);
            return;
        }

        try {
            setupAudioGraph();
            if (audioContext && audioContext.state === "suspended") {
                await audioContext.resume();
            }
            await audio.play();
            playing = true;
            playBtn.textContent = "⏸ หยุดชั่วคราว";
            statusEl.textContent = "♪ NOW PLAYING • NEON MODE ♪";
        } catch (error) {
            statusEl.textContent = "แตะเล่นอีกครั้งเพื่อเริ่มเสียง";
        }
    } else {
        audio.pause();
    }
});

document.getElementById("prevBtn").addEventListener("click", () => {
    playTrack(current - 1);
});

document.getElementById("nextBtn").addEventListener("click", () => {
    playTrack(current + 1);
});

audio.addEventListener("play", () => {
    playing = true;
    playBtn.textContent = "⏸ หยุดชั่วคราว";
    statusEl.textContent = "♪ NOW PLAYING • NEON MODE ♪";
});

audio.addEventListener("pause", () => {
    playing = false;
    playBtn.textContent = "▶ เล่นเพลงต่อ";
    if (audio.currentTime > 0 && !audio.ended) {
        statusEl.textContent = "PAUSED • กดเล่นเพื่อฟังต่อ";
    }
});

audio.addEventListener("ended", () => {
    if (TRACKS.length > 1) {
        playTrack(current + 1);
    } else if (TRACKS.length === 1) {
        audio.currentTime = 0;
        audio.play().catch(() => {});
    }
});

audio.addEventListener("timeupdate", () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
        progress.value = Math.round((audio.currentTime / audio.duration) * 1000);
    }
    timeLabel.textContent = formatTime(audio.currentTime) + " / " + formatTime(audio.duration);
});

audio.addEventListener("loadedmetadata", () => {
    timeLabel.textContent = formatTime(audio.currentTime) + " / " + formatTime(audio.duration);
});

audio.addEventListener("error", () => {
    statusEl.textContent = "เล่นไฟล์นี้ไม่ได้ ลองตรวจสอบชนิดไฟล์เพลง";
});

progress.addEventListener("input", () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
        audio.currentTime = (Number(progress.value) / 1000) * audio.duration;
    }
});

volume.addEventListener("input", () => {
    audio.volume = Number(volume.value) / 100;
    volumeLabel.textContent = volume.value + "%";
});

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

function drawVisualizer() {
    frame++;
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createRadialGradient(w / 2, h / 2, 5, w / 2, h / 2, w * 0.7);
    bg.addColorStop(0, "#171032");
    bg.addColorStop(1, "#050611");
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    let bass = 0;
    let level = 0;

    if (analyser && playing) {
        analyser.getByteFrequencyData(frequencyData);
        analyser.getByteTimeDomainData(timeData);

        const bassEnd = Math.min(24, frequencyData.length);
        for (let i = 0; i < bassEnd; i++) bass += frequencyData[i];
        bass = bassEnd ? bass / (bassEnd * 255) : 0;

        for (let i = 0; i < frequencyData.length; i++) {
            level += frequencyData[i];
        }
        level = level / (frequencyData.length * 255);
    }

    const centerY = h / 2;
    const barCount = Math.max(36, Math.min(100, Math.floor(w / 5)));
    const gap = 2;
    const barWidth = Math.max(2, (w - gap * (barCount - 1)) / barCount);

    for (let i = 0; i < barCount; i++) {
        let value = 0.025;

        if (analyser && playing && frequencyData) {
            const dataIndex = Math.floor(i / barCount * frequencyData.length);
            value = frequencyData[dataIndex] / 255;
        } else {
            value = 0.035 + Math.abs(Math.sin(frame * 0.025 + i * 0.2)) * 0.025;
        }

        const height = Math.max(3, value * h * 0.88);
        const x = i * (barWidth + gap);
        const hue = (frame * 1.5 + i * 5) % 360;

        const gradient = ctx.createLinearGradient(0, centerY - height / 2, 0, centerY + height / 2);
        gradient.addColorStop(0, `hsla(${hue},100%,70%,0.2)`);
        gradient.addColorStop(0.45, `hsl(${hue},100%,65%)`);
        gradient.addColorStop(1, `hsl(${(hue + 70) % 360},100%,55%)`);

        ctx.shadowBlur = playing ? 13 : 4;
        ctx.shadowColor = `hsl(${hue},100%,60%)`;
        ctx.fillStyle = gradient;
        ctx.fillRect(x, centerY - height / 2, barWidth, height);
        ctx.fillRect(x, centerY + height / 2, barWidth, 2);
    }

    ctx.shadowBlur = 0;

    if (analyser && playing && timeData) {
        ctx.beginPath();
        for (let i = 0; i < timeData.length; i++) {
            const x = i / (timeData.length - 1) * w;
            const y = timeData[i] / 255 * h;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#ffffff";
        ctx.shadowBlur = 12;
        ctx.shadowColor = "#00eaff";
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    const scale = 1 + bass * 0.23;
    speaker.style.transform = `scale(${scale})`;
    speaker.style.boxShadow =
        `0 0 ${18 + bass * 55}px rgba(184,60,255,${0.55 + bass * 0.4}),
         inset 0 0 ${20 + bass * 45}px rgba(0,234,255,${0.25 + bass * 0.5})`;

    requestAnimationFrame(drawVisualizer);
}

if (!TRACKS.length) {
    songName.textContent = "ยังไม่พบไฟล์เพลง";
    statusEl.textContent = "เพิ่มไฟล์เพลงในโฟลเดอร์โปรเจกต์";
    playlist.innerHTML =
        '<div class="empty">ไม่พบไฟล์เพลงที่รองรับ<br>ใส่ไฟล์ MP3 ไว้ข้าง app.py หรือในโฟลเดอร์ย่อย<br>แล้วรีเฟรชแอปอีกครั้งครับ 🎵</div>';
} else {
    setTrackName();
    renderPlaylist();
}

drawVisualizer();
</script>

</body>
</html>
"""

html = (
html_template
.replace("**TRACKS_JSON**", tracks_json)
.replace("**LOGO_JSON**", logo_json)
)

st.caption("🎧 TA101 • NEON MUSIC • เครื่องเล่นเพลงและกราฟเสียง")
components.html(html, height=1120, scrolling=True)
          
