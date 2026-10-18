import os
import random
import streamlit as st

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="SYNAPSE - Sound & Visual Therapy",
    page_icon="🎵",
    layout="centered",
)

# ---------------------------------------------------------
# ตกแต่งด้วย CSS แสงสีนีออนตามโทนโลโก้ (ฟ้า, แดงทอง, ม่วง, ดำอวกาศ)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #050b14;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* กล่องครอบโลโก้และหัวข้อพร้อมแสงนีออน */
    .neon-header {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: radial-gradient(circle, rgba(15,23,42,0.9) 0%, rgba(5,11,20,0.95) 100%);
        box-shadow: 0 0 20px rgba(0, 195, 255, 0.3), inset 0 0 15px rgba(147, 51, 234, 0.2);
        border: 1px solid rgba(0, 195, 255, 0.4);
        margin-bottom: 25px;
    }
    
    .neon-title {
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff3333, #00c3ff, #bf00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 10px rgba(0, 195, 255, 0.5);
    }
    
    .neon-subtitle {
        font-size: 14px;
        color: #a5b4fc;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    /* สไตล์เครื่องเล่นและปุ่มควบคุม */
    .stAudio {
        box-shadow: 0 0 15px rgba(0, 195, 255, 0.4);
        border-radius: 10px;
    }
    
    /* ปรับแต่ง Sidebar ให้เข้ากับธีม */
    [data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid rgba(147, 51, 234, 0.3);
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
        <div class="neon-title">SYNAPSE MUSIC THERAPY</div>
        <div class="neon-subtitle">SOUND & VISUAL THERAPY</div>
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
            caption="อยู่นิ่งๆ ไม่เจ็บตัว",
        )
    else:
        st.warning(
            "⚠️ ไม่พบไฟล์ 'logo1.jpg' กรุณานำไฟล์รูปมาไว้ที่โฟลเดอร์เดียวกัน"
        )

# ---------------------------------------------------------
# จำลองการดึงเพลงจากหน้าหลัก.py (หรือไฟล์เพลงในเครื่อง)
# ---------------------------------------------------------
# หมายเหตุ: คุณสามารถปรับเปลี่ยนให้ import ตัวแปรรายชื่อเพลงมาจากหน้าหลัก.py ได้โดยตรง
# เช่น: from หน้าหลัก import music_list
try:
    from หน้าหลัก import music_list  # พยายามดึงจากหน้าหลัก.py
except ImportError:
    # หากยังไม่มีไฟล์ หน้าหลัก.py หรือกำลังทดสอบ จะใช้รายการสำรองนี้แทน
    music_list = {
        "Synapse Healing Wave.mp3": "เพลงที่ 1: คลื่นเสียงบำบัดรักษาความผ่อนคลาย",
        "Deep Space Meditation.mp3": "เพลงที่ 2: ดนตรีสมาธิท่องอวกาศนีออน",
        "Cosmic Energy Recovery.mp3": (
            "เพลงที่ 3: พลังงานจักรวาลฟื้น 1 ฟูร่างกาย"
        ),
    }

# ตรวจสอบว่ามีไฟล์เพลงจริงไหม หรือสร้างรายชื่อจำลองสำหรับการแสดงผล
playlist = list(music_list.keys())

if not playlist:
    st.error("❌ไม่พบรายชื่อเพลงในระบบ กรุณาตรวจสอบไฟล์ หน้าหลัก.py")
    st.stop()

# ---------------------------------------------------------
# ระบบจัดการสถานะ (Session State) สำหรับควบคุมโหมดการเล่น
# ---------------------------------------------------------
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "play_mode" not in st.session_state:
    st.session_state.play_mode = "เล่นต่อเนื่อง (Continuous)"

# ---------------------------------------------------------
# แผงควบคุมด้านข้าง (Sidebar) สำหรับเลือกโหมดเพลง
# ---------------------------------------------------------
st.sidebar.markdown(
    "### 🎛️ ควบคุมโหมดการเล่น",
    help="เลือกรูปแบบการเล่นเพลงที่คุณต้องการ",
)
st.session_state.play_mode = st.sidebar.radio(
    "เลือกรูปแบบ:",
    [
        "เล่นต่อเนื่อง (Continuous)",
        "วนซ้ำทั้งหมด (Loop All)",
        "เล่นซ้ำเพลงเดียว (Repeat One)",
        "สุ่มเพลง (Shuffle)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎶 รายการเพลงทั้งหมด")
selected_song_from_list = st.sidebar.selectbox(
    "เลือกเพลงตรง:",
    playlist,
    format_func=lambda x: music_list.get(x, x),
)

# อัปเดต index ถ้าผู้ใช้เลือกจาก Sidebar
if selected_song_from_list != playlist[st.session_state.current_index]:
    st.session_state.current_index = playlist.index(selected_song_from_list)

# ---------------------------------------------------------
# ส่วนแสดงผลเครื่องเล่นเพลงหลัก
# ---------------------------------------------------------
current_song = playlist[st.session_state.current_index]
song_title = music_list.get(current_song, current_song)

st.markdown(f"### 🎧 กำลังเล่น: **{song_title}**")
st.markdown(
    f"<p style='color: #00c3ff;'>โหมดปัจจุบัน: {st.session_state.play_mode}</p>",
    unsafe_allow_html=True,
)

# ตรวจสอบว่ามีไฟล์เสียงอยู่จริงหรือไม่เพื่อป้องกัน Error
if os.path.exists(current_song):
    st.audio(current_song, format="audio/mp3")
else:
    st.info(
        f"💡 (โหมดจำลอง) ไม่พบไฟล์เสียงจริง `{current_song}` ในเครื่อง แต่ระบบจำลองพร้อมเล่นแล้ว คุณสามารถวางไฟล์ `.mp3` จริงชื่อตรงกันในโฟลเดอร์ได้เลย"
    )

# ---------------------------------------------------------
# ปุ่มควบคุมถัดไป / ก่อนหน้า พร้อมลูกเล่นตามโหมด
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
            pass  /ก
        else:
            st.session_state.current_index = (
                st.session_state.current_index + 1
            ) % len(playlist)
        st.rerun()

# หมายเหตุการเชื่อมต่อกับ หน้าหลัก.py
st.markdown("---")
st.caption(
    "💡 **คำแนะนำเพิ่มเติม:** โค้ดนี้ถูกออกแบบให้ดึงตัวแปร `music_list` มาจากไฟล์ `หน้าหลัก.py` โดยอัตโนมัติ หากใน `หน้าหลัก.py` มีการอัปโหลดเพลงใหม่เข้ามา รายชื่อในเครื่องเล่นนี้ก็จะอัปเดตตามทันทีครับ"
)
