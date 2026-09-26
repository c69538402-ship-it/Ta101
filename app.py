import os
import json
import csv
import io
from datetime import datetime

import streamlit as st
from pyproj import Geod


# ============================================================
# MON101 FIELD MEASURE
# Leaflet map + Streamlit Components v2
# ============================================================

st.set_page_config(
    page_title="Mon101 วัดพื้นที่แปลงนา",
    page_icon="📐",
    layout="wide",
)

# ------------------------------------------------------------
# พื้นฐาน
# ------------------------------------------------------------

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "logo.jpg")

DEFAULT_LAT = 17.4138
DEFAULT_LON = 102.7875
DEFAULT_ZOOM = 17

PRICE_PLOW = 250
PRICE_MILL = 350
PRICE_BOTH = 600

geod = Geod(ellps="WGS84")


# ============================================================
# Session State
# ============================================================

if "field_points" not in st.session_state:
    st.session_state.field_points = []

if "field_records" not in st.session_state:
    st.session_state.field_records = []

if "component_initialized" not in st.session_state:
    st.session_state.component_initialized = False


# ============================================================
# ฟังก์ชันคำนวณพื้นที่
# ============================================================

def calculate_area_m2(points):
    """คำนวณพื้นที่ polygon ด้วย WGS84 Geodesic"""

    if len(points) < 3:
        return 0.0

    lats = [float(p[0]) for p in points]
    lons = [float(p[1]) for p in points]

    area, _ = geod.polygon_area_perimeter(
        lons,
        lats,
    )

    return abs(float(area))


