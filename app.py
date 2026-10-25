
ต่อจาก สร้างเครื่องเล่นเพลง Streamlit (1)

ใช่ครับ

สุดยอดครับ! 🚀🌌 เราจะพา TA101 • NEON MUSIC ไปสู่เวอร์ชัน 3D SPACE EXPERIENCE กันเลยครับ

ผมจะยึดแนวทางนี้เป็นหลักครับ

🌌 ฉากอวกาศ 3 มิติ มีดาวพุ่งเข้าหากล้อง เนบิวลาสีฟ้า–ม่วง และมิติความลึก

💥 โลโก้แตกแล้วประกอบกลับ เป็นอนุภาคแสง โดยใช้โลโก้เดิมของคุณ

✨ ตัวหนังสือวิ้งแรง ๆ มีแสงวิ่งผ่านและเงานีออน

🔊 กราฟเสียงตอบสนองเพลงจริง พร้อมแรงกระแทกจากเบส

🎧 เครื่องเล่นเพลงใช้งานได้จริง มีเล่น/หยุด เพลงก่อนหน้า/ถัดไป และเล่นต่อเนื่อง

📱 ออกแบบแนวตั้ง ให้เหมาะกับการอัดคลิป TikTok, Reels และ Shorts

ผมจะไม่ตัดไฟล์เพลงหรือโลโก้เดิมออก และจะไม่ใช้แผ่นเสียงหมุน ๆ แบบเก่าครับ

ขั้นต่อไป: ผมจะทำโค้ด app.py ฉบับเต็มให้ โดยจัดโครงสร้าง HTML และ JavaScript ให้ถูกต้อง เพื่อหลีกเลี่ยงปัญหา SyntaxError ที่เราเจอก่อนหน้านี้ครับ 🔥


จัดมาคับ

จัดให้ครับ! 🚀🌌 รอบนี้เราจะทำ TA101 • NEON MUSIC — 3D SPACE EDITION ให้เป็นเครื่องเล่นเพลงแนวจักรวาลไซเบอร์แบบเต็มรูปแบบครับ

สิ่งที่เน้นเป็นพิเศษคือโลโก้แตกเป็นอนุภาคแล้วประกอบกลับ ฉากดาวมีมิติความลึก ตัวหนังสือวิ้ง และกราฟเสียงที่ตอบสนองต่อเสียงเพลงจริง โดยยังคงไฟล์เพลงและโลโก้เดิมไว้ครับ

ก่อนวางโค้ด: ให้แทนที่เนื้อหา ta101/app.py ทั้งหมดด้วยโค้ดชุดใหม่นี้ ส่วนไฟล์ logo1.jpg และไฟล์เพลง .mp3 ให้อยู่ในโฟลเดอร์เดียวกันเหมือนเดิม


import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • 3D SPACE MUSIC",
    page_icon="🌌",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            songs.append({"name": path.stem, "src": data_uri(path)})
        except OSError:
            pass

logo_src = ""
for filename in (
    "logo1.jpg", "logo.jpg", "logo1.jpeg", "logo.jpeg",
    "โลโก้.jpg", "logo1.png", "logo.png",
):
    path = ROOT / filename
    if path.is_file():
        try:
            logo_src = data_uri(path)
            break
        except OSError:
            pass

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")
logo_json = json.dumps(logo_src, ensure_ascii=False).replace("</", "<\\/")

