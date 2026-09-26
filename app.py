import os
import json
import csv
import io
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mon101 วัดพื้นที่แปลง",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "logo.jpg")

# ค้นหาเพลง .mp3/.wav/.m4a ในโฟลเดอร์เดียวกับ app.py โดยไม่ต้องมีไฟล์ music.py
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg")
AUDIO_FILES = sorted(
    f for f in os.listdir(APP_DIR)
    if f.lower().endswith(AUDIO_EXTS) and os.path.isfile(os.path.join(APP_DIR, f))
)

if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=110)

st.title("📐 Mon101 วัดพื้นที่แปลง")
st.caption("ภาพดาวเทียม • GPS • กากบาทกลางจอ • ปักหมุดทีละมุม • คำนวณ ไร่/งาน/ตารางวา")

st.info(
    "วิธีใช้: กด GPS เพื่อไปบริเวณแปลง → ซูม/เลื่อนภาพดาวเทียมให้มุมแปลงอยู่ตรงกากบาทกลางจอ "
    "→ กด 📌 ปักหมุด → ทำซ้ำจนครบทุกมุม → กด 💾 บันทึก"
)

html = r"""
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#111827;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
#map{height:72vh;min-height:520px;width:100%;position:relative}
.leaflet-control-attribution{font-size:9px}
.topbar{
  position:absolute;z-index:1000;top:10px;left:10px;right:10px;
  display:flex;gap:7px;flex-wrap:wrap;pointer-events:none;
}
.topbar button{
  pointer-events:auto;border:0;border-radius:10px;padding:10px 12px;
  background:#ffffffee;color:#111827;font-weight:700;font-size:14px;
  box-shadow:0 2px 10px #0005;
}
.topbar button:active{transform:scale(.97)}
#gps{background:#dbeafe}
#pin{background:#dcfce7}
#save{background:#fef3c7}
#new{background:#fee2e2}
#undo{background:#f3e8ff}
.crosshair{
 position:absolute;z-index:900;left:50%;top:50%;width:42px;height:42px;
 transform:translate(-50%,-50%);pointer-events:none;
}
.crosshair:before,.crosshair:after{content:"";position:absolute;background:#ff2d2d;box-shadow:0 0 2px #fff}
.crosshair:before{width:42px;height:3px;left:0;top:19px}
.crosshair:after{width:3px;height:42px;left:19px;top:0}
.cross-dot{
 position:absolute;left:50%;top:50%;width:9px;height:9px;
 transform:translate(-50%,-50%);border:2px solid white;background:#ff2d2d;border-radius:50%;
}
.panel{
 background:#111827;color:#f9fafb;padding:12px 14px;
 display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;
}
.card{background:#1f2937;border-radius:10px;padding:10px}
.label{font-size:12px;color:#9ca3af}
.value{font-size:19px;font-weight:800;margin-top:2px}
#status{grid-column:1/-1;color:#d1d5db;font-size:13px}
@media(max-width:700px){
 #map{height:68vh;min-height:460px}
 .topbar{gap:5px}
 .topbar button{padding:9px 10px;font-size:13px}
 .panel{grid-template-columns:repeat(2,minmax(0,1fr))}
}
</style>
</head>
<body>
<div id="map">
  <div class="topbar">
    <button id="gps">📍 GPS</button>
    <button id="pin">📌 ปักหมุด</button>
    <button id="undo">↩️ ลบล่าสุด</button>
    <button id="new">🗑️ เริ่มใหม่</button>
    <button id="save">💾 บันทึก</button>
  </div>
  <div class="crosshair"><div class="cross-dot"></div></div>
</div>

<div class="panel">
  <div class="card"><div class="label">จุดที่ปัก</div><div class="value" id="points">0</div></div>
  <div class="card"><div class="label">พื้นที่ ตร.ม.</div><div class="value" id="m2">0.00</div></div>
  <div class="card"><div class="label">ไร่</div><div class="value" id="rai">0.0000</div></div>
  <div class="card"><div class="label">งาน</div><div class="value" id="ngan">0.00</div></div>
  <div class="card"><div class="label">ตารางวา</div><div class="value" id="sqw">0.00</div></div>
  <div class="card"><div class="label">ไถ 250/ไร่</div><div class="value" id="plow">0.00 ฿</div></div>
  <div class="card"><div class="label">พรวน 350/ไร่</div><div class="value" id="till">0.00 ฿</div></div>
  <div class="card"><div class="label">ไถ+พรวน 600/ไร่</div><div class="value" id="both">0.00 ฿</div></div>
  <div id="status">พร้อมใช้งาน: เลื่อนแผนที่ให้มุมแปลงตรงกากบาท แล้วกดปักหมุด</div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function(){
"use strict";

const VIEW_KEY="mon101_satellite_view_v8";
const POINT_KEY="mon101_satellite_points_v8";
const RECORD_KEY="mon101_satellite_records_v8";

const defaultView={lat:17.4138,lng:102.7875,zoom:17};

function loadJSON(key,fallback){
  try{
    const x=localStorage.getItem(key);
    return x?JSON.parse(x):fallback;
  }catch(e){return fallback;}
}
function saveJSON(key,value){
  try{localStorage.setItem(key,JSON.stringify(value));}catch(e){}
}

const savedView=loadJSON(VIEW_KEY,defaultView);
const map=L.map("map",{
  center:[Number(savedView.lat)||defaultView.lat,Number(savedView.lng)||defaultView.lng],
  zoom:Number(savedView.zoom)||defaultView.zoom,
  zoomControl:true,
  attributionControl:true,
  maxZoom:20
});

const satellite=L.tileLayer(
 "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
 {
   maxZoom:20,
   maxNativeZoom:19,
   attribution:"Tiles © Esri"
 }
).addTo(map);

let points=loadJSON(POINT_KEY,[]);
if(!Array.isArray(points)) points=[];

let records=loadJSON(RECORD_KEY,[]);
if(!Array.isArray(records)) records=[];

let markerLayer=L.layerGroup().addTo(map);
let lineLayer=L.layerGroup().addTo(map);

function areaM2(a){
 if(a.length<3) return 0;
 const R=6378137;
 let s=0;
 for(let i=0;i<a.length;i++){
   const p=a[i], q=a[(i+1)%a.length];
   const x=p[1]*Math.PI/180, y=p[0]*Math.PI/180;
   const u=q[1]*Math.PI/180, v=q[0]*Math.PI/180;
   s+=(u-x)*(2+Math.sin(y)+Math.sin(v));
 }
 return Math.abs(s*R*R/2);
}

function format(n,d){
 return Number(n||0).toLocaleString("th-TH",{minimumFractionDigits:d,maximumFractionDigits:d});
}

function units(m2){
 const rai=m2/1600;
 const ngan=m2/400;
 const sqw=m2/4;
 return {rai,ngan,sqw};
}

function render(){
 markerLayer.clearLayers();
 lineLayer.clearLayers();

 points.forEach((p,i)=>{
   const m=L.circleMarker([p[0],p[1]],{
     radius:8,weight:3,color:"#ffffff",fillColor:"#ef4444",fillOpacity:1
   }).addTo(markerLayer);
   m.bindTooltip(String(i+1),{permanent:true,direction:"top",offset:[0,-8]});
 });

 if(points.length>=2){
   L.polyline(points,{color:"#00ff66",weight:4,opacity:.95}).addTo(lineLayer);
 }
 if(points.length>=3){
   L.polygon(points,{
     color:"#00ff66",weight:3,fillColor:"#22c55e",fillOpacity:.20
   }).addTo(lineLayer);
 }

 const m2=areaM2(points);
 const u=units(m2);
 document.getElementById("points").textContent=points.length;
 document.getElementById("m2").textContent=format(m2,2);
 document.getElementById("rai").textContent=format(u.rai,4);
 document.getElementById("ngan").textContent=format(u.ngan,2);
 document.getElementById("sqw").textContent=format(u.sqw,2);
 document.getElementById("plow").textContent=format(u.rai*250,2)+" ฿";
 document.getElementById("till").textContent=format(u.rai*350,2)+" ฿";
 document.getElementById("both").textContent=format(u.rai*600,2)+" ฿";
 saveJSON(POINT_KEY,points);
}

function status(t){
 document.getElementById("status").textContent=t;
}

map.on("moveend",()=>{
 const c=map.getCenter();
 saveJSON(VIEW_KEY,{lat:c.lat,lng:c.lng,zoom:map.getZoom()});
});

document.getElementById("gps").addEventListener("click",()=>{
 if(!navigator.geolocation){
   status("อุปกรณ์/เบราว์เซอร์นี้ไม่รองรับ GPS");
   return;
 }
 status("กำลังค้นหาตำแหน่ง GPS...");
 navigator.geolocation.getCurrentPosition(
   p=>{
     map.setView([p.coords.latitude,p.coords.longitude],19,{animate:true});
     status("ไปยังตำแหน่ง GPS แล้ว — กรุณาซูมและเลื่อนให้มุมแปลงตรงกากบาทก่อนปักหมุด");
   },
   e=>{
     status("GPS ใช้งานไม่ได้: "+(e.message||"กรุณาอนุญาตตำแหน่ง"));
   },
   {enableHighAccuracy:true,timeout:15000,maximumAge:0}
 );
});

document.getElementById("pin").addEventListener("click",()=>{
 const c=map.getCenter();
 points.push([Number(c.lat.toFixed(8)),Number(c.lng.toFixed(8))]);
 render();
 status("ปักหมุดจุดที่ "+points.length+" แล้ว — เลื่อนแผนที่ไปมุมถัดไปได้เลย");
});

document.getElementById("undo").addEventListener("click",()=>{
 if(points.length){
   points.pop();
   render();
   status("ลบจุดล่าสุดแล้ว");
 }else{
   status("ยังไม่มีจุดให้ลบ");
 }
});

document.getElementById("new").addEventListener("click",()=>{
 if(!confirm("เริ่มแปลงใหม่? จุดที่ยังไม่ได้บันทึกจะถูกลบ")) return;
 points=[];
 render();
 status("เริ่มแปลงใหม่แล้ว");
});

document.getElementById("save").addEventListener("click",()=>{
 if(points.length<3){
   status("ต้องมีอย่างน้อย 3 จุดจึงจะบันทึกพื้นที่ได้");
   return;
 }
 const m2=areaM2(points);
 const u=units(m2);
 const rec={
   date:new Date().toISOString(),
   points:points.map(p=>[p[0],p[1]]),
   area_m2:Number(m2.toFixed(2)),
   rai:Number(u.rai.toFixed(6)),
   ngan:Number(u.ngan.toFixed(4)),
   square_wah:Number(u.sqw.toFixed(2)),
   price_plow:Number((u.rai*250).toFixed(2)),
   price_till:Number((u.rai*350).toFixed(2)),
   price_both:Number((u.rai*600).toFixed(2))
 };
 records.push(rec);
 saveJSON(RECORD_KEY,records);
 downloadText("mon101_last_record.json",JSON.stringify(rec,null,2),"application/json");
 status("บันทึกแปลงแล้ว และดาวน์โหลดข้อมูลแปลงล่าสุดให้แล้ว");
});

function downloadText(name,text,type){
 const blob=new Blob([text],{type});
 const url=URL.createObjectURL(blob);
 const a=document.createElement("a");
 a.href=url;a.download=name;
 document.body.appendChild(a);a.click();a.remove();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
}

render();
})();
</script>
</body>
</html>
"""