def convert_area(area_m2):
    """แปลงตารางเมตร -> ไร่ งาน ตารางวา"""

    rai = int(area_m2 // 1600)

    remain = area_m2 - (rai * 1600)

    ngan = int(remain // 400)

    remain -= ngan * 400

    square_wa = remain / 4

    return rai, ngan, square_wa


def area_text(area_m2):
    rai, ngan, square_wa = convert_area(area_m2)

    return (
        f"{rai:,} ไร่ "
        f"{ngan:,} งาน "
        f"{square_wa:,.2f} ตารางวา"
    )


def calculate_prices(area_m2):
    rai_decimal = area_m2 / 1600

    return {
        "ไถ": rai_decimal * PRICE_PLOW,
        "ปั่น": rai_decimal * PRICE_MILL,
        "รวม": rai_decimal * PRICE_BOTH,
    }


# ============================================================
# โลโก้
# ============================================================

if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=120)


# ============================================================
# หัวข้อ
# ============================================================

st.title("📐 Mon101 วัดพื้นที่แปลงนา")

st.caption(
    "ซูมเข้า → เลื่อนแผนที่ → ให้กากบาทตรงจุด → "
    "กดปักหมุด"
)


# ============================================================
# CSS หน้า Streamlit
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-weight: 700;
    }

    .info-box {
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,.25);
        margin-bottom: 10px;
    }

    .small-note {
        font-size: 13px;
        opacity: .8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COMPONENT V2
# ============================================================

try:

    import streamlit.components.v2 as components

except Exception:

    st.error(
        "Streamlit รุ่นนี้ยังไม่รองรับ Components v2"
    )

    st.stop()


# ============================================================
# HTML
# ============================================================

MAP_HTML = """
<div class="app">

    <div class="toolbar">

        <button id="gpsBtn" class="tool gps">
            📍 GPS
        </button>

        <button id="satBtn" class="tool active">
            🛰️ ดาวเทียม
        </button>

        <button id="roadBtn" class="tool">
            🗺️ ถนน
        </button>

    </div>

    <div id="map"></div>

    <div class="crosshair">
        <div class="cross-h"></div>
        <div class="cross-v"></div>
        <div class="cross-dot"></div>
    </div>

    <div class="bottom-panel">

        <div class="panel-title">
            📌 ปักหมุดตรงกากบาท
        </div>

        <div class="panel-subtitle">
            ซูมและเลื่อนแผนที่ได้โดยไม่รีเฟรช
        </div>

        <button id="pinBtn" class="main-btn">
            📌 ปักหมุดจุดนี้
        </button>

        <div class="row">

            <button id="undoBtn" class="secondary-btn">
                ↩️ ลบล่าสุด
            </button>

            <button id="clearBtn" class="danger-btn">
                🗑️ เริ่มใหม่
            </button>

        </div>

        <div id="status" class="status">
            ยังไม่มีจุด
        </div>

    </div>

</div>
"""


# ============================================================
# CSS COMPONENT
# ============================================================

MAP_CSS = """
* {
    box-sizing: border-box;
}

.app {
    position: relative;
    width: 100%;
    height: 700px;
    border-radius: 14px;
    overflow: hidden;
    background: #ddd;
    font-family: Arial, sans-serif;
}

#map {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}

.toolbar {
    position: absolute;
    top: 12px;
    left: 12px;
    z-index: 5000;
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
}

.tool {
    border: none;
    border-radius: 9px;
    padding: 9px 12px;
    background: white;
    color: #222;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(0,0,0,.25);
}

.tool.active {
    background: #1683ff;
    color: white;
}

.tool:active {
    transform: scale(.97);
}

.crosshair {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 42px;
    height: 42px;
    transform: translate(-50%, -50%);
    z-index: 4500;
    pointer-events: none;
}

.cross-h {
    position: absolute;
    width: 42px;
    height: 3px;
    top: 19px;
    left: 0;
    background: #ff0000;
    box-shadow: 0 0 3px white;
}

.cross-v {
    position: absolute;
    width: 3px;
    height: 42px;
    left: 19px;
    top: 0;
    background: #ff0000;
    box-shadow: 0 0 3px white;
}

.cross-dot {
    position: absolute;
    width: 11px;
    height: 11px;
    left: 15px;
    top: 15px;
    background: #ff0000;
    border: 2px solid white;
    border-radius: 50%;
}

.bottom-panel {
    position: absolute;
    left: 12px;
    right: 12px;
    bottom: 12px;
    z-index: 5000;
    max-width: 390px;
    background: rgba(255,255,255,.96);
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 3px 16px rgba(0,0,0,.30);
}

.panel-title {
    font-weight: 700;
    font-size: 17px;
    margin-bottom: 3px;
}

.panel-subtitle {
    font-size: 12px;
    color: #555;
    margin-bottom: 8px;
}

.main-btn {
    width: 100%;
    border: none;
    border-radius: 10px;
    padding: 12px;
    background: #e31b23;
    color: white;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 7px;
}

.main-btn:active {
    transform: scale(.98);
}

.row {
    display: flex;
    gap: 7px;
}

.secondary-btn,
.danger-btn {
    flex: 1;
    border: none;
    border-radius: 9px;
    padding: 9px;
    font-weight: 600;
}

.secondary-btn {
    background: #eeeeee;
    color: #222;
}

.danger-btn {
    background: #ffe1e1;
    color: #a40000;
}

.status {
    margin-top: 8px;
    font-size: 13px;
    font-weight: 600;
}

.leaflet-control-attribution {
    font-size: 9px !important;
}

@media (max-width: 600px) {

    .app {
        height: 680px;
        border-radius: 10px;
    }

    .toolbar {
        left: 8px;
        top: 8px;
    }

    .tool {
        padding: 8px 9px;
        font-size: 12px;
    }

    .bottom-panel {
        left: 8px;
        right: 8px;
        bottom: 8px;
        max-width: none;
    }

    .panel-title {
        font-size: 15px;
    }
}
"""


# ============================================================
# JAVASCRIPT
# ============================================================

MAP_JS = r"""
export default function(component) {

    const {
        parentElement,
        data,
        setStateValue
    } = component;

    const mapElement = parentElement.querySelector("#map");

    const pinBtn = parentElement.querySelector("#pinBtn");
    const undoBtn = parentElement.querySelector("#undoBtn");
    const clearBtn = parentElement.querySelector("#clearBtn");

    const gpsBtn = parentElement.querySelector("#gpsBtn");
    const satBtn = parentElement.querySelector("#satBtn");
    const roadBtn = parentElement.querySelector("#roadBtn");

    const status = parentElement.querySelector("#status");

    // --------------------------------------------------------
    // Load Leaflet
    // --------------------------------------------------------

    function loadLeaflet() {

        return new Promise((resolve, reject) => {

            if (window.L) {
                resolve();
                return;
            }

            const css = document.createElement("link");

            css.rel = "stylesheet";
            css.href =
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";

            document.head.appendChild(css);

            const script = document.createElement("script");

            script.src =
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";

            script.onload = () => resolve();

            script.onerror = () =>
                reject(
                    new Error("โหลด Leaflet ไม่สำเร็จ")
                );

            document.head.appendChild(script);
        });
    }


    // --------------------------------------------------------
    // Local Storage
    // --------------------------------------------------------

    const STORAGE_POINTS =
        "mon101_field_points_v3";

    const STORAGE_RECORDS =
        "mon101_field_records_v3";

    const STORAGE_VIEW =
        "mon101_map_view_v3";


    function readJSON(key, fallback) {

        try {

            const raw = localStorage.getItem(key);

            if (!raw) {
                return fallback;
            }

            return JSON.parse(raw);

        } catch (e) {

            return fallback;
        }
    }


    function writeJSON(key, value) {

        try {

            localStorage.setItem(
                key,
                JSON.stringify(value)
            );

        } catch (e) {

            console.log(
                "localStorage error",
                e
            );
        }
    }


    // --------------------------------------------------------
    // Data จาก Python
    // --------------------------------------------------------

    let points =
        Array.isArray(data?.points)
            ? data.points
            : [];

    let records =
        Array.isArray(data?.records)
            ? data.records
            : [];


    // --------------------------------------------------------
    // ดึงข้อมูลเก่าจากเครื่อง
    // --------------------------------------------------------

    const storedPoints =
        readJSON(
            STORAGE_POINTS,
            null
        );

    const storedRecords =
        readJSON(
            STORAGE_RECORDS,
            null
        );


    if (
        Array.isArray(storedPoints) &&
        storedPoints.length > 0 &&
        points.length === 0
    ) {

        points = storedPoints;

        setStateValue(
            "points",
            points
        );
    }


    if (
        Array.isArray(storedRecords) &&
        storedRecords.length > 0 &&
        records.length === 0
    ) {

        records = storedRecords;

        setStateValue(
            "records",
            records
        );
    }


    // --------------------------------------------------------
    // โหลดแผนที่
    // --------------------------------------------------------

    let map = null;

    let satelliteLayer = null;

    let roadLayer = null;

    let polygonLayer = null;

    let markerLayer = [];

    let initialized = false;


    function saveView() {

        if (!map) {
            return;
        }

        const center =
            map.getCenter();

        const zoom =
            map.getZoom();

        writeJSON(
            STORAGE_VIEW,
            {
                lat: center.lat,
                lon: center.lng,
                zoom: zoom
            }
        );
    }


    // --------------------------------------------------------
    // คำนวณพื้นที่แบบ spherical approximation
    // ใช้สำหรับแสดงสถานะใน component
    // Python จะคำนวณ WGS84 อีกครั้งเป็นค่าหลัก
    // --------------------------------------------------------

    function calculateAreaM2(coords) {

        if (!coords || coords.length < 3) {
            return 0;
        }

        const R = 6378137;

        let area = 0;

        for (
            let i = 0;
            i < coords.length;
            i++
        ) {

            const p1 =
                coords[i];

            const p2 =
                coords[
                    (i + 1) %
                    coords.length
                ];

            const lon1 =
                p1[1] * Math.PI / 180;

            const lat1 =
                p1[0] * Math.PI / 180;

            const lon2 =
                p2[1] * Math.PI / 180;

            const lat2 =
                p2[0] * Math.PI / 180;

            area +=
                (lon2 - lon1) *
                (
                    2 +
                    Math.sin(lat1) +
                    Math.sin(lat2)
                );
        }

        area =
            Math.abs(
                area *
                R *
                R /
                2
            );

        return area;
    }


    function areaLabel(m2) {

        const rai =
            Math.floor(
                m2 / 1600
            );

        let remain =
            m2 -
            rai * 1600;

        const ngan =
            Math.floor(
                remain / 400
            );

        remain -=
            ngan * 400;

        const wa =
            remain / 4;

        return (
            rai.toLocaleString() +
            " ไร่ " +
            ngan.toLocaleString() +
            " งาน " +
            wa.toFixed(2) +
            " ตารางวา"
        );
    }


    // --------------------------------------------------------
    // วาดหมุด
    // --------------------------------------------------------

    function numberedIcon(number) {

        return L.divIcon({

            className: "",

            html:
                '<div style="' +
                'width:30px;' +
                'height:30px;' +
                'border-radius:50%;' +
                'background:#e31b23;' +
                'border:3px solid white;' +
                'box-shadow:0 2px 6px #333;' +
                'color:white;' +
                'font-weight:bold;' +
                'font-size:13px;' +
                'line-height:24px;' +
                'text-align:center;' +
                '">' +
                number +
                '</div>',

            iconSize: [
                30,
                30
            ],

            iconAnchor: [
                15,
                15
            ]
        });
    }


    function redraw() {

        if (!map) {
            return;
        }


        // ลบหมุดเก่า

        markerLayer.forEach(
            marker => {
                map.removeLayer(marker);
            }
        );

        markerLayer = [];


        // ลบ polygon เก่า

        if (polygonLayer) {

            map.removeLayer(
                polygonLayer
            );

            polygonLayer = null;
        }


        // วาดหมุดใหม่

        points.forEach(
            (point, index) => {

                const marker =
                    L.marker(
                        [
                            point[0],
                            point[1]
                        ],
                        {
                            icon:
                                numberedIcon(
                                    index + 1
                                )
                        }
                    ).addTo(map);

                marker.bindTooltip(
                    "จุดที่ " +
                    (index + 1),
                    {
                        direction:
                            "top"
                    }
                );

                markerLayer.push(
                    marker
                );
            }
        );


        // วาด polygon

        if (points.length >= 3) {

            polygonLayer =
                L.polygon(
                    points,
                    {
                        color: "#e31b23",
                        weight: 3,
                        fillColor:
                            "#ffd400",
                        fillOpacity:
                            0.28
                    }
                ).addTo(map);
        }


        const area =
            calculateAreaM2(
                points
            );


        if (points.length >= 3) {

            status.innerText =
                "📍 " +
                points.length +
                " จุด | 📐 " +
                areaLabel(area);

        } else {

            status.innerText =
                "📍 ปักแล้ว " +
                points.length +
                " จุด";
        }
    }


    // --------------------------------------------------------
    // เริ่มแผนที่
    // --------------------------------------------------------

    function initializeMap() {

        if (initialized) {
            return;
        }

        initialized = true;


        const storedView =
            readJSON(
                STORAGE_VIEW,
                null
            );


        let startLat =
            17.4138;

        let startLon =
            102.7875;

        let startZoom =
            17;


        if (
            storedView &&
            Number.isFinite(
                Number(
                    storedView.lat
                )
            ) &&
            Number.isFinite(
          
