import streamlit as st

# ตั้งค่าหน้าเว็บให้เป็นแบบ Wide Mode
st.set_page_config(
    page_title="TA101 NEON HI-FI MUSIC",
    page_icon="🎵",
    layout="wide"
)

# ส่วนตกแต่ง CSS สำหรับธีมนีออน Sci-Fi
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1b0a3f 0%, #05020d 100%);
        color: #ffffff;
    }
    .neon-box {
        background: rgba(10, 5, 30, 0.75);
        border: 2px solid rgba(0, 243, 255, 0.4);
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 15px rgba(189, 0, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 20px;
        margin-bottom: 20px;
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
    /*ซ่อน Streamlit Header และ Footer เดิมเพื่อความสวยงาม*/
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- ส่วนหัว (Header) ---
col_head1, col_head2, col_head3 = st.columns([1, 2, 1])

with col_head1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="background: rgba(0, 255, 0, 0.2); border: 1px solid rgba(0, 255, 0, 0.5); color: #00ff00; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                ● LIVE MUSIC
            </span>
        </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; color: #00f3ff; text-shadow: 0 0 10px rgba(0, 243, 255, 0.6);">
                TA101 <span style="color: #ff007f; text-shadow: 0 0 10px rgba(255, 0, 127, 0.6);">NEON HI-FI</span>
            </h1>
            <p style="margin: 0; font-size: 10px; letter-spacing: 2px; color: #d8b4fe;">MUSIC • DREAM • TOGETHER</p>
        </div>
    """, unsafe_allow_html=True)

with col_head3:
    st.markdown("""
        <div style="text-align: right;">
            <span style="background: rgba(0, 243, 255, 0.2); border: 1px solid #00f3ff; color: #00f3ff; padding: 6px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                🎵 Now Playing
            </span>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- ส่วนเนื้อหาหลัก (Main Dashboard) ---
col_left, col_mid, col_right = st.columns([4, 5, 3])

# ซ้าย: แสดงโลโก้ logo1.jpg
with col_left:
    st.markdown('<div class="neon-box" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h3 class="neon-text-cyan" style="font-size: 1.1rem; margin-bottom: 10px;">LOGO DISPLAY</h3>', unsafe_allow_html=True)
    
    try:
        # พยายามโหลดไฟล์รูปภาพ logo1.jpg ที่อยู่ในโฟลเดอร์เดียวกัน
        st.image("logo1.jpg", caption="TA101 Logo", use_container_width=True)
    except Exception:
        # กรณีที่ยังหาไฟล์ไม่พบ ให้แจ้งเตือนคำแนะนำ
        st.warning("⚠️ ยังไม่พบไฟล์รูปภาพชื่อ `logo1.jpg` ในโฟลเดอร์โปรเจกต์ กรุณาอัปโหลดไฟล์ `logo1.jpg` ไว้ที่เดียวกับ `app.py` บน GitHub ครับ")
        
    st.markdown('</div>', unsafe_allow_html=True)

# กลาง: เครื่องเล่นเพลง / ควบคุม / คลื่นเสียงจำลอง
with col_mid:
    # กล่องชื่อเพลงและเวลา
    st.markdown("""
        <div class="neon-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div>
                    <h4 style="margin: 0; color: #fff; font-size: 1rem;">🎧 ใส่ใจในเรื่องของ</h4>
                    <p style="margin: 0; font-size: 0.8rem; color: #00f3ff;">TA101</p>
                </div>
                <span style="font-family: monospace; font-size: 0.8rem; color: #ccc;">01:32 / 04:12</span>
            </div>
            <div style="background: #111; height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: linear-gradient(to right, #00f3ff, #ff007f); width: 35%; height: 100%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # จำลองปุ่มควบคุมการเล่นเพลงด้วย Streamlit Columns
    c_btn1, c_btn2, c_btn3, c_btn4, c_btn5 = st.columns(5)
    with c_btn1:
        st.button("🔀", use_container_width=True)
    with c_btn2:
        st.button("⏮️", use_container_width=True)
    with c_btn3:
        st.button("⏸️", use_container_width=True)
    with c_btn4:
        st.button("⏭️", use_container_width=True)
    with c_btn5:
        st.button("🔁", use_container_width=True)

# ขวา: Playlist
with col_right:
    st.markdown("""
        <div class="neon-box">
            <h4 class="neon-text-cyan" style="font-size: 1rem; margin-top: 0; border-bottom: 1px solid rgba(0,243,255,0.3); padding-bottom: 8px;">
                📑 Playlist
            </h4>
            <div style="background: rgba(0,243,255,0.1); border: 1px solid rgba(0,243,255,0.4); padding: 8px; border-radius: 8px; margin-bottom: 8px; font-size: 0.9px; color: #00f3ff;">
                ▶ 1. ใส่ใจในเรื่องของ
            </div>
            <div style="padding: 8px; font-size: 0.9rem; color: #ccc;">
                2. ทางของรอยยิ้ม
            </div>
            <div style="padding: 8px; font-size: 0.9rem; color: #ccc;">
                3. 4.mp3
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ส่วนล่าง: ปรับแต่งเสียง (Equalizer & Volume) ---
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    st.markdown("""
        <div class="neon-box" style="padding: 15px;">
            <p class="neon-text-cyan" style="margin: 0 0 10px 0; font-size: 0.9rem; font-weight: bold;">🎛️ Equalizer Panel</p>
        </div>
    """, unsafe_allow_html=True)
    eq1, eq2, eq3 = st.columns(3)
    with eq1:
        st.slider("Bass (+6 dB)", 0, 12, 6)
    with eq2:
        st.slider("Treble (+4 dB)", 0, 12, 4)
    with eq3:
        st.slider("Volume", 0, 100, 75)

with col_bot2:
    st.markdown("""
        <div class="neon-box" style="padding: 15px; text-align: center;">
            <p class="neon-text-pink" style="margin: 0 0 10px 0; font-size: 0.9rem; font-weight: bold;">✨ STATUS SYSTEM</p>
            <p style="margin: 0; font-size: 0.8rem; color: #d8b4fe;">System Connected • Neon Hi-Fi Audio Engine Active</p>
        </div>
    """, unsafe_allow_html=True)
    
