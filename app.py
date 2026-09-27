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
.stage{
 position:relative;width:100%;min-height:980px;overflow:hidden;
 background:
 radial-gradient(circle at 50% 42%,rgba(90,0,255,.22),transparent 28%),
 radial-gradient(circle at 10% 80%,rgba(0,234,255,.15),transparent 25%),
 radial-gradient(circle at 90% 70%,rgba(255,0,160,.15),transparent 25%),
 #020208;
}
.noise{position:absolute;inset:0;opacity:.045;pointer-events:none;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E")}
.blob{position:absolute;border-radius:50%;filter:blur(75px);opacity:.32;pointer-events:none}
.b1{width:430px;height:430px;background:#00eaff;left:-220px;top:180px;animation:float1 8s ease-in-out infinite alternate}
.b2{width:450px;height:450px;background:#ff009d;right:-240px;top:300px;animation:float2 10s ease-in-out infinite alternate}
.b3{width:380px;height:380px;background:#693cff;left:35%;bottom:-270px;animation:float3 9s ease-in-out infinite alternate}
@keyframes float1{to{transform:translate(120px,70px) scale(1.15)}}
@keyframes float2{to{transform:translate(-100px,-80px) scale(1.18)}}
@keyframes float3{to{transform:translate(30px,-100px) scale(1.1)}}

.top{
 position:relative;z-index:10;display:flex;align-items:center;justify-content:space-between;
 padding:20px 24px 0;
}
.brand{display:flex;align-items:center;gap:11px}
.logo{
 width:48px;height:48px;border-radius:14px;object-fit:cover;
 border:1px solid rgba(255,255,255,.3);
 box-shadow:0 0 22px rgba(0,234,255,.35);
}
.brandtxt{font-weight:900;letter-spacing:3px;font-size:13px}
.status{font-size:9px;letter-spacing:3px;color:#8b8c9c}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#00ffb7;
 box-shadow:0 0 12px #00ffb7;margin-right:7px;animation:blink 1s infinite}
@keyframes blink{50%{opacity:.25}}

.content{position:relative;z-index:5;width:min(620px,94vw);margin:25px auto 0;text-align:center}
.kicker{font-size:9px;letter-spacing:6px;color:#666879;margin-bottom:15px}
.discbox{position:relative;width:min(370px,76vw);aspect-ratio:1;margin:auto;display:grid;place-items:center}
.halo{
 position:absolute;inset:-8%;border-radius:50%;
 background:conic-gradient(#00eaff,#713cff,#ff009d,#ffdf4a,#00eaff);
 filter:blur(20px);opacity:.5;animation:spin 7s linear infinite;
}
.halo2{
 position:absolute;inset:-2%;border-radius:50%;
 background:conic-gradient(transparent,#00eaff,transparent,#ff00c8,transparent);
 animation:pulseRing .65s steps(2,end) infinite;
}
.disc{
 position:absolute;inset:4%;border-radius:50%;
 background:
 radial-gradient(circle at 50% 50%,rgba(0,234,255,.16) 0 9%,transparent 10%),
 radial-gradient(circle at 50% 50%,#11131d 0 28%,#06070c 29% 48%,#0e1018 49% 66%,#05060b 67%);
 border:1px solid rgba(255,255,255,.13);
 box-shadow:inset 0 0 65px #000,0 0 55px rgba(0,234,255,.16);

}
.disc.playing{animation:corePulse .42s steps(2,end) infinite}
.disc:after{
 content:"";position:absolute;inset:15%;border-radius:50%;
 border:1px solid rgba(255,255,255,.05);
}
.cover{
 position:absolute;width:38%;aspect-ratio:1;border-radius:50%;object-fit:cover;
 border:3px solid rgba(255,255,255,.5);z-index:4;
 box-shadow:0 0 25px rgba(0,234,255,.6),0 0 55px rgba(255,0,180,.25);
}
.center{
 position:absolute;width:68px;height:68px;border-radius:50%;z-index:6;
 background:rgba(3,4,10,.88);border:1px solid rgba(255,255,255,.24);
 box-shadow:0 0 18px rgba(0,234,255,.35),inset 0 0 22px rgba(255,0,200,.18);
 display:grid;place-items:center;
}
.musicMark{
 font-size:30px;font-weight:900;color:#fff;line-height:1;
 text-shadow:0 0 8px #00eaff,0 0 20px #ff00c8;
}
.musicPulse{
 position:absolute;inset:-7px;border-radius:50%;
 border:1px solid rgba(0,234,255,.65);
 animation:pulseRing .42s steps(2,end) infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes corePulse{
  0%{transform:scale(1)}
  45%{transform:scale(1.035)}
  55%{transform:scale(.985)}
  100%{transform:scale(1)}
}
@keyframes spinrev{to{transform:rotate(-360deg)}}
@keyframes pulseRing{
  0%{opacity:.45;transform:scale(.99)}
  50%{opacity:1;transform:scale(1.025)}
  100%{opacity:.45;transform:scale(.99)}
}

.title{
 margin:23px auto 0;max-width:94%;
 font-size:clamp(24px,5vw,40px);font-weight:900;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
 background:linear-gradient(90deg,#fff,#66edff,#b478ff,#ff62ca,#fff);
 background-size:300% auto;-webkit-background-clip:text;color:transparent;
 animation:shine 5s linear infinite;
}
@keyframes shine{to{background-position:300% center}}
.artist{margin-top:7px;font-size:9px;letter-spacing:5px;color:#77798c}

.wave{
 height:78px;margin:17px auto 0;display:flex;align-items:center;justify-content:center;
 gap:3px;overflow:hidden;
}
.bar{width:4px;height:5px;border-radius:20px;
 background:linear-gradient(to top,#00eaff,#7650ff,#ff00c8);
 box-shadow:0 0 9px rgba(0,234,255,.45);transition:height .025s steps(3,end)}

.times{display:flex;justify-content:space-between;color:#707184;font-size:10px;margin-top:3px}
.progress{height:5px;border-radius:20px;background:rgba(255,255,255,.08);overflow:hidden;cursor:pointer;margin-top:7px}
.fill{height:100%;width:0;border-radius:20px;background:linear-gradient(90deg,#00eaff,#7a4cff,#ff00c8);
 box-shadow:0 0 14px #00eaff}

.controls{display:flex;align-items:center;justify-content:center;gap:18px;margin-top:20px}
.btn{
 width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.11);
 background:rgba(255,255,255,.045);color:#fff;font-size:17px;cursor:pointer;
 transition:.18s
}
.btn:hover{transform:scale(1.08);box-shadow:0 0 22px rgba(0,234,255,.3)}
.play{
 width:67px;height:67px;border:0;
 background:linear-gradient(135deg,#00eaff,#7041ff,#ff00c8);
 box-shadow:0 0 25px rgba(0,234,255,.42),0 0 50px rgba(255,0,200,.18);
 font-size:23px
}
.play:hover{transform:scale(1.1)}

.playlist{
 width:min(720px,94vw);margin:22px auto 0;padding:10px;
 border:1px solid rgba(255,255,255,.07);border-radius:16px;
 background:rgba(255,255,255,.035);backdrop-filter:blur(18px);
 max-height:155px;overflow:auto;text-align:left;
}
.pltitle{font-size:8px;letter-spacing:4px;color:#686a7b;padding:4px 8px 8px}
.track{display:flex;align-items:center;gap:10px;padding:9px;border-radius:10px;
 color:#9294a5;font-size:11px;cursor:pointer}
.track:hover{background:rgba(255,255,255,.06);color:#fff}
.track.active{background:linear-gradient(90deg,rgba(0,234,255,.12),rgba(255,0,200,.06));
 color:#fff;box-shadow:inset 2px 0 #00eaff}
.num{width:22px;color:#555768}
.track.active .num{color:#00eaff}
.name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

.visualText{
 position:absolute;bottom:12px;left:0;right:0;text-align:center;
 color:#555768;font-size:7px;letter-spacing:4px
}
.fs{
 position:absolute;right:20px;top:75px;z-index:20;width:38px;height:38px;border-radius:50%;
 border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);
 color:#77798a;cursor:pointer
}
@media(max-width:600px){
 .stage{min-height:900px}
 .top{padding:16px}
 .content{margin-top:15px}
 .discbox{width:76vw}
 .playlist{max-height:125px}
 .fs{top:68px;right:13px}
 .status{display:none}
}
</style>
</head>
<body>
<div class="stage">
<div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
<div class="noise"></div>

<div class="top">
  <div class="brand">
    <img id="logo" class="logo" alt="logo">
    <div class="brandtxt">NEON VISION</div>
  </div>
  <div class="status"><span class="dot"></span>LIVE AUDIO VISUALIZER</div>
</div>

<button class="fs" onclick="fullscreen()">⛶</button>

<div class="content">
  <div class="kicker">♫  MUSIC • LIGHT • MOTION  ♫</div>

  <div class="discbox">
    <div class="halo"></div>
    <div class="halo2"></div>
    <div id="disc" class="disc"></div>
    <img id="cover" class="cover" alt="cover">
    <div class="center"><span class="musicMark">♫</span><span class="musicPulse"></span></div>
  </div>

  <div id="title" class="title">NEON MUSIC</div>
  <div class="artist">♫  MUSIC EXPERIENCE  ♫</div>

  <div id="wave" class="wave"></div>

  <div class="times">
    <span id="now">0:00</span>
    <span id="total">0:00</span>
  </div>

  <div id="progress" class="progress">
    <div id="fill" class="fill"></div>
  </div>

  <div class="controls">
    <button id="prev" class="btn">⏮</button>
    <button id="play" class="btn play">▶</button>
    <button id="next" class="btn">⏭</button>
  </div>

  <div class="playlist">
    <div class="pltitle">YOUR MUSIC</div>
    <div id="tracks"></div>
  </div>
</div>

<div class="visualText">NEON VISION MUSIC EXPERIENCE</div>
</div>

<script>
const songs = __SONGS__;
const logoSrc = __LOGO__;

let index = 0;
const audio = new Audio();
audio.preload = "auto";

const disc = document.getElementById("disc");
const cover = document.getElementById("cover");
const title = document.getElementById("title");
const play = document.getElementById("play");
const tracks = document.getElementById("tracks");
const now = document.getElementById("now");
const total = document.getElementById("total");
const fill = document.getElementById("fill");
const progress = document.getElementById("progress");
const wave = document.getElementById("wave");

if (logoSrc) {
  document.getElementById("logo").src = logoSrc;
  cover.src = logoSrc;
}

const bars = [];
for(let i=0;i<72;i++){
  const b=document.createElement("div");
  b.className="bar";
  wave.appendChild(b);
  bars.push(b);
}

let ctx=null, analyser=null, source=null, connected=false;

function safe(t){
  return String(t).replace(/[&<>"']/g,m=>({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[m]));
}

function fmt(v){
  if(!v || isNaN(v)) return "0:00";
  let m=Math.floor(v/60);
  let s=Math.floor(v%60);
  return m+":"+String(s).padStart(2,"0");
}

function analyserSetup(){
  if(connected) return;
  try{
    ctx=new (window.AudioContext||window.webkitAudioContext)();
    analyser=ctx.createAnalyser();
    analyser.fftSize=128;
    source=ctx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(ctx.destination);
    connected=true;
  }catch(e){console.log(e)}
}

function draw(){
  requestAnimationFrame(draw);
  if(analyser){
    const data=new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(data);
    bars.forEach((b,i)=>{
      const n=data[Math.floor(i*data.length/bars.length)]||0;
      const kick = (n > 145 ? Math.random()*28 : Math.random()*7);
      b.style.height=Math.max(5,Math.min(86,n*.52+kick))+"px";
    });
  }else{
    bars.forEach((b,i)=>{
      b.style.height=(7+Math.abs(Math.sin(Date.now()/250+i*.45))*18)+"px";
    });
  }
}
draw();

function render(){
  tracks.innerHTML="";
  songs.forEach((s,i)=>{
    const d=document.createElement("div");
    d.className="track"+(i===index?" active":"");
    d.innerHTML='<span class="num">'+String(i+1).padStart(2,"0")+
      '</span><span class="name">'+safe(s.name)+'</span>';
    d.onclick=()=>{load(i);playAudio()};
    tracks.appendChild(d);
  });
}

function load(i){
  index=(i+songs.length)%songs.length;
  audio.src=songs[index].src;
  title.textContent=songs[index].name;
  now.textContent="0:00";
  total.textContent="0:00";
  fill.style.width="0%";
  render();
}

async function playAudio(){
  analyserSetup();
  try{
    if(ctx && ctx.state==="suspended") await ctx.resume();
    await audio.play();
    play.textContent="❚❚";
    disc.classList.add("playing");
  }catch(e){console.log(e)}
}

function pauseAudio(){
  audio.pause();
  play.textContent="▶";
  disc.classList.remove("playing");
}

play.onclick=()=>audio.paused?playAudio():pauseAudio();
document.getElementById("prev").onclick=()=>{load(index-1);playAudio()};
document.getElementById("next").onclick=()=>{load(index+1);playAudio()};

audio.addEventListener("ended",()=>{load(index+1);playAudio()});

audio.addEventListener("loadedmetadata",()=>{
  total.textContent=fmt(audio.duration);
});

audio.addEventListener("timeupdate",()=>{
  now.textContent=fmt(audio.currentTime);
  if(audio.duration){
    fill.style.width=(audio.currentTime/audio.duration*100)+"%";
  }
});

progress.onclick=(e)=>{
  if(!audio.duration)return;
  const r=progress.getBoundingClientRect();
  audio.currentTime=((e.clientX-r.left)/r.width)*audio.duration;
};

function fullscreen(){
  const el=document.querySelector(".stage");
  if(!document.fullscreenElement){
    if(el.requestFullscreen)el.requestFullscreen();
  }else{
    document.exitFullscreen();
  }
}

load(0);
</script>
</body>
</html>
'''

page = page.replace("__SONGS__", songs_json)
page = page.replace("__LOGO__", logo_json)

components.html(page, height=980, scrolling=False)
