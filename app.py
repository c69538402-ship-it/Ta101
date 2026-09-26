import os
import json
from datetime import datetime

import folium
import pandas as pd
import streamlit as st
from folium.elements import MacroElement
from folium.plugins import Fullscreen, MousePosition
from pyproj import Geod
from shapely.geometry import Polygon, mapping, shape
from streamlit_folium import st_folium

try:
    from streamlit_js_eval import get_geolocation, streamlit_js_eval
except ImportError:
    get_geolocation = None
    streamlit_js_eval = None

st.set_page_config(page_title="Mon101 - วัดพื้นที่ไถนา", page_icon="📐", layout="wide")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "logo.jpg")
STORAGE_KEY = "mon101_field_measurements_v2"
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
    polygons = []
    if geom.geom_type == "Polygon":
        polygons = [geom]
    elif geom.geom_type == "MultiPolygon":
        polygons = list(geom.geoms)
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


def points_to_geometry(points):
    if len(points) < 3:
        return None
    # Shapely expects (lon, lat)
    poly = Polygon([(p[1], p[0]) for p in points])
    if not poly.is_valid:
        poly = poly.buffer(0)
    if poly.is_empty:
        return None
    return mapping(poly)


def add_center_crosshair(m):
    html = """
    <div style="
        position: fixed;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        pointer-events: none;
        width: 34px;
        height: 34px;
        border: 2px solid #ff3030;
        border-radius: 50%;
        box-sizing: border-box;
        background: rgba(255,255,255,0.05);
    ">
      <div style="position:absolute; left:15px; top:3px; width:2px; height:26px; background:#ff3030;"></div>
      <div style="position:absolute; left:3px; top:15px; width:26px; height:2px; background:#ff3030;"></div>
      <div style="position:absolute; left:12px; top:12px; width:8px; height:8px; background:#ff3030; border-radius:50%; border:1px solid white;"></div>
    </div>
    <div style="
        position: fixed;
        left: 50%;
        top: calc(50% + 24px);
        transform: translateX(-50%);
        z-index: 9999;
        pointer-events: none;
        background: rgba(0,0,0,0.68);
        color: white;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 11px;
        white-space: nowrap;
    ">จุดกลาง = จุดที่จะปักหมุด</div>
    """
    from branca.element import Element
    m.get_root().html.add_child(Element(html))


def make_map(center, zoom, points):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=None,
        control_scale=True,
        prefer_canvas=True,
        zoom_control=True,
    )

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Sources: Esri and the GIS User Community",
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

    add_center_crosshair(m)

    # GPS starting point, shown separately from the fixed center crosshair.
    folium.Marker(
        center,
        tooltip="📍 ตำแหน่งเริ่มต้นจาก GPS",
        popup=f"GPS: {center[0]:.6f}, {center[1]:.6f}",
        icon=folium.Icon(color="red", icon="location-arrow", prefix="fa"),
    ).add_to(m)

    # Numbered pins.
    for idx, p in enumerate(points, start=1):
        folium.Marker(
            p,
            tooltip=f"หมุดที่ {idx}",
            popup=f"หมุดที่ {idx}<br>Lat {p[0]:.6f}<br>Lon {p[1]:.6f}",
            icon=folium.DivIcon(
                html=f"<div style='font-size:13px;font-weight:bold;color:#fff;background:#1976d2;border:2px solid #fff;border-radius:50%;width:26px;height:26px;text-align:center;line-height:22px;box-shadow:0 1px 4px #333'>{idx}</div>"
            ),
        ).add_to(m)

    if len(points) >= 2:
        folium.PolyLine(
            points + ([points[0]] if len(points) >= 3 else []),
            color="#1976D2",
            weight=4,
            opacity=0.9,
        ).add_to(m)

    if len(points) >= 3:
        geometry = points_to_geometry(points)
        if geometry:
            folium.GeoJson(
                geometry,
                name="พื้นที่ที่วัด",
                style_function=lambda _: {
                    "color": "#00C853",
                    "weight": 4,
                    "fillColor": "#00C853",
                    "fillOpacity": 0.22,
                },
            ).add_to(m)

    Fullscreen(position="topright").add_to(m)
    MousePosition(position="bottomleft", separator=" | ", prefix="พิกัด: ").add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)
    return m


