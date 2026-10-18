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

    .stAudio {
        box-shadow: 0 0 15px rgba(0, 195, 255, 0.4);
        border-radius: 10px;
    }
    
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
            "⚠️ ไม่พบไฟล์ 'logo1.jpg' กรุณาตรวจสอบชื่อไฟล์ใน GitHub อีกครั้ง"
        )

# ---------------------------------------------------------
# ดึงรายชื่อไฟล์เพลง .mp3 จากโฟลเดอร์ปัจจุบันโดยอัตโนมัติ
# ---------------------------------------------------------
playlist = [f for f in os.listdir(".") if f.endswith(".mp3")]
playlist.sort()  # เรียงลำดับชื่อเพลงตามตัวอักษร

if not playlist:
    st.error(
        "❌ ไม่พบไฟล์เพลงนามสกุล .mp3 ในโฟลเดอร์ กรุณาอัปโหลดเพลงเข้ามาเพิ่ม"
    )
    st.stop()

# ---------------------------------------------------------
# ระบบจัดการสถานะ (Session State)
# ---------------------------------------------------------
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "play_mode" not in st.session_state:
    st.session_state.play_mode = "เล่นต่อเนื่อง (Continuous)"

# ---------------------------------------------------------
# เมนูด้านข้าง (Sidebar) สำหรับเลือกโหมดและเลือกเพลง
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ ควบคุมโหมดการเล่น")
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
st.sidebar.markdown("### 🎶 รายการเพลงทั้งหมดในระบบ")

# เลือกเพลงจากรายชื่อใน Sidebar (ตัดนามสกุล .mp3 ออกเพื่อให้แสดงผลสวยงาม)
selected_song = st.sidebar.selectbox(
    "เลือกเพลง:",
    playlist,
    format_func=lambda x: x.replace(".mp3", ""),
    index=st.session_state.current_index,
)

# อัปเดต index ทันทีถ้าผู้ใช้กดเลือกจาก Sidebar
if selected_song != playlist[st.session_state.current_index]:
    st.session_state.current_index = playlist.index(selected_song)

# ---------------------------------------------------------
# ส่วนแสดงผลเครื่องเล่นเพลงหลัก
# ---------------------------------------------------------
current_song_filename = playlist[st.session_state.current_index]
display_name = current_song_filename.replace(".mp3", "")

st.markdown(f"### 🎧 กำลังเล่น: **{display_name}**")
st.markdown(
    f"<p style='color: #00c3ff;'>โหมดปัจจุบัน: {st.session_state.play_mode} | เพลงที่ {st.session_state.current_index + 1} จาก {len(playlist)}</p>",
    unsafe_allow_html=True,
)

# เล่นไฟล์เสียงผ่าน Streamlit Audio
if os.path.exists(current_song_filename):
    st.audio(current_song_filename, format="audio/mp3")
else:
    st.error(f"❌ ไม่พบไฟล์เสียง: {current_song_filename}")

# ---------------------------------------------------------
# ปุ่มควบคุม (ก่อนหน้า, สุ่ม, ถัดไป)
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
            pass  # เล่นเพลงเดิมซ้ำ ไม่เปลี่ยน index
        elif st.session_state.play_mode == "วนซ้ำทั้งหมด (Loop All)":
            st.session_state.current_index = (
                st.session_state.current_index + 1
            ) % len(playlist)
        else:  # เล่นต่อเนื่อง (หยุดเมื่อหมดลิสต์ หรือวนกลับ)
            if st.session_state.current_index < len(playlist) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.current_index = (
                    0  # วนกลับเพลงแรกถ้าจบเพลย์ลิสต์
                )
        st.rerun()

st.markdown("---")
st.caption(
    "💡 โค้ดนี้ดึงไฟล์ `.mp3` และรูป `logo1.jpg` จากโฟลเดอร์หลักใน GitHub ของคุณมาแสดงผลและเล่นเพลงแบบอัตโนมัติเรียบร้อยแล้วครับ"
    )
