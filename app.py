import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
import html

st.set_page_config(
    page_title="NEON VISION MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).resolve().parent

# ---------------------------------------------------------
# หาเพลง MP3 และ logo.jpg อัตโนมัติจากโฟลเดอร์เดียวกับ app.py
# ---------------------------------------------------------
songs = []
for p in sorted(BASE.glob("*.mp3"), key=lambda x: x.name.lower()):
    try:
        data = base64.b64encode(p.read_bytes()).decode("ascii")
        songs.append({
            "name": p.stem,
            "src": "data:audio/mpeg;base64," + data
        })
    except Exception:
        pass

logo_src = ""
logo_path = BASE / "logo.jpg"
if logo_path.exists():
    try:
        logo_src = "data:image/jpeg;base64," + base64.b64encode(
            logo_path.read_bytes()
        ).decode("ascii")
    except Exception:
        logo_src = ""

if not songs:
    st.markdown(
        "<div style='height:80vh;display:grid;place-items:center;"
        "background:#03030a;color:white;text-align:center;font-family:Arial'>"
        "<div><div style='font-size:72px'>🎧</div>"
        "<h1 style='letter-spacing:5px'>NEON VISION MUSIC</h1>"
        "<p style='color:#888'>นำไฟล์ .mp3 และ logo.jpg มาวางไว้ข้าง app.py</p>"
        "</div></div>",
        unsafe_allow_html=True,
    )
    st.stop()

songs_json = json.dumps(songs, ensure_ascii=False)
logo_json = json.dumps(logo_src)

# ---------------------------------------------------------
# ใช้ triple single quote ภายใน page เพื่อเลี่ยงปัญหา quote ซ้อน
# ---------------------------------------------------------
page = r'''
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#020208;color:#fff;font-family:Arial,sans-serif}
body{overflow:hidden}
.stage{position:relative;width:100%;height:980px;max-height:100vh;overflow:hidden;background:radial-gradient(circle at 50% 38%,rgba(40,0,120,.25),transparent 28%),radial-gradient(circle at 5% 78%,rgba(0,234,255,.13),transparent 26%),radial-gradient(circle at 95% 72%,rgba(255,0,160,.14),transparent 27%),#020208}
.noise{position:absolute;inset:0;opacity:.035;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
.blob{position:absolute;border-radius:50%;filter:blur(75px);opacity:.26;pointer-events:none}.b1{width:420px;height:420px;background:#00eaff;left:-220px;top:180px;animation:float1 8s ease-in-out infinite alternate}.b2{width:440px;height:440px;background:#ff009d;right:-240px;top:300px;animation:float2 10s ease-in-out infinite alternate}.b3{width:360px;height:360px;background:#693cff;left:35%;bottom:-250px;animation:float3 9s ease-in-out infinite alternate}
@keyframes float1{to{transform:translate(120px,70px) scale(1.15)}}@keyframes float2{to{transform:translate(-100px,-80px) scale(1.18)}}@keyframes float3{to{transform:translate(30px,-100px) scale(1.1)}}
.top{position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:18px 22px 0}.brand{display:flex;align-items:center;gap:11px}.logo{width:50px;height:50px;border-radius:15px;object-fit:cover;border:1px solid rgba(255,255,255,.3);box-shadow:0 0 22px rgba(0,234,255,.35)}.brandtxt{font-weight:900;letter-spacing:3px;font-size:14px}.status{font-size:9px;letter-spacing:3px;color:#7d7e90}.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#00ffb7;box-shadow:0 0 12px #00ffb7;margin-right:7px;animation:blink 1s infinite}@keyframes blink{50%{opacity:.25}}
.content{position:relative;z-index:5;width:min(680px,94vw);height:calc(100% - 74px);margin:5px auto 0;text-align:center;display:flex;flex-direction:column;align-items:center}.kicker{font-size:9px;letter-spacing:6px;color:#686a7b;margin:5px 0 10px}.discbox{position:relative;width:min(330px,42vh,76vw);aspect-ratio:1;display:grid;place-items:center;flex:0 0 auto}
.halo{position:absolute;inset:-8%;border-radius:50%;background:conic-gradient(#00eaff,#7a3cff,#ff00c8,#ffe66b,#00eaff);filter:blur(20px);opacity:.48;animation:haloPulse .55s steps(2,end) infinite}
.halo2{position:absolute;inset:2%;border-radius:50%;border:2px dashed rgba(0,234,255,.32);box-shadow:0 0 35px rgba(0,234,255,.28),inset 0 0 35px rgba(255,0,200,.12);animation:ringSnap .65s steps(4,end) infinite}
.core{position:absolute;inset:15%;border-radius:50%;background:radial-gradient(circle at 50% 48%,rgba(0,234,255,.2),transparent 22%),radial-gradient(circle,#111526 0 32%,#070912 33% 63%,#03040a 64%);border:1px solid rgba(255,255,255,.16);box-shadow:inset 0 0 55px #000,0 0 45px rgba(0,234,255,.2);transition:transform .04s steps(2,end)}
.core:before{content:"";position:absolute;inset:10%;border-radius:50%;border:1px solid rgba(255,255,255,.09);box-shadow:0 0 22px rgba(255,0,200,.22)}
.core.playing{animation:corePulse .18s steps(2,end) infinite}
.cover{position:absolute;width:43%;aspect-ratio:1;border-radius:24%;object-fit:cover;border:2px solid rgba(255,255,255,.52);z-index:4;box-shadow:0 0 22px rgba(0,234,255,.65),0 0 45px rgba(255,0,180,.3);transition:transform .04s steps(2,end);filter:saturate(1.15)}
.center{position:absolute;width:82px;height:82px;border-radius:28px;z-index:6;background:rgba(3,4,10,.88);border:1px solid rgba(255,255,255,.22);box-shadow:0 0 20px rgba(0,234,255,.42),inset 0 0 24px rgba(255,0,200,.2);display:grid;place-items:center;transform:rotate(45deg);overflow:visible}
.center:before{content:"";position:absolute;inset:-11px;border-radius:34px;border:1px solid rgba(0,234,255,.38);box-shadow:0 0 18px rgba(0,234,255,.25)}
.musicMark{font-size:32px;font-weight:900;color:#fff;line-height:1;text-shadow:0 0 8px #00eaff,0 0 20px #ff00c8;transform:rotate(-45deg)}
.headphone{position:absolute;bottom:-44px;left:50%;transform:translateX(-50%);font-size:30px;color:#fff;text-shadow:0 0 8px #00eaff,0 0 18px #ff00c8;z-index:8;letter-spacing:-5px}
.musicPulse{position:absolute;inset:-10px;border-radius:34px;border:2px solid rgba(0,234,255,.7);animation:pulseRing .22s steps(2,end) infinite}
@keyframes corePulse{0%{transform:scale(1)}25%{transform:scale(1.045)}48%{transform:scale(.94)}68%{transform:scale(1.065)}100%{transform:scale(1)}}
@keyframes pulseRing{0%{opacity:.2;transform:scale(.9)}40%{opacity:1;transform:scale(1.08)}100%{opacity:.15;transform:scale(.94)}}
@keyframes haloPulse{0%,100%{transform:scale(.95);opacity:.32}50%{transform:scale(1.09);opacity:.7}}
@keyframes ringSnap{0%{transform:rotate(0deg) scale(.97)}45%{transform:rotate(90deg) scale(1.03)}100%{transform:rotate(180deg) scale(.98)}}
.title{margin:9px auto 0;max-width:94%;font-size:clamp(21px,4.2vw,34px);font-weight:900;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;background:linear-gradient(90deg,#fff,#66edff,#b478ff,#ff62ca,#ffe66b,#fff);background-size:350% auto;-webkit-background-clip:text;color:transparent;animation:shine 4s linear infinite}@keyframes shine{to{background-position:350% center}}.artist{margin-top:4px;font-size:8px;letter-spacing:5px;color:#77798c}
.waveWrap{position:relative;width:100%;height:128px;margin:10px auto 0;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:18px;background:linear-gradient(180deg,rgba(0,0,0,.08),rgba(0,0,0,.2));border:1px solid rgba(255,255,255,.04)}.centerLine{position:absolute;left:0;right:0;top:50%;height:2px;background:linear-gradient(90deg,transparent,#00eaff,#fff,#ff00c8,#ffe66b,#00eaff,transparent);opacity:.8;box-shadow:0 0 14px #00eaff,0 0 28px #ff00c8;z-index:2}.wave{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;gap:3px;overflow:hidden;padding:0 8px}.bar{width:4px;height:8px;border-radius:8px;flex:1 1 0;max-width:7px;min-width:2px;transform-origin:center;background:linear-gradient(to top,#00eaff,#7a4cff,#ff00c8,#ffe66b);box-shadow:0 0 9px #00eaff,0 0 14px #ff00c8;transition:height .012s steps(2,end),transform .012s steps(2,end),filter .04s}
.times{width:100%;display:flex;justify-content:space-between;color:#707184;font-size:10px;margin-top:0}.progress{width:100%;height:5px;border-radius:20px;background:rgba(255,255,255,.08);overflow:hidden;cursor:pointer;margin-top:6px}.fill{height:100%;width:0;border-radius:20px;background:linear-gradient(90deg,#00eaff,#7a4cff,#ff00c8,#ffe66b);box-shadow:0 0 14px #00eaff}
.controls{display:flex;align-items:center;justify-content:center;gap:18px;margin-top:14px}.btn{width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.13);background:rgba(255,255,255,.045);color:#fff;font-size:17px;cursor:pointer;transition:.16s}.btn:hover{transform:scale(1.08);box-shadow:0 0 22px rgba(0,234,255,.3)}.play{width:65px;height:65px;border:0;background:linear-gradient(135deg,#00eaff,#7041ff,#ff00c8);box-shadow:0 0 25px rgba(0,234,255,.42),0 0 50px rgba(255,0,200,.18);font-size:22px}.play:hover{transform:scale(1.09)}
.effects{width:100%;display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin-top:10px}.fx{border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.035);color:#858797;border-radius:999px;padding:7px 12px;font-size:8px;letter-spacing:1.8px;cursor:pointer}.fx.active{color:#fff;border-color:#00eaff;background:linear-gradient(90deg,rgba(0,234,255,.12),rgba(255,0,200,.11));box-shadow:0 0 15px rgba(0,234,255,.14)}
.fxpanel{width:min(520px,100%);display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:8px;padding:8px 10px;border:1px solid rgba(255,255,255,.06);border-radius:14px;background:rgba(0,0,0,.18)}.sliderBox{text-align:left}.sliderBox label{display:flex;justify-content:space-between;color:#77798c;font-size:7px;letter-spacing:1.5px;margin-bottom:3px}.sliderBox b{color:#cdd0df;font-weight:600}.sliderBox input{width:100%;accent-color:#00eaff;height:14px}.playlist{width:100%;margin:9px auto 0;padding:8px;border:1px solid rgba(255,255,255,.07);border-radius:14px;background:rgba(255,255,255,.035);backdrop-filter:blur(18px);flex:1;min-height:60px;max-height:135px;overflow:auto;text-align:left}.pltitle{font-size:8px;letter-spacing:4px;color:#686a7b;padding:2px 8px 5px}.track{display:flex;align-items:center;gap:10px;padding:7px 9px;border-radius:9px;color:#9294a5;font-size:10px;cursor:pointer}.track:hover{background:rgba(255,255,255,.06);color:#fff}.track.active{background:linear-gradient(90deg,rgba(0,234,255,.12),rgba(255,0,200,.06));color:#fff;box-shadow:inset 2px 0 #00eaff}.num{width:22px;color:#555768}.track.active .num{color:#00eaff}.name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fxCanvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:3}.beatFlash{position:absolute;inset:0;background:radial-gradient(circle at 50% 48%,rgba(255,255,255,.3),rgba(0,234,255,.12),transparent 55%);opacity:0;pointer-events:none;z-index:4;mix-blend-mode:screen}.visualText{position:absolute;bottom:7px;left:0;right:0;text-align:center;color:#4e5061;font-size:7px;letter-spacing:4px}.fs{position:absolute;right:18px;top:72px;z-index:20;width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);color:#888a9a;cursor:pointer;font-size:17px}
.stage.fx-rainbow .bar{background:linear-gradient(to top,#00eaff,#00ff88,#ffe600,#ff6a00,#ff00c8,#704cff);box-shadow:0 0 10px #ff00c8}.stage.fx-rainbow .halo{background:conic-gradient(#00eaff,#00ff88,#ffe600,#ff7a00,#ff00c8,#704cff,#00eaff)}.stage.fx-laser .bar{background:linear-gradient(to top,#ffffff,#ff003c,#ff00d4);box-shadow:0 0 13px #ff003c}.stage.fx-laser .fill{background:linear-gradient(90deg,#fff,#ff003c,#ff00d4)}.stage.fx-laser .halo{background:conic-gradient(#fff,#ff003c,#ff00d4,#fff)}.stage.fx-gold .bar{background:linear-gradient(to top,#fff7a8,#ffe066,#ff9f1c,#ff4d00);box-shadow:0 0 10px #ffb300}.stage.fx-gold .fill{background:linear-gradient(90deg,#fff7a8,#ffe066,#ff9f1c)}.stage.fx-gold .halo{background:conic-gradient(#fff7a8,#ff9f1c,#ff4d00,#fff7a8)}.stage.fx-calm .bar{background:linear-gradient(to top,#5cf2ff,#6a7dff,#c07cff);box-shadow:0 0 8px #6a7dff}.stage.fx-calm .halo{opacity:.35;animation-duration:2.2s}.stage.fx-calm .musicPulse{animation-duration:1s}
@media(max-height:820px){.top{padding-top:10px}.logo{width:42px;height:42px}.content{margin-top:0}.kicker{margin:1px 0 4px}.discbox{width:min(270px,35vh,68vw)}.title{margin-top:5px;font-size:25px}.artist{margin-top:2px}.waveWrap{height:86px;margin-top:4px}.controls{margin-top:8px}.effects{margin-top:5px}.playlist{max-height:92px;margin-top:5px}.fs{top:57px}}
@media(max-width:600px){.stage{height:100vh}.top{padding:10px 13px 0}.brandtxt{font-size:12px}.status{display:none}.content{width:94vw;height:calc(100% - 58px)}.discbox{width:min(280px,36vh,70vw)}.waveWrap{height:92px}.bar{width:3px;flex-basis:3px}.controls{gap:12px}.btn{width:43px;height:43px}.play{width:61px;height:61px}.playlist{max-height:105px}.fxpanel{grid-template-columns:1fr}.waveWrap{height:104px}.fs{top:54px;right:10px}}
@media (display-mode:fullscreen){#stage{height:100vh;width:100vw}.content{width:min(760px,94vw);height:calc(100% - 70px)}.discbox{width:min(360px,38vh,72vw)}.waveWrap{height:140px}.playlist{max-height:150px}}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;transition:none!important}}
</style>
</head>
<body>
<div id="stage" class="stage"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="noise"></div>
<div class="top"><div class="brand"><img id="logo" class="logo" alt="logo"><div class="brandtxt">NEON VISION</div></div><div class="status"><span class="dot"></span>LIVE AUDIO VISUALIZER</div></div>
<button id="fs" class="fs" type="button" title="เต็มหน้าจอ">⛶</button>
<div class="content"><div class="kicker">♫ MUSIC • LIGHT • MOTION ♫</div>
<div class="discbox"><div class="halo"></div><div class="halo2"></div><div id="disc" class="core"></div><canvas id="fxCanvas" class="fxCanvas"></canvas><div id="beatFlash" class="beatFlash"></div><img id="cover" class="cover" alt="cover"><div class="center"><span class="musicMark">♫</span><span class="musicPulse"></span></div><div class="headphone">◖🎧◗</div></div>
<div id="title" class="title">NEON MUSIC</div><div class="artist">♫ MUSIC EXPERIENCE ♫</div>
<div class="waveWrap"><div class="centerLine"></div><div id="wave" class="wave"></div></div>
<div class="times"><span id="now">0:00</span><span id="total">0:00</span></div><div id="progress" class="progress"><div id="fill" class="fill"></div></div>
<div class="controls"><button id="prev" class="btn" type="button">⏮</button><button id="play" class="btn play" type="button">▶</button><button id="next" class="btn" type="button">⏭</button></div>
<div class="effects"><button class="fx active" data-fx="cyber" type="button">CYBER</button><button class="fx" data-fx="rainbow" type="button">RAINBOW</button><button class="fx" data-fx="laser" type="button">LASER</button><button class="fx" data-fx="gold" type="button">GOLD</button><button class="fx" data-fx="calm" type="button">CALM</button></div><div class="fxpanel"><div class="sliderBox"><label>PUNCH <b id="punchVal">85</b></label><input id="punch" type="range" min="20" max="160" value="85"></div><div class="sliderBox"><label>GLOW <b id="glowVal">70</b></label><input id="glow" type="range" min="0" max="120" value="70"></div><div class="sliderBox"><label>SHAKE <b id="shakeVal">75</b></label><input id="shake" type="range" min="0" max="130" value="75"></div></div>
<div class="playlist"><div class="pltitle">YOUR MUSIC</div><div id="tracks"></div></div></div><div class="visualText">NEON VISION MUSIC EXPERIENCE</div></div>
<script>
const songs=__SONGS__;const logoSrc=__LOGO__;let index=0;
const audio=new Audio();audio.preload="auto";
const stage=document.getElementById("stage"),disc=document.getElementById("disc"),cover=document.getElementById("cover"),title=document.getElementById("title"),play=document.getElementById("play"),tracks=document.getElementById("tracks"),now=document.getElementById("now"),total=document.getElementById("total"),fill=document.getElementById("fill"),progress=document.getElementById("progress"),wave=document.getElementById("wave"),canvas=document.getElementById("fxCanvas"),flash=document.getElementById("beatFlash"),ctx2=canvas.getContext("2d");
if(logoSrc){document.getElementById("logo").src=logoSrc;cover.src=logoSrc;}
const bars=[];for(let i=0;i<68;i++){const b=document.createElement("div");b.className="bar";b.style.setProperty("--i",i);wave.appendChild(b);bars.push(b);}
let ctx=null,analyser=null,source=null,connected=false,energy=0,peak=0,lastBeat=0,particles=[];
let punch=.85,glow=.70,shake=.75;
function safe(t){return String(t).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));}
function fmt(v){if(!v||isNaN(v))return "0:00";const m=Math.floor(v/60),s=Math.floor(v%60);return m+":"+String(s).padStart(2,"0");}
function analyserSetup(){if(connected)return;try{ctx=new(window.AudioContext||window.webkitAudioContext)();analyser=ctx.createAnalyser();analyser.fftSize=512;analyser.smoothingTimeConstant=.08;source=ctx.createMediaElementSource(audio);source.connect(analyser);analyser.connect(ctx.destination);connected=true;}catch(e){console.log(e);}}
function resizeCanvas(){const r=canvas.getBoundingClientRect(),d=devicePixelRatio||1;canvas.width=Math.max(1,Math.floor(r.width*d));canvas.height=Math.max(1,Math.floor(r.height*d));ctx2.setTransform(d,0,0,d,0,0);}
window.addEventListener("resize",resizeCanvas);resizeCanvas();
function spawn(count=3,pow=1){const w=canvas.clientWidth,h=canvas.clientHeight,cx=w/2,cy=h*.48;for(let i=0;i<count;i++){const a=Math.random()*Math.PI*2,s=(.6+Math.random()*2.2)*pow;particles.push({x:cx,y:cy,vx:Math.cos(a)*s,vy:Math.sin(a)*s,r:1+Math.random()*2.6,life:1,h:Math.random()*360});}if(particles.length>180)particles.splice(0,particles.length-180);}
function drawParticles(){const w=canvas.clientWidth,h=canvas.clientHeight;ctx2.clearRect(0,0,w,h);ctx2.globalCompositeOperation="lighter";for(let i=particles.length-1;i>=0;i--){const p=particles[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.985;p.vy*=.985;p.life-=.014;if(p.life<=0||p.x<0||p.x>w||p.y<0||p.y>h){particles.splice(i,1);continue;}ctx2.beginPath();ctx2.arc(p.x,p.y,p.r*p.life,0,Math.PI*2);ctx2.fillStyle=`hsla(${p.h},100%,65%,${p.life*.72})`;ctx2.shadowBlur=10;ctx2.shadowColor=`hsl(${p.h} 100% 60%)`;ctx2.fill();}ctx2.shadowBlur=0;ctx2.globalCompositeOperation="source-over";}
function draw(){
 requestAnimationFrame(draw);
 let data=null;if(analyser){data=new Uint8Array(analyser.frequencyBinCount);analyser.getByteFrequencyData(data);}
 const t=performance.now()/1000;let bass=0,mid=0,high=0;
 if(data){for(let i=0;i<Math.min(14,data.length);i++)bass+=data[i];bass/=14*255;for(let i=14;i<70&&i<data.length;i++)mid+=data[i];mid/=56*255;for(let i=70;i<150&&i<data.length;i++)high+=data[i];high/=80*255;}
 else{bass=.18+Math.abs(Math.sin(t*3))*.24;mid=.22+Math.abs(Math.sin(t*4.3))*.18;high=.18+Math.abs(Math.sin(t*6.8))*.15;}
 energy=Math.min(1,bass*.72+mid*.2+high*.08);peak=Math.max(peak*.91,energy);
 const kick=Math.max(0,(energy-.32))*punch;
 bars.forEach((b,i)=>{
   let n=0;
   if(data){const pos=Math.floor((i/68)*data.length);let a=data[Math.max(0,pos-3)]||0,c=data[pos]||0,d=data[Math.min(data.length-1,pos+3)]||0;n=(a+c*2.4+d)/4.4;}
   else n=20+Math.abs(Math.sin(t*3+i*.63))*35;
   const side=i<34?i:67-i;
   const jitter=(Math.random()-0.5)*shake*18;
   const centerBoost=1+(1-side/34)*.48;
   const h=Math.max(5,Math.min(58