def load_saved_records():
    if streamlit_js_eval is None:
        return []
    try:
        raw = streamlit_js_eval(
            js_expressions=f"localStorage.getItem('{STORAGE_KEY}')",
            key="mon101_load_records",
        )
        if raw:
            data = json.loads(raw)
            return data if isinstance(data, list) else []
    except Exception:
        pass
    return []


def save_records_to_browser(records):
    if streamlit_js_eval is None:
        return
    try:
        payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"), default=str)
        js = f"localStorage.setItem('{STORAGE_KEY}', {json.dumps(payload, ensure_ascii=False)})"
        streamlit_js_eval(js_expressions=js, key=f"mon101_save_{len(records)}_{hash(payload)}")
    except Exception:
        pass


def clear_browser_records():
    if streamlit_js_eval is None:
        return
    try:
        streamlit_js_eval(
            js_expressions=f"localStorage.removeItem('{STORAGE_KEY}')",
            key="mon101_clear_records",
        )
    except Exception:
        pass


# -------------------- Session state --------------------
if "location" not in st.session_state:
    st.session_state.location = [17.4138, 102.7875]
if "map_center" not in st.session_state:
    st.session_state.map_center = list(st.session_state.location)
if "zoom" not in st.session_state:
    st.session_state.zoom = 17
if "points" not in st.session_state:
    st.session_state.points = []
if "records" not in st.session_state:
    st.session_state.records = None
if "request_location" not in st.session_state:
    st.session_state.request_location = False

# Restore browser-saved records once per session.
if st.session_state.records is None:
    st.session_state.records = load_saved_records()

show_logo()
st.title("📐 Mon101 — เครื่องวัดพื้นที่ไถนา")
st.caption("ซูมแผนที่ให้ใกล้ที่สุด แล้วเลื่อนแผนที่ให้ 'กากบาทกลางจอ' ตรงจุดจริง จากนั้นกดปุ่มปักหมุด — ไม่ต้องเอานิ้วจิ้มให้ตรง")

# -------------------- GPS --------------------
c1, c2 = st.columns([1, 3])
with c1:
    if st.button("📍 ใช้ตำแหน่งปัจจุบัน", use_container_width=True):
        st.session_state.request_location = True
with c2:
    st.caption("GPS ใช้เป็นจุดเริ่มต้นเท่านั้น หลังจากนั้นสามารถลากแผนที่ไปยังแปลงจริงได้")

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
        st.error("ไม่พบ streamlit-js-eval กรุณาตรวจ requirements.txt")
    elif loc and "coords" in loc:
        coords = loc["coords"]
        lat = coords.get("latitude")
        lon = coords.get("longitude")
        if lat is not None and lon is not None:
            st.session_state.location = [float(lat), float(lon)]
            st.session_state.map_center = [float(lat), float(lon)]
            st.session_state.request_location = False
            st.success(f"GPS: {float(lat):.6f}, {float(lon):.6f}")
            st.rerun()
    elif loc and "error" in loc:
        st.warning(f"อ่าน GPS ไม่สำเร็จ: {loc['error'].get('message', 'ไม่ทราบสาเหตุ')}")
    else:
        st.info("กำลังรอพิกัด GPS... กรุณาอนุญาต Location ในเบราว์เซอร์")

# -------------------- Map + side controls --------------------
st.subheader("🛰️ 1) เลื่อนแผนที่ให้กากบาทตรงจุดจริง")
left, right = st.columns([3.6, 1.2], gap="medium")

with left:
    map_state = st_folium(
        make_map(st.session_state.map_center, st.session_state.zoom, st.session_state.points),
        height=620,
        width=None,
        returned_objects=["center", "zoom"],
        key="mon101_map_v2",
    )

if map_state:
    center = map_state.get("center")
    if isinstance(center, dict) and center.get("lat") is not None and center.get("lng") is not None:
        st.session_state.map_center = [float(center["lat"]), float(center["lng"])]
    elif isinstance(center, (list, tuple)) and len(center) >= 2:
        st.session_state.map_center = [float(center[0]), float(center[1])]
    if map_state.get("zoom") is not None:
        st.session_state.zoom = int(map_state["zoom"])

