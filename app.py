import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบสถิติและเปรียบเทียบผลสลากกินแบ่งรัฐบาล", page_icon="📊", layout="wide")

st.title("📊 ระบบสถิติและเปรียบเทียบผลสลากกินแบ่งรัฐบาลย้อนหลัง")
st.markdown("ค้นหาข้อมูลย้อนหลัง พร้อมฟังก์ชันเปรียบเทียบสถิติตัวเลข")

# โหลดข้อมูลจากไฟล์ CSV (ดึงข้อมูลย้อนหลังทั้งหมดที่คุณเตรียมไว้)
@st.cache_data
def load_data():
    try:
        # อ่านไฟล์ lottery_data.csv ที่คุณสร้างเพิ่มขึ้นมา
        df = pd.read_csv("lottery_data.csv")
        return df
    except FileNotFoundError:
        # ข้อมูลสำรองกรณีที่ยังไม่ได้สร้างไฟล์ CSV
        data = [
            {"date": "16 กันยายน 2569", "day_month": "วันพุธ เดือนกันยายน", "moon": "แรม 10 ค่ำ เดือน 10", "zodiac_astrology": "ปีจอ / ราศีพฤษภ", "p1": "730640", "front3": "060, 521", "back3": "266, 041", "back2": 64},
            {"date": "1 กันยายน 2569", "day_month": "วันอังคาร เดือนกันยายน", "moon": "แรม 10 ค่ำ เดือน 9 (หลัง)", "zodiac_astrology": "ปีจอ / ราศีสิงห์", "p1": "417212", "front3": "257, 346", "back3": "136, 740", "back2": 4},
            {"date": "16 สิงหาคม 2569", "day_month": "วันอาทิตย์ เดือนสิงหาคม", "moon": "แรม 9 ค่ำ เดือน 9", "zodiac_astrology": "ปีจอ / ราศีสิงห์", "p1": "004615", "front3": "731, 429", "back3": "937, 094", "back2": 53},
        ]
        return pd.DataFrame(data)

df = load_data()

# สร้างเมนูหลัก (Tabs) เพื่อแบ่งระหว่างหน้าค้นหาปกติ กับหน้าเปรียบเทียบสถิติ
tab1, tab2 = st.tabs(["🔍 ค้นหาและคัดลอกข้อมูล", "📈 เปรียบเทียบสถิติและวิเคราะห์"])

with tab1:
    st.subheader("ค้นหาข้อมูลรายงวด")
    search_query = st.text_input("พิมพ์ค้นหา (เช่น วัน, เดือน, ปี หรือเลขท้าย):", "")
    
    if search_query:
        # กรองข้อมูลตามคำค้นหา
        filtered_df = df[df.astype(str).agg(' '.join, axis=1).str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df
        
    st.write(- พบข้อมูลทั้งหมด: {len(filtered_df)} งวด)
    
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### 📌 งวดวันที่: {row['date']}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"• **วัน/เดือน:** {row['day_month']}")
                st.write(f"• **ข้างขึ้น/ข้างแรม:** {row['moon']}")
                st.write(f"• **ปีนักษัตร / ราศี:** {row['zodiac_astrology']}")
                
            with col2:
                st.write(f"• **รางวัลที่ 1:** `{row['p1']}`")
                st.write(f"• **เลขหน้า 3 ตัว:** {row['front3']}")
                st.write(f"• **เลขท้าย 3 ตัว:** {row['back3']}")
                st.write(f"• **เลขท้าย 2 ตัว:** `{row['back2']}`")
                
            format_text = f"""วัน เดือน ปี: {row['date']}
วันอะไร เดือนอะไร: {row['day_month']}
ข้างขึ้นข้างแรม: {row['moon']}
ปีนักบัตร ราศรี: {row['zodiac_astrology']}
ผลหวย: รางวัลที่ 1 ({row['p1']}), เลขท้าย 2 ตัว ({row['back2']})"""
            
            with st.expander("📋 คัดลอกรูปแบบข้อความบันทึก"):
                st.code(format_text, language="text")
            st.markdown("---")

with tab2:
    st.subheader("📊 เปรียบเทียบและวิเคราะห์สถิติตัวเลข")
    
    # แปลงเลขท้าย 2 ตัวให้เป็นตัวเลขเพื่อนำมาจัดอันดับ
    if 'back2' in df.columns:
        df['back2_str'] = df['back2'].astype(str).str.zfill(2)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🏆 สถิติเลขท้าย 2 ตัวที่ออกบ่อยที่สุดในฐานข้อมูล")
            top_back2 = df['back2_str'].value_counts().head(5)
            st.dataframe(top_back2, use_container_width=True)
            
        with col_b:
            st.markdown("#### 📅 เปรียบเทียบตามราศี / ปีนักษัตร")
            if 'zodiac_astrology' in df.columns:
                zodiac_counts = df['zodiac_astrology'].value_counts()
                st.dataframe(zodiac_counts, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 📋 ตารางสรุปข้อมูลดิบทั้งหมด (สามารถใช้เช็กเทียบชนกันได้)")
        st.dataframe(df, use_container_width=True)
        
