
import streamlit as st
import os
import random
import base64
import mimetypes
from pathlib import Path
from html import escape

# ==============================
# TA101 • NEON MUSIC
# PART 1
# ==============================

st.set_page_config(
    page_title="TA101 • NEON MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"
}

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top, #172554 0%, #08091b 45%, #02030a 100%);
    color: #f8fafc;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.neon-title {
    text-align: center;
    font-size: clamp(34px, 6vw, 66px);
    font-weight: 900;
    letter-spacing: 5px;
    color: #ffffff;
    text-shadow:
        0 0 8px #00eaff,
        0 0 20px #00aaff,
        0 0 45px #8b5cf6;
    animation: glow 2.5s ease-in-out infinite alternate;
}
.neon-subtitle {
    text-align: center;
    color: #67e8f9;
    letter-spacing: 4px;
    font-size: 12px;
}
@keyframes glow {
    from { filter: brightness(.8); }
    to { filter: brightness(1.5); }
}
.neon-panel {
    border: 1px solid #06b6d4;
    border-radius: 18px;
    padding: 18px;
    background: linear-gradient(135deg,
        rgba(15,23,42,.96), rgba(49,20,90,.55));
    box-shadow: 0 0 18px rgba(6,182,212,.2),
                inset 0 0 18px rgba(139,92,246,.08);
}
div.stButton > button {
    border: 1px solid #22d3ee;
    border-radius: 12px;
    background: linear-gradient(120deg, #172554, #581c87);
    color: white;
    font-weight: bold;
    min-height: 44px;
}
div.stButton > button:hover {
    border-color: #f0abfc;
    color: #ffffff;
    box-shadow: 0 0 15px #a855f7;
}
div[data-testid="stAudio"] {
    border: 1px solid #8b5cf6;
    border-radius: 12px;
    padding: 8px;
}
section[data-testid="stSidebar"] {
    background: #08091b;
}
</style>
""", unsafe_allow_html=True)


def find_logo():
    candidates = [
        ROOT / "logo1.jpg",
        ROOT / "logo1.jpeg",
        ROOT / "logo1.png",
        ROOT / "logo.jpg",
        ROOT / "โลโก้.jpg",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def find_songs():
    songs = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        songs.append(path)
    return sorted(songs, key=lambda p: p.name.lower())


def song_label(path):
    return path.stem


def show_header():
    logo = find_logo()

    if logo:
        left, center, right = st.columns([1, 3, 1])
        with center:
            st.image(str(logo), width=260)

    st.markdown(
        '<div class="neon-title">TA101</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="neon-subtitle">'
        'NEON MUSIC • SOUND & SPACE EXPERIENCE'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")
    
# ==============================
# PART 2 — MUSIC PLAYER
# ==============================

def main():
    show_header()

    songs = find_songs()

    if not songs:
        st.markdown("""
        <div class="neon-panel">
            <h3>🎵 ยังไม่พบไฟล์เพลง</h3>
            <p>นำไฟล์ MP3 หรือ WAV ใส่ในโฟลเดอร์เดียวกับ app.py</p>
            <p>จากนั้นรีสตาร์ตแอป Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    labels = [song_label(p) for p in songs]

    if "track_index" not in st.session_state:
        st.session_state.track_index = 0
    if "shuffle_mode" not in st.session_state:
        st.session_state.shuffle_mode = False
    if "repeat_mode" not in st.session_state:
        st.session_state.repeat_mode = False

    # ป้องกัน index เกินจำนวนเพลง
    st.session_state.track_index %= len(songs)

    st.markdown("""
    <div class="neon-panel">
        <h2 style="text-align:center;color:#67e8f9">
            🎧 MUSIC CONTROL CENTER
        </h2>
        <p style="text-align:center;color:#c4b5fd">
            เลือกเพลง • ปรับเสียง • เพลิดเพลินกับแสงนีออน
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    selected = st.selectbox(
        "🎶 รายชื่อเพลงในโปรเจกต์",
        options=list(range(len(songs))),
        index=st.session_state.track_index,
        format_func=lambda i: labels[i],
        key="song_selector"
    )

    if selected != st.session_state.track_index:
        st.session_state.track_index = selected
        st.rerun()

    current = songs[st.session_state.track_index]

    st.markdown(
        '<div class="neon-panel">'
        '<p style="color:#a5f3fc;text-align:center">NOW PLAYING</p>'
        f'<h2 style="text-align:center;color:white;'
        f'text-shadow:0 0 12px #06b6d4">'
        f'🎵 {escape(current.stem)}</h2>'
        f'<p style="text-align:center;color:#c4b5fd">'
        f'TRACK {st.session_state.track_index + 1} / {len(songs)}'
        '</p></div>',
        unsafe_allow_html=True
    )

    st.write("")

    # อ่านไฟล์เสียงโดยตรงจากโปรเจกต์
    mime_type, _ = mimetypes.guess_type(str(current))
    if not mime_type:
        mime_type = "audio/mpeg"

    with open(current, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(
        audio_bytes,
        format=mime_type,
        autoplay=False
    )

    volume = st.slider(
        "🔊 ระดับเสียง",
        min_value=0,
        max_value=100,
        value=80,
        key="volume_control"
    )

    st.caption(
        "ระดับเสียงที่เลือก: "
        + str(volume)
        + "% — ปรับเสียงจากตัวควบคุมของเครื่องเล่นด้วย"
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("⏮ เพลงก่อนหน้า", use_container_width=True):
            st.session_state.track_index = (
                st.session_state.track_index - 1
            ) % len(songs)
            st.rerun()

    with c2:
        if st.button("🔀 สุ่มเพลงถัดไป", use_container_width=True):
            if len(songs) > 1:
                choices = [
                    i for i in range(len(songs))
                    if i != st.session_state.track_index
                ]
                st.session_state.track_index = random.choice(choices)
            st.rerun()

    with c3:
        if st.button("⏭ เพลงถัดไป", use_container_width=True):
            st.session_state.track_index = (
                st.session_state.track_index + 1
            ) % len(songs)
            st.rerun()

    st.write("")

    m1, m2 = st.columns(2)

    with m1:
        st.session_state.repeat_mode = st.toggle(
            "🔁 เล่นเพลงเดิมซ้ำ",
            value=st.session_state.repeat_mode,
            key="repeat_toggle"
        )

    with m2:
        st.session_state.shuffle_mode = st.toggle(
            "🎲 โหมดสุ่มเพลง",
            value=st.session_state.shuffle_mode,
            key="shuffle_toggle"
        )

    st.write("")

    st.markdown("""
    <div class="neon-panel">
        <h3 style="color:#67e8f9">🌌 NEON SOUND SYSTEM</h3>
        <p>💠 Cyan • 🔮 Purple • 💙 Electric Blue</p>
        <p>โลโก้และไฟล์เพลงเดิมจะถูกเก็บไว้</p>
        <p style="color:#c4b5fd">
            หากหน้าแอปเคยค้างที่โลโก้ โค้ดนี้จะเปิดหน้าเครื่องเล่น
            โดยตรง ไม่ต้องรอหน้าเปิดตัว
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📂 ดูรายชื่อไฟล์เพลงทั้งหมด"):
        for i, path in enumerate(songs, start=1):
            st.write(f"{i}. {path.name}")


if __name__ == "__main__":
    main()