with right:
    st.markdown("### 📌 ปักหมุด")
    st.write("เลื่อนแผนที่ให้กากบาทแดงตรงมุมแปลง แล้วกดปุ่มนี้")
    if st.button("📌 ปักหมุดตรงกลาง", type="primary", use_container_width=True):
        p = [round(float(st.session_state.map_center[0]), 7), round(float(st.session_state.map_center[1]), 7)]
        # Avoid accidental duplicate points.
        if not st.session_state.points or p != st.session_state.points[-1]:
            st.session_state.points.append(p)
        st.rerun()

    if st.session_state.points:
        st.markdown(f"**ปักแล้ว {len(st.session_state.points)} จุด**")
        for i, p in enumerate(st.session_state.points, start=1):
            st.caption(f"{i}. {p[0]:.7f}, {p[1]:.7f}")

    if st.button("↩️ ลบหมุดล่าสุด", use_container_width=True, disabled=not st.session_state.points):
        st.session_state.points.pop()
        st.rerun()

    if st.button("🗑️ เริ่มวัดแปลงใหม่", use_container_width=True, disabled=not st.session_state.points):
        st.session_state.points = []
        st.rerun()

    st.info("แนะนำให้ซูมระดับ 19–20 ก่อนปักหมุดมุมแปลง เพื่อให้กะตำแหน่งได้ละเอียดขึ้น")

# Build geometry from pinned points.
st.session_state.geometry = points_to_geometry(st.session_state.points)

# -------------------- Measurement --------------------
st.subheader("📏 2) ผลการวัด")
if len(st.session_state.points) < 3 or not st.session_state.geometry:
    st.warning(f"ต้องมีอย่างน้อย 3 หมุด ตอนนี้มี {len(st.session_state.points)} หมุด")
else:
    m2 = polygon_area(st.session_state.geometry)
    rai, ngan, wa, total_rai = area_parts(m2)
    plow = total_rai * PLOW_PRICE
    till = total_rai * TILL_PRICE
    total = total_rai * TOTAL_PRICE

    a, b, c, d = st.columns(4)
    a.metric("ไร่", f"{rai:,}")
    b.metric("งาน", f"{ngan:,}")
    c.metric("ตารางวา", f"{wa:,.2f}")
    d.metric("พื้นที่รวม (ไร่)", f"{total_rai:,.4f}")
    st.success(f"พื้นที่ทั้งหมด = {rai:,} ไร่ {ngan:,} งาน {wa:,.2f} ตารางวา ({m2:,.2f} ตร.ม.)")

    price_df = pd.DataFrame([
        {"รายการ": "1. ไถนา", "ราคา/ไร่": PLOW_PRICE, "พื้นที่ (ไร่)": total_rai, "เป็นเงิน (บาท)": plow},
        {"รายการ": "2. ปั่นดิน", "ราคา/ไร่": TILL_PRICE, "พื้นที่ (ไร่)": total_rai, "เป็นเงิน (บาท)": till},
        {"รายการ": "3. รวมไถนา + ปั่นดิน", "ราคา/ไร่": TOTAL_PRICE, "พื้นที่ (ไร่)": total_rai, "เป็นเงิน (บาท)": total},
    ])
    st.dataframe(price_df, use_container_width=True, hide_index=True)
    st.success(f"💰 รวมไถนา + ปั่นดิน = {total:,.2f} บาท")

    name = st.text_input("ชื่อแปลง / ชื่อลูกค้า", placeholder="เช่น นาแม่บุญมา แปลงที่ 1", key="field_name")
    save_col1, save_col2 = st.columns([2, 1])
    with save_col1:
        if st.button("💾 บันทึกแปลงนี้", type="primary", use_container_width=True):
            record = {
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
                "จำนวนหมุด": len(st.session_state.points),
                "หมุด": st.session_state.points,
                "geometry": st.session_state.geometry,
            }
            st.session_state.records.append(record)
            save_records_to_browser(st.session_state.records)
            st.success("บันทึกแล้ว และเก็บสำเนาไว้ในเบราว์เซอร์เครื่องนี้")
            st.rerun()
    with save_col2:
        st.download_button(
            "⬇️ ดาวน์โหลดข้อมูลแปลง",
            json.dumps(
                {
                    "ชื่อแปลง": name.strip() or "ไม่ระบุชื่อ",
                    "วันที่เวลา": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "พื้นที่_ตรม": round(m2, 2),
                    "พื้นที่_ไร่รวม": round(total_rai, 6),
                    "ไร่": rai,
                    "งาน": ngan,
                    "ตารางวา": round(wa, 2),
                    "ราคา_รวม": round(total, 2),
                    "หมุด": st.session_state.points,
                    "geometry": st.session_state.geometry,
                },
                ensure_ascii=False,
                indent=2,
            ),
            "mon101_field.json",
            "application/json",
            use_container_width=True,
        )

