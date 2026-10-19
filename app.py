import os
import random
import streamlit as st

# =========================
# ตั้งค่าหน้าแอป
# =========================
st.set_page_config(
    page_title="TA101 | Neon Music",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# ค้นหาเพลงและโลโก้
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logo_path = None
for logo_name in ["logo1.jpg", "logo.jpg", "logo1.png", "logo.png"]:
    candidate = os.path.join(BASE_DIR, logo_name)
    if os.path.isfile(candidate):
        logo_path = candidate
        break

music_files = []
for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [
        d for d in dirs
        if d not in [".git", "__pycache__", ".streamlit"]
    ]
    for file in files:
        if file.lower().endswith((".mp3", ".wav", ".ogg", ".m4a")):
            music_files.append(os.path.join(root, file))

music_files.sort(key=lambda p: os.path.basename(p).lower())

# =========================
# สีสันและเอฟเฟกต์
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top left, #35105e 0%, transparent 42%),
        radial-gradient(ellipse at bottom right, #063d56 0%, transparent 42%),
        linear-gradient(135deg, #080713, #101020 55%, #090b18);
    color: #ffffff;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.neon-title {
    text-align: center;
    font-size: clamp(34px, 7vw, 66px);
    font-weight: 900;
    letter-spacing: 4px;
    color: #ffffff;
    text-shadow:
        0 0 6px #fff,
        0 0 16px #00eaff,
        0 0 35px #a000ff,
        0 0 60px #ff00c8;
    animation: glow 2s ease-in-out infinite alternate;
}
.neon-subtitle {
    text-align: center;
    color: #62f7ff;
    letter-spacing: 4px;
    font-size: 13px;
    margin-bottom: 22px;
}
@keyframes glow {
    from { filter: brightness(0.85); }
    to { filter: brightness(1.35); }
}
.music-card {
    background: linear-gradient(145deg,
        rgba(31, 23, 57, 0.96),
        rgba(9, 22, 42, 0.96));
    border: 1px solid rgba(0, 238, 255, 0.65);
    border-radius: 24px;
    padding: 24px;
    box-shadow:
        0 0 14px rgba(0, 238, 255, 0.18),
        0 0 30px rgba(190, 0, 255, 0.12);
    margin-bottom: 20px;
}
.section-title {
    color: #ff7bea;
    font-size: 21px;
    font-weight: 800;
    text-shadow: 0 0 12px #ff00c8;
}
.neon-line {
    height: 3px;
    border-radius: 5px;
    background: linear-gradient(90deg,
        #00eaff, #a000ff, #ff00c8, #ffe600, #00ff9d);
    box-shadow: 0 0 14px #00eaff;
    margin: 15px 0 22px 0;
}
.visualizer {
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    overflow: hidden;
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 12px;
}
.bar {
    width: 5px;
    max-width: 3%;
    height: 18%;
    border-radius: 8px;
    background: linear-gradient(to top, #00eaff, #a000ff, #ff45c8);
    box-shadow: 0 0 9px #00eaff;
    animation: wave 0.75s ease-in-out infinite alternate;
}
@keyframes wave {
    0% { height: 12%; }
    50% { height: 95%; }
    100% { height: 30%; }
}
.bar:nth-child(3n) { animation-delay: -0.3s; background: #ff37d5; }
.bar:nth-child(4n) { animation-delay: -0.5s; background: #ffe600; }
.bar:nth-child(5n) { animation-delay: -0.2s; background: #00ff9d; }
.info-text {
    text-align: center;
    color: #b8c7ff;
    font-size: 13px;
}
div[data-testid="stAudio"] {
    border: 1px solid #7e5cff;
    border-radius: 14px;
    padding: 8px;
    background: rgba(15, 12, 35, 0.8);
}
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #72f7ff !important;
    font-weight: 700;
}
.stButton > button {
    border: 1px solid #00eaff;
    border-radius: 14px;
    background: linear-gradient(90deg, #641aff, #d000b9);
    color: white;
    font-weight: 800;
    box-shadow: 0 0 12px rgba(0,234,255,0.25);
}
.stButton > button:hover {
    border-color: #ffffff;
    color: #ffffff;
    box-shadow: 0 0 22px #c000ff;
}
.footer {
    text-align: center;
    color: #8c9abb;
    font-size: 12px;
    margin-top: 28px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ส่วนหัว
# =========================
if logo_path:
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(logo_path, use_container_width=True)

st.markdown(
    '<div class="neon-title">🎧 NEON MUSIC 🎧</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="neon-subtitle">T A 1 0 1 • MUSIC EXPERIENCE</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

# =========================
# กราฟเสียงตกแต่ง
# =========================
bars = "".join(
    f'<div class="bar" style="animation-duration:{random.uniform(0.4, 1.0):.2f}s"></div>'
    for _ in range(48)
)
st.markdown(
    f'<div class="visualizer">{bars}</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="info-text">✨ NEON LIGHTS • MUSIC • GOOD VIBES ✨</p>',
    unsafe_allow_html=True
)

st.write("")

# =========================
# เครื่องเล่นเพลง
# =========================
left_col, right_col = st.columns([1.3, 1], gap="large")

with left_col:
    st.markdown('<div class="music-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">🎵 MUSIC PLAYER</div>',
        unsafe_allow_html=True
    )

    if music_files:
        track_names = [
            os.path.relpath(path, BASE_DIR).replace("\\", "/")
            for path in music_files
        ]

        selected_name = st.selectbox(
            "เลือกเพลงที่ต้องการฟัง",
            track_names,
            key="selected_track"
        )

        selected_path = os.path.join(BASE_DIR, selected_name)

        st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)
        st.markdown("**🎶 กำลังเลือกเพลง**")
        st.write(os.path.basename(selected_name))

        try:
            with open(selected_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            file_ext = os.path.splitext(selected_path)[1].lower()
            audio_format = {
                ".mp3": "audio/mpeg",
                ".wav": "audio/wav",
                ".ogg": "audio/ogg",
                ".m4a": "audio/mp4"
            }.get(file_ext, "audio/mpeg")

            st.audio(audio_bytes, format=audio_format)

        except Exception as error:
            st.error(f"เปิดไฟล์เพลงไม่ได้: {error}")

        st.caption(f"พบเพลงทั้งหมด {len(music_files)} เพลง")
    else:
        st.warning(
            "ยังไม่พบไฟล์เพลง กรุณาอัปโหลดไฟล์ MP3 "
            "ไว้ใน Repository ของแอป"
        )
        st.code("app.py\nlogo1.jpg\nเพลงของคุณ.mp3")

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="music-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">🔊 SOUND STATION</div>',
        unsafe_allow_html=True
    )
    st.write("🎧 เปิดเสียงแล้วสนุกไปกับเพลงของคุณ")
    st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

    st.markdown("**🌈 NEON VISUALIZER**")
    st.markdown(
        '<p style="color:#b6c6ff">'
        'เอฟเฟกต์คลื่นเสียงตกแต่งหน้าจอ'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="
        font-size:48px;
        text-align:center;
        padding:18px 0;
        filter:drop-shadow(0 0 14px #00eaff);
    ">🎧 🔊 🎶</div>
    """, unsafe_allow_html=True)

    st.markdown("**💿 MUSIC MODE**")
    st.write("เลือกเพลงจากรายการทางฝั่งซ้าย แล้วกดเล่นได้เลย")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# รายชื่อเพลงทั้งหมด
# =========================
st.markdown('<div class="music-card">', unsafe_allow_html=True)
st.markdown(
    '<div class="section-title">📀 YOUR PLAYLIST</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="neon-line"></div>', unsafe_allow_html=True)

if music_files:
    for number, path in enumerate(music_files, start=1):
        name = os.path.relpath(path, BASE_DIR).replace("\\", "/")
        st.write(f"**{number:02d}.** 🎵 {name}")
else:
    st.info("เพิ่มไฟล์เพลงลงใน Repository เพื่อสร้าง Playlist")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer">'
    'TA101 • NEON MUSIC • MADE FOR MUSIC LOVERS 💜'
    '</div>',
    unsafe_allow_html=True
)
