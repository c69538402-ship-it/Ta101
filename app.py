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
# ตกแต่งด้วย CSS แสงสีนีออนกระแทกตา ตัวหนังสือวิ่ง และคลื่นเสียงเด้งแรง
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0d061f 50%, #050b14 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* กล่องหัวข้อเรืองแสงนีออน */
    .neon-header {
        text-align: center;
        padding: 25px;
        border-radius: 20px;
        background: radial-gradient(circle, rgba(15,23,42,0.95) 0%, rgba(5,11,20,0.98) 100%);
        box-shadow: 0 0 35px rgba(0, 195, 255, 0.5), inset 0 0 20px rgba(255, 0, 127, 0.4);
        border: 2px solid rgba(0, 195, 255, 0.7);
        margin-bottom: 20px;
    }
    
    .neon-title {
        font-size: 32px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff3333, #00c3ff, #bf00ff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 195, 255, 0.8);
        letter-spacing: 2px;
    }
    
    .neon-subtitle {
        font-size: 14px;
        color: #a5b4fc;
        letter-spacing: 4px;
        margin-top: 8px;
        text-shadow: 0 0 10px rgba(147, 51, 234, 0.9);
    }

    /* ตัวหนังสือวิ่ง (Marquee Text) สไตล์ป้ายไฟนีออน */
    .marquee-container {
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 0, 127, 0.5);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.3);
    }

    .marquee-text {
        display: inline-block;
        animation: marquee 10s linear infinite;
        font-size: 18px;
        font-weight: bold;
        color: #00c3ff;
        text-shadow: 0 0 10px #00c3ff;
    }

    @keyframes marquee {
        0% { transform: translate(100%, 0); }
        100% { transform: translate(-100%, 0); }
    }

    /* กราฟิกคลื่นเสียงกระแทกเด่งแรงๆ (Bass Drop Visualizer) */
    .visualizer-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        height: 70px;
        gap: 8px;
        margin: 20px 0;
        padding: 12px;
        background: rgba(3, 7, 18, 0.85);
        border-radius: 15px;
        border: 2px solid rgba(0, 195, 255, 0.5);
        box-shadow: 0 0 25px rgba(0, 195, 255, 0.4);
    }
    
    .bar {
        width: 10px;
        background: linear-gradient(180deg, #ff007f, #00c3ff, #bf00ff, #ff3333);
        border-radius: 6px;
        animation: heavyBounce 0.6s infinite ease-in-out alternate;
    }
    
    .bar:nth-child(1) { height: 40%; animation-delay: 0.1s; }
    .bar:nth-child(2) { height: 90%; animation-delay: 0.3s; }
    .bar:nth-child(3) { height: 100%; animation-delay: 0.05s; }
    .bar:nth-child(4) { height: 60%; animation-delay: 0.4s; }
    .bar:nth-child(5) { height: 95%; animation-delay: 0.2s; }
    .bar:nth-child(6) { height: 75%; animation-delay: 0.35s; }
    .bar:nth-child(7) { height: 100%; animation-delay: 0.15s; }
    .bar:nth-child(8) { height: 50%; animation-delay: 0.25s; }
    .bar:nth-child(9) { height: 85%; animation-delay: 0.45s; }

    @keyframes heavyBounce {
        0% { transform: scaleY(0.2); box-shadow: 0 0 5px #00c3ff; }
        100% { transform: scaleY(1.35); box-shadow: 0 0 25px #ff007f, 0 0 10px #ff3333; }
    }

    /* กล่องลำโพงทรงพลังเรืองแสง */
    .speaker-box {
        text-align: center;
        padding: 12px;
        background: radial-gradient(circle, rgba(147, 51, 234, 0.2) 0%, rgba(5, 11, 20, 0.8) 100%);
        border: 1px dashed rgba(147, 51, 234, 0.6);
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(147, 51, 234, 0.3);
    }

    .stAudio {
        box-shadow: 0 0 25px rgba(0, 195, 255, 0.6);
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
        <div class="neon-title">⚡ SYNAPSE SOUND LAB ⚡</div>
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
        st.warning("⚠️ ไม่พบไฟล์ 'logo1.jpg' ในระบบของคุณ")

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
# เมนูด้านข้าง (Sidebar)
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
st.sidebar.markdown("### 🎶 เพลงทั้งหมดในระบบ")
selected_song = st.sidebar.selectbox(
    "เลือกเพลงจากรายการ:",
    playlist,
    format_func=lambda x: "🎵 " + x.replace(".mp3", ""),
    index=st.session_state.current_index,
)

if selected_song != playlist[st.session_state.current_index]:
    st.session_state.current_index = playlist.index(selected_song)

# ---------------------------------------------------------
# ส่วนแสดงผลเครื่องเล่นเพลง & ลูกเล่นตัวหนังสือวิ่ง
# ---------------------------------------------------------
current_song_filename = playlist[st.session_state.current_index]
display_name = current_song_filename.replace(".mp3", "")

# แสดงตัวหนังสือวิ่งนีออน
st.markdown(
    f"""
    <div class="marquee-container">
        <div class="marquee-text">🔊 กำลังบรรเลงแท็กพิเศษ: {display_name} — (โหมด: {st.session_state.play_mode}) — อยู่นิ่งๆ ไม่เจ็บตัว 🎶</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 🔊 รูปลำโพงทรงพลังเรืองแสง
st.markdown(
    """
    <div class="speaker-box">
        <span style="font-size: 26px;">🔊 🎧 ⚡</span>
        <div style="color: #ff3333; font-weight: bold; font-size: 15px; margin-top: 5px;">SUBWOOFER NEON SYSTEM ACTIVE</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 📊 กราฟิกคลื่นเสียงกระแทกเด้งแรงๆ (Bass Drop Visualizer)
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
# แผงมิกเซอร์ควบคุมเสียง Fade In / Fade Out & Volume
# ---------------------------------------------------------
st.markdown("---")
col_mix1, col_mix2 = st.columns(2)

with col_mix1:
    volume_level = st.slider(
        "🎚️ ระดับความดังหลัก (Master Volume)", 0, 100, 85
    )
with col_mix2:
    fade_effect = st.selectbox(
        "🎛️ ลูกเล่นความดัง (Fade Effect)",
        [
            "ปกติ (Normal)",
            "ค่อยๆ ดังขึ้น (Fade In)",
            "ค่อยๆ เบาลงตอนจบ (Fade Out)",
            "ไดนามิกบีทกระแทก (Dynamic Boost)",
        ],
    )

st.write("")

# ---------------------------------------------------------
# ปุ่มกดควบคุม (ก่อนหน้า, สุ่ม, ถัดไป)
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
    "<p style='text-align: center; color: #00c3ff; font-size: 13px;'>✨ SYNAPSE SOUND LAB — อยู่นิ่งๆ ไม่เจ็บตัว พร้อมระเบิดความมันส์แล้ว ✨</p>",
    unsafe_allow_html=True,
)
