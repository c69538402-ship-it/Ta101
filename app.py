
import base64
import json
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 NEON MUSIC",
    page_icon="🎧",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".aac"}

def to_data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"

songs = []
for p in sorted(ROOT.iterdir(), key=lambda x: x.name.lower()):
    if p.is_file() and p.suffix.lower() in EXTS:
        try:
            songs.append({
                "name": p.stem,
                "src": to_data_uri(p),
            })
        except OSError:
            pass

logo_src = ""
for filename in ("logo.jpg", "logo1.jpg", "logo.jpeg", "logo1.jpeg", "โลโก้.jpg"):
    p = ROOT / filename
    if p.is_file():
        try:
            logo_src = to_data_uri(p)
            break
        except OSError:
            pass

page = r'''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#03040b;color:white;font-family:Arial,sans-serif}
#stage{height:100vh;min-height:600px;overflow:auto;position:relative;background:radial-gradient(ellipse at center,#19143b,#070914 65%,#02030a);--glow:1}
.ambient{position:absolute;width:45vw;height:45vw;border-radius:50%;filter:blur(70px);opacity:.22;pointer-events:none;background:#00d9ff;left:-15vw;top:10%;animation:float 8s infinite alternate}
.ambient.two{background:#d500ff;left:auto;right:-15vw;top:25%}
@keyframes float{to{transform:translate(8vw,-4vh) scale(1.2)}}
.top{height:60px;display:flex;align-items:center;justify-content:space-between;padding:10px 16px;position:relative;z-index:3}
.brand{font-weight:1000;letter-spacing:3px;font-size:clamp(15px,2vw,24px)}
.brand small{display:block;font-size:9px;color:#b5c7ff;letter-spacing:3px;margin-top:4px}
.shine{background:linear-gradient(100deg,#fff,#62f5ff,#ff5de8,#fff);background-size:250% auto;color:transparent;background-clip:text;-webkit-background-clip:text;animation:shine 3s linear infinite}
@keyframes shine{to{background-position:-250% center}}
button{cursor:pointer}
.full{border:1px solid #5cf2ff99;border-radius:30px;background:#10132be8;color:white;padding:12px;font-weight:bold;box-shadow:0 0 18px #5cf2ff33}
.layout{height:calc(100% - 60px);display:grid;grid-template-columns:minmax(120px,.7fr) minmax(280px,2fr) minmax(120px,.7fr);gap:14px;padding:8px 16px 16px;align-items:center;position:relative}
.logoPanel{display:flex;flex-direction:column;align-items:center;gap:18px}
.logoHalo{width:min(22vw,230px);aspect-ratio:1;border-radius:50%;display:grid;place-items:center;position:relative;background:#090e20;box-shadow:0 0 calc(35px * var(--glow)) #36eaff77;animation:breathe 1.1s ease-in-out infinite alternate}
.logoHalo:before,.logoHalo:after{content:"";position:absolute;inset:-10px;border:2px solid transparent;border-top-color:#5cf2ff;border-right-color:#ff54e8;border-radius:50%;filter:drop-shadow(0 0 9px #5cf2ff);animation:ring 2s ease-in-out infinite alternate}
.logoHalo:after{inset:-18px;border-bottom-color:#9a65ff;border-left-color:#ff54e8;animation-delay:-1s}
@keyframes ring{to{transform:scale(1.07);opacity:.45}}
@keyframes breathe{to{box-shadow:0 0 calc(55px * var(--glow)) #ff54e877;filter:brightness(1.25)}}
.logoHalo img{width:84%;height:84%;object-fit:contain;border-radius:50%;position:relative;z-index:1}
.caption{font-size:12px;letter-spacing:3px;font-weight:900;text-align:center}
.player{min-width:0;display:flex;flex-direction:column;align-items:center;gap:9px}
.eyebrow{font-size:10px;letter-spacing:3px;color:#b7c7ef}
.core{width:clamp(75px,9vw,120px);aspect-ratio:1;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle,#30325e,#080a17 70%);border:1px solid #9c7dff;box-shadow:0 0 30px #9d5cff66;transition:transform .08s}
.core span{font-size:52px;text-shadow:0 0 20px #5cf2ff}
.headphones{width:105px;filter:drop-shadow(0 0 9px #5cf2ff)}
.title{font-size:clamp(19px,2.8vw,34px);font-weight:1000;text-align:center;overflow-wrap:anywhere;line-height:1.2}
.subtitle{font-size:10px;letter-spacing:3px;color:#bac6e8;text-align:center}
.wave{height:clamp(90px,17vh,155px);width:100%;position:relative;background:repeating-linear-gradient(0deg,transparent 0 23px,#5c8bff13 24px),repeating-linear-gradient(90deg,transparent 0 5%,#5c8bff13 5.1% 5.2%)}
#wave{width:100%;height:100%}
.progress{width:100%;height:5px;border-radius:10px;background:#ffffff22;overflow:hidden;cursor:pointer}
#fill{width:0;height:100%;background:linear-gradient(90deg,#5cf2ff,#8d65ff,#ff54e8);box-shadow:0 0 12px #5cf2ff}
.times{width:100%;display:flex;justify-content:space-between;font-size:10px;color:#b7c6e9;margin-top:-4px}
.controls{display:flex;gap:14px;align-items:center}
.ctrl{width:43px;height:43px;border-radius:50%;background:#11162c;border:1px solid #ffffff33;color:white;font-size:17px}
#play{width:55px;height:55px;border:0;background:linear-gradient(135deg,#00d9ff,#8958ff,#ff54e8);box-shadow:0 0 24px #5cf2ff66;font-size:22px}
.label{font-size:9px;letter-spacing:3px;color:#b9c9ef;font-weight:bold}
.effects{display:flex;gap:5px;flex-wrap:wrap;justify-content:center}
.fx{padding:8px 10px;border-radius:20px;border:1px solid #ffffff33;background:#0d1024;color:#dce6ff;font-size:9px;font-weight:bold}
.fx.active{border-color:#5cf2ff;background:#10313d;box-shadow:0 0 13px #5cf2ff44}
.sliders{width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.sliders label{font-size:9px;color:#c5d0ef;display:flex;flex-direction:column;gap:5px}
input{width:100%;accent-color:#5cf2ff}
.playlist{max-height:65vh;overflow:auto;border:1px solid #ffffff25;border-radius:15px;padding:12px;background:#080b19d9}
.playlist h3{font-size:12px;letter-spacing:3px;margin:0 0 10px}
.track{width:100%;display:flex;gap:8px;padding:10px 7px;border:1px solid transparent;border-radius:8px;background:#ffffff09;color:#e7edff;text-align:left;margin-bottom:5px}
.track.selected{border-color:#5cf2ff99;background:#12303c}
.track span:nth-child(2){overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;font-size:10px}
.track span:first-child{color:#5cf2ff;font-size:10px}
@media(max-width:700px){
 .top{height:52px;padding:8px 10px}.brand{font-size:14px}.brand small{font-size:8px}.full{font-size:9px;padding:9px}
 .layout{height:calc(100% - 52px);grid-template-columns:1fr;grid-template-rows:auto 1fr auto;gap:6px;padding:5px 12px 12px;overflow:auto}
 .logoPanel{flex-direction:row;justify-content:center;gap:14px}.logoHalo{width:68px;flex:none}.logoHalo:before{inset:-5px}.logoHalo:after{inset:-9px}
 .caption{text-align:left;font-size:10px}.player{gap:7px}.core{width:70px}.core span{font-size:36px}.headphones{width:85px}.wave{height:95px}
 .playlist{max-height:115px}.playlist .track{padding:6px}.playlist h3{margin-bottom:5px}.sliders{gap:6px}
}
</style>
</head>
<body>
<div id="stage" class="fx-cyber">
<div class="ambient"></div><div class="ambient two"></div>
<div class="top"><div class="brand shine">TA101 • NEON MUSIC<small>♫ SOUND • LIGHT • MOTION ♫</small></div><button class="full" id="full">⛶ FULL SCREEN</button></div>
<div class="layout">
<section class="logoPanel">
<div class="logoHalo" id="halo"><img id="logo" alt="Logo"><span id="fallback" class="shine" style="font-size:50px">♫</span></div>
<div class="caption shine">FEEL THE MUSIC</div>
</section>
<section class="player">
<div class="eyebrow">NOW PLAYING • AUDIO REACTIVE</div>
<div class="core" id="core"><span>♫</span></div>
<svg class="headphones" viewBox="0 0 220 150">
<defs><linearGradient id="hg"><stop stop-color="#5cf2ff"/><stop offset=".5" stop-color="#9860ff"/><stop offset="1" stop-color="#ff54e8"/></linearGradient></defs>
<path d="M35 92C35 40 65 18 110 18s75 22 75 74" fill="none" stroke="url(#hg)" stroke-width="13" stroke-linecap="round"/>
<rect x="16" y="76" width="46" height="61" rx="17" fill="#11162a" stroke="url(#hg)" stroke-width="5"/>
<rect x="158" y="76" width="46" height="61" rx="17" fill="#11162a" stroke="url(#hg)" stroke-width="5"/>
<rect x="27" y="88" width="22" height="36" rx="10" fill="#5cf2ff"/><rect x="171" y="88" width="22" height="36" rx="10" fill="#ff54e8"/>
</svg>
<div style="width:100%"><div class="title shine" id="title">TA101 MUSIC</div><div class="subtitle" id="subtitle">♫ NEON AUDIO EXPERIENCE ♫</div></div>
<div class="wave"><svg id="wave" viewBox="0 0 1000 220" preserveAspectRatio="none"><defs><linearGradient id="grad"><stop stop-color="#5cf2ff"/><stop offset=".3" stop-color="#8a65ff"/><stop offset=".5" stop-color="#fff"/><stop offset=".75" stop-color="#ff54e8"/><stop offset="1" stop-color="#ff697c"/></linearGradient><filter id="blur"><feGaussianBlur stdDeviation="5"/></filter></defs><path id="glowPath" d="" fill="none" stroke="url(#grad)" stroke-width="12" opacity=".7" filter="url(#blur)"/><path id="linePath" d="" fill="none" stroke="url(#grad)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="progress" id="progress"><div id="fill"></div></div><div class="times"><span id="now">0:00</span><span id="end">0:00</span></div>
<div class="controls"><button class="ctrl" id="prev">⏮</button><button class="ctrl" id="play">▶</button><button class="ctrl" id="next">⏭</button></div>
<div class="label">CHOOSE YOUR EFFECT</div>
<div class="effects"><button class="fx active" data-fx="cyber">CYBER</button><button class="fx" data-fx="rainbow">RAINBOW</button><button class="fx" data-fx="laser">LASER</button><button class="fx" data-fx="gold">GOLD</button><button class="fx" data-fx="particle">PARTICLE</button><button class="fx" data-fx="calm">CALM</button></div>
<div class="sliders"><label>BASS PUNCH<input id="punch" type="range" min=".5" max="2.6" step=".1" value="1.7"></label><label>GLOW<input id="glow" type="range" min=".2" max="2" step=".1" value="1.2"></label><label>SHAKE<input id="shake" type="range" min="0" max="16" step="1" value="7"></label></div>
<div id="status" class="subtitle">AUTO NEXT ENABLED</div>
</section>
<aside class="playlist"><h3 class="shine">♫ PLAYLIST</h3><div id="tracks"></div></aside>
</div>
<script>
'''
const songs = __SONGS__;
const logoSrc = __LOGO__;
const $ = id => document.getElementById(id);
const audio = new Audio();
audio.preload = "auto";
let idx=0, playing=false, ctx=null, analyser=null, source=null, gain=null;
let punch=1.7, glow=1.2, shake=7, crossfading=false, raf=0;
function fmt(t){return Number.isFinite(t)?Math.floor(t/60)+":"+String(Math.floor(t%60)).padStart(2,"0"):"0:00";}
function name(s){return (s||"").replace(/\.[^/.]+$/,"").replace(/[_-]+/g," ");}
function status(s){$("status").textContent=s;}

