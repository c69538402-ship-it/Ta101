import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mon101 วัดพื้นที่แปลง", page_icon="📐", layout="wide")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_DIR, "logo.jpg")
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg")
AUDIO_FILES = sorted(
    f for f in os.listdir(APP_DIR)
    if f.lower().endswith(AUDIO_EXTS) and os.path.isfile(os.path.join(APP_DIR, f))
)

if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=110)

st.title("📐 Mon101 วัดพื้นที่แปลง")
st.caption("ภาพดาวเทียมเท่านั้น • GPS • กากบาทกลางจอ • ปักหมุด • บันทึกภาพ")

st.info(
    "กด GPS → รอภาพดาวเทียม → ซูม/เลื่อนให้มุมแปลงตรงกากบาท → "
    "กด 📌 ปักหมุด → ทำซ้ำจนครบ → กด 📷 บันทึกภาพ"
)

html = r"""
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">

<link rel="stylesheet"
 href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"
 crossorigin="anonymous">

<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#111827;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
#map{height:72vh;min-height:520px;width:100%;position:relative;background:#b7c59c}
.topbar{
 position:absolute;z-index:2000;top:10px;left:10px;right:10px;
 display:flex;gap:7px;flex-wrap:wrap;pointer-events:none
}
.topbar button{
 pointer-events:auto;border:0;border-radius:12px;padding:10px 13px;
 background:#ffffffee;color:#111827;font-weight:800;font-size:15px;
 box-shadow:0 2px 10px #0005
}
#gps{background:#dbeafe}#pin{background:#dcfce7}#photo{background:#fde68a}
#new{background:#fee2e2}#undo{background:#f3e8ff}#reload{background:#dff3ff}
.crosshair{
 position:absolute;z-index:1900;left:50%;top:50%;width:44px;height:44px;
 transform:translate(-50%,-50%);pointer-events:none
}
.crosshair:before,.crosshair:after{
 content:"";position:absolute;background:#ff2020;box-shadow:0 0 3px #fff
}
.crosshair:before{width:44px;height:3px;left:0;top:20px}
.crosshair:after{width:3px;height:44px;left:20px;top:0}
.cross-dot{
 position:absolute;left:50%;top:50%;width:9px;height:9px;
 transform:translate(-50%,-50%);border:2px solid white;background:#ff2020;border-radius:50%
}
#loading{
 position:absolute;z-index:1800;left:50%;top:50%;transform:translate(-50%,-50%);
 background:#111827ee;color:white;padding:14px 18px;border-radius:12px;
 font-weight:800;box-shadow:0 4px 20px #0007;text-align:center;display:block
}
#mapmsg{
 position:absolute;z-index:1700;left:50%;bottom:12px;transform:translateX(-50%);
 background:#111827dd;color:#fff;padding:7px 12px;border-radius:10px;
 font-size:12px;display:none;white-space:nowrap
}
.panel{
 background:#111827;color:#f9fafb;padding:12px 14px;
 display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px
}
.card{background:#1f2937;border-radius:10px;padding:10px}
.label{font-size:12px;color:#9ca3af}.value{font-size:19px;font-weight:800;margin-top:2px}
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
 <div id="loading">🛰️ กำลังโหลดภาพดาวเทียม...</div>
 <div id="mapmsg"></div>

 <div class="topbar" data-html2canvas-ignore="true">
  <button id="gps">📍 GPS</button>
  <button id="pin">📌 ปักหมุด</button>
  <button id="undo">↩️ ลบล่าสุด</button>
  <button id="new">🗑️ เริ่มใหม่</button>
  <button id="reload">🛰️ โหลดภาพใหม่</button>
  <button id="photo">📷 บันทึกภาพ</button>
 </div>

 <div class="crosshair" id="crosshair" data-html2canvas-ignore="true">
  <div class="cross-dot"></div>
 </div>
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
 <div id="status">กำลังโหลดภาพดาวเทียม...</div>
</div>

<script
 src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"
 crossorigin="anonymous"></script>

<script>
(function(){
"use strict";

function status(t){document.getElementById("status").textContent=t}
function showLoading(t){
 const x=document.getElementById("loading");
 x.textContent=t;x.style.display="block";
}
function hideLoading(){document.getElementById("loading").style.display="none"}

if(typeof L==="undefined"){
 document.getElementById("loading").innerHTML=
  "⚠️ โหลดระบบแผนที่ไม่สำเร็จ<br>กำลังลองใหม่...";
 setTimeout(function(){location.reload()},2500);
 return;
}

const VIEW_KEY="mon101_satellite_view_v11";
const POINT_KEY="mon101_satellite_points_v11";
const defaultView={lat:17.4138,lng:102.7875,zoom:17};

function load(k,f){
 try{const x=localStorage.getItem(k);return x?JSON.parse(x):f}
 catch(e){return f}
}
function save(k,v){
 try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}
}

const v=load(VIEW_KEY,defaultView);

const map=L.map("map",{
 center:[Number(v.lat)||defaultView.lat,Number(v.lng)||defaultView.lng],
 zoom:Number(v.zoom)||defaultView.zoom,
 zoomControl:true,
 attributionControl:true,
 maxZoom:20,
 minZoom:3
});

/* ใช้ภาพดาวเทียม Esri โดยตรงเท่านั้น */
const SAT_URL=
 "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";

let sat=L.tileLayer(SAT_URL,{
 maxZoom:20,
 maxNativeZoom:19,
 attribution:"Tiles © Esri"
}).addTo(map);

let firstTile=false;
let tileErrors=0;

sat.on("tileload",function(){
 firstTile=true;
 tileErrors=0;
 hideLoading();
 status("🛰️ ภาพดาวเทียมพร้อมแล้ว — เลื่อน/ซูมให้มุมแปลงตรงกากบาท");
});

sat.on("tileerror",function(){
 tileErrors++;
 if(!firstTile && tileErrors>=3){
   showLoading("⚠️ ภาพดาวเทียมกำลังโหลดช้า<br>ลองกด 🛰️ โหลดภาพใหม่");
   status("ยังรับภาพดาวเทียมไม่ได้จากเซิร์ฟเวอร์");
 }
});

setTimeout(function(){
 map.invalidateSize(true);
 if(!firstTile){
   status("กำลังรอภาพดาวเทียม... หากยังมืดให้กด 🛰️ โหลดภาพใหม่");
 }
},500);

const points=load(POINT_KEY,[]);
if(!Array.isArray(points))points=[];
const markers=L.layerGroup().addTo(map);
const lines=L.layerGroup().addTo(map);

function areaM2(a){
 if(a.length<3)return 0;
 const R=6378137;
 let s=0;
 for(let i=0;i<a.length;i++){
  const p=a[i],q=a[(i+1)%a.length];
  const x=p[1]*Math.PI/180,y=p[0]*Math.PI/180;
  const u=q[1]*Math.PI/180,w=q[0]*Math.PI/180;
  s+=(u-x)*(2+Math.sin(y)+Math.sin(w));
 }
 return Math.abs(s*R*R/2);
}

function fmt(n,d){
 return Number(n||0).toLocaleString("th-TH",{
  minimumFractionDigits:d,maximumFractionDigits:d
 });
}

function render(){
 markers.clearLayers();
 lines.clearLayers();

 points.forEach(function(p){
  L.circleMarker(p,{
   radius:5,weight:2,color:"#fff",fillColor:"#ef4444",fillOpacity:1
  }).addTo(markers);
 });

 if(points.length>=2){
  L.polyline(points,{color:"#00ff66",weight:4,opacity:.95}).addTo(lines);
 }
 if(points.length>=3){
  L.polygon(points,{
   color:"#00ff66",weight:3,fillColor:"#22c55e",fillOpacity:.18
  }).addTo(lines);
 }

 const m=areaM2(points),r=m/1600;
 document.getElementById("points").textContent=points.length;
 document.getElementById("m2").textContent=fmt(m,2);
 document.getElementById("rai").textContent=fmt(r,4);
 document.getElementById("ngan").textContent=fmt(m/400,2);
 document.getElementById("sqw").textContent=fmt(m/4,2);
 document.getElementById("plow").textContent=fmt(r*250,2)+" ฿";
 document.getElementById("till").textContent=fmt(r*350,2)+" ฿";
 document.getElementById("both").textContent=fmt(r*600,2)+" ฿";

 save(POINT_KEY,points);
}

map.on("moveend",function(){
 const c=map.getCenter();
 save(VIEW_KEY,{lat:c.lat,lng:c.lng,zoom:map.getZoom()});
});

document.getElementById("gps").onclick=function(){
 if(!navigator.geolocation){
  status("อุปกรณ์นี้ไม่รองรับ GPS");return;
 }
 status("กำลังค้นหา GPS...");
 navigator.geolocation.getCurrentPosition(
  function(p){
   map.setView([p.coords.latitude,p.coords.longitude],19,{animate:true});
   status("ถึงตำแหน่ง GPS แล้ว — เลื่อนภาพให้มุมแปลงตรงกากบาท");
  },
  function(e){
   status("GPS ใช้งานไม่ได้: "+(e.message||"กรุณาอนุญาตตำแหน่ง"));
  },
  {enableHighAccuracy:true,timeout:15000,maximumAge:0}
 );
};

document.getElementById("pin").onclick=function(){
 const c=map.getCenter();
 points.push([
  Number(c.lat.toFixed(8)),
  Number(c.lng.toFixed(8))
 ]);
 render();
 status("📌 ปักหมุดแล้ว "+points.length+" จุด — ไปมุมถัดไปได้เลย");
};

document.getElementById("undo").onclick=function(){
 if(points.length){
  points.pop();render();status("ลบจุดล่าสุดแล้ว");
 }else status("ยังไม่มีจุดให้ลบ");
};

document.getElementById("new").onclick=function(){
 if(confirm("เริ่มแปลงใหม่? จุดที่ยังไม่ได้บันทึกจะถูกลบ")){
  points.length=0;render();status("เริ่มแปลงใหม่แล้ว");
 }
};

document.getElementById("reload").onclick=function(){
 showLoading("🛰️ กำลังโหลดภาพดาวเทียมใหม่...");
 tileErrors=0;firstTile=false;
 map.removeLayer(sat);
 sat=L.tileLayer(SAT_URL,{
  maxZoom:20,maxNativeZoom:19,attribution:"Tiles © Esri"
 }).addTo(map);
 setTimeout(function(){map.invalidateSize(true)},300);
};

document.getElementById("photo").onclick=function(){
 /*
  ไม่พยายามแปลง tile ดาวเทียมเป็น canvas เพราะเบราว์เซอร์มือถืออาจบล็อก
  ภาพข้ามโดเมน ทำให้ภาพออกมามืด/ว่าง
  ใช้เมนูพิมพ์ของเบราว์เซอร์แทนเพื่อเก็บภาพที่ผู้ใช้เห็นจริง
 */
 document.getElementById("crosshair").style.visibility="hidden";
 setTimeout(function(){
  window.print();
  document.getElementById("crosshair").style.visibility="";
  status("เลือกบันทึก/พิมพ์จากเมนูของโทรศัพท์ได้");
 },150);
};

render();
})();
</script>

<style>
@media print{
 html,body{background:white!important}
 #map{height:100vh!important;min-height:100vh!important}
 .panel,.topbar,#loading,#mapmsg{display:none!important}
 .leaflet-control-zoom,.leaflet-control-attribution{display:none!important}
}
</style>

</body>
</html>
"""

components.html(html, height=900, scrolling=False)

st.divider()
st.subheader("🎵 เครื่องเล่นเพลง")
if AUDIO_FILES:
    for f in AUDIO_FILES:
        st.write("🎵 " + f)
        st.audio(os.path.join(APP_DIR, f))
else:
    st.caption("วางไฟล์ .mp3 / .wav / .m4a / .ogg ไว้โฟลเดอร์เดียวกับ app.py ได้เลย")

st.subheader("💰 อัตราค่าบริการ")
a,b,c=st.columns(3)
a.metric("ไถ","250 บาท/ไร่")
b.metric("พรวน/ปั่นดิน","350 บาท/ไร่")
c.metric("ไถ + พรวน","600 บาท/ไร่")
