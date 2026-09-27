```python
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
import html
import mimetypes

# ============================================================
# NEON MUSIC PLAYER
# วางไฟล์ .mp3 ไว้โฟลเดอร์เดียวกับ app.py
# ============================================================

st.set_page_config(
    page_title="NEON MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# ค้นหาเพลง MP3 อัตโนมัติ
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

mp3_files = sorted(
    [
        p for p in BASE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() == ".mp3"
    ],
    key=lambda x: x.name.lower()
)

songs = []

for file in mp3_files:
    try:
        raw = file.read_bytes()
        encoded = base64.b64encode(raw).decode("utf-8")

        songs.append({
            "name": file.stem,
            "file": file.name,
            "src": f"data:audio/mpeg;base64,{encoded}"
        })
    except Exception:
        pass


# ------------------------------------------------------------
# CSS หน้า Streamlit
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% 30%,
                rgba(94, 0, 255, 0.16),
                transparent 35%
            ),
            radial-gradient(
                circle at 20% 80%,
                rgba(0, 220, 255, 0.12),
                transparent 30%
            ),
            #03030a;
    }

    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        max-width: 1400px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# ถ้าไม่มีเพลง
# ------------------------------------------------------------

if not songs:
    st.markdown(
        """
        <div style="
            min-height:80vh;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            color:white;
            font-family:Arial,sans-serif;
        ">
            <div>
                <div style="font-size:80px;">🎧</div>

                <div style="
                    font-size:32px;
                    font-weight:900;
                    letter-spacing:5px;
                    margin:20px 0;
                    background:linear-gradient(
                        90deg,
                        #00eaff,
                        #8b5cff,
                        #ff2bd6
                    );
                    -webkit-background-clip:text;
                    color:transparent;
                ">
                    NEON MUSIC
                </div>

                <div style="
                    color:#9b9bad;
                    font-size:16px;
                    line-height:1.8;
                ">
                    ยังไม่พบไฟล์ MP3<br>
                    ให้วางไฟล์ <b style="color:#00eaff;">.mp3</b>
                    ไว้ในโฟลเดอร์เดียวกับ
                    <b style="color:white;">app.py</b>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# ------------------------------------------------------------
# เตรียมข้อมูลเพลง
# ------------------------------------------------------------

songs_json = json.dumps(songs, ensure_ascii=False)


# ------------------------------------------------------------
# HTML + CSS + JavaScript
# ------------------------------------------------------------

player_html = r"""
<!DOCTYPE html>

<html lang="th">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100%;
    overflow: hidden;
    background: #03030a;
    font-family:
        Arial,
        Helvetica,
        sans-serif;
}

body {
    color: white;
}

/* =========================================================
   BACKGROUND
   ========================================================= */

.scene {

    position: relative;

    width: 100%;

    min-height: 900px;

    overflow: hidden;

    background:
        radial-gradient(
            circle at 50% 30%,
            rgba(97, 0, 255, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 15% 80%,
            rgba(0, 229, 255, 0.13),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 70%,
            rgba(255, 0, 179, 0.12),
            transparent 25%
        ),
        #03030a;
}

/* moving neon lights */

.glow {

    position: absolute;

    width: 500px;
    height: 500px;

    border-radius: 50%;

    filter: blur(90px);

    opacity: .30;

    animation:
        floatingGlow 9s
        ease-in-out
        infinite alternate;
}

.glow.one {

    left: -180px;
    top: 100px;

    background: #00eaff;
}

.glow.two {

    right: -180px;
    top: 250px;

    background: #ff00cc;

    animation-delay: -3s;
}

.glow.three {

    left: 35%;
    bottom: -300px;

    background: #702cff;

    animation-delay: -6s;
}

@keyframes floatingGlow {

    0% {
        transform: translate3d(
            -30px,
            -20px,
            0
        ) scale(0.9);
    }

    100% {
        transform: translate3d(
            40px,
            30px,
            0
        ) scale(1.15);
    }
}


/* =========================================================
   TOP
   ========================================================= */

.topbar {

    position: relative;

    z-index: 5;

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 25px 30px 0;
}

.logo {

    font-size: 15px;

    font-weight: 900;

    letter-spacing: 5px;

    color: white;

    text-shadow:
        0 0 8px #00eaff,
        0 0 20px rgba(0,234,255,.6);
}

.live {

    display: flex;

    align-items: center;

    gap: 8px;

    color: #a7a7b7;

    font-size: 11px;

    letter-spacing: 2px;
}

.liveDot {

    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #00ffbf;

    box-shadow:
        0 0 8px #00ffbf,
        0 0 18px #00ffbf;

    animation: blink 1s infinite;
}

@keyframes blink {

    50% {
        opacity: .3;
    }
}


/* =========================================================
   MAIN PLAYER
   ========================================================= */

.player {

    position: relative;

    z-index: 3;

    width: min(560px, 94vw);

    margin: 35px auto 0;

    text-align: center;
}


/* =========================================================
   RECORD
   ========================================================= */

.recordWrap {

    position: relative;

    width: min(390px, 78vw);

    aspect-ratio: 1 / 1;

    margin: auto;

    display: flex;

    align-items: center;

    justify-content: center;
}

.recordGlow {

    position: absolute;

    width: 96%;

    height: 96%;

    border-radius: 50%;

    background:
        conic-gradient(
            from 0deg,
            #00eaff,
            #753cff,
            #ff00c8,
            #00eaff
        );

    filter: blur(28px);

    opacity: .55;

    animation: pulseGlow 3s ease-in-out infinite;
}

@keyframes pulseGlow {

    50% {
        transform: scale(1.08);
        opacity: .75;
    }
}

.record {

    position: relative;

    width: 92%;

    height: 92%;

    border-radius: 50%;

    background:
        repeating-radial-gradient(
            circle,
            #08080e 0px,
            #08080e 3px,
            #171722 4px,
            #07070d 7px
        );

    border: 2px solid rgba(
        255,
        255,
        255,
        .10
    );

    box-shadow:
        0 0 0 8px rgba(
            255,
            255,
            255,
            .02
        ),
        0 0 50px rgba(
            0,
            220,
            255,
            .28
        ),
        inset 0 0 80px rgba(
            0,
            0,
            0,
            .9
        );

    animation:
        recordSpin 7s
        linear
        infinite;

    animation-play-state: paused;
}

.record.playing {
    animation-play-state: running;
}

@keyframes recordSpin {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


/* record rainbow ring */

.ring {

    position: absolute;

    width: 94%;
    height: 94%;

    border-radius: 50%;

    border: 2px solid transparent;

    background:
        linear-gradient(#050509,#050509)
        padding-box,
        conic-gradient(
            #00eaff,
            #7b3cff,
            #ff00c8,
            #00eaff
        ) border-box;

    opacity: .85;

    animation:
        ringSpin 5s
        linear
        infinite;
}

@keyframes ringSpin {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(-360deg);
    }
}


/* center */

.center {

    position: absolute;

    width: 105px;
    height: 105px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #181827,
            #05050a 65%
        );

    border: 3px solid rgba(
        255,
        255,
        255,
        .12
    );

    box-shadow:
        0 0 30px
        rgba(0,234,255,.45),
        inset 0 0 25px
        rgba(255,0,200,.25);

    display: flex;

    align-items: center;

    justify-content: center;

    z-index: 5;
}

.centerIcon {

    font-size: 32px;

    filter:
        drop-shadow(
            0 0 8px
            rgba(0,234,255,.9)
        );
}


/* =========================================================
   SONG INFO
   ========================================================= */

.songInfo {

    margin-top: 30px;
}

.songTitle {

    font-size: clamp(
        25px,
        5vw,
        38px
    );

    font-weight: 900;

    line-height: 1.15;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;

    padding: 0 10px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #6defff,
            #c77dff,
            #ffffff
        );

    -webkit-background-clip: text;

    color: transparent;

    background-size: 250% auto;

    animation:
        titleMove 4s
        linear
        infinite;

    text-shadow:
        0 0 25px
        rgba(0,234,255,.15);
}

@keyframes titleMove {

    to {
        background-position:
            250% center;
    }
}

.subtitle {

    margin-top: 8px;

    color: #6f7081;

    font-size: 11px;

    letter-spacing: 4px;

    text-transform: uppercase;
}


/* =========================================================
   VISUALIZER
   ========================================================= */

.visualizer {

    height: 85px;

    margin-top: 18px;

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 4px;

    overflow: hidden;
}

.bar {

    width: 4px;

    min-height: 5px;

    height: 8px;

    border-radius: 20px;

    background:
        linear-gradient(
            to top,
            #00eaff,
            #7c3cff,
            #ff00c8
        );

    box-shadow:
        0 0 8px
        rgba(0,234,255,.5);

    transition:
        height .08s
        linear;
}


/* =========================================================
   PROGRESS
   ========================================================= */

.progressArea {

    margin-top: 10px;
}

.timeRow {

    display: flex;

    justify-content: space-between;

    color: #77788b;

    font-size: 10px;

    margin-bottom: 7px;
}

.progress {

    width: 100%;

    height: 5px;

    border-radius: 20px;

    background: rgba(
        255,
        255,
        255,
        .08
    );

    cursor: pointer;

    overflow: hidden;
}

.progressFill {

    width: 0%;

    height: 100%;

    border-radius: 20px;

    background:
        linear-gradient(
            90deg,
            #00eaff,
            #7a4cff,
            #ff00c8
        );

    box-shadow:
        0 0 15px
        rgba(0,234,255,.8);
}


/* =========================================================
   CONTROLS
   ========================================================= */

.controls {

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 22px;

    margin-top: 24px;
}

.control {

    width: 48px;
    height: 48px;

    border-radius: 50%;

    border: 1px solid rgba(
        255,
        255,
        255,
        .10
    );

    background: rgba(
        255,
        255,
        255,
        .04
    );

    color: white;

    font-size: 18px;

    cursor: pointer;

    display: flex;

    align-items: center;

    justify-content: center;

    transition: .2s;
}

.control:hover {

    transform: scale(1.08);

    border-color:
        rgba(0,234,255,.6);

    box-shadow:
        0 0 20px
        rgba(0,234,255,.3);
}

.play {

    width: 68px;
    height: 68px;

    border: none;

    background:
        linear-gradient(
            135deg,
            #00eaff,
            #713cff,
            #ff00c8
        );

    box-shadow:
        0 0 25px
        rgba(0,234,255,.45),
        0 0 50px
        rgba(255,0,200,.2);

    font-size: 25px;
}

.play:hover {

    transform: scale(1.10);

    box-shadow:
        0 0 35px
        rgba(0,234,255,.65),
        0 0 70px
        rgba(255,0,200,.35);
}


/* =========================================================
   PLAYLIST
   ========================================================= */

.playlist {

    position: relative;

    z-index: 5;

    width: min(
        700px,
        94vw
    );

    margin: 28px auto 0;

    padding: 12px;

    border-radius: 18px;

    background:
        rgba(
            255,
            255,
            255,
            .035
        );

    border: 1px solid rgba(
        255,
        255,
        255,
        .07
    );

    backdrop-filter: blur(18px);

    max-height: 190px;

    overflow-y: auto;
}

.playlistTitle {

    padding: 5px 8px 10px;

    color: #656678;

    font-size: 9px;

    letter-spacing: 3px;

    text-align: left;
}

.track {

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 10px 12px;

    margin: 3px 0;

    border-radius: 11px;

    cursor: pointer;

    color: #a3a4b5;

    font-size: 12px;

    transition: .2s;
}

.track:hover {

    background:
        rgba(
            255,
            255,
            255,
            .06
        );

    color: white;
}

.track.active {

    color: white;

    background:
        linear-gradient(
            90deg,
            rgba(0,234,255,.12),
            rgba(122,60,255,.08),
            rgba(255,0,200,.08)
        );

    box-shadow:
        inset 2px 0 0
        #00eaff;
}

.trackNumber {

    width: 22px;

    color: #565768;

    font-size: 10px;
}

.track.active .trackNumber {

    color: #00eaff;
}

.trackName {

    flex: 1;

    overflow: hidden;

    white-space: nowrap;

    text-overflow: ellipsis;
}


/* =========================================================
   FULLSCREEN
   ========================================================= */

.fullscreen {

    position: absolute;

    right: 25px;

    top: 70px;

    z-index: 20;

    width: 40px;
    height: 40px;

    border-radius: 50%;

    border: 1px solid rgba(
        255,
        255,
        255,
        .10
    );

    background:
        rgba(
            255,
            255,
            255,
            .04
        );

    color: #77788a;

    cursor: pointer;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 600px) {

    .scene {
        min-height: 850px;
    }

    .topbar {
        padding:
            18px
            18px
            0;
    }

    .player {
        margin-top: 18px;
    }

    .recordWrap {
        width: 76vw;
    }

    .center {
        width: 82px;
        height: 82px;
    }

    .centerIcon {
        font-size: 25px;
    }

    .controls {
        gap: 14px;
    }

    .control {
        width: 43px;
        height: 43px;
    }

    .play {
        width: 62px;
        height: 62px;
    }

    .playlist {
        margin-top: 20px;
        max-height: 145px;
    }

    .fullscreen {
        top: 65px;
        right: 15px;
    }
}

</style>

</head>


<body>

<div class="scene">

    <div class="glow one"></div>
    <div class="glow two"></div>
    <div class="glow three"></div>


    <div class="topbar">

        <div class="logo">
            NEON MUSIC
        </div>

        <div class="live">
            <span class="liveDot"></span>
            AUDIO VISUALIZER
        </div>

    </div>


    <button
        class="fullscreen"
        onclick="goFullscreen()"
        title="Fullscreen"
    >
        ⛶
    </button>


    <main class="player">


        <!-- RECORD -->

        <div class="recordWrap">

            <div class="recordGlow"></div>

            <div
                id="record"
                class="record"
            >

                <div class="ring"></div>

            </div>

            <div class="center">

                <div class="centerIcon">
                    🎧
                </div>

            </div>

        </div>


        <!-- SONG -->

        <div class="songInfo">

            <div
                id="songTitle"
                class="songTitle"
            >
                NEON MUSIC
            </div>

            <div class="subtitle">
                NOW PLAYING
            </div>

        </div>


        <!-- VISUALIZER -->

        <div
            id="visualizer"
            class="visualizer"
        >
        </div>


        <!-- PROGRESS -->

        <div class="progressArea">

            <div class="timeRow">

                <span id="currentTime">
                    0:00
                </span>

                <span id="duration">
                    0:00
                </span>

            </div>

            <div
                id="progress"
                class="progress"
            >

                <div
                    id="progressFill"
                    class="progressFill"
                >
                </div>

            </div>

        </div>


        <!-- CONTROLS -->

        <div class="controls">

            <button
                id="prevBtn"
                class="control"
            >
                ⏮
            </button>

            <button
                id="playBtn"
                class="control play"
            >
                ▶
            </button>

            <button
                id="nextBtn"
                class="control"
            >
                ⏭
            </button>

        </div>


        <!-- PLAYLIST -->

        <div class="playlist">

            <div class="playlistTitle">
                PLAYLIST
            </div>

            <div id="playlist"></div>

        </div>


    </main>

</div>


<script>

/* =========================================================
   SONG DATA
   ========================================================= */

const songs = __SONGS_DATA__;

let currentIndex = 0;

let audio = new Audio();

audio.preload = "auto";

let audioContext = null;

let analyser = null;

let sourceNode = null;

let connected = false;


/* =========================================================
   ELEMENTS
   ========================================================= */

co
