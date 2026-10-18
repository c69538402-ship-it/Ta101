import os
import random
import streamlit as st

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="SYNAPSE - Sound & Visual Therapy",
    page_icon="🎧",
    layout="centered",
)

# ---------------------------------------------------------
# ตกแต่งด้วย CSS แสงสีนีออนแพรวพราว กราฟิกคลื่นเสียง และมิกเซอร์
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #050b14 0%, #0d061f 50%, #02060d 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* กล่องหัวข้อเรืองแสงนีออน */
    .neon-header {
        text-align: center;
        padding: 25px;
        border-radius: 20px;
        background: radial-gradient(circle, rgba(15,23,42,0.95) 0%, rgba(5,11,20,0.98) 100%);
        box-shadow: 0 0 30px rgba(0, 195, 255, 0.4), inset 0 0 20px rgba(147, 51, 234, 0.3);
        border: 2px solid rgba(0, 195, 255, 0.6);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .neon-title {
        font-size: 32px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff3333, #00c3ff, #bf00ff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px rgba(0, 195, 255, 0.6);
        letter-spacing: 2px;
    }
    
    .neon-subtitle {
        font-size: 15px;
        color: #a5b4fc;
        letter-spacing: 4px;
        margin-top: 8px;
        text-shadow: 0 0 8px rgba(147, 51, 234, 0.8);
    }

    /* แอนิเมชันกราฟิกคลื่นเสียงพุ่ง (Visualizer Bar) */
    .visualizer-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        height: 55px;
        gap: 6px;
        margin: 20px 0;
        padding: 10px;
        background: rgba(3, 7, 18, 0.7);
        border-radius: 12px;
        border: 1px solid rgba(255, 0, 127, 0.4);
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.2);
    }
    
    .bar {
        width: 8px;
        background: linear-gradient(180deg, #00c3ff, #bf00ff, #ff3333);
        border-radius: 4px;
        animation: pulseBar 1.2s infinite ease-in-out alternate;
    }
    
    .bar:nth-child(1) { height: 30%; animation-delay: 0.1s; }
    .bar:nth-child(2) { height: 70%; animation-delay: 0.3s; }
    .bar:nth-child(3) { height: 95%; animation-delay: 0.2s; }
    .bar:nth-child(4) { height: 50%; animation-delay: 0.5s; }
    .bar:nth-child(5) { height: 85%; animation-delay: 0.15s; }
    .bar:nth-child(6) { height: 100%; animation-delay: 0.4s; }
    .bar:nth-child(7) { height: 60%; animation-delay: 0.25s; }
    .bar:nth-child(8) { height: 80%; animation-delay: 0.35s; }
    .bar:nth-child(9) { height: 40%; animation-delay: 0.05s; }

    @keyframes pulseBar {
        0% { transform: scaleY(0.4); box-shadow: 0 0 5px #00c3ff; }
        100% { transform: scaleY(1.1); box-shadow: 0 0 20px #ff3333; }
    }

    /* กล่องมิกเซอร์และอุปกรณ์จำลอง */
    .mixer-box {
        background: rgba(13, 22, 38, 0.8);
        border: 1px solid rgba(0, 195, 255, 0.3);
        padding: 15px 20px;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 195, 255, 0.2);
        margin-top: 15px;
    }

    .stAudio {
        box-shadow: 0 0 20px rgba(0, 195, 255, 0.5);
        border-radius: 12px;
    }
    
    [data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid rgba(147, 51, 234, 0.4);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# ส่วนหัวและแสดงโลโก้ logo1.jpg
# ---------------------------------------------------------
st.markdown(
    """
    <div class="neon-header">
        <div class="neon-title">⚡ SYNAPSE MUSIC LAB ⚡</div>
        <div class="neon-subtitle">SOUND & VISUAL THERAPY SYSTEM</div>
    </div>
""",
    unsafe_allow_html=True,
)

col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    if os.path.exists("logo1.jpg"):
        st.image(
            "logo1.jpg",
            use_container_width=True,
            caption="✨ อยู่นิ่งๆ ไม่เจ็บตัว ✨",
        )
    else:
        st.warning("⚠️ ไม่พบไฟล์ 'logo1.jpg' ใน GitHub ของคุณ")

# ---------------------------------------------------------
# ดึงรายชื่อเพลง .mp3 อัตโนมัติจาก GitHub
# ---------------------------------------------------------
playlist = [f for f in os.listdir(".") if f.endswith(".mp3")]
playlist.sort()

if not playlist:
    st.error(
        "❌ ไม่พบไฟล์เพลงนามสกุล .mp3 ในโฟลเดอร์ กรุณาตรวจสอบการอัปโหลดไฟล์เพลง"
    )
    st.stop()

# ---------------------------------------------------------
# Session State สำหรับจัดการเพลงและโหมด
# ---------------------------------------------------------
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "play_mode" not in st.session_state:
    st.session_state.play_mode = "เล่นต่อเนื่อง (Continuous)"

# ---------------------------------------------------------
# แผงควบคุมด้านข้าง (Sidebar) แพรวพราวด้วยไอคอน
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ คอนโซลควบคุมเพลง")
st.session_state.play_mode = st.sidebar.radio(
    "เลือกโหมดการเล่น:",
    [
        "เล่นต่อเนื่อง (Continuous)",
        "วนซ้ำทั้งหมด (Loop All)",
        "เล่นซ้ำเพลงเดียว (Repeat One)",
        "สุ่มเพลง (Shuffle)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎧 เพลงทั้งหมดในระบบ")
selected_song = st.sidebar.selectbox(
    "เลือกเพลงจากรายการ:",
    playlist,
    format_func=lambda x: "🎵 " + x.replace(".mp3", ""),
    index=st.session_state.current_index,
)

if selected_song != playlist[st.session_state.current_index]:
    st.session_state.current_index = playlist.index(selected_song)

# ---------------------------------------------------------
# ส่วนแสดงผลเครื่องเล่นเพลง & กราฟิกคลื่นเสียงพุ่ง
# ---------------------------------------------------------
current_song_filename = playlist[st.session_state.current_index]
display_name = current_song_filename.replace(".mp3", "")

st.markdown(
    f"<h3 style='text-align: center; color: #00c3ff;'>🎧 กำลังเล่น: <span style='color: #ff3333;'>{display_name}</span></h3>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; color: #a5b4fc; font-size: 13px;'>โหมด: {st.session_state.play_mode} | แทร็กที่ {st.session_state.current_index + 1} / {len(playlist)}</p>",
    unsafe_allow_html=True,
)

# 📊 กราฟิกคลื่นเสียงพุ่งวิบวับนีออน
st.markdown(
    """
    <div class="visualizer-container">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
""",
    unsafe_allow_html=True,
)

# เล่นไฟล์เสียงผ่าน Streamlit Audio
if os.path.exists(current_song_filename):
    st.audio(current_song_filename, format="audio/mp3")
else:
    st.error(f"❌ ไม่พบไฟล์เสียง: {current_song_filename}")

# ---------------------------------------------------------
# แผงควบคุมมิกเซอร์ (Audio Mixer & Effects)
# ---------------------------------------------------------
st.markdown(
    """
    <div class="mixer-box">
        <h4 style='color: #bf00ff; margin-top: 0;'>🎚️ ดีเจมิกเซอร์ & เอฟเฟกต์เสียง</h4>
    </div>
""",
    unsafe_allow_html=True,
)

col_mix1, col_mix2, col_mix3 = st.columns(3)

with col_mix1:
    volume_level = st.slider("🔊 ระดับความดัง", 0, 100, 80)
with col_mix2:
    pan_sound = st.select_slider(
        "🎛️ แพนเสียง (Pan L/R)",
        options=["ซ้ายสุด (Left)", "ตรงกลาง (Center)", "ขวาสุด (Right)"],
        value="ตรงกลาง (Center)",
    )
with col_mix3:
    bass_boost = st.selectbox(
        "🎧 โหมดหูฟัง/ลำโพง",
        ["ปกติ (Normal)", "เบสแน่น (Bass Boost)", "เสียงใส (Crystal Clear)"],
    )

st.write("")

# ---------------------------------------------------------
# ปุ่มกดควบคุม (ก่อนหน้า, สุ่ม, ถัดไป) ดีไซน์เรืองแสง
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏮️ เพลงก่อนหน้า", use_container_width=True):
        st.session_state.current_index = (
            st.session_state.current_index - 1
        ) % len(playlist)
        st.rerun()

with col2:
    if st.button("🔀 สุ่มเพลงทันที", use_container_width=True):
        st.session_state.current_index = random.randint(0, len(playlist) - 1)
        st.rerun()

with col3:
    if st.button("⏭️ เพลงถัดไป", use_container_width=True):
        if st.session_state.play_mode == "สุ่มเพลง (Shuffle)":
            st.session_state.current_index = random.randint(
                0, len(playlist) - 1
            )
        elif st.session_state.play_mode == "เล่นซ้ำเพลงเดียว (Repeat One)":
            pass  # เล่นเพลงเดิมซ้ำ
        elif st.session_state.play_mode == "วนซ้ำทั้งหมด (Loop All)":
            st.session_state.current_index = (
                st.session_state.current_index + 1
            ) % len(playlist)
        else:  # เล่นต่อเนื่อง
            if st.session_state.current_index < len(playlist) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.current_index = 0
        st.rerun()

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #00c3ff; font-size: 13px;'>✨ SYNAPSE SOUND LAB — อยู่นิ่งๆ ไม่เจ็บตัว พร้อมบรรเลงความสุขให้คุณแล้ว[span_2](start_span)[span_2](end_span)[span_3](start_span)[span_3](end_span) ✨</p>",
    unsafe_allow_html=True,
            )
