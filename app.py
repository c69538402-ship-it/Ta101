import os
import json
from datetime import datetime

import folium
import pandas as pd
import streamlit as st
from folium.plugins import Draw, Fullscreen, MousePosition
from pyproj import Geod
from shapely.geometry import shape
from streamlit_folium import st_folium

try:
    from streamlit_js_eval import get_geolocation
except ImportError:
    get_geolocation = None

st.set_page_config(page_title="Mon101 - วัดพื้นที่ไถนา", page_icon="📐", layout="wide")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "logo.jpg")
PLOW_PRICE = 250.0
TILL_PRICE = 350.0
TOTAL_PRICE = 600.0
GEOD = Geod(ellps="WGS84")


def show_logo():
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)


def area_parts(m2):
    rai = int(m2 // 1600)
    rest = m2 - rai * 1600
    ngan = int(rest // 400)
    wa = (rest - ngan * 400) / 4
    return rai, ngan, wa, m2 / 1600


def polygon_area(geometry):
    if not geometry:
        return 0.0
    geom = shape(geometry)
    polygons = [geom] if geom.geom_type == "Polygon" else list(geom.geoms) if geom.geom_type == "MultiPolygon" else []
    total = 0.0
    for poly in polygons:
        coords = list(poly.exterior.coords)
        lons = [p[0] for p in coords]
        lats = [p[1] for p in coords]
        a, _ = GEOD.polygon_area_perimeter(lons, lats)
        total += abs(a)
        for ring in poly.interiors:
            rc = list(ring.coords)
            a, _ = GEOD.polygon_area_perimeter([p[0] for p in rc], [p[1] for p in rc])
            total -= abs(a)
    return max(0.0, total)


def make_map(center, zoom, saved=None):
    m = folium.Map(location=center, zoom_start=zoom, tiles=None, control_scale=True, prefer_canvas=True)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Sources: Esri, DigitalGlobe, GeoEye, i-cubed, USDA FSA, USGS, AEX, Getmapping, Aerogrid, IGN, IGP, swisstopo, and the GIS User Community",
        name="🛰️ ภาพดาวเทียม",
        overlay=False,
        control=True,
        max_zoom=20,
    ).add_to(m)
    folium.TileLayer(
        "OpenStreetMap",
        name="🗺️ แผนที่ถนน",
        overlay=False,
        control=True,
        max_zoom=19,
    ).add_to(m)
    folium.Marker(
        center,
        tooltip="📍 จุดเริ่มต้น / ตำแหน่งปัจจุบัน",
        popup="จุดเริ่มต้นจากตำแหน่งเครื่อง",
        icon=folium.Icon(color="red", icon="crosshairs", prefix="fa"),
    ).add_to(m)
    if saved:
        folium.GeoJson(
            saved,
            name="แปลงที่วัด",
            style_function=lambda _: {"color": "#00FFFF", "weight": 4, "fillColor": "#00FFFF", "fillOpacity": 0.25},
        ).add_to(m)
    Draw(
        export=False,
        position="topleft",
        draw_options={"polyline": False, "polygon": True, "rectangle": True, "circle": False, "marker": False, "circlemarker": False},
        edit_options={"edit": True, "remove": True},
    ).add_to(m)
    Fullscreen(position="topright").add_to(m)
    MousePosition(position="bottomleft", separator=" | ", prefix="พิกัด: ").add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return m


if "location" not in st.session_state:
    st.session_state.location = [17.4138, 102.7875]
if "zoom" not in st.session_state:
    st.session_state.zoom = 16
if "geometry" not in st.session_state:
    st.session_state.geometry = None
if "records" not in st.session_state:
    st.session_state.records = []
if "request_location" not in st.session_state:
    st.session_state.request_location = False

show_logo()
st.title("📐 Mon101 — เครื่องวัดพื้นที่ไถนา")
st.caption("วัดพื้นที่จากแผนที่มุมสูง • วาดแนวเขตเอง • คำนวณเป็น ไร่ / งาน / ตารางวา • คำนวณราคา")
st.info("กด 'ใช้ตำแหน่งปัจจุบัน' เพื่อใช้ GPS ของเครื่องเป็นจุดเริ่มต้น แล้วลากแผนที่/ซูมไปยังแปลงที่ต้องการและใช้เครื่องมือรูปหลายเหลี่ยมวาดแนวเขต")

c1, c2 = st.columns([1, 3])
with c1:
    if st.button("📍 ใช้ตำแหน่งปัจจุบัน", use_container_width=True):
        st.session_state.request_location = True
with c2:
    st.caption("ต้องอนุญาต Location ในเบราว์เซอร์/มือถือ หากไม่อนุญาตยังสามารถเลื่อนแผนที่ไปวัดที่อื่นได้")

# streamlit-js-eval รุ่นปัจจุบันใช้ get_geolocation() โดยไม่รับ
# geolocation_options หรือ component_key และควรเรียก component
# นอก if/st.button branch
loc = None
if get_geolocation is not None:
    try:
        loc = get_geolocation()
    except Exception as exc:
        if st.session_state.request_location:
            st.warning("อ่าน GPS ไม่สำเร็จ")
            st.caption(str(exc))

if st.session_state.request_location:
    if get_geolocation is None:
        st.error("ไม่พบ streamlit-js-eval กรุณาใส่แพ็กเกจนี้ใน requirements.txt")
    elif loc and "coords" in loc:
        coords = loc["coords"]
        lat = coords.get("latitude")
        lon = coords.get("longitude")

        if lat is not None and lon is not None:
            st.session_state.location = [float(lat), float(lon)]
            st.session_state.request_location = False
            st.success(
                f"ตำแหน่งปัจจุบันจาก GPS: "
                f"{float(lat):.6f}, {float(lon):.6f}"
            )
            st.rerun()

    elif loc and "error" in loc:
        error_code = loc["error"].get("code")
        error_msg = loc["error"].get(
            "message",
            "ไม่สามารถอ่านตำแหน่งได้",
        )
        st.warning(
            f"อ่าน GPS ไม่สำเร็จ (รหัส {error_code}): {error_msg}"
        )
    else:
        st.info(
            "กำลังรอพิกัด GPS... กรุณากดอนุญาต Location "
            "ในหน้าต่างของเบราว์เซอร์"
        )

with st.expander("🧭 ถ้า GPS คลาดเคลื่อน: ใส่พิกัดเองได้"):
    st.caption(
        "ใช้สำหรับตรวจสอบหรือแก้ตำแหน่งเริ่มต้น กรณีมือถือจับตำแหน่งคลาดเคลื่อน"
    )
    mc1, mc2 = st.columns(2)

    with mc1:
        manual_lat = st.number_input(
            "ละติจูด (Latitude)",
            value=float(st.session_state.location[0]),
            format="%.6f",
            key="manual_lat",
        )

    with mc2:
        manual_lon = st.number_input(
            "ลองจิจูด (Longitude)",
            value=float(st.session_state.location[1]),
            format="%.6f",
            key="manual_lon",
        )

    if st.button(
        "📌 ใช้พิกัดนี้เป็นจุดเริ่มต้น",
        use_container_width=True,
    ):
        st.session_state.location = [
            float(manual_lat),
            float(manual_lon),
        ]
        st.success(
            f"ตั้งจุดเริ่มต้นแล้ว: "
            f"{manual_lat:.6f}, {manual_lon:.6f}"
        )
        st.rerun()


st.subheader("🛰️ แผนที่วัดพื้นที่")
map_state = st_folium(
    make_map(st.session_state.location, st.session_state.zoom, st.session_state.geometry),
    height=650,
    width=None,
    returned_objects=["last_active_drawing", "zoom"],
    key="mon101_map",
)
if map_state:
    if map_state.get("zoom"):
        st.session_state.zoom = int(map_state["zoom"])
    drawing = map_state.get("last_active_drawing")
    if drawing and drawing.get("geometry") and drawing["geometry"].get("type") in ("Polygon", "MultiPolygon"):
        st.session_state.geometry = drawing["geometry"]

st.subheader("📏 ผลการวัด")
if not st.session_state.geometry:
    st.warning("ยังไม่มีพื้นที่ที่วัด ให้ใช้เครื่องมือรูปหลายเหลี่ยมบนแผนที่แล้ววาดตามแนวเขตแปลง")
else:
    m2 = polygon_area(st.session_state.geometry)
    rai, ngan, wa, total_rai = area_parts(m2)
    plow = total_rai * PLOW_PRICE
    till = total_rai * TILL_PRICE
    total = plow + till

    a, b, c, d = st.columns(4)
    a.metric("ไร่", f"{rai:,}")
    b.metric("งาน", f"{ngan:,}")
    c.metric("ตารางวา", f"{wa:,.2f}")
    d.metric("พื้นที่รวม (ไร่)", f"{total_rai:,.4f}")
    st.success(f"พื้นที่ทั้งหมด = {rai:,} ไร่ {ngan:,} งาน {wa:,.2f} ตารางวา ({m2:,.2f} ตร.ม.)")

    st.subheader("💰 ตารางราคา")
    price_df = pd.DataFrame([
        {"รายการ": "1. ไถนา", "ราคา/ไร่": PLOW_PRICE, "พื้นที่ (ไร่)": total_rai, "เป็นเงิน (บาท)": plow},
        {"รายการ": "2. ปั่นดิน", "ราคา/ไร่": TILL_PRICE, "พื้นที่ (ไร่)": total_rai, "เป็นเงิน (บาท)": till},
        {"รายการ": "3. รวมไถนา + ปั่นดิน", "ราคา/ไร่": TOTAL_PRICE, "พื้นที่ (ไร่)": total_rai, "เป็นเงิน (บาท)": total},
    ])
    st.dataframe(price_df, use_container_width=True, hide_index=True)
    st.success(f"💰 รวมไถนา + ปั่นดิน = {total:,.2f} บาท")

    name = st.text_input("ชื่อแปลง / ชื่อลูกค้า", placeholder="เช่น นาแม่บุญมา แปลงที่ 1")
    if st.button("➕ บันทึกผลการวัดแปลงนี้", use_container_width=True):
        st.session_state.records.append({
            "วันที่เวลา": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "ชื่อแปลง": name.strip() or "ไม่ระบุชื่อ",
            "ไร่": rai,
            "งาน": ngan,
            "ตารางวา": round(wa, 2),
            "พื้นที่_ตรม": round(m2, 2),
            "พื้นที่_ไร่รวม": round(total_rai, 6),
            "ค่าไถนา_บาท": round(plow, 2),
            "ค่าปั่นดิน_บาท": round(till, 2),
            "รวม_บาท": round(total, 2),
            "พิกัดเริ่มต้น_lat": round(st.session_state.location[0], 6),
            "พิกัดเริ่มต้น_lon": round(st.session_state.location[1], 6),
            "geometry": st.session_state.geometry,
        })
        st.success("บันทึกแปลงแล้ว")

if st.session_state.records:
    st.divider()
    st.subheader("📋 รายการแปลงที่บันทึกไว้")
    rows = [{k: v for k, v in r.items() if k != "geometry"} for r in st.session_state.records]
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("⬇️ ดาวน์โหลด CSV", df.to_csv(index=False, encoding="utf-8-sig"), "mon101_field_measurements.csv", "text/csv", use_container_width=True)
    with c2:
        st.download_button("⬇️ ดาวน์โหลด JSON", json.dumps(st.session_state.records, ensure_ascii=False, indent=2, default=str), "mon101_field_measurements.json", "application/json", use_container_width=True)

st.divider()
show_logo()
st.subheader("🎵 เครื่องเล่นเพลง")
exts = (".mp3", ".wav", ".ogg", ".m4a", ".aac")
music = sorted([f for f in os.listdir(APP_DIR) if os.path.isfile(os.path.join(APP_DIR, f)) and f.lower().endswith(exts)])
if music:
    for f in music:
        st.write(f"🎵 {f}")
        with open(os.path.join(APP_DIR, f), "rb") as audio:
            st.audio(audio.read())
else:
    st.info("วางไฟล์เพลง .mp3 / .wav / .ogg / .m4a ไว้โฟลเดอร์เดียวกับ app.py")

st.divider()
st.subheader("⚖️ หมายเหตุเรื่องความเที่ยงธรรม")
st.markdown("""
- ระบบคำนวณพื้นที่จากพิกัดของเส้นที่ผู้ใช้วาดบนแผนที่ โดยใช้ WGS84/Geodesic
- ควรให้ทั้งเจ้าของนาและผู้รับจ้างดูเส้นเขตเดียวกัน และดาวน์โหลดไฟล์ผลการวัดเก็บไว้ทั้งสองฝ่าย
- GPS โทรศัพท์และภาพดาวเทียมมีความคลาดเคลื่อนได้ จึงไม่ควรใช้แทนการรังวัดที่ดินตามกฎหมาย
- หากมีข้อพิพาทเรื่องแนวเขตที่ดิน ควรใช้การรังวัดโดยผู้สำรวจ/หน่วยงานที่มีอำนาจ
- 1 ไร่ = 4 งาน = 400 ตารางวา = 1,600 ตารางเมตร
""")
st.caption("อัตราที่ตั้งไว้: ไถนา 250 บาท/ไร่ • ปั่นดิน 350 บาท/ไร่ • รวม 600 บาท/ไร่")