if(logoSrc){$("logo").src=logoSrc;$("fallback").style.display="none";}
else{$("logo").style.display="none";}

function playlist(){
 const box=$("tracks");box.innerHTML="";
 if(!songs.length){box.textContent="ไม่พบ MP3 — ให้วางเพลงไว้ข้าง app.py";return;}
 songs.forEach((s,i)=>{
  const b=document.createElement("button");b.className="track"+(i===idx?" selected":"");
  const n=document.createElement("span");n.textContent=String(i+1).padStart(2,"0");
  const t=document.createElement("span");t.textContent=name(s.name);
  const p=document.createElement("span");p.textContent=(i===idx&&playing)?"♫":"▶";
  b.append(n,t,p);b.onclick=()=>{idx=i;load(true);};box.appendChild(b);
 });
}
function load(autoplay){
 if(!songs.length)return;
 crossfading=false;audio.pause();audio.src=songs[idx].src;audio.load();
 $("title").textContent=name(songs[idx].name);
 $("now").textContent="0:00";$("end").textContent="0:00";$("fill").style.width="0%";
 playlist();status("TRACK "+(idx+1)+" / "+songs.length+" • AUTO NEXT");
 if(autoplay)play();
}
function setup(){
 if(ctx)return;
 ctx=new (window.AudioContext||window.webkitAudioContext)();
 analyser=ctx.createAnalyser();analyser.fftSize=2048;analyser.smoothingTimeConstant=.72;
 source=ctx.createMediaElementSource(audio);gain=ctx.createGain();
 source.connect(analyser);analyser.connect(gain);gain.connect(ctx.destination);
}
async function play(){
 if(!songs.length)return;
 try{
  setup();if(ctx.state==="suspended")await ctx.resume();
  await audio.play();playing=true;$("play").textContent="❚❚";
  playlist();status("♫ PLAYING • AUTO NEXT ENABLED");visual();
 }catch(e){status("แตะปุ่มเล่นอีกครั้งเพื่อเริ่มเสียง");}
}
function pause(){audio.pause();playing=false;$("play").textContent="▶";playlist();}
$("play").onclick=()=>playing?pause():play();
$("prev").onclick=()=>{if(songs.length){idx=(idx-1+songs.length)%songs.length;load(playing);}};
$("next").onclick=()=>{if(songs.length){idx=(idx+1)%songs.length;load(playing);}};
function nextCrossfade(){
 if(crossfading||!songs.length)return;
 crossfading=true;
 if(!ctx||!gain){idx=(idx+1)%songs.length;load(true);return;}
 const now=ctx.currentTime;
 gain.gain.cancelScheduledValues(now);gain.gain.setValueAtTime(gain.gain.value,now);
 gain.gain.linearRampToValueAtTime(.001,now+.65);
 setTimeout(()=>{
  idx=(idx+1)%songs.length;audio.pause();audio.src=songs[idx].src;audio.load();
  $("title").textContent=name(songs[idx].name);
  audio.addEventListener("canplay",function ready(){
   audio.removeEventListener("canplay",ready);
   const t=ctx.currentTime;gain.gain.cancelScheduledValues(t);
   gain.gain.setValueAtTime(.001,t);gain.gain.linearRampToValueAtTime(1,t+1);
   audio.play().then(()=>{playing=true;crossfading=false;$("play").textContent="❚❚";playlist();}).catch(()=>{crossfading=false;});
  },{once:true});
 },680);
}
audio.addEventListener("ended",()=>{if(!crossfading&&songs.length){idx=(idx+1)%songs.length;load(true);}});
audio.addEventListener("timeupdate",()=>{
 if(audio.duration>0){
  $("now").textContent=fmt(audio.currentTime);$("end").textContent=fmt(audio.duration);
  $("fill").style.width=(audio.currentTime/audio.duration*100)+"%";
  if(audio.duration-audio.currentTime<1.1&&!crossfading)nextCrossfade();
 }
});
$("progress").onclick=e=>{
 if(audio.duration>0){const r=e.currentTarget.getBoundingClientRect();audio.currentTime=(e.clientX-r.left)/r.width*audio.duration;}
};

