
from pathlib import Path
import base64
import json
import mimetypes
import streamlit as st

# ==========================================
# TA101 NEON MUSIC PLAYER
# ==========================================
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="TA101 Neon Music",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"
}

tracks = []

for path in sorted(BASE_DIR.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            tracks.append({
                "name": path.stem,
                "filename": path.name,
                "src": f"data:{mime};base64,{encoded}",
            })
        except OSError:
            pass

logo_path = BASE_DIR / "logo1.jpg"
if not logo_path.exists():
    logo_path = BASE_DIR / "logo.jpg"

logo_src = ""
if logo_path.exists():
    logo_mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
    logo_encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    logo_src = f"data:{logo_mime};base64,{logo_encoded}"

if not tracks:
    st.title("🎧 TA101 NEON MUSIC")
    if logo_path.exists():
        st.image(str(logo_path), width=260)
    st.warning(
        "ยังไม่พบไฟล์เพลง กรุณาวางไฟล์ MP3 หรือไฟล์เสียง "
        "ไว้ในโฟลเดอร์เดียวกับ app.py"
    )
    st.stop()

html = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing: border-box;
}

:root {
    --cyan: #00f6ff;
    --pink: #ff00d9;
    --purple: #9b4dff;
    --green: #39ff88;
}

body {
    margin: 0;
    padding: 10px;
    color: #ffffff;
    font-family: Arial, "Noto Sans Thai", sans-serif;
    background:
        radial-gradient(ellipse at 10% 0%, #351064 0%, transparent 42%),
        radial-gradient(ellipse at 100% 60%, #082f53 0%, transparent 40%),
        #05050d;
}

.shell {
    width: 100%;
    max-width: 1150px;
    margin: 0 auto;
    padding: 18px;
    border: 1px solid #713cff;
    border-radius: 25px;
    background: linear-gradient(145deg, #111124f5, #070710f8);
    box-shadow:
        0 0 25px #6c24ff45,
        inset 0 0 28px #00d9ff0b;
}

/* ===== HEADER / LOGO ===== */

.header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 15px;
    text-align: center;
    padding: 25px 12px;
    margin-bottom: 22px;
    border: 1px solid #00f6ff99;
    border-radius: 25px;
    background:
        radial-gradient(ellipse at center, #7100ff35, transparent 70%),
        linear-gradient(135deg, #111126, #080812);
    box-shadow:
        0 0 18px #00f6ff50,
        0 0 35px #ff00d925,
        inset 0 0 25px #6900ff25;
}

.logo {
    display: block;
    width: min(65vw, 300px);
    height: min(65vw, 300px);
    object-fit: contain;
    border-radius: 24px;
    border: 2px solid var(--cyan);
    padding: 5px;
    background: #090916;
    box-shadow: 0 0 15px var(--cyan), 0 0 35px var(--purple);
    animation: logoGlow 2.5s ease-in-out infinite alternate;
}

@keyframes logoGlow {
    from {
        box-shadow: 0 0 10px var(--cyan), 0 0 25px var(--purple);
    }
    to {
        box-shadow:
            0 0 22px var(--cyan),
            0 0 45px var(--pink),
            0 0 65px var(--purple);
    }
}

.brand {
    font-size: clamp(32px, 7vw, 68px);
    font-weight: 1000;
    letter-spacing: 2px;
    line-height: 1.2;
    color: #ffffff;
    background: linear-gradient(
        90deg,
        #00f6ff,
        #ffffff,
        #ff00d9,
        #a86bff,
        #00f6ff
    );
    background-size: 300% auto;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textShine 4s linear infinite;
    filter: drop-shadow(0 0 12px #00eaff);
}

@keyframes textShine {
    from { background-position: 0% center; }
    to { background-position: 300% center; }
}

.subtitle {
    margin-top: 10px;
    color: var(--cyan);
    font-size: clamp(11px, 3vw, 17px);
    font-weight: 900;
    letter-spacing: 3px;
    text-shadow: 0 0 8px var(--cyan), 0 0 18px var(--purple);
    animation: subtitleGlow 1.8s ease-in-out infinite alternate;
}

@keyframes subtitleGlow {
    from { opacity: 0.7; }
    to {
        opacity: 1;
        text-shadow: 0 0 12px var(--cyan), 0 0 28px var(--pink);
    }
}

/* ===== LAYOUT ===== */

.grid {
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
    gap: 18px;
}

.panel {
    min-width: 0;
    padding: 20px;
    margin-bottom: 18px;
    border: 1px solid #9b4dff99;
    border-radius: 22px;
    background:
        radial-gradient(ellipse at top left, #00f6ff12, transparent 60%),
        linear-gradient(145deg, #17172c, #080812);
    box-shadow:
        0 0 15px #6900ff40,
        inset 0 0 18px #00f6ff09;
}

.heading {
    color: var(--cyan);
    font-size: clamp(16px, 3vw, 21px);
    font-weight: 1000;
    letter-spacing: 1px;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid #00f6ff55;
    text-shadow: 0 0 8px var(--cyan), 0 0 18px var(--purple);
}

/* ===== NEON DISC ===== */

.disc-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 0 18px;
}

.disc {
    width: min(48vw, 230px);
    height: min(48vw, 230px);
    border-radius: 50%;
    border: 4px solid #b13cff;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        repeating-radial-gradient(circle, #171725 0 3px, #090910 4px 7px);
    box-shadow: 0 0 18px #c000ff, 0 0 45px #00d9ff40;
    position: relative;
}

.disc.playing {
    animation: spin 5s linear infinite;
}

.disc::before {
    content: "";
    position: absolute;
    inset: 12%;
    border-radius: 50%;
    border: 1px solid #00eaff66;
}

.disc-center {
    width: 27%;
    height: 27%;
    border-radius: 50%;
    background: radial-gradient(circle, white, #00eaff 35%, #a000ff 75%);
    box-shadow: 0 0 25px #00eaff;
    border: 3px solid #f8eaff;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.now-title {
    text-align: center;
    font-weight: 900;
    font-size: 20px;
    overflow-wrap: anywhere;
    text-shadow: 0 0 12px var(--cyan), 0 0 20px var(--purple);
    margin: 4px 0 8px;
}

.now-file {
    color: #a5a5ca;
    text-align: center;
    font-size: 12px;
    margin-bottom: 15px;
    overflow-wrap: anywhere;
}

/* ===== AUDIO VISUALIZER ===== */

canvas {
    display: block;
    width: 100%;
    height: 155px;
    border: 1px solid #332e64;
    border-radius: 14px;
    background: #060610;
    box-shadow: inset 0 0 15px #6500ff22, 0 0 10px #00eaff20;
}

/* ===== SPEAKERS / HEADPHONES ===== */

.speakers {
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 16px;
    margin: 25px 0 12px;
}

.speaker {
    width: 76px;
    height: 92px;
    flex-shrink: 0;
    border-radius: 16px;
    border: 2px solid var(--cyan);
    background: linear-gradient(145deg, #242441, #080811);
    box-shadow:
        0 0 12px var(--cyan),
        0 0 25px #00f6ff55,
        inset 0 0 15px #ff00d925;
    display: flex;
    align-items: center;
    justify-content: center;
}

.speaker::before {
    content: "";
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 4px solid var(--pink);
    background:
        radial-gradient(circle, #ffffff 0 5%, #00f6ff 8% 20%,
        #141429 24% 40%, #a000ff 45% 53%, #090913 58%);
    box-shadow: 0 0 12px var(--pink), inset 0 0 10px var(--cyan);
}

.headphone {
    font-size: clamp(45px, 10vw, 72px);
    line-height: 1;
    filter: drop-shadow(0 0 8px var(--pink)) drop-shadow(0 0 18px var(--cyan));
    animation: headphoneGlow 1.8s ease-in-out infinite alternate;
}

@keyframes headphoneGlow {
    from { filter: drop-shadow(0 0 7px var(--pink)); }
    to {
        filter: drop-shadow(0 0 14px var(--cyan))
                drop-shadow(0 0 22px var(--pink));
    }
}
</style>
</head>

<body>
<div class="shell" id="playerApp">

    <div class="header">
        <img class="logo" id="logo" src="__LOGO_SRC__" alt="TA101 Logo">
        <div>
            <div class="brand">TA101 MUSIC</div>
            <div class="subtitle">NEON SOUND EXPERIENCE</div>
        </div>
    </div>

    <div class="grid">
        <section>
            <div class="panel">
                <div class="heading">✦ NOW PLAYING</div>

                <div class="disc-wrap">
                    <div class="disc" id="disc">
                        <div class="disc-center"></div>
                    </div>
                </div>

                <div class="now-title" id="nowTitle">เลือกเพลงเพื่อเริ่มฟัง</div>
                <div class="now-file" id="nowFile"></div>

                <canvas id="visualizer"></canvas>

                <div class="speakers">
                    <div class="speaker"></div>
                    <div class="headphone">🎧</div>
                    <div class="speaker"></div>
                </div>

                <div class="controls">
                    <button id="shuffleBtn">🔀 สุ่ม</button>
                    <button id="prevBtn">⏮</button>
                    <button class="play" id="playBtn">▶</button>
                    <button id="nextBtn">⏭</button>
                    <button id="repeatBtn">🔁 ซ้ำ: ปิด</button>
                </div>

                <div class="status" id="status">● พร้อมเล่นเพลง</div>
            </div>

            <div class="panel">
                <div class="heading">🎚️ SOUND CONTROL</div>

                <label for="volume">
                    🔊 ระดับเสียง <span id="volumeValue">80%</span>
                </label>
                <input id="volume" type="range" min="0" max="100" value="80">

                <div class="eq-row">
                    <span>BASS</span>
                    <input id="bass" type="range" min="-12" max="12" value="0">
                    <span id="bassValue">0</span>
                </div>

                <div class="eq-row">
                    <span>MID</span>
                    <input id="mid" type="range" min="-12" max="12" value="0">
                    <span id="midValue">0</span>
                </div>

                <div class="eq-row">
                    <span>TREBLE</span>
                    <input id="treble" type="range" min="-12" max="12" value="0">
                    <span id="trebleValue">0</span>
                </div>

                <div class="small" style="margin-top:12px">
                    ปรับเสียงผ่านฟิลเตอร์เสียงของเบราว์เซอร์
                </div>

                <div class="controls">
                    <button id="resetEq">↺ รีเซ็ต EQ</button>
                    <button id="fullscreenBtn">⛶ เต็มหน้าจอ</button>
                </div>
            </div>
        </section>

        <section>
            <div class="panel">
                <div class="heading">📃 PLAYLIST</div>
                <div class="small" id="trackCount"></div>
                <div style="height:10px"></div>
                <div class="track-list" id="playlist"></div>
            </div>

            <div class="panel">
                <div class="heading">⚙️ PLAYBACK SETTINGS</div>

                <label for="playMode">โหมดเมื่อเพลงจบ</label>
                <select id="playMode">
                    <option value="continuous">เล่นเพลงถัดไปอัตโนมัติ</option>
                    <option value="repeat">เล่นเพลงเดิมซ้ำ</option>
                    <option value="stop">หยุดเมื่อเพลงจบ</option>
                </select>

                <label for="colorMode">ธีมกราฟเสียง</label>
                <select id="colorMode">
                    <option value="rainbow">Rainbow — สีรุ้ง</option>
                    <option value="cyan">Cyber Cyan — ฟ้า</option>
                    <option value="pink">Neon Pink — ชมพู</option>
                    <option value="green">Laser Green — เขียว</option>
                </select>

                <div class="small info">
                    • กราฟเสียงตอบสนองต่อเสียงเพลงจริง<br>
                    • เล่นเพลงต่อเนื่องตามโหมดที่เลือก<br>
                    • สุ่มเพลงจากรายการที่มี<br>
                    • ปรับเบส กลาง แหลม และระดับเสียงได้
                </div>
            </div>
        </section>
    </div>

    <div class="footer">TA101 • NEON MUSIC PLAYER • FEEL THE BEAT</div>
</div>
"""


<CodeBlock language="python" editable>
html += r"""
<style>
.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 9px;
    margin: 18px 0;
}

button {
    color: #ffffff;
    border: 1px solid #7e4dff;
    border-radius: 14px;
    padding: 11px 14px;
    background: linear-gradient(135deg, #241342, #101025);
    font-size: 14px;
    font-weight: 900;
    cursor: pointer;
    box-shadow: 0 0 12px #7300ff40;
    transition: all 0.2s ease;
}

button:hover {
    border-color: var(--cyan);
    box-shadow: 0 0 12px var(--cyan), 0 0 24px #ff00d975;
    transform: translateY(-2px);
}

button.active {
    border-color: var(--cyan);
    background: linear-gradient(135deg, #007c91, #7915b9);
    box-shadow: 0 0 16px var(--cyan);
}

.play {
    width: 62px;
    height: 62px;
    padding: 0;
    border-radius: 50%;
    font-size: 24px;
    background: linear-gradient(135deg, #8a22ff, #ff00c8);
    box-shadow: 0 0 16px var(--pink), 0 0 30px #00f6ff55;
}

.status {
    color: var(--green);
    text-align: center;
    font-size: 12px;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

label {
    display: block;
    color: #d2d0f4;
    font-size: 13px;
    margin: 15px 0 7px;
}

input[type="range"] {
    width: 100%;
    accent-color: var(--cyan);
    cursor: pointer;
}

select {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #5a49a8;
    color: white;
    background: #111124;
    font-size: 14px;
}

.eq-row {
    display: grid;
    grid-template-columns: 58px minmax(0, 1fr) 30px;
    gap: 9px;
    align-items: center;
    margin-top: 13px;
    font-size: 12px;
    color: #d5d3f5;
}

.track-list {
    max-height: 350px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.track {
    width: 100%;
    text-align: left;
    display: flex;
    align-items: center;
    gap: 10px;
    overflow-wrap: anywhere;
    background: #101020;
    border-color: #2d2b52;
    box-shadow: none;
}

.track.selected {
    background: linear-gradient(90deg, #26205d, #251035);
    border-color: var(--cyan);
    box-shadow: inset 3px 0 var(--cyan), 0 0 12px #00eaff25;
}

.track-no {
    color: var(--cyan);
    min-width: 25px;
}

.track-name {
    flex: 1;
    overflow-wrap: anywhere;
}

.small {
    font-size: 12px;
    line-height: 1.9;
    color: #a6a6c8;
}

.info {
    margin-top: 15px;
}

.footer {
    color: #7778a5;
    text-align: center;
    font-size: 11px;
    padding: 14px 0 0;
    letter-spacing: 2px;
}

@media (max-width: 720px) {
    body { padding: 5px; }
    .shell { padding: 11px; border-radius: 17px; }
    .grid { grid-template-columns: 1fr; gap: 0; }
    .panel { padding: 14px; }
    .logo {
        width: min(70vw, 260px);
        height: min(70vw, 260px);
    }
    .brand { letter-spacing: 1px; }
    canvas { height: 125px; }
    button { padding: 10px 12px; }
}
</style>

<script>
const TRACKS = __TRACKS_JSON__;

const audio = new Audio();
audio.preload = "metadata";
audio.volume = 0.8;

let currentIndex = 0;
let isPlaying = false;
let shuffle = false;
let repeatOne = false;
let audioContext = null;
let analyser = null;
let sourceNode = null;
let gainNode = null;
let bassFilter = null;
let midFilter = null;
let trebleFilter = null;
let dataArray = null;

const $ = id => document.getElementById(id);

const logo = $("logo");
if (logo && logo.getAttribute("src") &&
    logo.getAttribute("src") !== "__LOGO_SRC__") {
    logo.style.display = "block";
} else if (logo) {
    logo.style.display = "none";
}

function setStatus(message) {
    $("status").textContent = "● " + message;
}

function initAudioGraph() {
    if (audioContext) {
        if (audioContext.state === "suspended") {
            audioContext.resume();
        }
        return;
    }

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) {
        setStatus("เบราว์เซอร์นี้ไม่รองรับ Web Audio");
        return;
    }

    audioContext = new AudioCtx();

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    analyser.smoothingTimeConstant = 0.78;

    sourceNode = audioContext.createMediaElementSource(audio);
    gainNode = audioContext.createGain();

    bassFilter = audioContext.createBiquadFilter();
    bassFilter.type = "lowshelf";
    bassFilter.frequency.value = 180;

    midFilter = audioContext.createBiquadFilter();
    midFilter.type = "peaking";
    midFilter.frequency.value = 1000;
    midFilter.Q.value = 0.8;

    trebleFilter = audioContext.createBiquadFilter();
    trebleFilter.type = "highshelf";
    trebleFilter.frequency.value = 4000;

    sourceNode.connect(bassFilter);
    bassFilter.connect(midFilter);
    midFilter.connect(trebleFilter);
    trebleFilter.connect(gainNode);
    gainNode.connect(analyser);
    analyser.connect(audioContext.destination);

    dataArray = new Uint8Array(analyser.frequencyBinCount);
    applyVolume();
    applyEQ();
}

function applyVolume() {
    const volume = Number($("volume").value) / 100;
    audio.volume = volume;
    $("volumeValue").textContent = Math.round(volume * 100) + "%";
}

function applyEQ() {
    const bass = Number($("bass").value);
    const mid = Number($("mid").value);
    const treble = Number($("treble").value);

    $("bassValue").textContent = bass > 0 ? "+" + bass : bass;
    $("midValue").textContent = mid > 0 ? "+" + mid : mid;
    $("trebleValue").textContent = treble > 0 ? "+" + treble : treble;

    if (bassFilter) bassFilter.gain.value = bass;
    if (midFilter) midFilter.gain.value = mid;
    if (trebleFilter) trebleFilter.gain.value = treble;
}

function renderPlaylist() {
    const playlist = $("playlist");
    playlist.innerHTML = "";
    $("trackCount").textContent = TRACKS.length + " เพลงในรายการ";

    TRACKS.forEach((track, index) => {
        const button = document.createElement("button");
        button.className =
            "track" + (index === currentIndex ? " selected" : "");

        const number = document.createElement("span");
        number.className = "track-no";
        number.textContent = String(index + 1).padStart(2, "0");

        const name = document.createElement("span");
        name.className = "track-name";
        name.textContent = track.name;

        const icon = document.createElement("span");
        icon.textContent =
            index === currentIndex && isPlaying ? "🔊" : "♫";

        button.append(number, name, icon);
        button.addEventListener("click", () => {
            currentIndex = index;
            loadTrack(true);
        });

        playlist.appendChild(button);
    });
}

function loadTrack(autoplay) {
    if (!TRACKS.length) return;

    const track = TRACKS[currentIndex];

    audio.pause();
    isPlaying = false;
    audio.src = track.src;
    audio.load();

    $("nowTitle").textContent = track.name;
    $("nowFile").textContent = track.filename;
    $("playBtn").textContent = "▶";
    $("disc").classList.remove("playing");

    renderPlaylist();

    if (autoplay) {
        playTrack();
    } else {
        setStatus("เลือกแล้ว: " + track.name);
    }
}

async function playTrack() {
    if (!TRACKS.length) return;

    try {
        initAudioGraph();

    
        if (audioContext && audioContext.state === "suspended") {
            await audioContext.resume();
        }

        if (!audio.src) {
            audio.src = TRACKS[currentIndex].src;
        }

        await audio.play();

        isPlaying = true;
        $("playBtn").textContent = "❚❚";
        $("disc").classList.add("playing");
        setStatus("กำลังเล่น: " + TRACKS[currentIndex].name);
        renderPlaylist();

    } catch (error) {
        isPlaying = false;
        setStatus("เล่นไม่ได้ กรุณากดเล่นอีกครั้ง");
        console.error(error);
    }
}

function pauseTrack() {
    audio.pause();
    isPlaying = false;
    $("playBtn").textContent = "▶";
    $("disc").classList.remove("playing");
    setStatus("หยุดชั่วคราว");
    renderPlaylist();
}

function nextTrack(autoplay = true) {
    if (!TRACKS.length) return;

    if (shuffle && TRACKS.length > 1) {
        let next = currentIndex;

        while (next === currentIndex) {
            next = Math.floor(Math.random() * TRACKS.length);
        }

        currentIndex = next;
    } else {
        currentIndex = (currentIndex + 1) % TRACKS.length;
    }

    loadTrack(autoplay);
}

function previousTrack() {
    if (!TRACKS.length) return;

    if (audio.currentTime > 3) {
        audio.currentTime = 0;
        return;
    }

    currentIndex =
        (currentIndex - 1 + TRACKS.length) % TRACKS.length;

    loadTrack(true);
}

$("playBtn").addEventListener("click", () => {
    if (isPlaying) pauseTrack();
    else playTrack();
});

$("prevBtn").addEventListener("click", previousTrack);
$("nextBtn").addEventListener("click", () => nextTrack(true));

$("shuffleBtn").addEventListener("click", () => {
    shuffle = !shuffle;
    $("shuffleBtn").classList.toggle("active", shuffle);
    setStatus(shuffle ? "เปิดสุ่มเพลงแล้ว" : "ปิดสุ่มเพลงแล้ว");
});

$("repeatBtn").addEventListener("click", () => {
    repeatOne = !repeatOne;
    $("repeatBtn").textContent =
        repeatOne ? "🔂 ซ้ำ: เพลงเดียว" : "🔁 ซ้ำ: ปิด";
    $("repeatBtn").classList.toggle("active", repeatOne);
    audio.loop = repeatOne;
});

audio.addEventListener("ended", () => {
    isPlaying = false;
    $("playBtn").textContent = "▶";
    $("disc").classList.remove("playing");

    if (repeatOne) return;

    const mode = $("playMode").value;

    if (mode === "continuous") {
        nextTrack(true);
    } else if (mode === "repeat") {
        loadTrack(true);
    } else {
        setStatus("เพลงจบแล้ว");
        renderPlaylist();
    }
});

audio.addEventListener("error", () => {
    setStatus("ไฟล์เสียงนี้เปิดไม่ได้หรือรูปแบบไม่รองรับ");
});

$("volume").addEventListener("input", applyVolume);

["bass", "mid", "treble"].forEach(id => {
    $(id).addEventListener("input", () => {
        initAudioGraph();
        applyEQ();
    });
});

$("resetEq").addEventListener("click", () => {
    $("bass").value = 0;
    $("mid").value = 0;
    $("treble").value = 0;
    applyEQ();
});

$("fullscreenBtn").addEventListener("click", async () => {
    try {
        if (!document.fullscreenElement) {
            await $("playerApp").requestFullscreen();
        } else {
            await document.exitFullscreen();
        }
    } catch (error) {
        setStatus("อุปกรณ์นี้ไม่อนุญาตให้เต็มหน้าจอ");
    }
});

/* ===== กราฟเสียงนีออน ===== */

const canvas = $("visualizer");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    canvas.width = Math.max(1, Math.floor(rect.width * dpr));
    canvas.height = Math.max(1, Math.floor(rect.height * dpr));

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function drawVisualizer() {
    requestAnimationFrame(drawVisualizer);

    const rect = canvas.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#060610";
    ctx.fillRect(0, 0, width, height);

    const mode = $("colorMode").value;
    let values = [];

    if (analyser && dataArray && isPlaying) {
        analyser.getByteFrequencyData(dataArray);
        values = dataArray;
    }

    const count = 54;
    const gap = 3;
    const barWidth = Math.max(
        2,
        (width - gap * (count - 1)) / count
    );

    for (let i = 0; i < count; i++) {
        let amount = 0.035;

        if (values.length) {
            const idx = Math.floor(i / count * values.length);
            amount = values[idx] / 255;
        }

        const barHeight = Math.max(3, amount * height * 0.87);
        const x = i * (barWidth + gap);
        const y = (height - barHeight) / 2;

        let color;

        if (mode === "cyan") {
            color = "#00eaff";
        } else if (mode === "pink") {
            color = "#ff00c8";
        } else if (mode === "green") {
            color = "#39ff88";
        } else {
            color = "hsl(" +
                ((i * 7 + performance.now() * 0.025) % 360) +
                ", 100%, 60%)";
        }

        ctx.shadowBlur = 10;
        ctx.shadowColor = color;
        ctx.fillStyle = color;
        ctx.fillRect(x, y, barWidth, barHeight);
    }

    // เส้นคลื่นตรงกลาง
    ctx.beginPath();

    for (let x = 0; x < width; x += 3) {
        const amplitude = isPlaying ? 9 : 2;
        let value = 0;

        if (values.length) {
            const idx = Math.floor(x / width * values.length);
            value = (values[idx] / 255) * amplitude;
        }

        const y = height / 2 +
            Math.sin(x * 0.055 + performance.now() * 0.008) *
            (amplitude + value);

        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 1.4;
    ctx.shadowBlur = 12;
    ctx.shadowColor = "#00eaff";
    ctx.stroke();
    ctx.shadowBlur = 0;
}

window.addEventListener("resize", resizeCanvas);

resizeCanvas();
renderPlaylist();
loadTrack(false);
drawVisualizer();
</script>
</body>
</html>
"""

html = html.replace(
    "__TRACKS_JSON__",
    json.dumps(tracks, ensure_ascii=False)
)
html = html.replace("__LOGO_SRC__", logo_src)

st.iframe(html, height=1450)
