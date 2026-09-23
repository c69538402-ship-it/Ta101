import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบสถิติและเปรียบเทียบผลสลากกินแบ่งรัฐบาลย้อนหลัง", page_icon="📊", layout="wide")

st.title("📊 ระบบสถิติและเปรียบเทียบผลสลากกินแบ่งรัฐบาลย้อนหลัง")
st.markdown("รวมข้อมูลสถิติหวยย้อนหลัง พร้อมฟังก์ชันค้นหาและเปรียบเทียบตัวเลข")

# ฐานข้อมูลสถิติหวยย้อนหลัง (มีข้อมูลจำลองย้อนหลังให้คุณกดดูได้ทันที)
@st.cache_data
def load_data():
    data = [
        # ปี 2569
        {"date": "16 กันยายน 2569", "day_month": "วันพุธ เดือนกันยายน", "moon": "แรม 10 ค่ำ เดือน 10", "zodiac_astrology": "ปีจอ / ราศีพฤษภ", "p1": "730640", "front3": "060, 521", "back3": "266, 041", "back2": "64"},
        {"date": "1 กันยายน 2569", "day_month": "วันอังคาร เดือนกันยายน", "moon": "แรม 10 ค่ำ เดือน 9 (หลัง)", "zodiac_astrology": "ปีจอ / ราศีสิงห์", "p1": "417212", "front3": "257, 346", "back3": "136, 740", "back2": "04"},
        {"date": "16 สิงหาคม 2569", "day_month": "วันอาทิตย์ เดือนสิงหาคม", "moon": "แรม 9 ค่ำ เดือน 9", "zodiac_astrology": "ปีจอ / ราศีสิงห์", "p1": "004615", "front3": "731, 429", "back3": "937, 094", "back2": "53"},
        {"date": "1 สิงหาคม 2569", "day_month": "วันเสาร์ เดือนสิงหาคม", "moon": "แรม 13 ค่ำ เดือน 8", "zodiac_astrology": "ปีจอ / ราศีกรกฎ", "p1": "932479", "front3": "413, 672", "back3": "154, 039", "back2": "69"},
        {"date": "16 กรกฎาคม 2569", "day_month": "วันพฤหัสบดี เดือนกรกฎาคม", "moon": "แรม 2 ค่ำ เดือน 8", "zodiac_astrology": "ปีจอ / ราศีเมถุน", "p1": "639214", "front3": "683, 709", "back3": "746, 427", "back2": "71"},
        {"date": "1 กรกฎาคม 2569", "day_month": "วันพุธ เดือนกรกฎาคม", "moon": "แรม 2 ค่ำ เดือน 7", "zodiac_astrology": "ปีจอ / ราศีเมถุน", "p1": "751495", "front3": "001, 980", "back3": "304, 531", "back2": "62"},
        {"date": "16 มิถุนายน 2569", "day_month": "วันอังคาร เดือนมิถุนายน", "moon": "แรม 2 ค่ำ เดือน 7", "zodiac_astrology": "ปีจอ / ราศีเมถุน", "p1": "287184", "front3": "758, 434", "back3": "007, 721", "back2": "48"},
        {"date": "1 มิถุนายน 2569", "day_month": "วันจันทร์ เดือนมิถุนายน", "moon": "แรม 1 ค่ำ เดือน 6", "zodiac_astrology": "ปีจอ / ราศีพฤษภ", "p1": "173770", "front3": "848, 415", "back3": "410, 938", "back2": "95"},
        
        # ปี 2568 (ตัวอย่างย้อนหลัง)
        {"date": "30 ธันวาคม 2568", "day_month": "วันอังคาร เดือนธันวาคม", "moon": "ขึ้น 11 ค่ำ เดือน 2", "zodiac_astrology": "ปีระกา / ราศีธนู", "p1": "625520", "front3": "351, 882", "back3": "146, 858", "back2": "80"},
        {"date": "16 ธันวาคม 2568", "day_month": "วันอังคาร เดือนธันวาคม", "moon": "แรม 12 ค่ำ เดือน 1", "zodiac_astrology": "ปีระกา / ราศีธนู", "p1": "435116", "front3": "321, 608", "back3": "530, 241", "back2": "47"},
        {"date": "1 ธันวาคม 2568", "day_month": "วันจันทร์ เดือนธันวาคม", "moon": "แรม 12 ค่ำ เดือน 12", "zodiac_astrology": "ปีระกา / ราศีพิจิก", "p1": "251547", "front3": "303, 317", "back3": "384, 915", "back2": "97"},
        {"date": "16 พฤศจิกายน 2568", "day_month": "วันอาทิตย์ เดือนพฤศจิกายน", "moon": "แรม 12 ค่ำ เดือน 12", "zodiac_astrology": "ปีระกา / ราศีพิจิก", "p1": "596164", "front3": "402, 497", "back3": "216, 735", "back2": "64"},
        {"date": "1 พฤศจิกายน 2568", "day_month": "วันเสาร์ เดือนพฤศจิกายน", "moon": "แรม 11 ค่ำ เดือน 11", "zodiac_astrology": "ปีระกา / ราศีพิจิก", "p1": "972163", "front3": "105, 782", "back3": "058, 291", "back2": "63"},
        {"date": "16 ตุลาคม 2568", "day_month": "วันพฤหัสบดี เดือนตุลาคม", "moon": "แรม 10 ค่ำ เดือน 11", "zodiac_astrology": "ปีระกา / ราศีตุลย์", "p1": "481312", "front3": "241, 638", "back3": "456, 981", "back2": "12"},
        {"date": "1 ตุลาคม 2568", "day_month": "วันพุธ เดือนตุลาคม", "moon": "แรม 9 ค่ำ เดือน 10", "zodiac_astrology": "ปีระกา / ราศีกันย์", "p1": "727376", "front3": "129, 390", "back3": "014, 532", "back2": "76"},
        {"date": "16 กันยายน 2568", "day_month": "วันอังคาร เดือนกันยายน", "moon": "แรม 9 ค่ำ เดือน 10", "zodiac_astrology": "ปีระกา / ราศีกันย์", "p1": "356541", "front3": "114, 892", "back3": "302, 755", "back2": "41"},
    ]
    return pd.DataFrame(data)

df = load_data()

# สร้างเมนูหลัก (Tabs) ระหว่างหน้าค้นหา กับ หน้าเปรียบเทียบสถิติ
tab1, tab2 = st.tabs(["🔍 ค้นหาและดูย้อนหลัง", "📈 เปรียบเทียบสถิติและวิเคราะห์"])

with tab1:
    st.subheader("ค้นหาข้อมูลสถิติย้อนหลัง")
    search_query = st.text_input("พิมพ์ค้นหา (เช่น ปี 2568, เดือนกันยายน, หรือเลขท้าย):", "")
    
    if search_query:
        def search_row(row):
            return search_query.lower() in " ".join(row.astype(str).values).lower()
        filtered_df = df[df.apply(search_row, axis=1)]
    else:
        filtered_df = df
        
    st.write(f"• พบข้อมูลทั้งหมด: {len(filtered_df)} งวด")
    
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
    
    if 'back2' in df.columns:
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
            
