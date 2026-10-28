import base64
import json
import mimetypes
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

# 1. ดึงไฟล์เพลง .mp3 ทั้งหมดจากหน้าหลัก (Root Directory)
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
  if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
    try:
      mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
      encoded = base64.b64encode(path.read_bytes()).decode("ascii")
      songs.append(
          {
              "name": path.stem,
              "src": f"data:{mime};base64,{encoded}",
          }
      )
    except OSError:
      continue

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")

# 2. ค้นหารูปโลโก้ logo1.jpg (หรือนามสกุลใกล้เคียง)
logo_data = ""
for candidate in (
    "logo1.jpg",
    "logo1.jpeg",
    "logo1.png",
    "โลโก้.jpg",
    "logo.jpg",
):
  logo_path = ROOT / candidate
  if logo_path.is_file():
    try:
      mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
      logo_data = f"data:{mime};base64,{base64.b64encode(logo_path.read_bytes()).decode('ascii')}"
      break
    except OSError:
      pass

logo_json = json.dumps(logo_data)

# 3. HTML / Three.js / Web Audio API Component
player_html = (
    r"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Prompt:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--a:#00f5ff;--b:#bd00ff;--panel:rgba(5,8,25,.76)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02030b;color:#fff;font-family:Prompt,sans-serif}
#stage{position:relative;width:100%;height: min(940px,100vh);min-height:650px;overflow:hidden;background:radial-gradient(ellipse at 50% 45%,#10133c 0%,#050615 48%,#010208 100%);isolation:isolate}
#space{position:absolute;inset:0;width:100%;height:100%;z-index:0}
.aurora{position:absolute;inset:-20%;z-index:1;pointer-events:none;background:conic-gradient(from 30deg at 50% 50%,transparent,#00eaff12,transparent,#b400ff18,transparent);filter:blur(45px);animation:aurora 18s linear infinite}
@keyframes aurora{to{transform:rotate(360deg)}}
.hud{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:clamp(14px,3vw,30px);pointer-events:none}
.hud>*{pointer-events:auto}
.top{width:100%;display:flex;flex-direction:column;align-items:center;gap:8px}
.brand{font-family:Orbitron,sans-serif;font-weight:900;letter-spacing:clamp(3px,1vw,8px);font-size:clamp(23px,4.5vw,48px);text-align:center;color:#eafcff;text-shadow:0 0 8px var(--a),0 0 25px var(--a),0 0 50px var(--b);animation:flicker 3.5s ease-in-out infinite alternate}
@keyframes flicker{from{filter:brightness(.86);text-shadow:0 0 8px var(--a),0 0 22px var(--a),0 0 35px var(--b)}to{filter:brightness(1.25);text-shadow:0 0 12px var(--a),0 0 32px var(--a),0 0 65px var(--b)}}
.subtitle{font-size:10px;letter-spacing:4px;color:#c7d6ff;text-align:center}
.themes{display:flex;gap:10px;margin-top:3px}
.theme{width:23px;height:23px;border:2px solid #ffffffc9;border-radius:50%;cursor:pointer;box-shadow:0 0 13px currentColor}
.theme:focus{outline:2px solid white;outline-offset:3px}
#t1{background:linear-gradient(135deg,#00f5ff,#bd00ff);color:#00f5ff}
#t2{background:linear-gradient(135deg,#00ff82,#0055ff);color:#00ff82}
#t3{background:linear-gradient(135deg,#ff7a00,#ff006e);color:#ff7a00}
#t4{background:linear-gradient(135deg,#fff,#7777ff);color:#fff}
.center{position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);width:min(68vw,460px);height:min(68vw,460px);max-height:48vh;display:grid;place-items:center;pointer-events:none}
.ring{position:absolute;border-radius:50%;border:1px solid color-mix(in srgb,var(--a) 75%,transparent);box-shadow:0 0 20px color-mix(in srgb,var(--a) 60%,transparent),inset 0 0 20px color-mix(in srgb,var(--b) 30%,transparent)}
.r1{inset:2%;animation:orbit 20s linear infinite}
.r2{inset:10%;border-style:dashed;opacity:.65;animation:orbit 32s linear infinite reverse}
.r3{inset:18%;border-width:2px;opacity:.4;animation:pulse 2.8s ease-in-out infinite}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes pulse{50%{transform:scale(1.06);opacity:.9}}
#logo{width:38%;height:38%;object-fit:contain;border-radius:50%;border:2px solid var(--a);box-shadow:0 0 20px var(--a),0 0 55px var(--b),inset 0 0 20px var(--a);background:#060817;animation:logoGlow 2.2s ease-in-out infinite alternate}
@keyframes logoGlow{to{box-shadow:0 0 35px var(--a),0 0 85px var(--b),inset 0 0 30px var(--a);filter:brightness(1.15)}}
#logo-placeholder{font-family:Orbitron,sans-serif;color:var(--a);font-size:12px;text-shadow:0 0 15px var(--a);text-align:center}
#burst{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
#burst-btn{pointer-events:auto;position:absolute;bottom:calc(100% + 12px);left:50%;transform:translateX(-50%);border:1px solid var(--a);border-radius:30px;background:#060817aa;color:#fff;padding:7px 13px;font:11px Prompt,sans-serif;white-space:nowrap;box-shadow:0 0 15px var(--a);cursor:pointer}
.visual{width:min(900px,100%);height:clamp(80px,15vh,145px);display:block;filter:drop-shadow(0 0 8px var(--a));margin-bottom:10px}
.panel{width:min(760px,100%);border:1px solid color-mix(in srgb,var(--a) 80%,white 5%);border-radius:22px;padding:clamp(14px,2.5vw,24px);background:var(--panel);backdrop-filter:blur(18px);box-shadow:0 0 25px color-mix(in srgb,var(--a) 18%,transparent),inset 0 0 24px #8a00ff0b}
.track{display:flex;align-items:center;gap:12px;min-width:0;margin-bottom:15px}
.thumb{width:54px;height:54px;flex:0 0 54px;border-radius:12px;border:1px solid var(--b);object-fit:cover;box-shadow:0 0 15px var(--b)}
.tracktext{min-width:0;flex:1}
#track-title{font-size:clamp(14px,2vw,18px);font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-shadow:0 0 12px var(--a)}
#track-sub{font-size:11px;color:var(--a);margin-top:3px}
#playlist{max-width:42%;border:1px solid #ffffff36;background:#080b1c;color:white;padding:8px;border-radius:9px;font:11px Prompt,sans-serif}
.progress{height:7px;background:#ffffff22;border-radius:20px;overflow:hidden;cursor:pointer}
#fill{height:100%;width:0%;background:linear-gradient(90deg,var(--a),var(--b),#fff);box-shadow:0 0 14px var(--a)}
.times{display:flex;justify-content:space-between;font-size:10px;color:#aeb9dc;margin-top:5px}
.controls{display:flex;align-items:center;justify-content:center;gap:clamp(13px,4vw,30px);margin-top:14px}
.ctrl{border:0;background:transparent;color:#eaf5ff;font-size:20px;cursor:pointer;text-shadow:0 0 12px var(--a);padding:6px}
.ctrl:hover,.ctrl.active{color:var(--a);filter:drop-shadow(0 0 9px var(--a))}
#play{width:58px;height:58px;border:0;border-radius:50%;font-size:21px;color:#fff;cursor:pointer;background:linear-gradient(135deg,var(--a),var(--b));box-shadow:0 0 22px var(--a),0 0 45px #bd00ff77}
.options{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:12px}
.pill{font:11px Prompt,sans-serif;color:#e7eaff;border:1px solid #ffffff3d;border-radius:20px;padding:6px 12px;background:#ffffff0a;cursor:pointer}
.pill.active{border-color:var(--a);box-shadow:0 0 12px color-mix(in srgb,var(--a) 45%,transparent);color:var(--a)}
#start{position:absolute;inset:0;z-index:9;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;background:radial-gradient(ellipse at center,#11143bea,#010208f5);transition:opacity .6s}
#start h2{font:900 clamp(22px,4vw,42px) Orbitron,sans-serif;color:var(--a);text-shadow:0 0 20px var(--a);margin:0 0 12px}
#start p{color:#c8d4f4;max-width:480px;font-size:13px;line-height:1.8}
#start button{margin-top:12px;padding:13px 25px;border:0;border-radius:30px;color:#fff;font:700 14px Prompt,sans-serif;background:linear-gradient(100deg,var(--a),var(--b));box-shadow:0 0 25px var(--a);cursor:pointer}
.foot{font:9px Orbitron,sans-serif;letter-spacing:2px;color:#93a2d2;margin-top:9px;text-align:center}
@media(max-width:560px){#stage{min-height:620px}.hud{padding:12px}.center{top:40%;width:min(78vw,360px);height:min(78vw,360px);max-height:38vh}.visual{height:75px;margin-bottom:6px}.panel{padding:13px}.thumb{width:43px;height:43px;flex-basis:43px}.controls{gap:15px}#play{width:51px;height:51px}.subtitle{letter-spacing:2px}.foot{font-size:8px}}
</style>
</head>
<body>
<div id="stage">
 <canvas id="space"></canvas><div class="aurora"></div>
 <div class="center">
  <div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
  <img id="logo" alt="TA101 logo" style="display:none">
  <div id="logo-placeholder">TA101<br>NEON MUSIC</div>
  <canvas id="burst"></canvas>
  <button id="burst-btn" type="button">✦ โลโก้แตกตัว / ประกอบกลับ</button>
 </div>
 <div class="hud">
  <div class="top">
   <div class="brand">TA101 • NEON MUSIC</div>
   <div class="subtitle">3D COSMIC AUDIO EXPERIENCE</div>
   <div class="themes">
    <button class="theme" id="t1" aria-label="Cyber neon"></button>
    <button class="theme" id="t2" aria-label="Matrix green"></button>
    <button class="theme" id="t3" aria-label="Solar flare"></button>
    <button class="theme" id="t4" aria-label="Ice space"></button>
   </div>
  </div>
  <div style="flex:1"></div>
  <canvas class="visual" id="wave"></canvas>
  <div class="panel">
   <div class="track">
    <img class="thumb" id="thumb" alt="Album art" style="display:none">
    <div class="tracktext"><div id="track-title">กำลังเตรียมเพลง...</div><div id="track-sub">TA101 LOCAL PLAYLIST</div></div>
    <select id="playlist" aria-label="เลือกเพลง"><option>กำลังโหลดรายการเพลง</option></select>
   </div>
   <div class="progress" id="progress"><div id="fill"></div></div>
   <div class="times"><span id="elapsed">0:00</span><span id="duration">0:00</span></div>
   <div class="controls">
    <button class="ctrl" id="prev" title="เพลงก่อน">⏮</button>
    <button id="play" title="เล่น / หยุด">▶</button>
    <button class="ctrl" id="next" title="เพลงถัดไป">⏭</button>
   </div>
   <div class="options">
    <button class="pill active" id="loop">↻ วนซ้ำรายการ</button>
    <button class="pill" id="shuffle">⤨ สุ่มเพลง</button>
    <button class="pill" id="single">♪ เล่นเพลงเดียว</button>
    <button class="pill" id="fullscreen">⛶ เต็มจอ</button>
   </div>
  </div>
  <div class="foot">SPACE • LIGHT • SOUND • 1.618 ENERGY</div>
 </div>
 <div id="start">
  <h2>ENTER THE COSMOS</h2>
  <p>ฉากอวกาศสามมิติ • อนุภาคโลโก้ • ไฟนีออน • คลื่นเสียงตามเพลงจริง<br>แตะเพื่อเริ่มเพลงและเปิดใช้งานระบบวิเคราะห์เสียง</p>
  <button id="enter">✦ เริ่มประสบการณ์ TA101</button>
 </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const SONGS = __SONGS_REPLACE__;
const LOGO = __LOGO_REPLACE__;
const $ = id => document.getElementById(id);
const audio = new Audio();
audio.preload = "auto";
audio.crossOrigin = "anonymous";
let index=0, playing=false, shuffle=false, loopList=true, single=false;
let ctx=null, analyser=null, source=null, freq=null, waveData=null;
let scene,camera,renderer,stars,core,coreMat,clock;
const stage=$("stage");

function setTheme(a,b){
 document.documentElement.style.setProperty("--a",a);
 document.documentElement.style.setProperty("--b",b);
 if(stars && stars.material) stars.material.color.set(a);
 if(coreMat) coreMat.color.set(b);
}
$("t1").onclick=()=>setTheme("#00f5ff","#bd00ff");
$("t2").onclick=()=>setTheme("#00ff82","#0055ff");
$("t3").onclick=()=>setTheme("#ff7a00","#ff006e");
$("t4").onclick=()=>setTheme("#e8f5ff","#7777ff");

if(LOGO){
 $("logo").src=LOGO;
 $("logo").style.display="block";
 $("thumb").src=LOGO;
 $("thumb").style.display="block";
 $("logo-placeholder").style.display="none";
}

function timeText(s){
 if(!Number.isFinite(s))return "0:00";
 s=Math.max(0,Math.floor(s));
 return Math.floor(s/60)+":"+String(s%60).padStart(2,"0");
}

function initAudio(){
 if(ctx)return;
 const AC=window.AudioContext||window.webkitAudioContext;
 if(!AC)return;
 ctx=new AC();
 analyser=ctx.createAnalyser();
 analyser.fftSize=256;
 analyser.smoothingTimeConstant=.78;
 source=ctx.createMediaElementSource(audio);
 source.connect(analyser);
 analyser.connect(ctx.destination);
 freq=new Uint8Array(analyser.frequencyBinCount);
 waveData=new Uint8Array(analyser.fftSize);
}

function fillPlaylist(){
 const sel=$("playlist");
 sel.innerHTML="";
 if(!SONGS.length){
  sel.innerHTML='<option value="">ไม่พบไฟล์เพลง .mp3 ในหน้าหลัก</option>';
  $("track-title").textContent="ไม่พบไฟล์เพลง MP3";
  $("track-sub").textContent="กรุณาวางไฟล์เพลงไว้หน้าเดียวกับ app.py";
  return;
 }
 SONGS.forEach((s,i)=>{
  const op=document.createElement("option");
  op.value=String(i);
  op.textContent=(i+1)+". "+s.name;
  sel.appendChild(op);
 });
 loadTrack(0);
}

function loadTrack(i){
 if(!SONGS.length)return;
 index=(i+SONGS.length)%SONGS.length;
 audio.src=SONGS[index].src;
 audio.load();
 $("track-title").textContent=SONGS[index].name;
 $("track-sub").textContent="TRACK "+(index+1)+" / "+SONGS.length;
 $("playlist").value=String(index);
 $("fill").style.width="0%";
 $("elapsed").textContent="0:00";
 $("duration").textContent="0:00";
}

async function playAudio(){
 if(!SONGS.length)return;
 initAudio();
 if(ctx && ctx.state==="suspended"){try{await ctx.resume()}catch(e){}}
 try{
  await audio.play();
  playing=true;
  $("play").textContent="Ⅱ";
 }catch(e){
  playing=false;
  $("play").textContent="▶";
  $("track-sub").textContent="แตะปุ่มเล่นอีกครั้ง หากเบราว์เซอร์บล็อกเสียง";
 }
}

function pauseAudio(){
 audio.pause();
 playing=false;
 $("play").textContent="▶";
}

function nextTrack(fromEnded=false){
 if(!SONGS.length)return;
 if(single && fromEnded){pauseAudio();audio.currentTime=0;return;}
 if(shuffle && SONGS.length>1){
  let n=index;
  while(n===index)n=Math.floor(Math.random()*SONGS.length);
  loadTrack(n);
 } else if(fromEnded && !loopList && index===SONGS.length-1){
  pauseAudio();
  return;
 } else {
  loadTrack(index+1);
 }
 if(playing || fromEnded) playAudio();
}

$("play").onclick=()=>playing?pauseAudio():playAudio();
$("next").onclick=()=>nextTrack(false);
$("prev").onclick=()=>{
 if(audio.currentTime>3){audio.currentTime=0;return;}
 loadTrack(index-1);
 if(playing)playAudio();
};
$("playlist").onchange=e=>{
 loadTrack(Number(e.target.value));
 playAudio();
};

$("loop").onclick=()=>{
 loopList=!loopList;
 $("loop").classList.toggle("active",loopList);
 if(loopList){single=false;$("single").classList.remove("active");}
};
$("shuffle").onclick=()=>{
 shuffle=!shuffle;
 $("shuffle").classList.toggle("active",shuffle);
};
$("single").onclick=()=>{
 single=!single;
 $("single").classList.toggle("active",single);
 if(single){loopList=false;$("loop").classList.remove("active");}
 else{loopList=true;$("loop").classList.add("active");}
};

audio.addEventListener("ended",()=>nextTrack(true));
audio.addEventListener("loadedmetadata",()=>{$("duration").textContent=timeText(audio.duration)});
audio.addEventListener("timeupdate",()=>{
 if(audio.duration){
  $("fill").style.width=(audio.currentTime/audio.duration*100)+"%";
  $("elapsed").textContent=timeText(audio.currentTime);
 }
});
$("progress").onclick=e=>{
 if(audio.duration){
  const r=e.currentTarget.getBoundingClientRect();
  audio.currentTime=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width))*audio.duration;
 }
};

$("enter").onclick=async()=>{
 initAudio();
 if(ctx&&ctx.state==="suspended"){try{await ctx.resume()}catch(e){}}
 $("start").style.opacity="0";
 setTimeout(()=>$("start").style.display="none",620);
 await playAudio();
};

$("fullscreen").onclick=async()=>{
 try{
  if(!document.fullscreenElement)await stage.requestFullscreen();
  else await document.exitFullscreen();
 }catch(e){}
};

fillPlaylist();

/* Three.js 3D Cosmic Starfield & Core */
const canvas=$("space");
try{
 scene=new THREE.Scene();
 scene.fog=new THREE.FogExp2(0x03040c,0.0038);
 camera=new THREE.PerspectiveCamera(62,1,.1,1200);
 camera.position.z=90;
 renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.8));

 const positions=new Float32Array(2400*3), colors=new Float32Array(2400*3);
 for(let i=0;i<2400;i++){
  positions[i*3]=(Math.random()-.5)*330;
  positions[i*3+1]=(Math.random()-.5)*210;
  positions[i*3+2]=(Math.random()-.5)*650;
  const c=new THREE.Color().setHSL(.52+Math.random()*.28,.85,.55+Math.random()*.3);
  colors.set([c.r,c.g,c.b],i*3);
 }
 const geo=new THREE.BufferGeometry();
 geo.setAttribute("position",new THREE.BufferAttribute(positions,3));
 geo.setAttribute("color",new THREE.BufferAttribute(colors,3));
 stars=new THREE.Points(geo,new THREE.PointsMaterial({size:1.05,vertexColors:true,transparent:true,opacity:.9,depthWrite:false}));
 scene.add(stars);

 const coreGeo=new THREE.IcosahedronGeometry(17,2);
 coreMat=new THREE.MeshBasicMaterial({color:0xbd00ff,wireframe:true,transparent:true,opacity:.19});
 core=new THREE.Mesh(coreGeo,coreMat);
 scene.add(core);

 const ringGeo=new THREE.TorusGeometry(23,.09,8,240);
 const ringMat=new THREE.MeshBasicMaterial({color:0x00f5ff,transparent:true,opacity:.65});
 const ring=new THREE.Mesh(ringGeo,ringMat);
 ring.rotation.x=1.05;
 scene.add(ring);

 const ring2=new THREE.Mesh(new THREE.TorusGeometry(29,.045,6,240),new THREE.MeshBasicMaterial({color:0xbd00ff,transparent:true,opacity:.55}));
 ring2.rotation.y=.9;
 ring2.rotation.x=.4;
 scene.add(ring2);

 clock=new THREE.Clock();
 function resize3d(){
  const w=stage.clientWidth,h=stage.clientHeight;
  camera.aspect=w/h;
  camera.updateProjectionMatrix();
  renderer.setSize(w,h,false);
 }
 window.addEventListener("resize",resize3d);
 resize3d();

 function render3d(){
  requestAnimationFrame(render3d);
  const t=clock.getElapsedTime();
  stars.rotation.y+=.00045;
  stars.rotation.x=Math.sin(t*.08)*.025;
  core.rotation.x=t*.12;
  core.rotation.y=t*.18;
  ring.rotation.z=t*.12;
  ring2.rotation.z=-t*.09;

  let energy=0;
  if(analyser&&freq&&playing){
   analyser.getByteFrequencyData(freq);
   for(let i=0;i<freq.length;i++)energy+=freq[i];
   energy=energy/freq.length/255;
  }
  const s=1+energy*.32;
  core.scale.setScalar(s);
  core.rotation.z=t*.06;

  camera.position.x=Math.sin(t*.09)*2.2;
  camera.position.y=Math.cos(t*.11)*1.5;
  camera.lookAt(0,0,0);
  renderer.render(scene,camera);
 }
 render3d();
}catch(err){console.warn("3D renderer error:",err)}

/* Audio-reactive Waveform */
const wc=$("wave"),wctx=wc.getContext("2d");
function drawWave(){
 requestAnimationFrame(drawWave);
 const dpr=Math.min(devicePixelRatio||1,2),w=wc.clientWidth,h=wc.clientHeight;
 if(wc.width!==Math.floor(w*dpr)||wc.height!==Math.floor(h*dpr)){
  wc.width=Math.floor(w*dpr);
  wc.height=Math.floor(h*dpr);
 }
 wctx.setTransform(dpr,0,0,dpr,0,0);
 wctx.clearRect(0,0,w,h);
 if(analyser&&waveData&&playing)analyser.getByteTimeDomainData(waveData);
 const mid=h*.5,points=Math.max(120,Math.floor(w*.8));
 for(let layer=0;layer<3;layer++){
  wctx.beginPath();
  wctx.lineWidth=layer===0?2.8:1.1;
  wctx.strokeStyle=layer===0?"#00f5ff":layer===1?"#bd00ff":"#ffffff88";
  wctx.shadowBlur=layer===0?16:8;
  wctx.shadowColor=layer===1?"#bd00ff":"#00f5ff";
  for(let i=0;i<=points;i++){
   const x=i/points*w;
   let v=0;
   if(analyser&&waveData&&playing){
    const j=Math.floor(i/points*(waveData.length-1));
    v=(waveData[j]-128)/128;
   }else{
    v=Math.sin(i*.12+performance.now()*.0015+layer)*.08+Math.sin(i*.035-performance.now()*.001)*.04;
   }
   const amp=(playing?h*.38:h*.18)*(1-layer*.22);
   const y=mid+v*amp+Math.sin(i*.08+performance.now()*.001+layer)*3;
      if(i===0)wctx.moveTo(x,y);else wctx.lineTo(x,y);
  }
  wctx.stroke();
 }
 wctx.shadowBlur=0;
}
drawWave();

/* Logo Burst & Reassembly (เอฟเฟกต์แตกกระจายและรวมร่างต่อเนื่อง) */
const bc=$("burst"),bctx=bc.getContext("2d");
let particles=[],isBurst=false;

function initBurst(){
 bc.width=bc.clientWidth*window.devicePixelRatio;
 bc.height=bc.clientHeight*window.devicePixelRatio;
 particles=[];
 const count=140;
 const cx=bc.width/2, cy=bc.height/2;
 for(let i=0;i<count;i++){
  const angle=Math.random()*Math.PI*2;
  const speed=Math.random()*6+2;
  particles.push({
   x:cx, y:cy,
   ox:cx+(Math.random()-.5)*120,
   oy:cy+(Math.random()-.5)*120,
   vx:Math.cos(angle)*speed,
   vy:Math.sin(angle)*speed,
   size:Math.random()*3+1.5,
   color:Math.random()>.5?"#00f5ff":"#bd00ff"
  });
 }
}

function updateBurst(){
 bctx.clearRect(0,0,bc.width,bc.height);
 if(isBurst){
  particles.forEach(p=>{
   p.x+=p.vx;
   p.y+=p.vy;
   bctx.fillStyle=p.color;
   bctx.beginPath();
   bctx.arc(p.x,p.y,p.size,0,Math.PI*2);
   bctx.fill();
  });
 }
 requestAnimationFrame(updateBurst);
}

$("burst-btn").onclick=()=>{
 isBurst=!isBurst;
 if(isBurst){
  initBurst();
  $("logo").style.transform="scale(0.1)";
  $("logo").style.opacity="0.2";
  setTimeout(()=>{
   isBurst=false;
   $("logo").style.transform="scale(1)";
   $("logo").style.opacity="1";
  },1400);
 }
};
updateBurst();
</script>
</body>
</html>
"""
    .replace("__SONGS_REPLACE__", songs_json)
    .replace("__LOGO_REPLACE__", logo_json)
)

# ใช้ st.iframe ตามมาตรฐานใหม่ของ Streamlit
html_bytes = player_html.encode("utf-8")
base64_html = base64.b64encode(html_bytes).decode("ascii")
st.iframe(
    f"data:text/html;base64,{base64_html}", height=720, scrolling=False
)
