import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบสถิติและเปรียบเทียบผลสลากกินแบ่งรัฐบาลย้อนหลัง", page_icon="📊", layout="wide")

st.title("📊 ระบบสถิติและเปรียบเทียบผลสลากกินแบ่งรัฐบาลย้อนหลัง")
st.markdown("ค้นหาข้อมูลสถิติย้อนหลัง พร้อมฟังก์ชันเปรียบเทียบตัวเลขและจัดเก็บข้อมูล")

# โหลดข้อมูลจากไฟล์ lottery_data.csv
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("lottery_data.csv", dtype=str)
        return df
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ lottery_data.csv กรุณาสร้างไฟล์ข้อมูลบน GitHub ก่อนครับ")
        return pd.DataFrame()

df = load_data()

# สร้างเมนูหลัก (Tabs) ระหว่างหน้าค้นหา กับ หน้าเปรียบเทียบสถิติ
tab1, tab2 = st.tabs(["🔍 ค้นหาและดูย้อนหลัง", "📈 เปรียบเทียบสถิติและวิเคราะห์"])

with tab1:
    st.subheader("ค้นหาข้อมูลสถิติย้อนหลัง")
    search_query = st.text_input("พิมพ์ค้นหา (เช่น ปี 2568, เดือนกันยายน, หรือเลขท้าย):", "")
    
    if search_query and not df.empty:
        def search_row(row):
            return search_query.lower() in " ".join(row.astype(str).values).lower()
        filtered_df = df[df.apply(search_row, axis=1)]
    else:
        filtered_df = df
        
    st.write(f"• พบข้อมูลทั้งหมด: {len(filtered_df)} งวด")
    
    if not filtered_df.empty:
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
                
                with st.expander("📋 คัดลอกรูปแบบข้อความไปบันทึก"):
                    st.code(format_text, language="text")
                st.markdown("---")

with tab2:
    st.subheader("📊 เปรียบเทียบและวิเคราะห์สถิติตัวเลข")
    
    if not df.empty and 'back2' in df.columns:
        df['back2_str'] = df['back2'].astype(str).str.zfill(2)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### 🏆 สถิติเลขท้าย 2 ตัวในฐานข้อมูลย้อนหลัง")
            top_back2 = df['back2_str'].value_counts().head(5)
            st.dataframe(top_back2, use_container_width=True)
            
        with col_b:
            st.markdown("#### 📅 เปรียบเทียบตามราศี / ปีนักษัตร")
            if 'zodiac_astrology' in df.columns:
                zodiac_counts = df['zodiac_astrology'].value_counts()
                st.dataframe(zodiac_counts, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 📋 ตารางสรุปข้อมูลย้อนหลังทั้งหมด")
        st.dataframe(df, use_container_width=True)
        
