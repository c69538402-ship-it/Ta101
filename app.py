import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="บันทึกผลสลากกินแบ่งรัฐบาลย้อนหลัง", page_icon="🔢", layout="wide")

# ข้อมูลตัวอย่างสถิติหวยย้อนหลัง (คุณสามารถเพิ่มข้อมูลลงใน List นี้ได้เรื่อยๆ)
# รูปแบบ: วันเดือนปี, วัน, เดือน, ข้างขึ้นข้างแรม, ปีนักษัตร, ราศี, รางวัลที่1, หน้า3ตัว, ท้าย3ตัว, ท้าย2ตัว
lottery_data = [
    {
        "date": "16 กันยายน 2569",
        "day_month": "วันพุธ เดือนกันยายน",
        "moon": "แรม 10 ค่ำ เดือน 10",
        "zodiac_astrology": "ปีจอ / ราศีพฤษภ",
        "p1": "730640", "front3": "060, 521", "back3": "266, 041", "back2": "64"
    },
    {
        "date": "1 กันยายน 2569",
        "day_month": "วันอังคาร เดือนกันยายน",
        "moon": "แรม 10 ค่ำ เดือน 9 (หลัง)",
        "zodiac_astrology": "ปีจอ / ราศีสิงห์",
        "p1": "417212", "front3": "257, 346", "back3": "136, 740", "back2": "04"
    },
    {
        "date": "16 สิงหาคม 2569",
        "day_month": "วันอาทิตย์ เดือนสิงหาคม",
        "moon": "แรม 9 ค่ำ เดือน 9",
        "zodiac_astrology": "ปีจอ / ราศีสิงห์",
        "p1": "004615", "front3": "731, 429", "back3": "937, 094", "back2": "53"
    },
    {
        "date": "1 สิงหาคม 2569",
        "day_month": "วันเสาร์ เดือนสิงหาคม",
        "moon": "แรม 13 ค่ำ เดือน 8",
        "zodiac_astrology": "ปีจอ / ราศีกรกฎ",
        "p1": "932479", "front3": "413, 672", "back3": "154, 039", "back2": "69"
    },
    {
        "date": "16 กรกฎาคม 2569",
        "day_month": "วันพฤหัสบดี เดือนกรกฎาคม",
        "moon": "แรม 2 ค่ำ เดือน 8",
        "zodiac_astrology": "ปีจอ / ราศีเมถุน",
        "p1": "639214", "front3": "683, 709", "back3": "746, 427", "back2": "71"
    },
    {
        "date": "1 กรกฎาคม 2569",
        "day_month": "วันพุธ เดือนกรกฎาคม",
        "moon": "แรม 2 ค่ำ เดือน 7",
        "zodiac_astrology": "ปีจอ / ราศีเมถุน",
        "p1": "751495", "front3": "001, 980", "back3": "304, 531", "back2": "62"
    },
    # ตัวอย่างย้อนหลังไปปี 2568 (สามารถเพิ่มข้อมูลอื่นๆ ต่อได้ตรงนี้)
    {
        "date": "30 ธันวาคม 2568",
        "day_month": "วันอังคาร เดือนธันวาคม",
        "moon": "ขึ้น 11 ค่ำ เดือน 2",
        "zodiac_astrology": "ปีระกา / ราศีธนู",
        "p1": "625520", "front3": "351, 882", "back3": "146, 858", "back2": "80"
    },
    {
        "date": "16 ธันวาคม 2568",
        "day_month": "วันอังคาร เดือนธันวาคม",
        "moon": "แรม 12 ค่ำ เดือน 1",
        "zodiac_astrology": "ปีระกา / ราศีธนู",
        "p1": "435116", "front3": "321, 608", "back3": "530, 241", "back2": "47"
    }
]

st.title("🎯 ระบบบันทึกและค้นหาผลสลากกินแบ่งรัฐบาล")
st.markdown("---")

# ช่องค้นหา
search_query = st.text_input("🔍 ค้นหา (พิมพ์วันที่, เดือน, ปี, หรือเลขท้าย):", "")

# กรองข้อมูลตามคำค้นหา
filtered_data = []
for item in lottery_data:
    combined_text = f"{item['date']} {item['day_month']} {item['moon']} {item['zodiac_astrology']} {item['p1']} {item['back2']}"
    if search_query.lower() in combined_text.lower():
        filtered_data.append(item)

st.subheader(f"ผลการบันทึกทั้งหมด (พบ {len(filtered_data)} งวด)")

# แสดงผลแบบการ์ดสวยงาม พร้อมปุ่มก็อปปี้ข้อมูล
for idx, item in enumerate(filtered_data):
    with st.container():
        st.markdown(f"### 📌 งวดวันที่: {item['date']}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"• **วัน/เดือน:** {item['day_month']}")
            st.write(f"• **ข้างขึ้น/ข้างแรม:** {item['moon']}")
            st.write(f"• **ปีนักษัตร / ราศี:** {item['zodiac_astrology']}")
            
        with col2:
            st.write(f"• **รางวัลที่ 1:** `{item['p1']}`")
            st.write(f"• **เลขหน้า 3 ตัว:** {item['front3']}")
            st.write(f"• **เลขท้าย 3 ตัว:** {item['back3']}")
            st.write(f"• **เลขท้าย 2 ตัว:** `{item['back2']}`")
            
        # ปุ่มสำหรับแสดงข้อความแบบก๊อปปี้ไปบันทึกได้ง่าย
        format_text = f"""วัน เดือน ปี: {item['date']}
วันอะไร เดือนอะไร: {item['day_month']}
ข้างขึ้นข้างแรม: {item['moon']}
ปีนักบัตร ราศรี: {item['zodiac_astrology']}
ผลหวย: รางวัลที่ 1 ({item['p1']}), เลขท้าย 2 ตัว ({item['back2']})"""
        
        with st.expander("📋 คัดลอกรูปแบบข้อความบันทึก"):
            st.code(format_text, language="text")
            
        st.markdown("---")

# ส่วนสำหรับแนะนำการเพิ่มข้อมูล 12 ปี
st.sidebar.header("💡 คำแนะนำเพิ่มเติม")
st.sidebar.info(
    "คุณสามารถเพิ่มข้อมูลย้อนหลัง 12 ปี (ประมาณเกือบ 300 งวด) "
    "เข้าไปในตัวแปร `lottery_data` ในโค้ด Python นี้ได้เรื่อยๆ หรือจะปรับให้เชื่อมต่อกับฐานข้อมูล CSV / Google Sheets เพื่อความสะดวกในการอัปเดตข้อมูลจำนวนมากครับ"
          )