page = r'''
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;background:#03030b;color:white;font-family:system-ui,sans-serif}
body{overflow-x:hidden}
#universe{position:relative;isolation:isolate;overflow:hidden;min-height:100vh;
max-width:900px;margin:auto;padding:18px 15px 30px;
background:radial-gradient(ellipse at 50% 35%,#211747,#090a1b 50%,#02030a)}
#space,#dust{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
#space{z-index:-2}#dust{z-index:-1}
.nebula{position:absolute;inset:-20%;z-index:-1;pointer-events:none;filter:blur(38px);
background:radial-gradient(ellipse at 15% 25%,#00d9ff40,transparent 35%),
radial-gradient(ellipse at 85% 35%,#ff00c833,transparent 35%),
radial-gradient(ellipse at 55% 80%,#652bff40,transparent 40%);
animation:nebula 12s ease-in-out infinite alternate}
@keyframes nebula{to{transform:translate(2%,-2%) scale(1.12)}}
.top{display:flex;justify-content:space-between;align-items:center;gap:10px;
padding:5px 0 15px;border-bottom:1px solid #8c9bff35}
.brand{font-size:clamp(18px,4vw,29px);font-weight:1000;letter-spacing:.08em;
background:linear-gradient(90deg,#4af7ff,#c4a4ff,#ff56db,#4af7ff);
background-size:250% auto;color:transparent;background-clip:text;
-webkit-background-clip:text;animation:shine 4s linear infinite;
filter:drop-shadow(0 0 12px #44dfff)}
.tag{font-size:9px;letter-spacing:.2em;color:#a9b8e9;margin-top:5px}
@keyframes shine{to{background-position:250% center}}
button{color:white;cursor:pointer;font-family:inherit;transition:transform .15s,filter .15s}
button:active{transform:scale(.94);filter:brightness(1.5)}
.full{border:1px solid #55efff;border-radius:24px;padding:10px 12px;
background:#10142a;font-size:10px;font-weight:900;box-shadow:0 0 20px #00cfff55}
.hero{text-align:center;padding:30px 0 8px}
.logo-stage{width:min(55vw,245px);aspect-ratio:1;margin:0 auto 20px;
position:relative;display:grid;place-items:center}
.logo-stage:before,.logo-stage:after{content:"";position:absolute;inset:-9%;
border:2px solid #45efff;border-radius:50%;box-shadow:0 0 22px #00eaff;
animation:ring 3s ease-in-out infinite}
.logo-stage:after{inset:-18%;border-color:#e44cff;border-style:dashed;
box-shadow:0 0 25px #b34cff;animation:ring 4s ease-in-out infinite reverse}
@keyframes ring{50%{transform:scale(1.07) rotate(9deg);opacity:.55}}
.logo-glow{position:absolute;inset:0;border-radius:50%;
background:radial-gradient(circle,#8a4dff77,transparent 70%);
filter:blur(18px);animation:glow 1.6s infinite alternate}
@keyframes glow{to{transform:scale(1.2);opacity:.6}}
#logoImage{position:relative;width:100%;height:100%;object-fit:contain;
border-radius:50%;z-index:2;filter:drop-shadow(0 0 15px #32eaff);
animation:breath 2.4s ease-in-out infinite;transition:opacity .3s}
@keyframes breath{50%{transform:scale(1.045);filter:drop-shadow(0 0 30px #d43cff)}}
#logoFallback{position:absolute;z-index:2;font-size:24px;font-weight:1000;
text-shadow:0 0 12px #3ff,0 0 30px #f3c}
#logoParticles{position:absolute;z-index:4;inset:-20%;width:140%;height:140%;
pointer-events:none}
#logoBurst{position:absolute;z-index:5;bottom:-12px;left:50%;transform:translateX(-50%);
white-space:nowrap;border:1px solid #c39bff;border-radius:25px;padding:8px 12px;
background:#101127dd;font-size:10px;font-weight:900;box-shadow:0 0 20px #a64dff}
.feel{font-size:clamp(13px,3.5vw,19px);font-weight:1000;letter-spacing:.2em;
background:linear-gradient(90deg,#fff,#43f5ff,#c3a5ff,#ff5cdb,#fff);
background-size:300% auto;color:transparent;background-clip:text;
-webkit-background-clip:text;animation:shine 3s linear infinite}
.status{text-align:center;font-size:10px;letter-spacing:.14em;color:#b8c7f7;margin:24px 0 14px}
.record-wrap{width:min(35vw,150px);aspect-ratio:1;margin:0 auto 17px}
.record{width:100%;height:100%;border-radius:50%;position:relative;
background:repeating-radial-gradient(circle,#090a12 0 3px,#34334c 4px 5px,#11111b 6px 8px);
border:2px solid #a66aff;box-shadow:0 0 24px #955cff,0 0 50px #d52bff55;
transition:filter .15s,transform .15s}
.record:before{content:"TA";position:absolute;inset:30%;border-radius:50%;
display:grid;place-items:center;background:linear-gradient(135deg,#44eaff,#6c43ff,#ed3bd2);
font-weight:1000;box-shadow:0 0 20px #995cff}
.track{text-align:center;font-size:clamp(20px,5.5vw,31px);font-weight:1000;
line-height:1.4;overflow-wrap:anywhere;
background:linear-gradient(90deg,#fff,#53f5ff,#c6a6ff,#ff5bdb,#fff);
background-size:250% auto;color:transparent;background-clip:text;
-webkit-background-clip:text;animation:shine 5s linear infinite}
.subtrack{text-align:center;font-size:9px;letter-spacing:.2em;color:#9baedb;margin-top:5px}
.visual{height:165px;margin:23px 0 12px;border:1px solid #8b85ff55;border-radius:14px;
overflow:hidden;background:#050817cc;box-shadow:inset 0 0 28px #552dff44}
#scope{width:100%;height:100%;display:block}
input[type=range]{width:100%;accent-color:#ef4bd8}
.times{display:flex;justify-content:space-between;font-size:11px;color:#bac9ef}
.controls{display:flex;justify-content:center;align-items:center;gap:clamp(12px,5vw,32px);margin:19px 0 22px}
.ctrl{width:58px;height:58px;border-radius:50%;border:1px solid #898bff99;
background:#10142b;font-size:20px;box-shadow:0 0 20px #614bff55}
.ctrl.main{width:82px;height:82px;font-size:29px;border:0;
background:linear-gradient(135deg,#22e7ff,#7550ff 55%,#f32dc8);
box-shadow:0 0 30px #4fbcff,0 0 55px #b22fff}
.heading{text-align:center;font-size:11px;font-weight:1000;letter-spacing:.2em;
color:#d4d9ff;margin:22px 0 12px}
.effects{display:flex;justify-content:center;gap:7px;flex-wrap:wrap}
.effect{font-size:11px;font-weight:900;padding:9px 11px;border-radius:22px;
border:1px solid #777bbd;background:#11152b}
.effect.active{border-color:#42f5ff;background:linear-gradient(110deg,#12394b,#3a2051);
box-shadow:0 0 20px #36dfff}
.panel{padding:14px;margin-top:16px;border-radius:16px;border:1px solid #8877ff77;
background:#0c1025ee;box-shadow:inset 0 0 22px #593cff33}
.row{display:flex;justify-content:space-between;align-items:center;gap:10px;
margin:8px 0;font-size:12px;color:#d8e1ff}
select{max-width:68%;padding:8px;border-radius:9px;background:#151a30;color:white;border:1px solid #717cc7}
.knob{margin:15px 0}
.knob label{display:flex;justify-content:space-between;font-size:11px;color:#cbd7ff;margin-bottom:5px}
.smallbtn{border:1px solid #626eaa;background:#12172d;border-radius:20px;padding:8px 10px;font-size:10px}
.footer{text-align:center;font-size:9px;color:#6876a9;letter-spacing:.18em;margin-top:22px}
@media(min-width:650px){#universe{padding:24px 35px}.visual{height:190px}}
</style>
</head>
<body>
<div id="universe">
<canvas id="space"></canvas><canvas id="dust"></canvas><div class="nebula"></div>
<header class="top">
  <div><div class="brand">TA101 • 3D SPACE MUSIC</div>
  <div class="tag">COSMIC SOUND EXPERIENCE</div></div>
  <button class="full" id="fullBtn">⛶ FULL SCREEN</button>
</header>
<section class="hero">
  <div class="logo-stage" id="logoStage">
    <div class="logo-glow"></div>
    <div id="logoFallback">SYNAPSE</div>
    <img id="logoImage" alt="โลโก้เพลง" style="display:none">
    <canvas id="logoParticles"></canvas>
    <button id="logoBurst">✦ LOGO DISINTEGRATE / REBUILD ✦</button>
  </div>
  <div class="feel">FEEL THE UNIVERSE</div>
</section>
<div class="status" id="status">SPACE ENGINE READY • AUDIO REACTIVE</div>
<div class="record-wrap"><div class="record"></div></div>
<div class="track" id="trackName">กำลังเตรียมเพลง…</div>
<div class="subtrack">♫ SOUND • LIGHT • MOTION ♫</div>
<div class="visual"><canvas id="scope"></canvas></div>
<input id="seek" type="range" min="0" max="1000" value="0">
<div class="times"><span id="elapsed">0:00</span><span id="duration">0:00</span></div>
<div class="controls">
  <button class="ctrl" id="prevBtn">◀◀</button>
  <button class="ctrl main" id="playBtn">▶</button>
  <button class="ctrl" id="nextBtn">▶▶</button>
</div>
<div class="heading">CHOOSE YOUR COSMIC LIGHT</div>
<div class="effects">
  <button class="effect active" data-effect="CYBER">CYBER</button>
  <button class="effect" data-effect="RAINBOW">RAINBOW</button>
  <button class="effect" data-effect="LASER">LASER</button>
  <button class="effect" data-effect="GOLD">GOLD</button>
  <button class="effect" data-effect="PARTICLE">PARTICLE</button>
  <button class="effect" data-effect="CALM">CALM</button>
</div>
<div class="panel">
  <div class="row"><span>PLAY MODE</span><select id="mode">
    <option value="next">AUTO NEXT</option><option value="loop">LOOP ALL</option>
    <option value="one">REPEAT ONE</option><option value="shuffle">SHUFFLE</option>
  </select></div>
  <div class="row"><span>SONG LIBRARY</span><span id="trackCount">0 SONGS</span></div>
  <div class="knob"><label><span>BASS PUNCH</span><span id="punchVal">1.8×</span></label>
    <input id="punch" type="range" min=".5" max="3" step=".1" value="1.8"></div>
  <div class="knob"><label><span>NEON GLOW</span><span id="glowVal">1.8×</span></label>
    <input id="glow" type="range" min=".5" max="3" step=".1" value="1.8"></div>
  <div class="knob"><label><span>SPACE ENERGY</span><span id="energyVal">8</span></label>
    <input id="energy" type="range" min="0" max="12" value="8"></div>
  <div class="row"><button class="smallbtn" id="rebuildBtn">✦ REBUILD LOGO</button>
    <span>3D STARFIELD ON</span></div>
</div>
<div class="footer">TA101 • ENTER THE COSMOS • NEON SPACE EDITION</div>
</div>
<script>
const songs = __SONGS__;
const logoSrc = __LOGO__;
const $ = id => document.getElementById(id);
const audio = new Audio();
audio.preload = "metadata";

let idx=0, playing=false, audioCtx=null, analyser=null, sourceNode=null;
let punch=1.8, glow=1.8, spaceEnergy=8, effect="CYBER", seeking=false, smoothBass=0;
const palettes={
 CYBER:["#42f5ff","#a45bff","#ff3bc8"],
 RAINBOW:["#ff3157","#ffcf45","#3bffb2","#3ba8ff","#e94cff"],
 LASER:["#54faff","#ffffff","#ff42d6"],
 GOLD:["#fff0a0","#ffb52e","#fff7db"],
 PARTICLE:["#45f8ff","#b15cff","#ff4fd8"],
 CALM:["#72d9ff","#a5a4ff","#e1c6ff"]
};
function fmt(t){return !Number.isFinite(t)||t<0?"0:00":Math.floor(t/60)+":"+String(Math.floor(t%60)).padStart(2,"0");}
function initAudio(){
 if(audioCtx)return;
 try{
  audioCtx=new(window.AudioContext||window.webkitAudioContext)();
  analyser=audioCtx.createAnalyser();analyser.fftSize=2048;analyser.smoothingTimeConstant=.78;
  sourceNode=audioCtx.createMediaElementSource(audio);
  sourceNode.connect(analyser);analyser.connect(audioCtx.destination);
 }catch(e){$("status").textContent="AUDIO READY • VISUAL ENGINE ON";}
}
function updateTrack(){
 if(!songs.length){
  $("trackName").textContent="ยังไม่พบไฟล์เพลง";
  $("status").textContent="ใส่ไฟล์ MP3 ไว้ในโฟลเดอร์เดียวกับ app.py";
  $("trackCount").textContent="0 SONGS";return;
 }
 $("trackName").textContent=songs[idx].name;
 $("trackCount").textContent=(idx+1)+" / "+songs.length+" SONGS";
 $("seek").value=0;$("elapsed").textContent="0:00";$("duration").textContent="0:00";
}
function loadTrack(n,autoplay=false){
 if(!songs.length)return;
 idx=(n+songs.length)%songs.length;audio.src=songs[idx].src;audio.load();updateTrack();
 if(autoplay)playAudio();
}
function nextTrack(dir=1){
 if(!songs.length)return;
 const mode=$("mode").value;
 if(mode==="one"&&dir===1){loadTrack(idx,true);return;}
 if(mode==="shuffle"&&songs.length>1){
  let n=idx;while(n===idx)n=Math.floor(Math.random()*songs.length);idx=n;
 }else idx=(idx+dir+songs.length)%songs.length;
 loadTrack(idx,true);
}
async function playAudio(){
 if(!songs.length)return;initAudio();
 if(audioCtx&&audioCtx.state==="suspended"){try{await audioCtx.resume();}catch(e){}}
 try{await audio.play();playing=true;$("playBtn").textContent="Ⅱ";$("status").textContent="COSMIC AUDIO REACTIVE • LIVE";}
 catch(e){playing=false;$("playBtn").textContent="▶";$("status").textContent="แตะปุ่มเล่นอีกครั้งเพื่อเริ่มเพลง";}
}
function pauseAudio(){audio.pause();playing=false;$("playBtn").textContent="▶";}
$("playBtn").addEventListener("click",()=>playing?pauseAudio():playAudio());
$("nextBtn").addEventListener("click",()=>nextTrack(1));
$("prevBtn").addEventListener("click",()=>audio.currentTime>3?audio.currentTime=0:nextTrack(-1));
$("fullBtn").addEventListener("click",async()=>{
 try{if(!document.fullscreenElement)await $("universe").requestFullscreen();else await document.exitFullscreen();}
 catch(e){$("status").textContent="อุปกรณ์นี้ไม่รองรับเต็มหน้าจอ";}
});
audio.addEventListener("ended",()=>{if($("mode").value==="one")loadTrack(idx,true);else nextTrack(1);});
audio.addEventListener("play",()=>{playing=true;$("playBtn").textContent="Ⅱ";});
audio.addEventListener("pause",()=>{playing=false;$("playBtn").textContent="▶";});
audio.addEventListener("loadedmetadata",()=>{$("duration").textContent=fmt(audio.duration);});
audio.addEventListener("timeupdate",()=>{
 if(!seeking&&Number.isFinite(audio.duration)&&audio.duration>0){
  $("seek").value=Math.round(audio.currentTime/audio.duration*1000);
  $("elapsed").textContent=fmt(audio.currentTime);
 }
});
$("seek").addEventListener("input",()=>{
 seeking=true;
 if(Number.isFinite(audio.duration)&&audio.duration>0){
  audio.currentTime=Number($("seek").value)/1000*audio.duration;
  $("elapsed").textContent=fmt(audio.currentTime);
 }
});
$("seek").addEventListener("change",()=>seeking=false);
$("punch").addEventListener("input",e=>{punch=+e.target.value;$("punchVal").textContent=punch.toFixed(1)+"×";});
$("glow").addEventListener("input",e=>{glow=+e.target.value;$("glowVal").textContent=glow.toFixed(1)+"×";});
$("energy").addEventListener("input",e=>{spaceEnergy=+e.target.value;$("energyVal").textContent=spaceEnergy;});
document.querySelectorAll("[data-effect]").forEach(b=>b.addEventListener("click",()=>{
 effect=b.dataset.effect;
 document.querySelectorAll("[data-effect]").forEach(x=>x.classList.toggle("active",x===b));
}));

if(logoSrc){$("logoImage").src=logoSrc;$("logoImage").style.display="block";$("logoFallback").style.display="none";}

/* 3D starfield: stars move towards the viewer */
const space=$("space"),sc=space.getContext("2d");
const dust=$("dust"),dc=dust.getContext("2d");
let stars=[];
function newStar(w,h){return{x:(Math.random()-.5)*w,y:(Math.random()-.5)*h,z:Math.random()*.95+.05};}
function resizeSpace(){
 const r=$("universe").getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);
 [space,dust].forEach(c=>{c.width=Math.floor(r.width*d);c.height=Math.floor(r.height*d);c.style.width=r.width+"px";c.style.height=r.height+"px";});
 sc.setTransform(d,0,0,d,0,0);dc.setTransform(d,0,0,d,0,0);
 stars=Array.from({length:Math.min(250,Math.floor(r.width*.5))},()=>newStar(r.width,r.height));
}
function drawSpace(){
 requestAnimationFrame(drawSpace);
 const w=$("universe").clientWidth,h=$("universe").clientHeight;if(!w||!h)return;
 sc.clearRect(0,0,w,h);
 const cx=w/2,cy=h*.43;
 for(const s of stars){
  s.z-=.0015+(playing?smoothBass*.009*spaceEnergy/8:0);
  if(s.z<=.035)Object.assign(s,newStar(w,h),{z:1});
  const scale=1/s.z,x=cx+s.x*scale,y=cy+s.y*scale;
  if(x<0||x>w||y<0||y>h){Object.assign(s,newStar(w,h),{z:.98});continue;}
  const radius=Math.max(.4,(1-s.z)*2.5);
  sc.beginPath();sc.arc(x,y,radius,0,Math.PI*2);
  sc.fillStyle=effect==="GOLD"?"#ffe2a0":"#a5efff";
  sc.shadowBlur=radius*6;sc.shadowColor=effect==="GOLD"?"#ffbb45":"#40eaff";sc.fill();
  if(playing&&smoothBass>.25&&s.z<.4){
   sc.strokeStyle=`rgba(80,220,255,${smoothBass*.6})`;sc.lineWidth=radius;
   sc.beginPath();sc.moveTo(x,y);sc.lineTo(x+(x-cx)*.04*spaceEnergy,y+(y-cy)*.04*spaceEnergy);sc.stroke();
  }
 }
 sc.shadowBlur=0;
 dc.clearRect(0,0,w,h);
 const colors=palettes[effect]||palettes.CYBER;
 for(let i=0;i<35;i++){
  const x=(i*83+performance.now()*.012*(i%3+1))%w;
  const y=(i*137+Math.sin(performance.now()*.0008+i)*25+h)%h;
  dc.globalAlpha=.2+smoothBass*.5;dc.fillStyle=colors[i%colors.length];
  dc.beginPath();dc.arc(x,y,1+(i%3)*.5+smoothBass*2,0,Math.PI*2);dc.fill();
 }
 dc.globalAlpha=1;
}

/* Audio-reactive waveform */
const canvas=$("scope"),g=canvas.getContext("2d");
let bins=new Uint8Array(1024),wave=new Uint8Array(2048);
function resizeScope(){
 const r=canvas.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);
 canvas.width=Math.max(1,Math.floor(r.width*d));canvas.height=Math.max(1,Math.floor(r.height*d));
 g.setTransform(d,0,0,d,0,0);
}
function drawScope(){
 requestAnimationFrame(drawScope);
 const w=canvas.clientWidth,h=canvas.clientHeight;if(!w||!h)return;
 let level=0;
 if(analyser){
  analyser.getByteFrequencyData(bins);analyser.getByteTimeDomainData(wave);
  for(let i=0;i<22;i++)level+=bins[i];level=level/22/255;
 }
 smoothBass=smoothBass*.78+level*.22;
 const colors=palettes[effect]||palettes.CYBER;
 const grad=g.createLinearGradient(0,0,w,0);
 colors.forEach((c,i)=>grad.addColorStop(i/Math.max(1,colors.length-1),c));
 g.clearRect(0,0,w,h);g.fillStyle="#050817";g.fillRect(0,0,w,h);
 g.strokeStyle="#7f91ff22";g.lineWidth=1;
 for(let x=0;x<w;x+=25){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke();}
 for(let y=0;y<h;y+=25){g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke();}
 const mid=h*.58,points=Math.max(100,Math.floor(w));
 g.save();g.strokeStyle=grad;g.lineWidth=2.5;g.lineJoin="round";
 g.shadowBlur=14*glow;g.shadowColor=colors[1]||colors[0];g.beginPath();
 for(let i=0;i<points;i++){
  const x=i/(points-1)*w;let v;
  if(analyser&&playing){const wi=Math.floor(i/(poi
  }
 g.stroke();
 for(let i=0;i<31;i++){
  const x=(i+.5)/31*w,taper=1-Math.abs((i-15)/15)*.7;
  const amp=analyser&&playing?bins[Math.min(1023,i*3)]/255:.08+Math.abs(Math.sin(performance.now()*.002+i))*.14;
  const peak=(5+Math.pow(amp,1.6)*h*.65*punch)*taper;
  g.globalAlpha=.5+amp*.5;g.lineWidth=1.5+amp*2;
  g.beginPath();g.moveTo(x,mid+5);g.lineTo(x,mid-peak);g.stroke();
 }
 g.restore();g.globalAlpha=1;
 $("logoImage").style.filter=`drop-shadow(0 0 ${10+smoothBass*22*glow}px #32eaff) drop-shadow(0 0 ${15+smoothBass*25*glow}px #c13cff)`;
 const rec=document.querySelector(".record");
 rec.style.filter=`brightness(${1+smoothBass*glow})`;
 rec.style.transform=`scale(${1+(playing?smoothBass*.055:0)})`;
}
/* Logo particle burst and reconstruction effect */
const particleCanvas=$("logoParticles"),pg=particleCanvas.getContext("2d");
let dots=[],bursting=false,burstStart=0;
function resizeLogo(){
 const r=$("logoStage").getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);
 particleCanvas.width=Math.floor(r.width*1.4*d);particleCanvas.height=Math.floor(r.height*1.4*d);
 particleCanvas.style.width="140%";particleCanvas.style.height="140%";
 pg.setTransform(d,0,0,d,0,0);
}
function createDots(){
 const w=particleCanvas.width/(Math.min(devicePixelRatio||1,2));
 const h=particleCanvas.height/(Math.min(devicePixelRatio||1,2));
 dots=[];
 for(let i=0;i<190;i++){
  const a=Math.random()*Math.PI*2,r=Math.sqrt(Math.random())*Math.min(w,h)*.32;
  const tx=w/2+Math.cos(a)*r,ty=h/2+Math.sin(a)*r;
  dots.push({x:tx,y:ty,tx,ty,vx:0,vy:0,size:.7+Math.random()*2.2,color:palettes[effect][i%palettes[effect].length]});
 }
}
function burstLogo(){
 if(bursting)return;
 bursting=true;burstStart=performance.now();$("logoImage").style.opacity=".05";
 for(const p of dots){
  const a=Math.atan2(p.ty-particleCanvas.clientHeight/2,p.tx-particleCanvas.clientWidth/2);
  const force=35+Math.random()*100;
  p.vx=Math.cos(a)*force+(Math.random()-.5)*35;
  p.vy=Math.sin(a)*force+(Math.random()-.5)*35;
 }
 $("status").textContent="LOGO DISINTEGRATING • COSMIC PARTICLES";
}
for(const p of dots){
  if(bursting&&elapsed<900){p.x+=p.vx*.016;p.y+=p.vy*.016;p.vx*=.985;p.vy*=.985;}
  else{p.x+=(p.tx-p.x)*.085;p.y+=(p.ty-p.y)*.085;}
  pg.globalAlpha=bursting?.95:.35+smoothBass*.5;
  pg.fillStyle=p.color;pg.shadowBlur=bursting?13:5;pg.shadowColor=p.color;
  pg.beginPath();pg.arc(p.x,p.y,p.size*(1+smoothBass*.7),0,Math.PI*2);pg.fill();
 }
 pg.globalAlpha=1;pg.shadowBlur=0;
}
$("logoBurst").addEventListener("click",burstLogo);
$("rebuildBtn").addEventListener("click",burstLogo);
window.addEventListener("resize",()=>{resizeSpace();resizeScope();resizeLogo();createDots();});
resizeSpace();resizeScope();resizeLogo();createDots();
drawSpace();drawScope();animateLogo();
updateTrack();
if(songs.length)loadTrack(0,false);
</script>
</body>
</html>
'''
page = page.replace("__SONGS__", songs_json).replace("__LOGO__", logo_json)

st.markdown(
    """
    <style>
    #MainMenu,footer,header{visibility:hidden}
    .stApp{background:#03030b}
    .block-container{padding:0!important;max-width:100%!important}
    iframe{display:block;border:0}
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(page, height=1900, scrolling=True)
