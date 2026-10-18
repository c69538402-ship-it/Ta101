# SYNAPSE NEON MUSIC PLAYER
# Streamlit music player
# วางไฟล์นี้ไว้โฟลเดอร์เดียวกับ app.py และ logo1.jpg

from pathlib import Path
import base64
import html
import json
import mimetypes

import streamlit as st
import streamlit.components.v1 as components

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"
}


def get_track(item):
    """อ่านเพลงจากไฟล์ใน GitHub, UploadedFile หรือ URL"""

    try:
        if isinstance(item, dict):
            title = (
                item.get("title")
                or item.get("name")
                or item.get("ชื่อเพลง")
                or "เพลงไม่มีชื่อ"
            )

            url = item.get("url") or item.get("src")

            if url:
                return {
                    "title": str(title),
                    "src": str(url)
                }

            item = (
                item.get("path")
                or item.get("file_path")
                or item.get("file")
                or item.get("audio")
                or item.get("uploaded_file")
                or item.get("data")
            )

            if item is None:
                return None

        if isinstance(item, (str, Path)):
            path = Path(item)

            if (
                not path.is_file()
                or path.suffix.lower() not in AUDIO_EXTENSIONS
            ):
                return None

            filename = path.name
            raw = path.read_bytes()

        elif isinstance(item, (bytes, bytearray)):
            filename = "เพลง.mp3"
            raw = bytes(item)

        elif hasattr(item, "getvalue"):
            filename = getattr(item, "name", "เพลง.mp3")
            raw = item.getvalue()

        elif hasattr(item, "read"):
            filename = getattr(item, "name", "เพลง.mp3")

            try:
                item.seek(0)
            except Exception:
                pass

            raw = item.read()

            try:
                item.seek(0)
            except Exception:
                pass

        else:
            return None

        mime = mimetypes.guess_type(filename)[0] or "audio/mpeg"

        return {
            "title": Path(filename).stem,
            "src": (
                f"data:{mime};base64,"
                f"{base64.b64encode(raw).decode('ascii')}"
            )
        }

    except Exception:
        return None


def find_tracks(songs=None, folder="."):
    """ค้นหาเพลงจากรายการที่ส่งเข้ามาและโฟลเดอร์ใน Repository"""

    candidates = []

    if songs is not None:
        if isinstance(songs, (list, tuple)):
            candidates.extend(songs)
        else:
            candidates.append(songs)

    root = Path(folder)
    seen_paths = set()

    # ค้นหา MP3 ในโฟลเดอร์หลักและโฟลเดอร์ย่อยที่กำหนด
    for directory in (
        root,
        root / "music",
        root / "songs",
        root / "audio"
    ):
        if directory.is_dir():
            for path in sorted(
                directory.iterdir(),
                key=lambda p: p.name.casefold()
            ):
                if (
                    path.is_file()
                    and path.suffix.lower() in AUDIO_EXTENSIONS
                    and str(path.resolve()) not in seen_paths
                ):
                    seen_paths.add(str(path.resolve()))
                    candidates.append(path)

    tracks = []
    seen_tracks = set()

    for item in candidates:
        track = get_track(item)

        if track and track.get("src"):
            key = (track["title"], len(track["src"]))

            if key not in seen_tracks:
                seen_tracks.add(key)
                tracks.append(track)

    return tracks


