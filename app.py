import os
import base64
import streamlit as st
import streamlit.components.v1 as components

# MON101 GALAXY SATELLITE
# Put app.py, logo1.jpg and optional music files in the same GitHub folder.

st.set_page_config(
    page_title="MON101 • GALAXY SATELLITE",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "logo1.jpg")
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".aac", ".flac")
AUDIO_FILES = sorted(
    f for f in os.listdir(APP_DIR)
    if f.lower().endswith(AUDIO_EXTS)
    and os.path.isfile(os.path.join(APP_DIR, f))
)

st.markdown("""
<style>
.stApp {
  background: radial-gradient(ellipse at 50% 0%, #102b55 0%, #071225 42%, #030711 100%);
  color: #f4f8ff;
}
[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1rem; padding-bottom: 2rem; max-width: 1500px;}
h1,h2,h3 {color:#eaf8ff;}
div[data-testid="stMetric"] {
  background:linear-gradient(145deg,#101f3b,#081323);
  border:1px solid #17618b;border-radius:14px;padding:12px 14px;
  box-shadow:0 0 16px #00cfff18;
}
div[data-testid="stMetricLabel"] {color:#9edcf4;}
div[data-testid="stMetricValue"] {color:#fff;}
</style>
""", unsafe_allow_html=True)

