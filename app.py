import streamlit as st

# ตั้งค่าหน้าเว็บแบบ Wide Mode
st.set_page_config(
    page_title="TA101 NEON HI-FI MUSIC",
    page_icon="🎵",
    layout="wide"
)

# โค้ด CSS ตกแต่งหน้าตาให้เป็นธีมนีออน Sci-Fi ตามรูปเป๊ะ ๆ
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Prompt:wght@300;400;600&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #1b0a3f 0%, #05020d 100%);
        font-family: 'Prompt', 'Orbitron', sans-serif;
        color: #fff;
    }
    
    /* กล่องกรอบนีออนกระจกแก้ว */
    .neon-box {
        background: rgba(10, 5, 30, 0.75);
        border: 2px solid rgba(0, 243, 255, 0.4);
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 15px rgba(189, 0, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 15px;
        margin-bottom: 15px;
    }

    .neon-text-cyan {
        color: #00f3ff;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.6);
        font-family: 'Orbitron', sans-serif;
    }

    .neon-text-pink {
        color: #ff007f;
        text-shadow: 0 0 10px rgba(255, 0, 127, 0.6);
        font-family: 'Orbitron', sans-serif;
    }

    /* ซ่อนแถบเมนู Streamlit ด้านบนและ Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ปรับแต่งปุ่มกดใน Streamlit ให้เข้ากับธีม */
    .stButton>button {
        background: linear-gradient(135deg, rgba(0,243,255,0.2), rgba(255,0,127,0.2));
        border: 1px solid #00f3ff;
        color: #00f3ff;
        border-radius: 50px;
        box-shadow: 0 0 10px rgba(0,243,255,0.3);
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(0,243,255,0.5), rgba(255,0,127,0.5));
        color: #fff;
        border-color: #ff007f;
        box-shadow: 0 0 20px rgba(255,0,127,0.8);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลเพลย์ลิสต์ (ดึงเพลงมาเปิดต่อเนื่อง)
# ==========================================
playlist = [
    {"title": "ใส่ใจในเรื่องของ", "artist": "TA101", "file": "song1.mp3"},
    {"title": "ทางของรอยยิ้ม", "artist": "TA101", "file": "song2.mp3"},
    {"title": "4.mp3", "artist": "TA101", "file": "song3.mp3"}
]

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

current_song = playlist[st.session_state.current_index]

# ==========================================
# 2. ส่วนหัวแอป (Header)
# ==========================================
col_h1, col_h2, col_h3 = st.columns([1, 2, 1])

with col_h1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding-top: 10px;">
            <span style="background: rgba(0, 255, 0, 0.2); border: 1px solid rgba(0, 255, 0, 0.5); color: #00ff00; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                ● LIVE MUSIC
            </span>
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; color: #00f3ff; text-shadow: 0 0 15px rgba(0, 243, 255, 0.8); font-family: 'Orbitron';">
                TA101 <span style="color: #ff007f; text-shadow: 0 0 15px rgba(255, 0, 127, 0.8);">NEON HI-FI</span>
            </h1>
            <p style="margin: 0; font-size: 11px; letter-spacing: 3px; color: #d8b4fe; font-family: 'Orbitron';">MUSIC • DREAM • TOGETHER</p>
        </div>
    """, unsafe_allow_html=True)

with col_h3:
    st.markdown("""
        <div style="text-align: right; padding-top: 10px;">
            <span style="background: rgba(0, 243, 255, 0.2); border: 1px solid #00f3ff; color: #00f3ff; padding: 8px 18px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                🎵 Now Playing
            </span>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# ==========================================
# 3. ส่วนเนื้อหาหลัก (Dashboard 3 คอลัมน์ตามรูป)
# ==========================================
col_left, col_mid, col_right = st.columns([3, 5, 3])

# -- คอลัมน์ซ้าย: วงกลมโลโก้ (ดึง logo1.jpg มาแสดง) --
with col_left:
    st.markdown('<div class="neon-box" style="text-align: center; padding: 20px;">', unsafe_allow_html=True)
    st.markdown('<h3 class="neon-text-cyan" style="font-size: 1rem; margin-bottom: 10px;">NEON HIFI SYSTEM</h3>', unsafe_allow_html=True)
    
    try:
        # แสดงรูป logo1.jpg ที่อัปโหลดเข้ามา
        st.image("logo1.jpg", use_container_width=True)
    except Exception:
        st.warning("⚠️ กรุณาอัปโหลดไฟล์รูปภาพชื่อ `logo1.jpg` ไว้ใน GitHub โฟลเดอร์เดียวกับ `app.py`")
        
    st.markdown('</div>', unsafe_allow_html=True)

# -- คอลัมน์กลาง: แผงควบคุมเพลง + หลอดเวลา + เครื่องเล่นเสียง --
with col_mid:
    # กรอบแสดงชื่อเพลงและแถบเวลา
    st.markdown(f"""
        <div class="neon-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <h4 style="margin: 0; color: #fff; font-size: 1.1rem;">🎧 {current_song['title']}</h4>
                    <p style="margin: 0; font-size: 0.85rem; color: #00f3ff;">{current_song['artist']}</p>
                </div>
                <span style="font-family: monospace; font-size: 0.8rem; color: #00f3ff;">01:32 / 04:12</span>
            </div>
            <div style="background: rgba(0,0,0,0.5); height: 8px; border-radius: 4px; overflow: hidden; border: 1px solid rgba(0,243,255,0.3);">
                <div style="background: linear-gradient(to right, #00f3ff, #ff007f); width: 35%; height: 100%; box-shadow: 0 0 10px #00f3ff;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # จำลองแผง Equalizer Visualizer ขยับเป็นแท่งนีออน
    st.markdown("""
        <div class="neon-box" style="display: flex; justify-content: space-between; align-items: flex-end; height: 90px; padding: 10px 15px;">
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 40%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 70%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 50%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 90%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 60%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 80%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 45%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 85%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 55%; border-radius: 3px;"></div>
            <div style="width: 6%; background: linear-gradient(to top, #ff007f, #00f3ff); height: 75%; border-radius: 3px;"></div>
        </div>
    """, unsafe_allow_html=True)

    # 🔊 ตัวเล่นเสียงจริง (Streamlit Audio เล่นเพลงต่อเนื่อง)
    try:
        st.audio(current_song['file'], format="audio/mp3", autoplay=True)
    except Exception:
        st.info(f"💡 คำแนะนำ: นำไฟล์เพลง `.mp3` ชื่อ `{current_song['file']}` มาใส่ไว้ใน GitHub เพื่อให้เล่นเพลงจริงได้ครับ")

    # ปุ่มควบคุมมัลติมีเดีย (Shuffle, Prev, Pause/Play, Next, Repeat)
    c_btn1, c_btn2, c_btn3, c_btn4, c_btn5 = st.columns(5)
    with c_btn1:
        st.button("🔀", use_container_width=True)
    with c_btn2:
        if st.button("⏮️", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index - 1) % len(playlist)
            st.rerun()
    with c_btn3:
        st.button("⏸️", use_container_width=True)
    with c_btn4:
        if st.button("⏭️", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(playlist)
            st.rerun()
    with c_btn5:
        st.button("🔁", use_container_width=True)

# -- คอลัมน์ขวา: Playlist กดเลือกเพลง --
with col_right:
    st.markdown("""
        <div class="neon-box">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,243,255,0.3); padding-bottom: 8px; margin-bottom: 10px;">
                <span class="neon-text-cyan" style="font-weight: bold; font-size: 0.95rem;">📑 Playlist</span>
                <span style="font-size: 0.8rem; color: #00f3ff;">🔀 🔁</span>
            </div>
    """, unsafe_allow_html=True)

    # สร้างปุ่มเลือกเพลงใน Playlist
    for idx, song in enumerate(playlist):
        is_active = (idx == st.session_state.current_index)
        label = f"▶ {song['title']}" if is_active else f"{idx+1}. {song['title']}"
        if st.button(label, key=f"pl_{idx}", use_container_width=True):
            st.session_state.current_index = idx
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. ส่วนล่าง: Equalizer Sliders & Volume ควบคุมเสียง
# ==========================================
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    st.markdown("""
        <div class="neon-box" style="padding: 12px 15px;">
            <p class="neon-text-cyan" style="margin: 0 0 8px 0; font-size: 0.85rem; font-weight: bold;">🎛️ Frequency Equalizer</p>
        </div>
    """, unsafe_allow_html=True)
    eq_1, eq_2, eq_3, eq_4 = st.columns(4)
    with eq_1:
        st.slider("60Hz", 0, 100, 60, label_visibility="collapsed")
        st.caption("60")
    with eq_2:
        st.slider("310Hz", 0, 100, 50, label_visibility="collapsed")
        st.caption("310")
    with eq_3:
        st.slider("1K", 0, 100, 75, label_visibility="collapsed")
        st.caption("1K")
    with eq_4:
        st.slider("16K", 0, 100, 65, label_visibility="collapsed")
        st.caption("16K")

with col_bot2:
    st.markdown("""
        <div class="neon-box" style="padding: 12px 15px;">
            <p class="neon-text-pink" style="margin: 0 0 8px 0; font-size: 0.85rem; font-weight: bold;">🔊 Audio Output Control</p>
        </div>
    """, unsafe_allow_html=True)
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        st.slider("Bass", 0, 12, 6)
        st.caption("+6 dB")
    with v_col2:
        st.slider("Treble", 0, 12, 4)
        st.caption("+4 dB")
    with v_col3:
        st.slider("Volume", 0, 100, 75)
        st.caption("75%")
        