# -------------------- Saved records --------------------
st.divider()
st.subheader("📋 3) รายการที่บันทึกไว้")
st.caption("รายการจะถูกเก็บในพื้นที่จัดเก็บของเบราว์เซอร์เครื่องนี้ เพื่อไม่ให้หายเมื่อปิด/เปิดหน้าแอปใหม่ ควรดาวน์โหลด CSV/JSON สำรองด้วย")

if st.session_state.records:
    rows = [{k: v for k, v in r.items() if k not in ("geometry", "หมุด")} for r in st.session_state.records]
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    dl1, dl2, dl3 = st.columns(3)
    with dl1:
        st.download_button(
            "⬇️ ดาวน์โหลด CSV",
            df.to_csv(index=False, encoding="utf-8-sig"),
            "mon101_field_measurements.csv",
            "text/csv",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            "⬇️ ดาวน์โหลด JSON",
            json.dumps(st.session_state.records, ensure_ascii=False, indent=2, default=str),
            "mon101_field_measurements.json",
            "application/json",
            use_container_width=True,
        )
    with dl3:
        if st.button("🗑️ ลบรายการที่บันทึกทั้งหมด", use_container_width=True):
            st.session_state.records = []
            clear_browser_records()
            st.success("ลบรายการในเครื่องนี้แล้ว")
            st.rerun()
else:
    st.info("ยังไม่มีรายการบันทึก")

# -------------------- Manual coordinates --------------------
with st.expander("🧭 GPS คลาดเคลื่อน / ใส่พิกัดเริ่มต้นเอง"):
    mc1, mc2 = st.columns(2)
    with mc1:
        manual_lat = st.number_input("Latitude", value=float(st.session_state.location[0]), format="%.7f", key="manual_lat")
    with mc2:
        manual_lon = st.number_input("Longitude", value=float(st.session_state.location[1]), format="%.7f", key="manual_lon")
    if st.button("📌 ใช้พิกัดนี้", use_container_width=True):
        st.session_state.location = [float(manual_lat), float(manual_lon)]
        st.session_state.map_center = [float(manual_lat), float(manual_lon)]
        st.rerun()

# -------------------- Music --------------------
st.divider()
show_logo()
st.subheader("🎵 เครื่องเล่นเพลง")
exts = (".mp3", ".wav", ".ogg", ".m4a", ".aac")
music = sorted([
    f for f in os.listdir(APP_DIR)
    if os.path.isfile(os.path.join(APP_DIR, f)) and f.lower().endswith(exts)
])
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
- ใช้กากบาทกลางจอแทนการเอานิ้วจิ้มบนแผนที่โดยตรง เพื่อลดความคลาดเคลื่อนจากนิ้วบังตำแหน่ง
- คำนวณพื้นที่จากพิกัดหมุดด้วย WGS84/Geodesic
- ควรให้เจ้าของนาและผู้รับจ้างเห็นหมุด/เส้นเขตเดียวกัน และเก็บไฟล์ JSON หรือ CSV ไว้ทั้งสองฝ่าย
- GPS โทรศัพท์และภาพดาวเทียมมีความคลาดเคลื่อนได้ จึงไม่ใช่การรังวัดที่ดินตามกฎหมาย
- หากมีข้อพิพาทเรื่องแนวเขตที่ดิน ควรใช้การรังวัดโดยผู้สำรวจ/หน่วยงานที่มีอำนาจ
- 1 ไร่ = 4 งาน = 400 ตารางวา = 1,600 ตารางเมตร
""")
st.caption("อัตราที่ตั้งไว้: ไถนา 250 บาท/ไร่ • ปั่นดิน 350 บาท/ไร่ • รวม 600 บาท/ไร่")
