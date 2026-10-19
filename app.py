
# ============================================================
# SYNAPSE NEON MUSIC PLAYER
# PART 1 OF 3
# ============================================================

from pathlib import Path
import base64
import json
import mimetypes

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SYNAPSE NEON MUSIC PLAYER",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo1.jpg"

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".m4a",
    ".aac", ".opus", ".flac"
}


def load_logo():
    if LOGO_PATH.is_file():
        mime = mimetypes.guess_type(str(LOGO_PATH))[0] or "image/jpeg"
        encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{encoded}"
    return ""


def load_tracks():
    tracks = []

    for path in sorted(BASE_DIR.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file():
            continue

        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            continue

        try:
            raw = path.read_bytes()
            if not raw:
                continue

            mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
            encoded = base64.b64encode(raw).decode("ascii")

            tracks.append({
                "title": path.stem,
                "filename": path.name,
                "src": f"data:{mime};base64,{encoded}",
            })

        except OSError:
            continue

    return tracks


tracks = load_tracks()
logo_src = load_logo()

st.markdown(
    """
    <style>
    #MainMenu, footer, header, [data-testid="stToolbar"] {
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 10%, #241044 0%, transparent 40%),
            radial-gradient(ellipse at 85% 30%, #003b50 0%, transparent 40%),
            linear-gradient(145deg, #05030d, #080a19 55%, #10051d);
        color: #f8f7ff;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1100px;
        padding-top: 1rem;
    }

    h1, h2, h3, p, label {
        color: #f8f7ff;
    }

    .synapse-title {
        text-align: center;
        font-size: clamp(30px, 6vw, 58px);
        font-weight: 900;
        letter-spacing: 7px;
        color: #ffffff;
        text-shadow:
            0 0 8px #00eaff,
            0 0 20px #00eaff,
            0 0 45px #9a36ff;
        margin-bottom: 0;
    }

    .synapse-subtitle {
        text-align: center;
        color: #9dfaff;
        font-size: 12px;
        letter-spacing: 4px;
        margin-bottom: 22px;
    }

    div[data-testid="stButton"] button {
        border: 1px solid #00eaff;
        border-radius: 14px;
        background: linear-gradient(135deg, #151c38, #24103c);
        color: white;
        box-shadow: 0 0 12px #00eaff44;
        font-weight: bold;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #ff38d1;
        color: white;
        box-shadow: 0 0 22px #ff38d177;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="synapse-title">SYNAPSE</div>'
    '<div class="synapse-subtitle">'
    'SOUND & VISUAL THERAPY • NEON AUDIO EXPERIENCE'
    '</div>',
    unsafe_allow_html=True,
)

if not logo_src:
    st.info("ไม่พบ logo1.jpg กรุณาวางไฟล์ไว้ข้าง app.py")

if not tracks:
    st.warning(
        "ไม่พบไฟล์เพลง กรุณาวาง MP3 หรือไฟล์เสียง "
        "ไว้ในโฟลเดอร์เดียวกับ app.py"
    )
 
# ============================================================
# PART 2 OF 3 — PLAYER HTML / CSS
# วางต่อจากช่วงที่ 1 ทันที
# ============================================================

if tracks:
    tracks_json = json.dumps(tracks, ensure_ascii=False)

    player_html = r"""
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 10px 4px 25px;
    background: transparent;
    color: #fff;
    font-family: Arial, Tahoma, sans-serif;
}

:root {
    --cyan: #00f5ff;
    --pink: #ff31d2;
    --purple: #a64dff;
    --green: #5dffbd;
}

.player {
    max-width: 1050px;
    margin: auto;
    padding: 20px;
    overflow: hidden;
    border: 1px solid #00eaff88;
    border-radius: 26px;
    background:
        radial-gradient(ellipse at 50% 0%, #25205a99, transparent 55%),
        linear-gradient(145deg, #090d20, #100a21 65%, #071522);
    box-shadow: 0 0 22px #00eaff22, inset 0 0 45px #6d31ff12;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    border-bottom: 1px solid #ffffff18;
    padding-bottom: 14px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo, .logo-placeholder {
    width: 66px;
    height: 66px;
    object-fit: cover;
    border-radius: 17px;
    border: 1px solid var(--cyan);
    box-shadow: 0 0 15px #00eaff88, 0 0 28px #a64dff55;
}

.logo-placeholder {
    display: grid;
    place-items: center;
    font-size: 34px;
}

.brand-name {
    font-size: 19px;
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow: 0 0 12px var(--cyan);
}

.brand-desc {
    margin-top: 5px;
    color: #9ba9d7;
    font-size: 10px;
    letter-spacing: 2px;
}

.live {
    color: var(--green);
    font-size: 11px;
    letter-spacing: 2px;
    text-shadow: 0 0 10px var(--green);
}

.visual-area {
    margin: 18px 0;
    padding: 12px;
    border: 1px solid #ffffff12;
    border-radius: 20px;
    background: #03061188;
    overflow: hidden;
}

.visual-top, .visual-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    color: #9ca8cf;
    font-size: 10px;
    letter-spacing: 1px;
}

#visualizer {
    width: 100%;
    height: 145px;
    display: block;
}

.main-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 16px;
}

.panel {
    padding: 16px;
    border: 1px solid #a64dff55;
    border-radius: 20px;
    background: rgba(13, 16, 39, .92);
    min-width: 0;
    box-shadow: inset 0 0 25px #a64dff09;
}

.panel-heading {
    color: var(--cyan);
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 14px;
}

.deck {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.vinyl-wrap {
    width: min(64vw, 235px);
    aspect-ratio: 1;
    position: relative;
    display: grid;
    place-items: center;
    margin: 5px auto 20px;
}

.vinyl {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: repeating-radial-gradient(
        circle at center,
        #11131b 0px,
        #242638 2px,
        #080a11 4px,
        #171a28 6px
    );
    border: 2px solid #4a4565;
    box-shadow: inset 0 0 25px #000, 0 0 20px #00eaff20;
    position: relative;
    animation: spin 5s linear infinite;
    animation-play-state: paused;
}

.vinyl.playing { animation-play-state: running; }

.vinyl::before {
    content: "";
    position: absolute;
    inset: 10%;
    border-radius: 50%;
    border: 1px solid #ffffff12;
    box-shadow: 0 0 0 10px #ffffff04, 0 0 0 22px #ffffff04;
}

.vinyl-label {
    position: absolute;
    width: 34%;
    aspect-ratio: 1;
    top: 33%;
    left: 33%;
    border-radius: 50%;
    background: conic-gradient(#00eaff, #8b37ff, #ff31d2, #00eaff);
    border: 4px solid #0c0d18;
    display: grid;
    place-items: center;
    overflow: hidden;
}

.vinyl-label img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.vinyl-hole {
    position: absolute;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #f5f5ff;
    box-shadow: 0 0 8px white;
}

@keyframes spin { to { transform: rotate(360deg); } }

.track-title {
    width: 100%;
    text-align: center;
    font-size: clamp(15px, 2.5vw, 21px);
    font-weight: 800;
    overflow-wrap: anywhere;
    text-shadow: 0 0 12px #00eaff66;
    margin: 3px 0 5px;
}

.track-subtitle {
    text-align: center;
    color: #929fc7;
    font-size: 11px;
    margin-bottom: 14px;
}

.progress { width: 100%; }

.time-row {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #b7c4eb;
    margin: 7px 0;
}

input[type=range] {
    width: 100%;
    accent-color: var(--cyan);
    cursor: pointer;
}

.controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    margin: 16px 0 10px;
    flex-wrap: wrap;
}

.ctrl {
    min-width: 40px;
    height: 40px;
    border-radius: 13px;
    border: 1px solid #a64dff88;
    color: white;
    background: #15152e;
    cursor: pointer;
    font-size: 17px;
}

.ctrl:hover, .ctrl.active {
    border-color: var(--cyan);
    box-shadow: 0 0 15px #00eaff66;
    color: var(--cyan);
}

.ctrl.play {
    width: 58px;
    height: 52px;
    border-color: var(--cyan);
    background: linear-gradient(135deg, #07566c, #64268c);
    font-size: 22px;
    box-shadow: 0 0 20px #00eaff44;
}

.mode-label {
    text-align: center;
    color: #9dfaff;
    font-size: 10px;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.eq-row { margin: 16px 0; }

.eq-head {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    font-size: 12px;
    margin-bottom: 7px;
}

.eq-value { color: var(--cyan); }

.speaker-row {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 10px 0 4px;
}

.speaker {
    width: 64px;
    height: 98px;
    border-radius: 15px;
    border: 1px solid #a64dff88;
    background: linear-gradient(145deg, #18182b, #090b17);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
    box-shadow: 0 0 15px #a64dff22;
}

.speaker-cone {
    border: 3px solid #00eaff;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: radial-gradient(circle, #a64dff, #10101d 65%);
    box-shadow: 0 0 12px #00eaff66;
    animation: pulse 1.3s ease-in-out infinite alternate;
}

.speaker-small {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid #ff31d2;
    box-shadow: 0 0 10px #ff31d266;
}

.speaker-label {
    color: #a2afd7;
    font-size: 9px;
    letter-spacing: 1px;
}

@keyframes pulse {
    from { transform: scale(.92); }
    to { transform: scale(1.04); }
}

.playlist { margin-top: 16px; }

.playlist-head {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    color: #9ca9d4;
    font-size: 11px;
    margin-bottom: 10px;
}

.track-list {
    max-height: 230px;
    overflow-y: auto;
    scrollbar-color: #7138ac #0c1020;
    scrollbar-width: thin;
}

.track-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 10px;
    margin-bottom: 6px;
    text-align: left;
    color: #dbe2ff;
    background: #ffffff05;
    border: 1px solid #ffffff12;
    border-radius: 12px;
    cursor: pointer;
    font-size: 12px;
    overflow-wrap: anywhere;
}

.track-item:hover {
    border-color: #00eaff66;
    background: #00eaff0b;
}

.track-item.selected {
    border-color: #00eaffaa;
    background: linear-gradient(90deg, #00eaff14, #a64dff18);
    box-shadow: inset 3px 0 #00eaff;
}

.track-number { color: #8b9ac7; min-width: 22px; font-size: 10px; }
.track-name { flex: 1; }
.track-status { color: #00eaff; font-size: 10px; }

#notice {
    color: #ffbbeb;
    font-size: 11px;
    min-height: 16px;
    margin-top: 6px;
}

.bottom-line {
    text-align: center;
    color: #6e7ca7;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 18px;
}

@media (max-width: 600px) {
    .player { padding: 12px; border-radius: 20px; }
    .main-grid { grid-template-columns: 1fr; }
    .panel { padding: 13px; }
    .logo, .logo-placeholder { width: 54px; height: 54px; }
    .brand-name { font-size: 16px; }
    #visualizer { height: 115px; }
}
</style>
</head>

<body>
<div class="player" id="player">

    <div class="topbar">
        <div class="brand">
            <div id="logoBox"></div>
            <div>
                <div class="brand-name">SYNAPSE</div>
                <div class="brand-desc">NEON AUDIO EXPERIENCE</div>
            </div>
        </div>
        <div class="live">● AUDIO SYSTEM ONLINE</div>
    </div>

    <div class="visual-area">
        <div class="visual-top">
            <span>LIVE AUDIO SPECTRUM</span>
            <span id="visualStatus">READY TO PLAY</span>
        </div>
        <canvas id="visualizer"></canvas>
        <div class="visual-bottom">
            <span>LOW FREQUENCY</span>
            <span>REAL-TIME WAVEFORM</span>
            <span>HIGH FREQUENCY</span>
        </div>
    </div>

    <div class="main-grid">
        <div class="panel">
            <div class="panel-heading">◉ TURNTABLE / NOW PLAYING</div>

            <div class="deck">
                <div class="vinyl-wrap">
                    <div class="vinyl" id="vinyl">
                        <div class="vinyl-label" id="vinylLabel">
                            <div class="vinyl-hole"></div>
                        </div>
                    </div>
                </div>

                <div class="track-title" id="trackTitle">เตรียมเพลง...</div>
                <div class="track-subtitle" id="trackSubtitle">SYNAPSE NEON PLAYER</div>

                <audio id="audio" preload="metadata"></audio>

                <div class="progress">
                    <input id="seek" type="range" min="0" max="1000" value="0">
                    <div class="time-row">
                        <span id="currentTime">00:00</span>
                        <span id="duration">00:00</span>
                    </div>
                </div>

                <div class="controls">
                    <button class="ctrl" id="shuffleBtn" title="สุ่มเพลง">🔀</button>
                    <button class="ctrl" id="prevBtn" title="เพลงก่อนหน้า">⏮</button>
                    <button class="ctrl play" id="playBtn" title="เล่น/หยุด">▶</button>
                    <button class="ctrl" id="nextBtn" title="เพลงถัดไป">⏭</button>
                    <button class="ctrl" id="modeBtn" title="โหมดเล่น">🔁</button>
                </div>

                <div class="mode-label" id="modeLabel">โหมดเล่นต่อเนื่อง</div>

                <div class="eq-row">
                    <div class="eq-head">
                        <span>🔊 MASTER VOLUME</span>
                        <span class="eq-value" id="volumeVal">75%</span>
                    </div>
                    <input id="volume" type="range" min="0" max="100" value="75">
                </div>

                <div class="speaker-row">
                    <div class="speaker">
                        <div class="speaker-small"></div>
                        <div class="speaker-cone"></div>
                        <div class="speaker-label">LEFT</div>
                    </div>
                    <div style="text-align:center">
                        <div style="font-size:35px;filter:drop-shadow(0 0 12px #00eaff)">🎧</div>
                        <div style="font-size:10px;color:#9ca9d4;letter-spacing:2px">STEREO</div>
                    </div>
                    <div class="speaker">
                        <div class="speaker-small"></div>
                        <div class="speaker-cone"></div>
                        <div class="speaker-label">RIGHT</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel" id="mixerPanel">
            <div class="panel-heading">✦ NEON AUDIO MIXER</div>

            <div class="eq-row">
                <div class="eq-head">
                    <span>🔴 BASS / เสียงทุ้ม</span>
                    <span class="eq-value" id="bassVal">0 dB</span>
                </div>
                <input id="bass" type="range" min="-12" max="12" value="0">
            </div>

            <div class="eq-row">
                <div class="eq-head">
                    <span>🟣 MID / เสียงกลาง</span>
                    <span class="eq-value" id="midVal">0 dB</span>
                </div>
                <input id="mid" type="range" min="-12" max="12" value="0">
            </div>

            <div class="eq-row">
                <div class="eq-head">
                    <span>🔵 TREBLE / เสียงแหลม</span>
                    <span class="eq-value" id="trebleVal">0 dB</span>
                </div>
                <input id="treble" type="range" min="-12" max="12" value="0">
            </div>

            <div class="eq-row">
                <div class="eq-head">
                    <span>✨ NEON GLOW / แสง</span>
                    <span class="eq-value" id="glowVal">65%</span>
                </div>
                <input id="glow" type="range" min="0" max="100" value="65">
            </div>

            <div class="eq-row">
                <div class="eq-head">
                    <span>🌈 WAVE COLOR / สีกราฟ</span>
                    <span class="eq-value" id="colorVal">NEON</span>
                </div>
                <input id="color" type="range" min="0" max="100" value="50">
            </div>

            <div class="panel-heading" style="margin-top:25px">◈ PLAYLIST / คลังเพลง</div>
            <div class="playlist-head">
                <span id="songCount">0 TRACKS</span>
                <span>LOCAL MUSIC LIBRARY</span>
            </div>

            <div class="track-list" id="trackList"></div>
            <div id="notice"></div>

            <button class="ctrl" id="fullscreenBtn"
                style="width:100%;margin-top:12px;font-size:12px">
                ⛶ FULL SCREEN / เต็มหน้าจอ
            </button>
        </div>
    </div>

    <div class="bottom-line">
        SYNAPSE • SOUND IS ENERGY • FEEL THE FREQUENCY
    </div>
</div>
""" 

# ============================================================
# PART 3 OF 3 — JAVASCRIPT + START PLAYER
# วางต่อจากช่วงที่ 2 ทันที
# ============================================================

    player_html += r"""
<script>
const TRACKS = __TRACKS_JSON__;
const LOGO_SRC = __LOGO_SRC__;

const $ = id => document.getElementById(id);
const audio = $("audio");
const vinyl = $("vinyl");
const player = $("player");
const canvas = $("visualizer");
const ctx = canvas.getContext("2d");

let currentIndex = 0;
let mode = "all";
let isSeeking = false;
let audioContext = null;
let analyser = null;
let sourceNode = null;
let bassFilter = null;
let midFilter = null;
let trebleFilter = null;
let frequencyData = null;
let timeData = null;
let colorShift = 0;

const modes = [
    {id: "all", label: "โหมดเล่นต่อเนื่อง", icon: "🔁"},
    {id: "shuffle", label: "โหมดสุ่มเพลง", icon: "🔀"},
    {id: "one", label: "โหมดวนเพลงเดียว", icon: "🔂"}
];

function setupLogo() {
    const box = $("logoBox");

    if (LOGO_SRC) {
        const img = document.createElement("img");
        img.className = "logo";
        img.src = LOGO_SRC;
        img.alt = "SYNAPSE logo";
        box.appendChild(img);

        const labelImg = img.cloneNode();
        $("vinylLabel").prepend(labelImg);
        labelImg.style.cssText =
            "width:100%;height:100%;object-fit:cover;border-radius:50%;";
    } else {
        box.innerHTML = '<div class="logo-placeholder">🎧</div>';
        $("vinylLabel").textContent = "S";
    }
}

function formatTime(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) return "00:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return String(mins).padStart(2, "0") + ":" +
        String(secs).padStart(2, "0");
}

function showNotice(message) {
    $("notice").textContent = message;
}

function renderPlaylist() {
    const list = $("trackList");
    list.innerHTML = "";
    $("songCount").textContent = TRACKS.length + " TRACKS";

    TRACKS.forEach((track, index) => {
        const button = document.createElement("button");
        button.className = "track-item" +
            (index === currentIndex ? " selected" : "");
        button.type = "button";

        const number = document.createElement("span");
        number.className = "track-number";
        number.textContent = String(index + 1).padStart(2, "0");

        const name = document.createElement("span");
        name.className = "track-name";
        name.textContent = track.title;

        const status = document.createElement("span");
        status.className = "track-status";
        status.textContent =
            index === currentIndex && !audio.paused ? "▶" : "♫";

        button.append(number, name, status);
        button.addEventListener("click", () => loadTrack(index, true));
        list.appendChild(button);
    });
}

function initAudioGraph() {
    if (audioContext) {
        if (audioContext.state === "suspended") audioContext.resume();
        return;
    }

    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) {
        showNotice("เบราว์เซอร์นี้ไม่รองรับ EQ");
        return;
    }

    try {
        audioContext = new AudioContextClass();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        analyser.smoothingTimeConstant = 0.78;

        bassFilter = audioContext.createBiquadFilter();
        bassFilter.type = "lowshelf";
        bassFilter.frequency.value = 250;

        midFilter = audioContext.createBiquadFilter();
        midFilter.type = "peaking";
        midFilter.frequency.value = 1000;
        midFilter.Q.value = 0.8;

        trebleFilter = audioContext.createBiquadFilter();
        trebleFilter.type = "highshelf";
        trebleFilter.frequency.value = 3500;

        sourceNode = audioContext.createMediaElementSource(audio);
        sourceNode.connect(bassFilter);
        bassFilter.connect(midFilter);
        midFilter.connect(trebleFilter);
        trebleFilter.connect(analyser);
        analyser.connect(audioContext.destination);

        frequencyData = new Uint8Array(analyser.frequencyBinCount);
        timeData = new Uint8Array(analyser.fftSize);
        showNotice("");
    } catch (error) {
        showNotice("เริ่มระบบ EQ ไม่สำเร็จ");
    }
}

function loadTrack(index, autoplay = false) {
    if (!TRACKS.length) return;

    currentIndex = (index + TRACKS.length) % TRACKS.length;
    audio.src = TRACKS[currentIndex].src;
    audio.load();

    $("trackTitle").textContent = TRACKS[currentIndex].title;
    $("trackSubtitle").textContent =
        "TRACK " + String(currentIndex + 1).padStart(2, "0") +
        " / " + String(TRACKS.length).padStart(2, "0");

    $("currentTime").textContent = "00:00";
    $("duration").textContent = "00:00";
    $("seek").value = 0;

    renderPlaylist();

    if (autoplay) {
        initAudioGraph();
        audio.play().then(updatePlayState).catch(() => {
            showNotice("แตะปุ่มเล่นอีกครั้งเพื่อเริ่มเสียงเพลง");
            updatePlayState();
        });
    } else {
        updatePlayState();
    }
}

function updatePlayState() {
    const playing = !audio.paused;

    $("playBtn").textContent = playing ? "❚❚" : "▶";
    $("visualStatus").textContent = playing
        ? "● PLAYING LIVE" : "READY / PAUSED";

    vinyl.classList.toggle("playing", playing);
    renderPlaylist();

    $("shuffleBtn").classList.toggle("active", mode === "shuffle");
    $("modeBtn").classList.toggle("active", mode === "one");

    const currentMode = modes.find(m => m.id === mode) || modes[0];
    $("modeBtn").textContent = currentMode.icon;
    $("modeLabel").textContent = currentMode.label;
}

function playAudio() {
    initAudioGraph();

    if (audioContext && audioContext.state === "suspended") {
        audioContext.resume();
    }

    if (audio.paused) {
        audio.play().then(updatePlayState).catch(() => {
            showNotice("เล่นเพลงไม่ได้ กรุณาลองเลือกเพลงใหม่");
        });
    } else {
        audio.pause();
        updatePlayState();
    }
}

function nextTrack() {
    if (mode === "shuffle" && TRACKS.length > 1) {
        let next = currentIndex;
        while (next === currentIndex) {
            next = Math.floor(Math.random() * TRACKS.length);
        }
        loadTrack(next, true);
    } else {
        loadTrack(currentIndex + 1, true);
    }
}

function previousTrack() {
    if (audio.currentTime > 3) {
        audio.currentTime = 0;
    } else if (mode === "shuffle" && TRACKS.length > 1) {
        let prev = currentIndex;
        while (prev === currentIndex) {
            prev = Math.floor(Math.random() * TRACKS.length);
        }
        loadTrack(prev, true);
    } else {
        loadTrack(currentIndex - 1, true);
    }
}

function onTrackEnded() {
    if (mode === "one") {
        audio.currentTime = 0;
        audio.play().catch(updatePlayState);
    } else if (mode === "shuffle" && TRACKS.length > 1) {
        nextTrack();
    } else if (currentIndex < TRACKS.length - 1) {
        loadTrack(currentIndex + 1, true);
    } else {
        loadTrack(0, false);
    }
}

function drawVisualizer() {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = Math.max(1, rect.width);
    const height = Math.max(1, rect.height);

    if (canvas.width !== Math.floor(width * dpr) ||
        canvas.height !== Math.floor(height * dpr)) {
        canvas.width = Math.floor(width * dpr);
        canvas.height = Math.floor(height * dpr);
    }

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, width, height);

    const active = !audio.paused && analyser;

    if (active) {
        analyser.getByteFrequencyData(frequencyData);
        analyser.getByteTimeDomainData(timeData);
    }

    const glow = Number($("glow").value) / 100;
    const hueShift = Number($("color").value) * 2.4;
    colorShift = (colorShift + 0.25) % 360;

    ctx.beginPath();

    for (let i = 0; i < width; i++) {
        let sample = 128;

        if (active && timeData.length) {
            const idx = Math.min(
                timeData.length - 1,
                Math.floor(i / width * timeData.length)
            );
            sample = timeData[idx];
        } else {
            sample = 128 + Math.sin(i * 0.055 + colorShift * 0.03) * 3;
        }

        const y = height / 2 + ((sample - 128) / 128) * height * 0.38;
        if (i === 0) ctx.moveTo(i, y);
        else ctx.lineTo(i, y);
    }

    const waveGradient = ctx.createLinearGradient(0, 0, width, 0);
    waveGradient.addColorStop(0, "#00eaff");
    waveGradient.addColorStop(
        0.5,
        "hsl(" + ((200 + hueShift + colorShift) % 360) + ",100%,65%)"
    );
    waveGradient.addColorStop(1, "#ff31d2");

    ctx.strokeStyle = waveGradient;
    ctx.lineWidth = 2;
    ctx.shadowBlur = 12 * glow;
    ctx.shadowColor = "#00eaff";
    ctx.stroke();
    ctx.shadowBlur = 0;

    const count = 54;
    const gap = 3;
    const barWidth = Math.max(1, (width - gap * (count - 1)) / count);
    const baseline = height - 5;

    for (let i = 0; i < count; i++) {
        let value;

        if (active && frequencyData) {
            const idx = Math.floor(i / count * frequencyData.length);
            value = frequencyData[idx] / 255;
        } else {
            value = 0.05 +
                Math.abs(Math.sin(i * 0.33 + colorShift * 0.03)) * 0.08;
        }

        const barHeight = Math.max(3, value * height * 0.75);
        const x = i * (barWidth + gap);
        const gradient = ctx.createLinearGradient(
            0, baseline - barHeight, 0, baseline
        );

        gradient.addColorStop(0, "#ff31d2");
        gradient.addColorStop(0.5, "#a64dff");
        gradient.addColorStop(1, "#00eaff");

        ctx.fillStyle = gradient;
        ctx.shadowBlur = 8 * glow;
        ctx.shadowColor = "#a64dff";
        ctx.fillRect(x, baseline - barHeight, barWidth, barHeight);
    }

    ctx.shadowBlur = 0;
    requestAnimationFrame(drawVisualizer);
}


// ปุ่มควบคุม
$("playBtn").addEventListener("click", playAudio);
$("prevBtn").addEventListener("click", previousTrack);
$("nextBtn").addEventListener("click", nextTrack);

$("shuffleBtn").addEventListener("click", () => {
    mode = mode === "shuffle" ? "all" : "shuffle";
    updatePlayState();
});

$("modeBtn").addEventListener("click", () => {
    const index = modes.findIndex(m => m.id === mode);
    mode = modes[(index + 1) % modes.length].id;
    updatePlayState();
});

$("volume").addEventListener("input", event => {
    audio.volume = Number(event.target.value) / 100;
    $("volumeVal").textContent = event.target.value + "%";
});

function setEQ(filter, value) {
    if (filter && audioContext) {
        filter.gain.setTargetAtTime(
            Number(value), audioContext.currentTime, 0.03
        );
    }
}

["bass", "mid", "treble"].forEach(id => {
    $(id).addEventListener("input", () => {
        if (!audioContext) initAudioGraph();

        const filter = id === "bass" ? bassFilter :
            id === "mid" ? midFilter : trebleFilter;

        setEQ(filter, $(id).value);
        $(id + "Val").textContent = $(id).value + " dB";
    });
});

$("glow").addEventListener("input", event => {
    const value = Number(event.target.value) / 100;
    $("glowVal").textContent = event.target.value + "%";

    player.style.boxShadow =
        "0 0 " + (12 + value * 32) +
        "px rgba(0,220,255," + (value * 0.35) + ")," +
        "inset 0 0 40px rgba(140,55,255," + (value * 0.14) + ")";

    document.querySelectorAll(".speaker").forEach(speaker => {
        speaker.style.boxShadow =
            "0 0 " + (5 + value * 20) +
            "px rgba(0,234,255," + value + ")";
    });
});

$("color").addEventListener("input", event => {
    const value = Number(event.target.value);
    $("colorVal").textContent =
        value < 34 ? "CYAN" : value < 67 ? "PURPLE" : "RAINBOW";
});

$("seek").addEventListener("input", () => {
    isSeeking = true;
});

$("seek").addEventListener("change", event => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
        audio.currentTime =
            Number(event.target.value) / 1000 * audio.duration;
    }
    isSeeking = false;
});

audio.addEventListener("timeupdate", () => {
    $("currentTime").textContent = formatTime(audio.currentTime);

    if (!isSeeking && Number.isFinite(audio.duration) && audio.duration > 0) {
        $("seek").value =
            Math.round(audio.currentTime / audio.duration * 1000);
    }
});

audio.addEventListener("loadedmetadata", () => {
    $("duration").textContent = formatTime(audio.duration);
});

audio.addEventListener("play", updatePlayState);
audio.addEventListener("pause", updatePlayState);
audio.addEventListener("ended", onTrackEnded);

audio.addEventListener("error", () => {
    showNotice("ไฟล์เพลงนี้เล่นไม่ได้ หรือรูปแบบไฟล์ไม่รองรับ");
});

$("fullscreenBtn").addEventListener("click", () => {
    if (!document.fullscreenElement) {
        const result = player.requestFullscreen?.();
        if (result && result.catch) {
            result.catch(() => showNotice("เบราว์เซอร์ไม่อนุญาตเต็มหน้าจอ"));
        }
    } else {
        document.exitFullscreen?.();
    }
});

setupLogo();
audio.volume = 0.75;

if (TRACKS.length) {
    loadTrack(0, false);
} else {
    $("trackTitle").textContent = "ยังไม่พบเพลง";
    $("trackSubtitle").textContent = "เพิ่มไฟล์เพลงในโฟลเดอร์แอป";
    $("trackList").textContent = "ไม่พบไฟล์เสียง";
}

drawVisualizer();
</script>
</body>
</html>
"""

    player_html = (
        player_html
        .replace("__TRACKS_JSON__", tracks_json)
        .replace("__LOGO_SRC__", logo_src)
    )

    components.iframe(
    srcdoc=player_html,
    height=1120,
    scrolling=True
    )


# ส่วนท้ายของแอป
st.markdown(
    """
    <div style="
        text-align:center;
        color:#8492bd;
        font-size:11px;
        letter-spacing:2px;
        padding:10px 0 20px;
    ">
        SYNAPSE NEON MUSIC PLAYER • MADE FOR MUSIC LOVERS
    </div>
    """,
    unsafe_allow_html=True,
)