components.html(html, height=900, scrolling=False)

st.divider()
st.subheader("🎵 เครื่องเล่นเพลง")
if AUDIO_FILES:
    for filename in AUDIO_FILES:
        st.write(f"🎵 {filename}")
        st.audio(os.path.join(APP_DIR, filename))
else:
    st.caption("ถ้ามีไฟล์เพลง .mp3 / .wav / .m4a / .ogg อยู่โฟลเดอร์เดียวกับ app.py แอปจะแสดงเพลงให้อัตโนมัติ โดยไม่ต้องสร้าง music.py")

st.subheader("💰 อัตราค่าบริการ")
c1, c2, c3 = st.columns(3)
c1.metric("ไถ", "250 บาท/ไร่")
c2.metric("พรวน/ปั่นดิน", "350 บาท/ไร่")
c3.metric("ไถ + พรวน", "600 บาท/ไร่")

st.caption(
    "หมายเหตุ: พื้นที่จากภาพดาวเทียมและ GPS เป็นการวัดสำหรับงานภาคสนาม/ตกลงพื้นที่ "
    "ไม่ใช่การรังวัดที่ดินตามกฎหมาย หากเป็นข้อพิพาทเขตที่ดินควรใช้การรังวัดโดยหน่วยงานหรือช่างรังวัดที่เกี่ยวข้อง"
)