def render_music_player(
    songs=None,
    logo_path="logo1.jpg",
    title="SYNAPSE",
    folder="."
):
    """แสดงเครื่องเล่นเพลง SYNAPSE ใน Streamlit"""

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(
                    ellipse at 8% 12%,
                    #00c4ff20, transparent 32%
                ),
                radial-gradient(
                    ellipse at 94% 32%,
                    #ec00ff1e, transparent 30%
                ),
                linear-gradient(
                    135deg, #030611, #080c20 52%, #090416
                );
        }

        .synapse-title {
            text-align: center;
            font-size: clamp(28px, 5vw, 48px);
            font-weight: 950;
            letter-spacing: 3px;
            color: #fff;
            text-shadow:
                0 0 8px #00eaff,
                0 0 22px #007bff,
                0 0 38px #e500ff;
        }

        .synapse-sub {
            text-align: center;
            color: #9cfaff;
            letter-spacing: 3px;
            font-size: 12px;
            margin-bottom: 1rem;
        }

        div[data-testid="stImage"] img {
            filter: drop-shadow(0 0 12px #00d2ff88);
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # โลโก้
    logo = Path(logo_path)

    if logo.is_file():
        left, center, right = st.columns([1, 2, 1])

        with center:
            st.image(str(logo), width="stretch")

    else:
        st.warning(
            f"ไม่พบไฟล์ {logo_path} "
            "กรุณาวาง logo1.jpg ไว้โฟลเดอร์เดียวกับ app.py"
        )

    st.markdown(
        f'<div class="synapse-title">{html.escape(title)}</div>'
        '<div class="synapse-sub">'
        'SOUND & VISUAL THERAPY • NEON AUDIO EXPERIENCE'
        '</div>',
        unsafe_allow_html=True
    )

    # โหลดรายการเพลง
    tracks = find_tracks(songs=songs, folder=folder)

    if not tracks:
        st.error(
            "ยังไม่พบไฟล์เพลง กรุณาวาง MP3 ไว้ในโฟลเดอร์หลัก "
            "หรือในโฟลเดอร์ music/"
        )

        st.code(
            'from music import render_music_player\n'
            'render_music_player(logo_path="logo1.jpg")',
            language="python"
        )

        return

    payload = json.dumps(
        tracks,
        ensure_ascii=False
    ).replace("</", "<\\/")

    player_html = r"""
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
:root {
    color-scheme: dark;
    --cyan: #00eaff;
    --pink: #ff22d6;
    --violet: #863dff;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: transparent;
    color: #f5f8ff;
    font-family: Arial, sans-serif;
}

.panel {
    padding: 18px;
    border-radius: 24px;
    border: 1px solid #00eaff9c;
    background:
        radial-gradient(ellipse at 0 0, #152c65, transparent 42%),
        radial-gradient(ellipse at 100% 100%, #3a124e, transparent 45%),
        linear-gradient(145deg, #030714, #080d20 60%, #100719);
    box-shadow:
        0 0 18px #00d9ff36,
        inset 0 0 28px #8c37ff1b;
    overflow: hidden;
}

.top {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 15px;
}

.live {
    width: 10px;
    height: 10px;
    flex-shrink: 0;
    border-radius: 50%;
    background: #67ffbd;
    box-shadow: 0 0 12px #67ffbd;
    animation: blink 1.3s infinite alternate;
}

@keyframes blink {
    to { opacity: .35; }
}

.brand {
    color: #9afaff;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 900;
}

.status {
    margin-left: auto;
    color: #aab8d9;
    font-size: 10px;
}

.layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 15px;
}

.nowbox {
    padding: 15px;
    border: 1px solid #863dff88;
    border-radius: 18px;
    background: #080b1bc9;
    box-shadow: inset 0 0 18px #5b2aff16;
}

.eyebrow {
    color: #ff82eb;
    font-size: 10px;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.song {
    color: white;
    font-size: clamp(19px, 4vw, 27px);
    font-weight: 900;
    line-height: 1.4;
    overflow-wrap: anywhere;
    text-shadow: 0 0 8px #00dfff, 0 0 20px #743aff;
}

.subline {
    text-align: center;
    color: #9cadd2;
    font-size: 11px;
    margin-top: 7px;
}

.visual {
    height: 90px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    margin: 12px 0;
}

.bar {
    width: 4px;
    height: var(--h);
    max-height: 78px;
    border-radius: 8px;
    background: linear-gradient(
        0deg, #783bff, #00f0ff, #ff32d7
    );
    box-shadow: 0 0 10px #00dfff;
    animation: beat var(--speed) ease-in-out infinite alternate;
    animation-play-state: paused;
}

.playing .bar {
    animation-play-state: running;
}

@keyframes beat {
    from {
        transform: scaleY(.22);
        opacity: .5;
    }
    to {
        transform: scaleY(1);
        opacity: 1;
    }
}

.seek {
    width: 100%;
    accent-color: #00eaff;
    cursor: pointer;
}

.times {
    display: flex;
    justify-content: space-between;
    color: #9badd2;
    font-size: 11px;
    margin-top: 5px;
}

.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 16px 0;
}

button {
    cursor: pointer;
    color: white;
    border: 1px solid #00eaff9c;
    background: linear-gradient(135deg, #101a3a, #16102d);
    border-radius: 14px;
    padding: 10px 13px;
    transition: .2s;
}

button:hover {
    border-color: #ff27d8;
    box-shadow: 0 0 17px #ff27d855;
    transform: translateY(-1px);
}

.mainbtn {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    font-size: 22px;
    background: linear-gradient(
        135deg, #00cfff, #763dff 60%, #ed28d5
    );
    box-shadow: 0 0 18px #00cfff77;
}

.opts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

label {
    display: block;
    color: #9badd2;
    font-size: 10px;
    margin-bottom: 6px;
}

select {
    width: 100%;
    padding: 10px;
    color: white;
    background: #0c1430;
    border: 1px solid #00dfff86;
    border-radius: 12px;
}

.vol {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 14px 0;
    color: #aab9d8;
    font-size: 12px;
}

.vol input {
    flex: 1;
    accent-color: #ff27d8;
}

.listhead {
    display: flex;
    justify-content: space-between;
    color: #91faff;
    font-weight: 900;
    font-size: 11px;
    letter-spacing: 2px;
    margin: 17px 0 8px;
}

.search {
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid #753fff9c;
    background: #080d20;
    color: white;
    margin-bottom: 9px;
}

.playlist {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 230px;
    overflow-y: auto;
}

.track {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    text-align: left;
    padding: 10px;
    border: 1px solid #243259;
    background: #080e22;
    border-radius: 11px;
}

.track.active {
    border-color: #ff2bd6;
    background: #21113b;
    box-shadow: 0 0 13px #ff27d52c;
}

.num {
    min-width: 23px;
    color: #00eaff;
    font-size: 11px;
}

.trackname {
    flex: 1;
    overflow-wrap: anywhere;
    font-size: 12px;
}

.playingtag {
    font-size: 9px;
    color: #ff7ce8;
}

.mixer {
    border: 1px solid #ff29d580;
    border-radius: 17px;
    padding: 14px;
    margin-top: 14px;
    background: linear-gradient(120deg, #0a1024, #130a26);
    box-shadow: inset 0 0 20px #ff22d610;
}

.mixhead {
    color: #ff8bf0;
    letter-spacing: 3px;
    font-weight: 900;
    font-size: 12px;
    margin-bottom: 12px;
}

.mixgrid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
}

.mixitem {
    text-align: center;
    color: #aebcdb;
    font-size: 10px;
}

.mixitem input {
    width: 100%;
    accent-color: #ff29d8;
}

.mixval {
    color: #8cfaff;
    font-size: 10px;
}

.speakerrow {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    color: #8cfaff;
    font-size: 12px;
}

.note {
    text-align: center;
    color: #667ba6;
    font-size: 10px;
    margin-top: 14px;
}

@media (min-width: 650px) {
    .layout {
        grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr);
    }
}

@media (max-width: 420px) {
    .panel { padding: 12px; }
    .opts { grid-template-columns: 1fr; }
    .controls { gap: 7px; }
    .mixgrid { gap: 5px; }
}
</style>
</head>

<body>
<div class="panel" id="panel">
<div class="top">
    <span class="live"></span>
    <span class="brand">SYNAPSE • SOUND & VISUAL THERAPY</span>
    <span class="status" id="status">READY</span>
</div>

<div class="layout">

<section class="nowbox">
    <div class="eyebrow">♫ NOW PLAYING / กำลังเล่น</div>
    <div class="song" id="songTitle">เตรียมเพลง...</div>
    <div class="subline" id="counter"></div>

    <div class="visual" id="visual"></div>
    <audio id="audio" preload="metadata"></audio>

    <input class="seek" id="seek" type="range"
           min="0" max="1000" value="0">

    <div class="times">
        <span id="elapsed">0:00</span>
        <span id="duration">0:00</span>
    </div>

    <div class="controls">
        <button id="prev" title="เพลงก่อนหน้า">⏮</button>
        <button class="mainbtn" id="toggle" title="เล่น/หยุด">▶</button>
        <button id="next" title="เพลงถัดไป">⏭</button>
        <button id="restart" title="เริ่มเพลงนี้ใหม่">↻</button>
    </div>

    <div class="opts">
        <div>
            <label for="mode">PLAY MODE • โหมดเล่น</label>
            <select id="mode">
                <option value="continuous">▶ ต่อเนื่องตามลำดับ</option>
                <option value="shuffle">🔀 สุ่มเพลงต่อเนื่อง</option>
                <option value="single">■ เพลงเดียวแล้วหยุด</option>
                <option value="repeat">🔁 วนเพลงเดิม</option>
            </select>
        </div>
        <div>
            <label for="pick">SELECT TRACK • เลือกเพลง</label>
            <select id="pick"></select>
        </div>
    </div>

    <div class="vol">
        <span>🔊</span>
        <span>VOLUME</span>
        <input id="volume" type="range" min="0" max="100" value="80">
        <span id="volvalue">80%</span>
    </div>
</section>

<section>
    <div class="listhead">
        <span>♫ PLAYLIST</span>
        <span id="total"></span>
    </div>

    <input class="search" id="search"
           placeholder="⌕ ค้นหาชื่อเพลง..." autocomplete="off">

    <div class="playlist" id="playlist"></div>

    <div class="mixer">
        <div class="mixhead">〰 NEON MIXER</div>
        <div class="mixgrid">
            <div class="mixitem">
                BASS
                <input id="bass" type="range" min="0" max="100" value="65">
                <div class="mixval" id="bassval">65%</div>
            </div>
            <div class="mixitem">
                MID
                <input id="mid" type="range" min="0" max="100" value="50">
                <div class="mixval" id="midval">50%</div>
            </div>
            <div class="mixitem">
                TREBLE
                <input id="treble" type="range" min="0" max="100" value="75">
                <div class="mixval" id="trebleval">75%</div>
            </div>
            <div class="mixitem">
                GLOW
                <input id="glow" type="range" min="0" max="100" value="80">
                <div class="mixval" id="glowval">80%</div>
            </div>
        </div>
        <div class="speakerrow">
            <span>🔊 SPEAKER MODE</span>
            <span id="speakerstate">NEON ON</span>
        </div>
    </div>
</section>

</div>
<div class="note">NEON AUDIO EXPERIENCE • เลือกเพลงแล้วกด ▶ เพื่อเริ่มฟัง</div>
</div>

<script>
const tracks = __TRACKS__;
const $ = id => document.getElementById(id);
const audio = $("audio");
const panel = $("panel");

let index = 0;
let seeking = false;

// สร้างกราฟเสียงหลากสี
for (let i = 0; i < 43; i++) {
    const bar = document.createElement("span");
    bar.className = "bar";
    bar.style.setProperty(
        "--h",
        (8 + Math.abs(Math.sin(i * 1.55)) * 70) + "px"
    );
    bar.style.setProperty("--speed", (0.25 + (i % 9) * 0.075) + "s");
    bar.style.animationDelay = (-i * 0.05) + "s";
    $("visual").appendChild(bar);
}

function formatTime(value) {
    if (!Number.isFinite(value) || value < 0) return "0:00";
    return Math.floor(value / 60) + ":" +
        String(Math.floor(value % 60)).padStart(2, "0");
}

function setStatus(value) {
    $("status").textContent = value;
}

function renderPlaylist() {
    $("pick").innerHTML = "";

    tracks.forEach((track, i) => {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = (i + 1) + ". " + track.title;
        $("pick").appendChild(option);
    });

    $("total").textContent = tracks.length + " TRACKS";
    drawPlaylist();
}

function drawPlaylist() {
    const query = $("search").value.trim().toLocaleLowerCase();
    $("playlist").innerHTML = "";

    tracks.forEach((track, i) => {
        if (!track.title.toLocaleLowerCase().includes(query)) return;

        const button = document.createElement("button");
        button.className = "track" + (i === index ? " active" : "");

        const number = document.createElement("span");
        number.className = "num";
        number.textContent = String(i + 1).padStart(2, "0");

        const name = document.createElement("span");
        name.className = "trackname";
        name.textContent = track.title;

        const tag = document.createElement("span");
        tag.className = "playingtag";
        tag.textContent = i === index ? "NOW PLAYING" : "▶";

        button.append(number, name, tag);
        button.addEventListener("click", () => {
            loadTrack(i);
            playAudio();
        });

        $("playlist").appendChild(button);
    });
}

function loadTrack(i, autoplay = false) {
    if (!tracks.length) return;

    index = (i + tracks.length) % tracks.length;

    audio.src = tracks[index].src;
    audio.load();

    $("songTitle").textContent = tracks[index].title;
    $("counter").textContent =
        "TRACK " + (index + 1) + " / " + tracks.length;

    $("pick").value = String(index);
    $("seek").value = 0;
    $("elapsed").textContent = "0:00";
    $("duration").textContent = "0:00";

    drawPlaylist();

    if (autoplay) {
        playAudio();
    } else {
        setStatus("READY");
        $("toggle").textContent = "▶";
        panel.classList.remove("playing");
    }
}

async function playAudio() {
    try {
        await audio.play();
        $("toggle").textContent = "Ⅱ";
        setStatus("PLAYING");
        panel.classList.add("playing");
    } catch (error) {
        setStatus("กด ▶ เพื่อเล่น");
        $("toggle").textContent = "▶";
    }
}

function pauseAudio() {
    audio.pause();
    $("toggle").textContent = "▶";
    setStatus("PAUSED");
    panel.classList.remove("playing");
}

function nextTrack() {
    const mode = $("mode").value;

    if (mode === "single") {
        audio.pause();
        audio.currentTime = 0;
        $("seek").value = 0;
        $("toggle").textContent = "▶";
        setStatus("FINISHED");
        panel.classList.remove("playing");
        return;
    }

    if (mode === "repeat") {
        audio.currentTime = 0;
        playAudio();
        return;
    }

    let next = index;

    if (mode === "shuffle" && tracks.length > 1) {
        do {
            next = Math.floor(Math.random() * tracks.length);
        } while (next === index);
    } else {
        next = index + 1;
    }

    if (next >= tracks.length) {
        if (mode === "continuous") {
            next = 0;
        } else {
            audio.pause();
            audio.currentTime = 0;
            setStatus("PLAYLIST END");
            panel.classList.remove("playing");
            return;
        }
    }

    loadTrack(next, true);
}

// ปุ่มควบคุมเพลง
$("toggle").addEventListener("click", () => {
    if (audio.paused) playAudio();
    else pauseAudio();
});

$("prev").addEventListener("click", () => {
    loadTrack(index - 1, true);
});

$("next").addEventListener("click", nextTrack);

$("restart").addEventListener("click", () => {
    audio.currentTime = 0;
    playAudio();
});

$("pick").addEventListener("change", () => {
    loadTrack(Number($("pick").value), true);
});

$("search").addEventListener("input", drawPlaylist);

audio.addEventListener("ended", nextTrack);

audio.addEventListener("timeupdate", () => {
    if (!seeking && audio.duration > 0) {
        $("seek").value = Math.round(
            audio.currentTime / audio.duration * 1000
        );
    }

    $("elapsed").textContent = formatTime(audio.currentTime);
    $("duration").textContent = formatTime(audio.duration);
});

$("seek").addEventListener("input", () => {
    seeking = true;
});

$("seek").addEventListener("change", () => {
    if (audio.duration > 0) {
        audio.currentTime =
            Number($("seek").value) / 1000 * audio.duration;
    }
    seeking = false;
});

$("volume").addEventListener("input", event => {
    audio.volume = Number(event.target.value) / 100;
    $("volvalue").textContent = event.target.value + "%";
});

audio.volume = 0.8;

// ปรับแสงของแผงมิกเซอร์
["bass", "mid", "treble", "glow"].forEach(id => {
    $(id).addEventListener("input", event => {
        $(id + "val").textContent = event.target.value + "%";

        if (id === "glow") {
            const value = Number(event.target.value) / 100;

            panel.style.boxShadow =
                "0 0 " + (8 + value * 24) +
                "px rgba(0,220,255," + (value * 0.35) + ")," +
                "inset 0 0 28px rgba(140,55,255," +
                (value * 0.14) + ")";
        }
    });
});

renderPlaylist();
loadTrack(0);
</script>
</body>
</html>
"""

            st.iframe(
        player_html.replace("__TRACKS__", payload),
        height=1040,
            )

# เปิดไฟล์นี้โดยตรงก็ได้
if __name__ == "__main__":
    st.set_page_config(
        page_title="SYNAPSE Music Player",
        page_icon="🎧",
        layout="wide"
    )

    render_music_player(logo_path="logo1.jpg")
