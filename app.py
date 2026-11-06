from pathlib import Path
import base64
import json
import mimetypes
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • NEON SPACE MUSIC",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            songs.append({
                "name": path.stem,
                "src": f"data:{mime};base64,{encoded}",
            })
        except OSError:
            continue

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")

logo_data = ""
for candidate in ("logo1.jpg", "logo1.jpeg", "logo1.png", "โลโก้.jpg", "logo.jpg"):
    logo_path = ROOT / candidate
    if logo_path.is_file():
        try:
            mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
            logo_data = f"data:{mime};base64,{base64.b64encode(logo_path.read_bytes()).decode('ascii')}"
            break
        except OSError:
            pass

logo_json = json.dumps(logo_data)

player_html = r"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Prompt:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--a:#00f5ff;--b:#bd00ff;--panel:rgba(5,8,25,.76)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02030b;color:#fff;font-family:Prompt,sans-serif}
#stage{position:relative;width:100%;height:min(940px,100vh);min-height:650px;overflow:hidden;background:radial-gradient(ellipse at 50% 45%,#10133c 0%,#050615 48%,#010208 100%);isolation:isolate}
#cosmic-nebula{position:absolute;inset:-18%;z-index:0;pointer-events:none;overflow:hidden;background:
radial-gradient(ellipse at 22% 32%,#183c9b88 0%,transparent 27%),
radial-gradient(ellipse at 78% 28%,#8b18b588 0%,transparent 25%),
radial-gradient(ellipse at 62% 78%,#007e9d66 0%,transparent 30%),
radial-gradient(ellipse at 35% 78%,#4c176b77 0%,transparent 29%),
radial-gradient(ellipse at center,#10133c 0%,#050615 47%,#010208 100%);
filter:saturate(1.35);animation:nebula-drift 28s ease-in-out infinite alternate}
#cosmic-nebula:before,#cosmic-nebula:after{content:"";position:absolute;inset:-25%;background:conic-gradient(from 0deg at 50% 50%,transparent 0deg,#00eaff15 55deg,transparent 115deg,#bd00ff20 205deg,transparent 270deg,#00f5ff10 320deg,transparent);filter:blur(42px);animation:aurora 35s linear infinite}
#cosmic-nebula:after{opacity:.65;transform:scale(.8) rotate(35deg);animation-duration:47s;animation-direction:reverse}
@keyframes nebula-drift{from{transform:translate3d(-1.5%,1%,0) scale(1)}to{transform:translate3d(1.5%,-1%,0) scale(1.08)}}
#space{position:absolute;inset:0;width:100%;height:100%;z-index:1}
.aurora{position:absolute;inset:-20%;z-index:2;pointer-events:none;background:conic-gradient(from 30deg at 50% 50%,transparent,#00eaff12,transparent,#b400ff18,transparent);filter:blur(45px);animation:aurora 18s linear infinite}
@keyframes aurora{to{transform:rotate(360deg)}}
.center{z-index:3}
.hud{position:absolute;inset:0;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:clamp(14px,3vw,30px);pointer-events:none}
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
#logo{display:none!important}
#logo-motion{position:absolute;width:58%;height:58%;z-index:2;overflow:visible;filter:drop-shadow(0 0 15px var(--a))}
#logo-placeholder{font-family:Orbitron,sans-serif;color:var(--a);font-size:12px;text-shadow:0 0 15px var(--a);text-align:center}
#burst{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
#burst-btn{pointer-events:auto;position:absolute;bottom:calc(100% + 12px);left:50%;transform:translateX(-50%);border:1px solid var(--a);border-radius:30px;background:#060817aa;color:#fff;padding:7px 13px;font:11px Prompt,sans-serif;white-space:nowrap;box-shadow:0 0 15px var(--a);cursor:pointer}
.visual{width:min(1000px,100%);height:clamp(125px,22vh,205px);display:block;filter:drop-shadow(0 0 12px var(--a));margin-bottom:5px;overflow:visible}
.panel{width:min(760px,100%);border:1px solid color-mix(in srgb,var(--a) 80%,white 5%);border-radius:22px;padding:clamp(14px,2.5vw,24px);background:var(--panel);backdrop-filter:blur(18px);box-shadow:0 0 25px color-mix(in srgb,var(--a) 18%,transparent),inset 0 0 24px #8a00ff0b}
.track{display:flex;align-items:center;gap:12px;min-width:0;margin-bottom:15px}
.thumb{width:54px;height:54px;flex:0 0 54px;border-radius:12px;border:1px solid var(--b);object-fit:cover;box-shadow:0 0 15px var(--b)}
.tracktext{min-width:0;flex:1}
#track-title{font-family:Orbitron,Prompt,sans-serif;font-size:clamp(15px,2.4vw,22px);font-weight:900;letter-spacing:.4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;background:linear-gradient(90deg,#fff,var(--a),#fff,var(--b),#fff);background-size:240% auto;-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 8px var(--a));animation:title-flow 5s linear infinite}
@keyframes title-flow{to{background-position:240% center}}
#track-sub{font-size:10px;color:var(--a);margin-top:5px;letter-spacing:2px;text-shadow:0 0 9px var(--a)}
.mixer{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:17px;padding:12px 14px;border:1px solid #ffffff20;border-radius:15px;background:linear-gradient(120deg,#00eaff0b,#bd00ff12);box-shadow:inset 0 0 18px #00eaff09}
.mix-channel{min-width:0}
.mix-head{display:flex;justify-content:space-between;gap:6px;font:10px Orbitron,sans-serif;letter-spacing:1px;color:#dceaff;margin-bottom:8px}
.mix-head b{color:var(--a);font-weight:700}
.mix-channel input{width:100%;height:5px;accent-color:var(--a);cursor:pointer;filter:drop-shadow(0 0 4px var(--a))}
.mixer-title{text-align:center;font:9px Orbitron,sans-serif;letter-spacing:3px;color:var(--b);margin-top:15px;text-shadow:0 0 10px var(--b)}
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
@media(max-width:560px){#stage{min-height:620px}.hud{padding:12px}.center{top:38%;width:min(78vw,360px);height:min(78vw,360px);max-height:36vh}.visual{height:clamp(110px,17vh,150px);margin-bottom:4px}.panel{padding:12px}.thumb{width:43px;height:43px;flex-basis:43px}.controls{gap:15px}#play{width:51px;height:51px}.subtitle{letter-spacing:2px}.foot{font-size:8px}.mixer{gap:8px;padding:10px 8px}.mix-head{font-size:8px;letter-spacing:.4px}}
</style>
</head>
<body>
<div id="stage">
 <div id="cosmic-nebula" aria-hidden="true"></div><canvas id="space"></canvas><div class="aurora"></div>
 <div class="center">
  <div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
  <img id="logo" alt="TA101 logo source" style="display:none">
  <canvas id="logo-motion" aria-label="Animated TA101 logo"></canvas>
  <div id="logo-placeholder">TA101<br>NEON MUSIC</div>
  <canvas id="burst"></canvas>
  <button id="
  .burst-btn" type="button">✦ แตกตัว / ประกอบโลโก้</button>
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
   <div class="mixer-title">✦ NEON MIX CONSOLE ✦</div>
   <div class="mixer">
    <div class="mix-channel"><div class="mix-head"><span>VOLUME</span><b id="vol-value">80%</b></div><input id="volume" type="range" min="0" max="100" value="80" aria-label="ปรับความดัง"></div>
    <div class="mix-channel"><div class="mix-head"><span>BASS</span><b id="bass-value">+4 dB</b></div><input id="bass" type="range" min="-12" max="12" value="4" aria-label="ปรับเสียงเบส"></div>
    <div class="mix-channel"><div class="mix-head"><span>TREBLE</span><b id="treble-value">+2 dB</b></div><input id="treble" type="range" min="-12" max="12" value="2" aria-label="ปรับเสียงแหลม"></div>
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
const SONGS = __SONGS__;
const LOGO = __LOGO__;
const $ = id => document.getElementById(id);
const audio = new Audio();
audio.preload = "auto";
audio.crossOrigin = "anonymous";
let index=0, playing=false, shuffle=false, loopList=true, single=false;
let ctx=null, analyser=null, source=null, freq=null, waveData=null, bassFilter=null, trebleFilter=null, masterGain=null;
let scene,camera,renderer,stars,core,coreMat,clock;
const stage=$("stage");
$("volume").addEventListener("input",e=>{
 const v=Number(e.target.value);
 $("vol-value").textContent=v+"%";
 if(masterGain&&ctx)masterGain.gain.setTargetAtTime(v/100,ctx.currentTime,.03);
});

$("bass").addEventListener("input",e=>{
 const v=Number(e.target.value);
 $("bass-value").textContent=(v>0?"+":"")+v+" dB";
 if(bassFilter&&ctx)bassFilter.gain.setTargetAtTime(v,ctx.currentTime,.03);
});

$("treble").addEventListener("input",e=>{
 const v=Number(e.target.value);
 $("treble-value").textContent=(v>0?"+":"")+v+" dB";
 if(trebleFilter&&ctx)trebleFilter.gain.setTargetAtTime(v,ctx.currentTime,.03);
});

/* ฉากอวกาศ 3 มิติด้วย Three.js */
const canvas=$("space");
try{
 scene=new THREE.Scene();
 scene.fog=new THREE.FogExp2(0x03040c,0.0038);
 camera=new THREE.PerspectiveCamera(62,1,.1,1200);
 camera.position.z=90;
 renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.8));

 const positions=new Float32Array(2400*3);
 const colors=new Float32Array(2400*3);

 for(let i=0;i<2400;i++){
  positions[i*3]=(Math.random()-.5)*330;
  positions[i*3+1]=(Math.random()-.5)*210;
  positions[i*3+2]=(Math.random()-.5)*650;
  const c=new THREE.Color().setHSL(.52+Math.random()*.28,.85,.55+Math.random()*.3);
  colors.set([c.r,c.g,c.b],i*3);
 }
 
 if(!size||!logoParticles.length)return;

 const {w,h}=size;
 const now=performance.now();
 const t=now*.001;

 let energy=0;

 if(analyser&&freq&&playing){
  analyser.getByteFrequencyData(freq);
  for(let i=0;i<freq.length;i++)energy+=freq[i];
  energy=energy/freq.length/255;
 }

 lctx.clearRect(0,0,w,h);
 bctx.clearRect(0,0,bc.clientWidth,bc.clientHeight);

 const progress=Math.min(1,(now-burstStart)/1300);
 const scatter=burstMode?progress:1-progress;

 for(const q of logoParticles){
  const drift=Math.sin(t*1.7+q.phase)*(1.5+energy*8);
  const flutter=Math.cos(t*1.3+q.phase)*(1.5+energy*8);

  const tx=q.tx+drift;
  const ty=q.ty+flutter;
  const sx=q.sx+Math.sin(t+q.phase)*22;
  const sy=q.sy+Math.cos(t*.9+q.phase)*22;

  const x=tx+(sx-tx)*scatter;
  const y=ty+(sy-ty)*scatter;
  const radius=q.r*(1+energy*1.8)*(1+Math.sin(t*2+q.phase)*.13);

  lctx.beginPath();
  lctx.fillStyle=q.color;
  lctx.shadowColor=Math.random()>.5?"#00f5ff":"#bd00ff";
  lctx.shadowBlur=8+energy*18;
  lctx.arc(x,y,radius,0,Math.PI*2);
  lctx.fill();

  if(burstMode&&Math.random()>.68){
   bctx.beginPath();
   bctx.fillStyle=q.color;
   bctx.shadowColor="#00f5ff";
   bctx.shadowBlur=10;
   bctx.arc(x,y,Math.max(.6,radius*.65),0,Math.PI*2);
   bctx.fill();
  }
 }

 lctx.shadowBlur=0;
 bctx.shadowBlur=0;
}

buildAnimatedLogo();
animateLogo();
window.addEventListener("resize",buildAnimatedLogo);
</script>
</body>
</html>"""

player_html = (
    player_html
    .replace("__SONGS__", songs_json)
    .replace("__LOGO__", logo_json)
)

st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility:hidden;}
    .stApp, [data-testid="stAppViewContainer"] {background:#02030b;}
    .block-container {padding:0 !important;max-width:100% !important;}
    iframe {border:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

if not songs:
    st.info("ยังไม่พบไฟล์เพลงในโฟลเดอร์เดียวกับ app.py ให้วางไฟล์ MP3 ไว้ใน GitHub repository เดียวกัน")

st.caption("🌌 ฉากอวกาศสร้างด้วย CSS และ Three.js ภายในแอป ไม่ใช้คลิปหรือภาพสต็อกภายนอก")
components.html(player_html, height=980, scrolling=False)