function frame(){
 if(analyser){
  const data=new Uint8Array(analyser.frequencyBinCount);analyser.getByteFrequencyData(data);
  let d="";
  for(let i=0;i<220;i++){
   const x=i/219*1000,p=i/219;
   const center=Math.pow(Math.max(0,Math.sin(p*Math.PI)),2.5);
   const amp=(data[Math.min(data.length-1,Math.floor(i/220*data.length*.5))]||0)/255;
   const spikes=(Math.sin(i*.7)>0.90?1.5:.45);
   const y=110-amp*center*105*punch*spikes;
   d+=(i?" L ":"M ")+x.toFixed(1)+" "+y.toFixed(1);
  }
  $("linePath").setAttribute("d",d);$("glowPath").setAttribute("d",d);
  let bass=0;for(let i=0;i<40;i++)bass+=data[i];bass/=40*255;
  $("core").style.transform=`scale(${1+bass*.3*punch}) translate(${(Math.random()-.5)*shake*bass*.12}px,${(Math.random()-.5)*shake*bass*.12}px)`;
  $("halo").style.transform=`scale(${1+bass*.17*punch})`;
  $("halo").style.filter=`brightness(${1+bass*.8})`;
  $("stage").style.setProperty("--glow",glow*(.7+bass));
 }else{
  const d="M0 110 L300 110 L350 100 L390 25 L420 190 L450 65 L485 110 L1000 110";
  $("linePath").setAttribute("d",d);$("glowPath").setAttribute("d",d);
 }
 raf=requestAnimationFrame(frame);
}
function visual(){if(!raf)frame();}
document.querySelectorAll(".fx").forEach(b=>b.onclick=()=>{
 document.querySelectorAll(".fx").forEach(x=>x.classList.remove("active"));b.classList.add("active");
 document.querySelectorAll("#stage")[0].className="";$("stage").classList.add("fx-"+b.dataset.fx);
 const colors={gold:["#ffe08a","#ff9c46","#fff0a8"],rainbow:["#5cf2ff","#ff54e8","#8b65ff"],laser:["#5cf2ff","#ff3366","#8b65ff"],particle:["#5cf2ff","#ff54e8","#8b65ff"],calm:["#8bdcff","#a6aaff","#c9a8ff"],cyber:["#5cf2ff","#ff54e8","#8b65ff"]};
 const c=colors[b.dataset.fx];document.documentElement.style.setProperty("--cyan",c[0]);document.documentElement.style.setProperty("--pink",c[1]);
});
$("punch").oninput=e=>punch=+e.target.value;
$("glow").oninput=e=>glow=+e.target.value;
$("shake").oninput=e=>shake=+e.target.value;
$("full").onclick=async()=>{
 try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen();}
 catch(e){status("ใช้เมนูเบราว์เซอร์เลือกเต็มจอได้ครับ");}
};
document.addEventListener("fullscreenchange",()=>{$("full").textContent=document.fullscreenElement?"✕ EXIT FULL SCREEN":"⛶ FULL SCREEN";});
document.addEventListener("keydown",e=>{
 if(e.key.toLowerCase()==="f")$("full").click();
 if(e.code==="Space"&&!["INPUT","BUTTON"].includes(document.activeElement.tagName)){e.preventDefault();playing?pause():play();}
});
if(songs.length)load(false);
else{$("title").textContent="NO MP3 FOUND";status="เพิ่มไฟล์เพลงไว้ในโฟลเดอร์เดียวกับ app.py";}
visual();
</script>
</div>
</body>
</html>
'''
page = page.replace("__SONGS__", json.dumps(songs, ensure_ascii=False))
page = page.replace("__LOGO__", json.dumps(logo_src, ensure_ascii=False))

st.markdown("""
<style>
#MainMenu,header,footer{visibility:hidden}
.stApp{background:#03040b}
.block-container{padding:0!important;max-width:100%!important}
iframe{border:0!important}
</style>
""", unsafe_allow_html=True)

components.html(page, height=900, scrolling=False)