# Animated logo hero. The logo remains a normal image file in the repo.
if os.path.isfile(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("ascii")
    logo_html = f'<img class="hero-logo" src="data:image/jpeg;base64,{logo_b64}" alt="MON101">'
else:
    logo_html = '<div class="missing">ไม่พบ logo1.jpg — กรุณาวางไฟล์ไว้ข้าง app.py</div>'

st.markdown(f"""
<style>
.hero {{
  position:relative; overflow:hidden; min-height:255px; margin-bottom:16px;
  border:1px solid #1a9ed0; border-radius:24px;
  background:
    radial-gradient(ellipse at 20% 45%,#123f75 0%,transparent 42%),
    radial-gradient(ellipse at 85% 20%,#38165d 0%,transparent 38%),
    linear-gradient(125deg,#030817,#081b35 55%,#09091d);
  box-shadow:0 0 25px #00cfff35,inset 0 0 35px #1476a533;
  display:flex;align-items:center;justify-content:center;
  padding:22px 16px;perspective:1000px;
}}
.hero:before {{
  content:"";position:absolute;width:370px;height:370px;border:1px solid #00d9ff66;
  border-radius:50%;box-shadow:0 0 25px #00bfff33,inset 0 0 25px #00bfff22;
  animation:orbit 18s linear infinite;
}}
.hero:after {{
  content:"";position:absolute;inset:-30%;
  background:linear-gradient(110deg,transparent 42%,#ffffff16 49%,#00d9ff33 51%,transparent 58%);
  transform:translateX(-100%);animation:beam 7s ease-in-out infinite;pointer-events:none;
}}
.hero-logo {{
  position:relative;z-index:2;width:min(78%,560px);max-height:225px;object-fit:contain;
  filter:drop-shadow(0 0 9px #00cfff) drop-shadow(0 0 24px #4c35ff88);
  animation:logoFloat 5s ease-in-out infinite;transform-style:preserve-3d;
}}
.missing {{
  z-index:2;color:#9cecff;text-align:center;padding:25px;border:1px dashed #00cfff;border-radius:18px;
}}
.hero-tag {{
  position:absolute;z-index:3;bottom:13px;left:0;right:0;text-align:center;
  color:#9beeff;letter-spacing:4px;font-size:12px;font-weight:800;text-shadow:0 0 12px #00cfff;
}}
@keyframes orbit {{to{{transform:rotate(360deg)}}}}
@keyframes beam {{0%,65%{{transform:translateX(-100%)}}100%{{transform:translateX(100%)}}}}
@keyframes logoFloat {{
  0%,100%{{transform:rotateY(-5deg) rotateX(2deg) translateY(0)}}
  50%{{transform:rotateY(5deg) rotateX(-2deg) translateY(-8px)}}
}}
@media(max-width:650px) {{
  .hero{{min-height:200px;padding:14px 8px;border-radius:17px}}
  .hero:before{{width:255px;height:255px}}
  .hero-logo{{width:92%;max-height:155px}}
  .hero-tag{{font-size:9px;letter-spacing:2px}}
}}
</style>
<div class="hero">
  {logo_html}
  <div class="hero-tag">MON101 • GALAXY SATELLITE • FIELD SYSTEM</div>
</div>
""", unsafe_allow_html=True)

st.title("🛰️ MON101 • วัดพื้นที่แปลง")
st.caption("GALAXY SATELLITE FIELD SYSTEM | ภาพดาวเทียม • GPS • ปักหมุด • คำนวณพื้นที่ • ประเมินค่าบริการ")
st.info(
    "วิธีใช้: กด GPS เพื่อไปยังตำแหน่งปัจจุบัน จากนั้นเลื่อน/ซูมภาพให้มุมแปลงอยู่ใต้กากบาท "
    "แล้วกดปักหมุด ทำซ้ำให้ครบทุกมุม (อย่างน้อย 3 จุด) ระบบจะคำนวณพื้นที่ให้อัตโนมัติ"
)

html = r"""
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#030914;color:#f5fbff;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
#map{height:68vh;min-height:470px;width:100%;position:relative;background:#101c2b}
.topbar{position:absolute;z-index:2000;top:10px;left:10px;right:10px;display:flex;gap:7px;flex-wrap:wrap;pointer-events:none}
.topbar button{pointer-events:auto;border:1px solid #ffffff66;border-radius:11px;padding:10px 13px;background:#07172bef;color:#fff;font-weight:800;font-size:14px;box-shadow:0 0 12px #00cfff55}
#gps{border-color:#00d9ff;color:#9ff5ff}#pin{border-color:#00ff9d;color:#baffdd}
#photo{border-color:#ffc84a;color:#ffe6a0}#new{border-color:#ff5577;color:#ffb5c5}
#undo{border-color:#b77aff;color:#e0c4ff}#reload{border-color:#46aaff;color:#b5e3ff}
.crosshair{position:absolute;z-index:1900;left:50%;top:50%;width:46px;height:46px;transform:translate(-50%,-50%);pointer-events:none;filter:drop-shadow(0 0 4px #000)}
.crosshair:before,.crosshair:after{content:"";position:absolute;background:#ff2929;box-shadow:0 0 4px #fff}
.crosshair:before{width:46px;height:3px;left:0;top:21px}
.crosshair:after{width:3px;height:46px;left:21px;top:0}
.cross-dot{position:absolute;left:50%;top:50%;width:10px;height:10px;transform:translate(-50%,-50%);border:2px solid white;background:#ff2020;border-radius:50%}
#loading{position:absolute;z-index:1800;left:50%;top:50%;transform:translate(-50%,-50%);background:#061326ed;color:white;padding:14px 18px;border:1px solid #00cfff;border-radius:12px;font-weight:800;box-shadow:0 0 22px #00cfff66;text-align:center;display:block}
.panel{background:linear-gradient(135deg,#071326,#101b34);color:#f9fafb;padding:12px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;border:1px solid #164b70;border-top:0}
.card{background:linear-gradient(145deg,#142643,#091426);border:1px solid #23527a;border-radius:11px;padding:10px;min-width:0}
.label{font-size:12px;color:#8fdcf7}.value{font-size:19px;font-weight:850;margin-top:3px;color:#fff;overflow-wrap:anywhere}
#status{grid-column:1/-1;color:#b9d8e8;font-size:13px;padding:5px}
@media(max-width:700px){#map{height:65vh;min-height:440px}.topbar{gap:5px}.topbar button{padding:9px 10px;font-size:12px}.panel{grid-template-columns:repeat(2,minmax(0,1fr))}.value{font-size:17px}}
@media print{html,body{background:white!important}#map{height:100vh!important;min-height:100vh!important}.panel,.topbar,#loading{display:none!important}.leaflet-control-zoom,.leaflet-control-attribution{display:none!important}}
</style>
</head>
<body>
<div id="map">
 <div id="loading">🛰️ กำลังเชื่อมต่อภาพดาวเทียม...</div>
 <div class="topbar">
  <button id="gps">📍 GPS</button><button id="pin">📌 ปักหมุด</button>
  <button id="undo">↩️ ลบล่าสุด</button><button id="new">🗑️ เริ่มใหม่</button>
  <button id="reload">🛰️ โหลดภาพใหม่</button><button id="photo">📷 พิมพ์/บันทึก</button>
 </div>
 <div class="crosshair" id="crosshair"><div class="cross-dot"></div></div>
</div>
<div class="panel">
 <div class="card"><div class="label">จุดที่ปัก</div><div class="value" id="points">0</div></div>
 <div class="card"><div class="label">พื้นที่ ตร.ม.</div><div class="value" id="m2">0.00</div></div>
 <div class="card"><div class="label">พื้นที่ ไร่ (ทศนิยม)</div><div class="value" id="rai">0.0000</div></div>
 <div class="card"><div class="label">งาน</div><div class="value" id="ngan">0</div></div>
 <div class="card"><div class="label">ตารางวา</div><div class="value" id="sqw">0.00</div></div>
 <div class="card"><div class="label">ไถ 250 บาท/ไร่</div><div class="value" id="plow">0.00 ฿</div></div>
 <div class="card"><div class="label">พรวน 350 บาท/ไร่</div><div class="value" id="till">0.00 ฿</div></div>
 <div class="card"><div class="label">ไถ + พรวน 600 บาท/ไร่</div><div class="value" id="both">0.00 ฿</div></div>
 <div class="card" style="grid-column:1/-1"><div class="label">หน่วยพื้นที่แบบไทย</div><div class="value" id="thaiArea">0 ไร่ 0 งาน 0 ตารางวา</div></div>
 <div id="status">กำลังโหลดภาพดาวเทียม...</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function(){
"use strict";
const $=id=>document.getElementById(id);
function status(t){$("status").textContent=t}
function showLoading(t){$("loading").textContent=t;$("loading").style.display="block"}
function hideLoading(){$("loading").style.display="none"}
if(typeof L==="undefined"){showLoading("โหลด Leaflet ไม่สำเร็จ กรุณาตรวจอินเทอร์เน็ตแล้วรีเฟรช");status("ไม่สามารถโหลดระบบแผนที่ได้");return}

const VIEW_KEY="mon101_galaxy_view_v12";
const POINT_KEY="mon101_galaxy_points_v12";
const defaultView={lat:17.4138,lng:102.7875,zoom:17};
function load(key,fallback){try{const v=localStorage.getItem(key);return v?JSON.parse(v):fallback}catch(e){return fallback}}
function save(key,value){try{localStorage.setItem(key,JSON.stringify(value))}catch(e){}}
const savedView=load(VIEW_KEY,defaultView);
const map=L.map("map",{center:[Number(savedView.lat)||defaultView.lat,Number(savedView.lng)||defaultView.lng],zoom:Number(savedView.zoom)||defaultView.zoom,zoomControl:true,maxZoom:20,minZoom:3});
const SAT_URL="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";
let satellite=L.tileLayer(SAT_URL,{maxZoom:20,maxNativeZoom:19,attribution:"Tiles © Esri"}).addTo(map);
let gotTile=false, tileErrors=0;
satellite.on("tileload",()=>{gotTile=true;tileErrors=0;hideLoading();status("🛰️ ภาพดาวเทียมพร้อมแล้ว — เลื่อน/ซูมให้มุมแปลงตรงกากบาท")});
satellite.on("tileerror",()=>{tileErrors++;if(!gotTile&&tileErrors>=3){showLoading("ภาพดาวเทียมโหลดไม่สำเร็จ ลองกดโหลดภาพใหม่");status("ตรวจสอบอินเทอร์เน็ตหรือเซิร์ฟเวอร์ภาพดาวเทียม")}});
setTimeout(()=>map.invalidateSize(true),500);

let points=load(POINT_KEY,[]);
if(!Array.isArray(points))points=[];
const pointLayer=L.layerGroup().addTo(map);
const shapeLayer=L.layerGroup().addTo(map);

function areaM2(coords){
 if(coords.length<3)return 0;
 const R=6378137;let sum=0;
 for(let i=0;i<coords.length;i++){
  const p=coords[i],q=coords[(i+1)%coords.length];
  const x=p[1]*Math.PI/180,y=p[0]*Math.PI/180;
  const u=q[1]*Math.PI/180,w=q[0]*Math.PI/180;
  sum+=(u-x)*(2+Math.sin(y)+Math.sin(w));
 }
 return Math.abs(sum*R*R/2);
}
function fmt(n,d){return Number(n||0).toLocaleString("th-TH",{minimumFractionDigits:d,maximumFractionDigits:d})}
function render(){
 pointLayer.clearLayers();shapeLayer.clearLayers();
 points.forEach((p,i)=>L.circleMarker(p,{radius:6,weight:2,color:"#fff",fillColor:"#ff3030",fillOpacity:1}).bindTooltip("จุด "+(i+1)).addTo(pointLayer));
 if(points.length>=2)L.polyline(points,{color:"#00ff9d",weight:3,opacity:.95,dashArray:"8 5"}).addTo(shapeLayer);
 if(points.length>=3)L.polygon(points,{color:"#00ff9d",weight:3,fillColor:"#22c55e",fillOpacity:.2}).addTo(shapeLayer);
 const m=areaM2(points), raiDecimal=m/1600;
 const rai=Math.floor(m/1600), afterRai=m-rai*1600;
 const ngan=Math.floor(afterRai/400), sqw=(afterRai-ngan*400)/4;
 $("points").textContent=points.length;
 $("m2").textContent=fmt(m,2);
 $("rai").textContent=fmt(raiDecimal,4);
 $("ngan").textContent=ngan;
 $("sqw").textContent=fmt(sqw,2);
 $("thaiArea").textContent=rai+" ไร่ "+ngan+" งาน "+fmt(sqw,2)+" ตารางวา";
 $("plow").textContent=fmt(raiDecimal*250,2)+" ฿";
 $("till").textContent=fmt(raiDecimal*350,2)+" ฿";
 $("both").textContent=fmt(raiDecimal*600,2)+" ฿";
 save(POINT_KEY,points);
}
map.on("moveend",()=>{const c=map.getCenter();save(VIEW_KEY,{lat:c.lat,lng:c.lng,zoom:map.getZoom()})});

$("gps").onclick=function(){
 if(!navigator.geolocation){status("อุปกรณ์หรือเบราว์เซอร์นี้ไม่รองรับ GPS");return}
 status("กำลังค้นหาตำแหน่ง GPS — กรุณาอนุญาตตำแหน่ง");
 navigator.geolocation.getCurrentPosition(
  p=>{map.setView([p.coords.latitude,p.coords.longitude],19,{animate:true});status("พบตำแหน่ง GPS แล้ว — เลื่อนภาพให้มุมแปลงตรงกากบาท")},
  e=>{status("GPS ใช้งานไม่ได้: "+e.message+" (ต้องเปิดผ่าน HTTPS และอนุญาตตำแหน่ง)")},
  {enableHighAccuracy:true,timeout:20000,maximumAge:0}
 );
};
$("pin").onclick=function(){
 const c=map.getCenter();points.push([Number(c.lat.toFixed(8)),Number(c.lng.toFixed(8))]);
 render();status("📌 ปักหมุดแล้ว "+points.length+" จุด — เลื่อนไปยังมุมถัดไปได้เลย");
};
$("undo").onclick=function(){if(points.length){points.pop();render();status("ลบจุดล่าสุดแล้ว")}else status("ยังไม่มีจุดให้ลบ")};
$("new").onclick=function(){if(confirm("เริ่มแปลงใหม่และลบจุดที่ปักทั้งหมดหรือไม่?")){points=[];render();status("เริ่มแปลงใหม่แล้ว")}};
$("reload").onclick=function(){
 showLoading("🛰️ กำลังโหลดภาพดาวเทียมใหม่...");gotTile=false;tileErrors=0;
 map.removeLayer(satellite);
 satellite=L.tileLayer(SAT_URL,{maxZoom:20,maxNativeZoom:19,attribution:"Tiles © Esri"}).addTo(map);
 setTimeout(()=>map.invalidateSize(true),300);
};
$("photo").onclick=function(){
 $("crosshair").style.visibility="hidden";
 setTimeout(()=>{window.print();$("crosshair").style.visibility="";status("ใช้เมนูพิมพ์ของเบราว์เซอร์เพื่อบันทึกเป็น PDF หรือภาพ")},150);
};
render();
})();
</script>
</body>
</html>
"""

# Keep enough height for map + calculation panel on mobile/desktop.
components.html(html, height=900, scrolling=True)

st.divider()
st.subheader("🎵 เครื่องเล่นเพลง")
if AUDIO_FILES:
    for filename in AUDIO_FILES:
        st.write("🎵 " + filename)
        file_path = os.path.join(APP_DIR, filename)
        audio_format = "audio/mpeg" if filename.lower().endswith(".mp3") else None
        st.audio(file_path, format=audio_format)
else:
    st.caption("วางไฟล์ .mp3 / .wav / .m4a / .ogg ไว้โฟลเดอร์เดียวกับ app.py ได้")

st.divider()
st.subheader("💰 อัตราค่าบริการ")
a, b, c = st.columns(3)
a.metric("ไถ", "250 บาท/ไร่")
b.metric("พรวน/ปั่นดิน", "350 บาท/ไร่")
c.metric("ไถ + พรวน", "600 บาท/ไร่")

st.caption("หมายเหตุ: GPS ใช้ตำแหน่งของอุปกรณ์ที่เปิดแอปเท่านั้น ต้องอนุญาตตำแหน่งและเปิดเว็บผ่าน HTTPS; ค่าพื้นที่เป็นค่าประมาณจากพิกัดที่ปัก ควรตรวจสอบกับการวัดภาคสนามก่อนใช้คิดค่าบริการจริง")
