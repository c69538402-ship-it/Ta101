
from pathlib import Path
import random
import streamlit as st

# ==========================================
# TA101 NEON MUSIC PLAYER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="TA101 | Neon Music Player",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ค้นหาไฟล์เพลงและโลโก้
audio_extensions = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"}

tracks = sorted(
    [
        p for p in BASE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in audio_extensions
    ],
    key=lambda p: p.name.lower(),
)

logo_path = BASE_DIR / "logo1.jpg"
if not logo_path.exists():
    logo_path = BASE_DIR / "logo.jpg"

# ==========================================
# NEON STYLE
# ==========================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top, #25104a 0%, #09091b 48%, #03040b 100%);
    color: #ffffff;
}
.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.neon-title {
    text-align: center;
    font-size: clamp(35px, 6vw, 65px);
    font-weight: 900;
    letter-spacing: 5px;
    color: #ffffff;
    text-shadow:
        0 0 6px #fff,
        0 0 15px #00eaff,
        0 0 35px #00aaff,
        0 0 65px #a000ff;
    animation: glow 2s ease-in-out infinite alternate;
}
.neon-subtitle {
    text-align: center;
    color: #00f7ff;
    letter-spacing: 4px;
    font-size: 14px;
    margin-bottom: 25px;
}
@keyframes glow {
    from { text-shadow: 0 0 8px #00eaff, 0 0 20px #0088ff; }
    to { text-shadow: 0 0 15px #ff00ee, 0 0 35px #8a00ff, 0 0 60px #00eaff; }
}
.panel {
    background: linear-gradient(145deg, #15142c, #090b19);
    border: 1px solid #513cff;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 0 20px #5400ff35, inset 0 0 20px #00d9ff0b;
    margin-bottom: 18px;
}
.panel-title {
    color: #00f7ff;
    font-size: 20px;
    font-weight: 800;
    text-shadow: 0 0 10px #00d9ff;
}
.disco {
    width: 155px;
    height: 155px;
    margin: 12px auto 24px auto;
    border-radius: 50%;
    background: repeating-radial-gradient(
        circle, #111 0px, #25243b 3px, #080812 6px, #29233e 9px
    );
    border: 5px solid #a000ff;
    box-shadow: 0 0 15px #a000ff, 0 0 35px #00eaff66;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: spin 8s linear infinite;
}
.disco-center {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: radial-gradient(circle, #ffffff, #00eaff 35%, #a000ff 70%);
    box-shadow: 0 0 20px #00eaff;
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.visualizer {
    height: 105px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    overflow: hidden;
    border-radius: 15px;
    background: #050511;
    border: 1px solid #302c76;
    padding: 10px;
}
.bar {
    width: 5px;
    max-width: 2.5%;
    height: var(--h);
    border-radius: 8px;
    background: linear-gradient(to top, #7a00ff, #00eaff, #ff00c8);
    box-shadow: 0 0 9px #00eaff;
    animation: pulse var(--speed) ease-in-out infinite alternate;
    animation-delay: var(--delay);
}
@keyframes pulse {
    from { transform: scaleY(.25); opacity: .6; }
    to { transform: scaleY(1); opacity: 1; }
}
.footer {
    text-align: center;
    color: #7f80b5;
    padding: 20px 0;
    font-size: 12px;
}
div[data-testid="stAudio"] {
    border: 1px solid #403b83;
    border-radius: 14px;
    padding: 8px;
    background: #111126;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #00f7ff !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

if logo_path.exists():
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(str(logo_path), use_container_width=True)

st.markdown(
    '<div class="neon-title">TA101 MUSIC</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="neon-subtitle">✦ NEON SOUND EXPERIENCE ✦</div>',
    unsafe_allow_html=True,
)

# ==========================================
# VISUAL EFFECTS
# ==========================================

bars = []
for i in range(38):
    height = random.randint(25, 100)
    speed = round(random.uniform(0.35, 1.2), 2)
    delay = round(random.uniform(-1.5, 0), 2)
    bars.append(
        f'<div class="bar" style="--h:{height}%;'
        f'--speed:{speed}s;--delay:{delay}s"></div>'
    )

st.markdown(
    '<div class="visualizer">' + "".join(bars) + '</div>',
    unsafe_allow_html=True,
)

st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        '<div class="panel" style="text-align:center">'
        '<div style="font-size:36px">🔊</div>'
        '<div class="panel-title">NEON BASS</div>'
        '<div style="color:#aaa">Feel the rhythm</div></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="panel" style="text-align:center">'
        '<div style="font-size:36px">🎧</div>'
        '<div class="panel-title">PURE SOUND</div>'
        '<div style="color:#aaa">Enjoy your music</div></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div class="panel" style="text-align:center">'
        '<div style="font-size:36px">💿</div>'
        '<div class="panel-title">MUSIC ZONE</div>'
        '<div style="color:#aaa">Enter the beat</div></div>',
        unsafe_allow_html=True,
    )

# ==========================================
# MUSIC PLAYER
# ==========================================

st.markdown(
    '<div class="panel-title">🎵 MUSIC PLAYER</div>',
    unsafe_allow_html=True,
)

if not tracks:
    st.warning(
        "ยังไม่พบไฟล์เพลง กรุณาอัปโหลดไฟล์ MP3 "
        "หรือไฟล์เสียงอื่นไว้ในโฟลเดอร์เดียวกับ app.py"
    )
else:
    track_names = [p.name for p in tracks]

    if "selected_track" not in st.session_state:
        st.session_state.selected_track = track_names[0]

    if st.session_state.selected_track not in track_names:
        st.session_state.selected_track = track_names[0]

    selected = st.selectbox(
        "เลือกเพลง",
        track_names,
        index=track_names.index(st.session_state.selected_track),
        key="track_selector",
    )
    st.session_state.selected_track = selected

    current_track = BASE_DIR / selected

    st.markdown(
        '<div class="disco"><div class="disco-center"></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="text-align:center;color:#fff;font-size:21px;'
        f'font-weight:800;margin-bottom:12px">'
        f'🎶 {selected}</div>',
        unsafe_allow_html=True,
    )

    # ใช้เครื่องเล่นเสียงมาตรฐานของ Streamlit
    try:
        with current_track.open("rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mpeg")

    except OSError as error:
        st.error(f"ไม่สามารถเปิดไฟล์เพลงได้: {error}")

    st.caption(
        "ใช้ปุ่มเล่นและแถบเสียงของเครื่องเล่นด้านบน "
        "เพื่อเล่น หยุด และปรับเสียง"
    )

    st.divider()

    st.markdown(
        '<div class="panel-title">🎛️ MUSIC CONTROLS</div>',
        unsafe_allow_html=True,
    )

    mode = st.selectbox(
        "โหมดเลือกเพลง",
        [
            "เล่นเพลงที่เลือก",
            "สุ่มเลือกเพลง",
            "เลือกเพลงถัดไป",
        ],
    )

    if st.button("✨ ใช้โหมดที่เลือก", use_container_width=True):
        if mode == "สุ่มเลือกเพลง":
            choices = [name for name in track_names if name != selected]
            if choices:
                st.session_state.selected_track = random.choice(choices)
            else:
                st.session_state.selected_track = selected
            st.rerun()

        elif mode == "เลือกเพลงถัดไป":
            index = track_names.index(selected)
            st.session_state.selected_track = track_names[
                (index + 1) % len(track_names)
            ]
            st.rerun()

        else:
            st.success("เลือกเพลงปัจจุบันแล้ว")

    st.markdown(
        '<div class="panel-title">📃 PLAYLIST</div>',
        unsafe_allow_html=True,
    )

    for number, track in enumerate(tracks, start=1):
        if track.name == selected:
            st.markdown(
                f"**🔊 {number}. {track.name} — กำลังเลือกอยู่**"
            )
        else:
            st.write(f"🎵 {number}. {track.name}")

# ==========================================
# FOOTER
# ==========================================

st.markdown(
    '<div class="footer">'
    'TA101 NEON MUSIC PLAYER • MADE FOR MUSIC LOVERS'
    '</div>',
    unsafe_allow_html=True,
        )
