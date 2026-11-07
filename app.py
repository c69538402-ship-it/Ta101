from pathlib import Path
import random
import mimetypes
import streamlit as st

# =========================================================
# TA101 • NEON MUSIC PLAYER — stable mobile-friendly edition
# ใช้เครื่องเล่นเสียง Native ของ Streamlit เพื่อเลี่ยง iframe จอดำ
# วาง app.py, logo1.jpg และไฟล์เพลงไว้โฟลเดอร์เดียวกันได้เลย
# =========================================================

st.set_page_config(
    page_title="TA101 • NEON MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}
LOGO_NAMES = ("logo1.jpg", "logo1.jpeg", "logo1.png")

# ---------- NEON SPACE THEME ----------
st.markdown("""
<style>
.stApp {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(0,190,255,.20), transparent 38%),
    radial-gradient(ellipse at 10% 55%, rgba(125,45,255,.16), transparent 35%),
    radial-gradient(ellipse at 90% 75%, rgba(0,255,180,.10), transparent 32%),
    linear-gradient(160deg,#020611 0%,#071126 48%,#090419 100%);
  color:#effaff;
}
header[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:1150px;padding-top:1rem;padding-bottom:2rem;}
h1,h2,h3,p,label {color:#effaff;}
.ta-title {
  text-align:center;font-weight:1000;letter-spacing:3px;
  font-size:clamp(30px,6vw,58px);line-height:1.15;
  color:#fff;text-shadow:0 0 8px #00eaff,0 0 22px #168cff,0 0 42px #a000ff;
  animation:glow 2.6s ease-in-out infinite alternate;
}
.ta-sub {
  text-align:center;color:#7cecff;letter-spacing:5px;
  font-size:12px;margin-top:9px;margin-bottom:20px;
}
@keyframes glow {
  from {filter:brightness(.9);text-shadow:0 0 7px #00eaff,0 0 18px #168cff;}
  to {filter:brightness(1.25);text-shadow:0 0 12px #00eaff,0 0 30px #8b35ff,0 0 48px #00bfff;}
}
.logo-wrap {display:flex;justify-content:center;margin:8px 0 16px;}
.logo-wrap img {
  width:min(210px,48vw);height:auto;max-height:210px;object-fit:contain;
  border-radius:50%;padding:5px;
  border:1px solid rgba(76,230,255,.75);
  box-shadow:0 0 18px #00d9ff,0 0 42px #743cff;
  animation:logoPulse 2.2s ease-in-out infinite;
}
@keyframes logoPulse {
  0%,100% {transform:scale(1);filter:brightness(1);}
  50% {transform:scale(1.035);filter:brightness(1.18);}
}
.panel {
  background:linear-gradient(145deg,rgba(10,25,52,.94),rgba(12,7,35,.94));
  border:1px solid rgba(58,220,255,.42);border-radius:20px;
  padding:18px;box-shadow:0 0 20px rgba(0,190,255,.12),inset 0 0 22px rgba(110,60,255,.08);
}
div.stButton > button {
  border:1px solid #35dfff;border-radius:13px;
  color:#eaffff;background:linear-gradient(135deg,#092747,#26104a);
  box-shadow:0 0 12px #00cfff55;
  font-weight:800;min-height:44px;
}
div.stButton > button:hover {
  border-color:#fff;color:#fff;box-shadow:0 0 20px #00dfff;
}
div[data-testid="stAudio"] {width:100%;}
.stSelectbox label {color:#8cefff!important;font-weight:800;}
hr {border-color:#25436c;}
.equalizer {height:54px;display:flex;align-items:end;justify-content:center;gap:5px;margin:8px auto 18px;}
.equalizer span {
  display:block;width:7px;border-radius:8px 8px 2px 2px;
  background:linear-gradient(0deg,#00eaff,#8b5cff,#ff42d6);
  box-shadow:0 0 9px #00dfff;animation:eq .75s ease-in-out infinite alternate;
}
.equalizer span:nth-child(1){height:20%;animation-delay:-.1s}
.equalizer span:nth-child(2){height:55%;animation-delay:-.5s}
.equalizer span:nth-child(3){height:80%;animation-delay:-.2s}
.equalizer span:nth-child(4){height:38%;animation-delay:-.7s}
.equalizer span:nth-child(5){height:95%;animation-delay:-.3s}
.equalizer span:nth-child(6){height:48%;animation-delay:-.6s}
.equalizer span:nth-child(7){height:72%;animation-delay:-.4s}
.equalizer span:nth-child(8){height:30%;animation-delay:-.8s}
.equalizer span:nth-child(9){height:88%;animation-delay:-.2s}
.equalizer span:nth-child(10){height:42%;animation-delay:-.5s}
@keyframes eq {from{transform:scaleY(.35);opacity:.65}to{transform:scaleY(1);opacity:1}}
.small-note {text-align:center;color:#8baacb;font-size:12px;}
</style>
""", unsafe_allow_html=True)

def find_logo():
    for name in LOGO_NAMES:
        p = ROOT / name
        if p.is_file():
            return p
    return None
 def find_songs():
    found = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        try:
            rel = p.relative_to(ROOT)
            if any(part.startswith(".") or part in {"__pycache__", ".venv", "venv"} for part in rel.parts):
                continue
            found.append(p)
        except (OSError, ValueError):
            continue
    return sorted(found, key=lambda p: (p.stem.casefold(), p.name.casefold()))

songs = find_songs()
logo = find_logo()

# ---------- HEADER ----------
st.markdown('<div class="ta-title">🎧 TA101 • NEON MUSIC</div>', unsafe_allow_html=True)
st.markdown('<div class="ta-sub">MUSIC • DREAM • TOGETHER</div>', unsafe_allow_html=True)

if logo:
    import base64
    import mimetypes as mt
    logo_mime = mt.guess_type(logo.name)[0] or "image/jpeg"
    logo_b64 = base64.b64encode(logo.read_bytes()).decode("ascii")
    st.markdown(
        f'<div class="logo-wrap"><img src="data:{logo_mime};base64,{logo_b64}" alt="TA101 logo"></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="small-note">ไม่พบ logo1.jpg — วางไฟล์โลโก้ไว้ข้าง app.py เพื่อแสดงโลโก้</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="equalizer">' + "".join("<span></span>" for _ in range(10)) + '</div>',
    unsafe_allow_html=True,
)

# ---------- PLAYER ----------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### 🎵 MUSIC PLAYER")

if not songs:
    st.warning("ยังไม่พบไฟล์เพลง กรุณาวางไฟล์ MP3 / WAV / M4A หรือไฟล์เสียงอื่นไว้ในโฟลเดอร์เดียวกับ app.py หรือในโฟลเดอร์ย่อย")
    st.caption("รองรับ: " + ", ".join(sorted(AUDIO_EXTENSIONS)))
else:
    if "ta101_index" not in st.session_state:
        st.session_state.ta101_index = 0
    if "ta101_shuffle" not in st.session_state:
        st.session_state.ta101_shuffle = False
    if "ta101_repeat" not in st.session_state:
        st.session_state.ta101_repeat = False

    st.session_state.ta101_index = max(0, min(st.session_state.ta101_index, len(songs)-1))

    selected = st.selectbox(
        "เลือกรายชื่อเพลง",
        options=list(range(len(songs))),
        format_func=lambda i: songs[i].stem,
        index=st.session_state.ta101_index,
        key="ta101_song_select",
    )
    st.session_state.ta101_index = selected
    current = songs[selected]

    st.markdown(f"**กำลังเลือกเพลง:** `{current.stem}`")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⏮ ก่อนหน้า", use_container_width=True):
            st.session_state.ta101_index = (selected - 1) % len(songs)
            st.rerun()
    with col2:
        if st.button("🔀 สุ่มเพลง", use_container_width=True):
            st.session_state.ta101_shuffle = not st.session_state.ta101_shuffle
            st.rerun()
    with col3:
        if st.button("🔁 วนซ้ำเพลง", use_container_width=True):
            st.session_state.ta101_repeat = not st.session_state.ta101_repeat
            st.rerun()
    with col4:
        if st.button("⏭ เพลงถัดไป", use_container_width=True):
            if st.session_state.ta101_shuffle and len(songs) > 1:
                choices = [i for i in range(len(songs)) if i != selected]
                st.session_state.ta101_index = random.choice(choices)
            else:
                st.session_state.ta101_index = (selected + 1) % len(songs)
            st.rerun()

    state_a, state_b = st.columns(2)
    with state_a:
        st.caption("🔀 สุ่มเพลง: " + ("เปิด" if st.session_state.ta101_shuffle else "ปิด"))
    with state_b:
        st.caption("🔁 วนซ้ำเพลง: " + ("เปิด" if st.session_state.ta101_repeat else "ปิด"))

    try:
        audio_bytes = current.read_bytes()
        mime = mimetypes.guess_type(current.name)[0] or "audio/mpeg"
        st.audio(
            audio_bytes,
            format=mime,
            loop=st.session_state.ta101_repeat,
            autoplay=False,
        )
        st.caption(f"🎧 {current.name}  •  {len(songs)} เพลงในคลัง")
    except Exception as e:
        st.error(f"เปิดไฟล์เพลงนี้ไม่ได้: {e}")

    with st.expander("📂 รายชื่อเพลงทั้งหมด", expanded=False):
        for i, p in enumerate(songs, start=1):
            st.write(f"{i:02d}. {p.stem}")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    '<div class="small-note">TA101 • MUSIC • DREAM • TOGETHER<br>'
    'คงไฟล์เพลงต้นฉบับและ logo1.jpg ไว้ในโฟลเดอร์เดียวกับ app.py</div>',
    unsafe_allow_html=True,
)   
