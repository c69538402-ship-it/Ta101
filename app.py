
import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • NEON MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            songs.append({"name": path.stem, "src": data_uri(path)})
        except OSError:
            pass

logo_src = ""
for filename in (
    "logo.jpg", "logo1.jpg", "logo.jpeg", "logo1.jpeg",
    "โลโก้.jpg", "logo.png", "logo1.png"
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
html,body{margin:0;background:#050610;color:#fff;
font-family:system-ui,"Segoe UI",sans-serif}
body{overflow-x:hidden}
#stage{position:relative;isolation:isolate;overflow:hidden;
max-width:900px;min-height:100vh;margin:auto;padding:20px 17px 30px;
background:radial-gradient(ellipse at 50% 28%,#25204c,#101225 45%,#04050c 100%)}
#stage:before,#stage:after{content:"";position:absolute;z-index:-1;
inset:-20%;pointer-events:none;filter:blur(45px);opacity:.7;
animation:ambient 7s ease-in-out infinite alternate}
#stage:before{background:radial-gradient(ellipse at 20% 30%,#00dfff66,transparent 38%),
radial-gradient(ellipse at 80% 40%,#ff00d455,transparent 35%)}
#stage:after{background:radial-gradient(ellipse at 50% 80%,#762bff55,transparent 40%)}
@keyframes ambient{to{transform:translate(2%,-2%) scale(1.1)}}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:10px;
padding:5px 0 17px;border-bottom:1px solid #9baaff30}
.brand{font-size:clamp(17px,4vw,29px);font-weight:1000;letter-spacing:.11em;
background:linear-gradient(90deg,#48f5ff,#b3a3ff,#ff4fd7);
-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 0 12px #8265ff88)}
.tagline{font-size:10px;letter-spacing:.2em;color:#b8caff;font-weight:900;margin-top:5px}
button{cursor:pointer;color:white;transition:filter .15s,transform .15s}
button:active{transform:scale(.94);filter:brightness(1.5)}
.fullscreen{padding:11px 13px;border:1px solid #4deaff;border-radius:30px;
background:#101429;font-size:11px;font-weight:900;white-space:nowrap;
box-shadow:0 0 20px #21dfff45}
.hero{text-align:center;padding:28px 0 4px}
.logo-ring{position:relative;width:min(52vw,235px);aspect-ratio:1;margin:0 auto 20px;
padding:7px;border-radius:50%;background:linear-gradient(140deg,#40f6ff,#8050ff,#ff39d0);
box-shadow:0 0 24px #00dfffcc,0 0 55px #9c39ff99,0 0 90px #ff38ca35;
animation:logoPulse 2s ease-in-out infinite}
.logo-ring:before,.logo-ring:after{content:"";position:absolute;border-radius:50%;pointer-events:none}
.logo-ring:before{inset:-12px;border:2px solid #d15cff;
box-shadow:0 0 20px #b54cff,0 0 38px #ff3bc8;animation:ringPulse 2s infinite}
.logo-ring:after{inset:-22px;border:1px solid #42f5ff99;
box-shadow:0 0 22px #42f5ff;animation:ringPulse 3s infinite reverse}
#logoImage{width:100%;height:100%;object-fit:cover;border-radius:50%;
border:3px solid #111329;position:relative;z-index:1;background:#111329}
.fallback{position:absolute;inset:7px;display:grid;place-items:center;
border-radius:50%;font-weight:1000;font-size:25px;letter-spacing:.06em;
text-shadow:0 0 10px #42f5ff,0 0 28px #ff3bc8}
@keyframes logoPulse{50%{transform:scale(1.05);filter:brightness(1.35)}}
@keyframes ringPulse{50%{transform:scale(1.06);opacity:1}}
.feel{font-size:clamp(12px,3.3vw,18px);letter-spacing:.24em;font-weight:950;
background:linear-gradient(90deg,#42f5ff,#e1d2ff,#ff4bcf);
-webkit-background-clip:text;background-clip:text;color:transparent}
.status{text-align:center;margin:27px 0 14px;font-size:10px;
letter-spacing:.18em;font-weight:900;color:#aebde9}
.record-wrap{width:min(43vw,175px);aspect-ratio:1;margin:0 auto 17px}
.record{position:relative;width:100%;height:100%;border-radius:50%;
background:repeating-radial-gradient(circle,#11121b 0 3px,#343346 4px 5px,#080910 6px 8px);
border:2px solid #a16aff;
box-shadow:0 0 25px #955cff,0 0 55px #c43cff65,inset 0 0 22px #000;
animation:recordPulse 2s ease-in-out infinite}
.record:before{content:"";position:absolute;inset:18%;border-radius:50%;
background:radial-gradient(circle,#36324c,#121321 70%,#080910);
border:1px solid #aaaaff77}
.record-label{position:absolute;z-index:2;inset:35%;border-radius:50%;
display:grid;place-items:center;background:linear-gradient(135deg,#35eaff,#6b5dff,#ff42ce);
font-size:clamp(12px,4vw,20px);font-weight:1000;
box-shadow:0 0 20px #5c9dff}
.record-hole{position:absolute;z-index:3;width:6%;aspect-ratio:1;
left:47%;top:47%;border-radius:50%;background:#080913}
@keyframes recordPulse{50%{box-shadow:0 0 35px #955cff,0 0 70px #e832ff99,inset 0 0 22px #000}}
#trackName{font-size:clamp(20px,5.5vw,31px);font-weight:1000;
line-height:1.4;overflow-wrap:anywhere;
background:linear-gradient(90deg,#e6fcff,#aaa9ff,#ff8ce7);
-webkit-background-clip:text;background-clip:text;color:transparent}
.subtrack{font-size:10px;letter-spacing:.23em;color:#b4c5ed;font-weight:900;margin-top:5px}
.visualizer{height:155px;margin:22px 0 12px;border-radius:13px;overflow:hidden;
background:linear-gradient(180deg,#10162b99,#07081255);
border:1px solid #8e8cff25;box-shadow:inset 0 0 25px #5233a422}
#scope{width:100%;height:100%;display:block}
input[type=range]{width:100%;accent-color:#ff4bd5}
.progress{display:flex;justify-content:space-between;font-size:12px;color:#c5cbed}
.controls{display:flex;align-items:center;justify-content:center;gap:clamp(12px,5vw,34px);margin:20px 0}
.ctrl{width:60px;height:60px;border:1px solid #8b9cff66;border-radius:50%;
background:#12162a;font-size:21px;font-weight:900;box-shadow:0 0 18px #6d5aff22}
.ctrl.main{width:86px;height:86px;border:0;font-size:30px;
background:linear-gradient(135deg,#25dfff,#665aff 55%,#f23bc9);
box-shadow:0 0 28px #7760ffcc,0 0 55px #ff35c966}
.section{text-align:center;letter-spacing:.22em;color:#c7d3ff;
font-size:12px;font-weight:1000;margin:24px 0 13px}
.effects{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.effect{border:1px solid #8f9bcb77;border-radius:28px;
background:#111528;padding:10px 13px;font-size:12px;font-weight:900}
.effect.active{border-color:#49f5ff;background:linear-gradient(120deg,#113c56,#37204e);
box-shadow:0 0 20px #3beaff88}
.panel{margin-top:17px;padding:14px;border:1px solid #8d83ff55;
border-radius:17px;background:#101326cc;box-shadow:inset 0 0 24px #4733a422}
.line{display:flex;align-items:center;justify-content:space-between;gap:10px;
margin:8px 0;font-size:12px;color:#d8e0ff}
select{max-width:65%;padding:8px;border-radius:9px;background:#151a30;color:white;border:1px solid #737ec2}
.knob{margin:15px 0}
.knob label{display:flex;justify-content:space-between;font-size:12px;color:#d3dcff;margin-bottom:5px}
.footer{text-align:center;margin-top:22px;color:#6977a6;font-size:10px;letter-spacing:.18em}
@media(min-width:700px){#stage{padding:28px 35px}.visualizer{height:190px}}
</style>
</head>
<body>
<div id="stage">
  <header class="topbar">
    <div>
      <div class="brand">TA101 • NEON MUSIC</div>
      <div class="tagline">♫ SOUND • LIGHT • MOTION ♫</div>
    </div>
    <button class="fullscreen" id="fullBtn">⛶ FULL SCREEN</button>
  </header>

  <section class="hero">
    <div class="logo-ring">
      <div class="fallback" id="fallbackLogo">SYNAPSE</div>
      <img id="logoImage" alt="SYNAPSE" style="display:none">
    </div>
    <div class="feel">FEEL THE MUSIC</div>
  </section>

  <div class="status" id="status">LIVE AUDIO REACTIVE • NEON POWER</div>

  <div class="record-wrap">
    <div class="record">
      <div class="record-label">TA</div>
      <div class="record-hole"></div>
    </div>
  </div>

  <div style="text-align:center">
    <div id="trackName">กำลังเตรียมเพลง…</div>
    <div class="subtrack">♫ NEON AUDIO EXPERIENCE ♫</div>
  </div>

  <div class="visualizer"><canvas id="scope"></canvas></div>
  <input id="seek" type="range" min="0" max="1000" value="0">
  <div class="progress"><span id="elapsed">0:00</span><span id="duration">0:00</span></div>

  <div class="controls">
    <button class="ctrl" id="prevBtn">◀◀</button>
    <button class="ctrl main" id="playBtn">▶</button>
    <button class="ctrl" id="nextBtn">▶▶</button>
  </div>

  <div class="section">CHOOSE YOUR EFFECT</div>
  <div class="effects">
    <button class="effect active" data-effect="CYBER">CYBER</button>
    <button class="effect" data-effect="RAINBOW">RAINBOW</button>
    <button class="effect" data-effect="LASER">LASER</button>
    <button class="effect" data-effect="GOLD">GOLD</button>
    <button class="effect" data-effect="PARTICLE">PARTICLE</button>
    <button class="effect" data-effect="CALM">CALM</button>
  </div>

  <div class="panel">
    <div class="line"><span>PLAY MODE</span>
      <select id="mode">
        <option value="next">AUTO NEXT</option>
        <option value="loop">LOOP ALL</option>
        <option value="one">REPEAT ONE</option>
        <option value="shuffle">SHUFFLE</option>
      </select>
    </div>
    <div class="line"><span>TRACK</span><span id="trackCount">0 SONGS</span></div>
    <div class="knob">
      <label for="punch"><span>BASS PUNCH</span><span id="punchVal">1.7×</span></label>
      <input id="punch" type="range" min="0.5" max="3" step="0.1" value="1.7">
    </div>
    <div class="knob">
      <label for="glow"><span>NEON GLOW</span><span id="glowVal">1.2×</span></label>
      <input id="glow" type="range" min="0.5" max="2.5" step="0.1" value="1.2">
    </div>
    <div class="knob">
      <label for="shake"><span>ENERGY SHAKE</span><span id="shakeVal">7</span></label>
      <input id="shake" type="range" min="0" max="12" step="1" value="7">
    </div>
  </div>
  <div class="footer">TA101 • SOUND INTO LIGHT • NEON EXPERIENCE</div>
</div>

<script>
const songs = __SONGS__;
const logoSrc = __LOGO__;
const $ = id => document.getElementById(id);
const audio = new Audio();
audio.preload = "metadata";

let idx = 0, playing = false, audioCtx = null, analyser = null;
let sourceNode = null, punch = 1.7, glow = 1.2, shake = 7;
let effect = "CYBER", seeking = false, bass = 0, smoothBass = 0;
const canvas = $("scope");
const g = canvas.getContext("2d");
let bins = new Uint8Array(1024);
let wave = new Uint8Array(2048);

const palettes = {
  CYBER:["#42f5ff","#a45bff","#ff3bc8"],
  RAINBOW:["#ff334f","#ffe84a","#35ffb2","#39a8ff","#e94cff"],
  LASER:["#54faff","#ffffff","#ff42d6"],
  GOLD:["#fff0a0","#ffb52e","#fff7db"],
  PARTICLE:["#45f8ff","#b15cff","#ff4fd8"],
  CALM:["#72d9ff","#a5a4ff","#e1c6ff"]
};

function fmt(t){
  if(!Number.isFinite(t)||t<0)return "0:00";
  return Math.floor(t/60)+":"+String(Math.floor(t%60)).padStart(2,"0");
}

function initAudio(){
  if(audioCtx)return;
  try{
    audioCtx=new (window.AudioContext||window.webkitAudioContext)();
    analyser=audioCtx.createAnalyser();
    analyser.fftSize=2048;
    analyser.smoothingTimeConstant=.78;
    sourceNode=audioCtx.createMediaElementSource(audio);
    sourceNode.connect(analyser);
    analyser.connect(audioCtx.destination);
  }catch(e){
    $("status").textContent="NEON VISUAL MODE • AUDIO READY";
  }
}

function updateTrack(){
  if(!songs.length){
    $("trackName").textContent="ยังไม่พบไฟล์เพลง";
    $("status").textContent="ใส่ไฟล์ MP3 ไว้ในโฟลเดอร์เดียวกับ app.py";
    $("trackCount").textContent="0 SONGS";
    return;
  }
  $("trackName").textContent=songs[idx].name;
  $("trackCount").textContent=(idx+1)+" / "+songs.length+" SONGS";
  $("seek").value=0;
  $("elapsed").textContent="0:00";
  $("duration").textContent="0:00";
}

function loadTrack(n, autoplay=false){
  if(!songs.length)return;
  idx=(n+songs.length)%songs.length;
  audio.src=songs[idx].src;
  audio.load();
  updateTrack();
  if(autoplay)playAudio();
}

function nextTrack(direction=1){
  if(!songs.length)return;
  const mode=$("mode").value;
  if(mode==="one"&&direction===1){
    loadTrack(idx,true);
    return;
  }
  if(mode==="shuffle"&&songs.length>1){
    let next=idx;
    while(next===idx)next=Math.floor(Math.random()*songs.length);
    idx=next;
  }else{
    idx=(idx+direction+songs.length)%songs.length;
  }
  loadTrack(idx,true);
}

async function playAudio(){
  if(!songs.length)return;
  initAudio();
  if(audioCtx&&audioCtx.state==="suspended"){
    try{await audioCtx.resume();}catch(e){}
  }
  try{
    await audio.play();
    playing=true;
    $("playBtn").textContent="Ⅱ";
    $("status").textContent="LIVE AUDIO REACTIVE • NEON POWER";
  }catch(e){
    playing=false;
    $("playBtn").textContent="▶";
    $("status").textContent="แตะปุ่มเล่นอีกครั้งเพื่อเริ่มเพลง";
  }
}

function pauseAudio(){
  audio.pause();
  playing=false;
  $("playBtn").textContent="▶";
}

$("playBtn").addEventListener("click",()=>playing?pauseAudio():playAudio());
$("nextBtn").addEventListener("click",()=>nextTrack(1));
$("prevBtn").addEventListener("click",()=>{
  if(audio.currentTime>3)audio.currentTime=0;
  else nextTrack(-1);
});

$("fullBtn").addEventListener("click",async()=>{
  try{
    if(!document.fullscreenElement)await $("stage").requestFullscreen();
    else await document.exitFullscreen();
  }catch(e){
    $("status").textContent="อุปกรณ์นี้ไม่รองรับโหมดเต็มหน้าจอ";
  }
});

audio.addEventListener("ended",()=>{
  if($("mode").value==="one")loadTrack(idx,true);
  else nextTrack(1);
});
audio.addEventListener("play",()=>{
  playing=true;
  $("playBtn").textContent="Ⅱ";
});
audio.addEventListener("pause",()=>{
  playing=false;
  $("playBtn").textContent="▶";
});
audio.addEventListener("loadedmetadata",()=>{
  $("duration").textContent=fmt(audio.duration);
});
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

$("punch").addEventListener("input",e=>{
  punch=Number(e.target.value);
  $("punchVal").textContent=punch.toFixed(1)+"×";
});
$("glow").addEventListener("input",e=>{
  glow=Number(e.target.value);
  $("glowVal").textContent=glow.toFixed(1)+"×";
});
$("shake").addEventListener("input",e=>{
  shake=Number(e.target.value);
  $("shakeVal").textContent=shake;
});
document.querySelectorAll("[data-effect]").forEach(button=>{
  button.addEventListener("click",()=>{
    effect=button.dataset.effect;
    document.querySelectorAll("[data-effect]").forEach(b=>{
      b.classList.toggle("active",b===button);
    });
  });
});

function resizeCanvas(){
  const rect=canvas.getBoundingClientRect();
  const d=Math.min(window.devicePixelRatio||1,2);
  canvas.width=Math.max(1,Math.floor(rect.width*d));
  canvas.height=Math.max(1,Math.floor(rect.height*d));
  g.setTransform(d,0,0,d,0,0);
}
window.addEventListener("resize",resizeCanvas);

function draw(){
  requestAnimationFrame(draw);
  const w=canvas.clientWidth,h=canvas.clientHeight;
  if(!w||!h)return;

  let energy=.025;
  if(analyser){
    analyser.getByteFrequencyData(bins);
    analyser.getByteTimeDomainData(wave);
    let sum=0;
    for(let i=0;i<18;i++)sum+=bins[i];
    bass=sum/18/255;
    smoothBass=smoothBass*.78+bass*.22;
    energy=.025+smoothBass*punch*.19;
  }

  const palette=palettes[effect]||palettes.CYBER;
  const gradient=g.createLinearGradient(0,0,w,0);
  palette.forEach((c,i)=>gradient.addColorStop(i/Math.max(1,palette.length-1),c));

  g.clearRect(0,0,w,h);
  g.fillStyle="#070916";
  g.fillRect(0,0,w,h);

  g.strokeStyle="#8d9cff19";
  g.lineWidth=1;
  for(let x=0;x<w;x+=28){
    g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke();
  }
  for(let y=0;y<h;y+=28){
    g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke();
  }

  const mid=h*.58;
  const points=Math.max(80,Math.floor(w/2));
  const calm=effect==="CALM"?.55:1;

  // Waveform derived from the real audio analyser when playback is active.
  g.save();
  g.strokeStyle=gradient;
  g.lineWidth=2.5;
  g.lineJoin="round";
  g.lineCap="round";
  g.shadowBlur=14*glow;
  g.shadowColor=palette[1]||palette[0];
  g.beginPath();

  for(let i=0;i<points;i++){
    const x=i/(points-1)*w;
    let v;
    if(analyser&&playing){
      const wi=Math.floor(i/(points-1)*(wave.length-1));
      v=(wave[wi]-128)/128;
    }else{
      v=Math.sin(i*.17+performance.now()*.002)*.07;
    }
    const y=mid+v*h*(.5+energy*1.5)*calm;
    if(i===0)g.moveTo(x,y);else g.lineTo(x,y);
  }
  g.stroke();

  // Bass peaks react to low-frequency audio data.
  for(let i=0;i<25;i++){
    const x=(i+.5)/25*w;
    const taper=1-Math.abs((i-12)/12)*.68;
    const level=analyser&&playing?bins[Math.min(1023,i*3)]/255:
      .2+Math.abs(Math.sin(performance.now()*.002+i))*.18;
    const peak=(8+Math.pow(level,1.7)*h*.55*punch)*taper*calm;
    g.globalAlpha=.45+level*.55;
    g.lineWidth=2+level*1.5;
    g.beginPath();
    g.moveTo(x,mid+4);
    g.lineTo(x,mid-peak);
    g.stroke();
  }
  g.restore();

  g.save();
  g.strokeStyle=gradient;
  g.lineWidth=3;
  g.shadowBlur=18*glow;
  g.shadowColor=palette[0];
  g.beginPath();g.moveTo(0,mid+5);g.lineTo(w,mid+5);g.stroke();
  g.restore();

  const ring=document.querySelector(".logo-ring");
  const record=document.querySelector(".record");
  ring.style.filter=`brightness(${1+smoothBass*glow*.7})`;
  record.style.filter=`brightness(${1+smoothBass*glow})`;
  record.style.transform=`scale(${1+(playing?smoothBass*.04:0)})`;
  if(shake>0&&playing&&smoothBass>.35){
    const amount=Math.min(shake,smoothBass*shake);
    $("stage").style.backgroundPosition=`${Math.sin(performance.now()*.04)*amount}px 0`;
  }else{
    $("stage").style.backgroundPosition="0 0";
  }
}

if(logoSrc){
  $("logoImage").src=logoSrc;
  $("logoImage").style.display="block";
  $("fallbackLogo").style.display="none";
}

resizeCanvas();
updateTrack();
if(songs.length)loadTrack(0,false);
draw();
</script>
</body>
</html>
'''

page = page.replace("__SONGS__", songs_json).replace("__LOGO__", logo_json)

st.markdown(
    """
    <style>
    #MainMenu,footer,header{visibility:hidden}
    .stApp{background:#050610}
    .block-container{padding:0!important;max-width:100%!important}
    iframe{display:block;border:0}
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(page, height=1750, scrolling=True)
