
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
    initial_sidebar_state="collapsed",
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
html,body{
 margin:0;background:#03030b;color:#fff;
 font-family:system-ui,"Segoe UI",sans-serif
}
body{overflow-x:hidden}
#universe{
 position:relative;isolation:isolate;overflow:hidden;
 max-width:900px;min-height:100vh;margin:auto;
 padding:16px 15px 28px;
 background:radial-gradient(ellipse at 50% 35%,#211747,#090a1b 52%,#02030a)
}
#space,#dust{
 position:absolute;inset:0;width:100%;height:100%;
 pointer-events:none
}
#space{z-index:-2}
#dust{z-index:-1}
.nebula{
 position:absolute;inset:-20%;z-index:-1;pointer-events:none;
 filter:blur(38px);
 background:
 radial-gradient(ellipse at 15% 25%,#00d9ff55,transparent 35%),
 radial-gradient(ellipse at 85% 35%,#ff00c844,transparent 35%),
 radial-gradient(ellipse at 55% 80%,#652bff55,transparent 40%);
 animation:nebula 12s ease-in-out infinite alternate
}
@keyframes nebula{
 to{transform:translate(2%,-2%) scale(1.12)}
}
.top{
 display:flex;justify-content:space-between;align-items:center;
 gap:10px;padding:5px 0 14px;
 border-bottom:1px solid #8c9bff35
}
.brand{
 font-size:clamp(17px,4.2vw,28px);font-weight:1000;
 letter-spacing:.06em;
 background:linear-gradient(90deg,#4af7ff,#c4a4ff,#ff56db,#4af7ff);
 background-size:250% auto;color:transparent;
 background-clip:text;-webkit-background-clip:text;
 animation:shine 4s linear infinite;
 filter:drop-shadow(0 0 12px #44dfff)
}
.tag{
 font-size:9px;letter-spacing:.16em;
 color:#a9b8e9;margin-top:5px
}
@keyframes shine{
 to{background-position:250% center}
}
button{
 color:white;cursor:pointer;font-family:inherit;
 transition:transform .15s,filter .15s
}
button:active{transform:scale(.94);filter:brightness(1.5)}
.full{
 border:1px solid #55efff;border-radius:24px;
 padding:10px 11px;background:#10142a;
 font-size:10px;font-weight:900;white-space:nowrap;
 box-shadow:0 0 20px #00cfff55
}
.hero{text-align:center;padding:25px 0 5px}
.logo-stage{
 width:min(47vw,205px);aspect-ratio:1;margin:0 auto 17px;
 position:relative;display:grid;place-items:center
}
.logo-stage:before,.logo-stage:after{
 content:"";position:absolute;inset:-7%;
 border:2px solid #45efff;border-radius:50%;
 box-shadow:0 0 22px #00eaff;
 animation:ring 3s ease-in-out infinite
}
.logo-stage:after{
 inset:-14%;border-color:#e44cff;border-style:dashed;
 box-shadow:0 0 25px #b34cff;
 animation:ring 4s ease-in-out infinite reverse
}
@keyframes ring{
 50%{transform:scale(1.06) rotate(9deg);opacity:.6}
}
.logo-glow{
 position:absolute;inset:0;border-radius:50%;
 background:radial-gradient(circle,#8a4dff77,transparent 70%);
 filter:blur(18px);animation:glow 1.6s infinite alternate
}
@keyframes glow{
 to{transform:scale(1.2);opacity:.6}
}
#logoImage{
 position:relative;width:100%;height:100%;object-fit:contain;
 border-radius:50%;z-index:2;
 filter:drop-shadow(0 0 15px #32eaff);
 animation:breath 2.4s ease-in-out infinite;
 transition:opacity .3s
}
@keyframes breath{
 50%{transform:scale(1.045);
 filter:drop-shadow(0 0 28px #d43cff)}
}
#logoFallback{
 position:absolute;z-index:2;font-size:22px;font-weight:1000;
 text-shadow:0 0 12px #3ff,0 0 30px #f3c
}
#logoParticles{
 position:absolute;z-index:4;inset:-20%;
 width:140%;height:140%;pointer-events:none
}
#logoBurst{
 position:relative;z-index:5;
 border:1px solid #c39bff;border-radius:25px;
 padding:9px 12px;background:#101127ee;
 font-size:10px;font-weight:900;
 box-shadow:0 0 18px #a64dff
}
.feel{
 font-size:clamp(12px,3.5vw,18px);
 font-weight:1000;letter-spacing:.14em;
 background:linear-gradient(90deg,#fff,#43f5ff,#c3a5ff,#ff5cdb,#fff);
 background-size:300% auto;color:transparent;
 background-clip:text;-webkit-background-clip:text;
 animation:shine 3s linear infinite
}
.status{
 text-align:center;font-size:10px;letter-spacing:.12em;
 color:#b8c7f7;margin:22px 0 13px
}
.record-wrap{
 width:min(31vw,125px);aspect-ratio:1;margin:0 auto 16px
}
.record{
 width:100%;height:100%;border-radius:50%;position:relative;
 background:repeating-radial-gradient(
 circle,#090a12 0 3px,#34334c 4px 5px,#11111b 6px 8px
 );
 border:2px solid #a66aff;
 box-shadow:0 0 24px #955cff,0 0 50px #d52bff55;
 transition:filter .15s,transform .15s
}
.record:before{
 content:"TA";position:absolute;inset:30%;
 border-radius:50%;display:grid;place-items:center;
 background:linear-gradient(135deg,#44eaff,#6c43ff,#ed3bd2);
 font-weight:1000;box-shadow:0 0 20px #995cff
}
.track{
 text-align:center;font-size:clamp(19px,5vw,30px);
 font-weight:1000;line-height:1.4;overflow-wrap:anywhere;
 background:linear-gradient(90deg,#fff,#53f5ff,#c6a6ff,#ff5bdb,#fff);
 background-size:250% auto;color:transparent;
 background-clip:text;-webkit-background-clip:text;
 animation:shine 5s linear infinite
}
.subtrack{
 text-align:center;font-size:9px;letter-spacing:.17em;
 color:#9baedb;margin-top:5px
}
.visual{
 height:150px;margin:20px 0 12px;
 border:1px solid #8b85ff55;border-radius:14px;
 overflow:hidden;background:#050817cc;
 box-shadow:inset 0 0 28px #552dff44
}
#scope{width:100%;height:100%;display:block}
input[type=range]{width:100%;accent-color:#ef4bd8}
.times{
 display:flex;justify-content:space-between;
 font-size:11px;color:#bac9ef
}
.controls{
 display:flex;justify-content:center;align-items:center;
 gap:clamp(12px,5vw,32px);margin:18px 0 22px
}
.ctrl{
 width:56px;height:56px;border-radius:50%;
 border:1px solid #898bff99;background:#10142b;
 font-size:19px;box-shadow:0 0 20px #614bff55
}
.ctrl.main{
 width:78px;height:78px;font-size:28px;border:0;
 background:linear-gradient(135deg,#22e7ff,#7550ff 55%,#f32dc8);
 box-shadow:0 0 30px #4fbcff,0 0 55px #b22fff
}
.heading{
 text-align:center;font-size:11px;font-weight:1000;
 letter-spacing:.17em;color:#d4d9ff;margin:22px 0 12px
}
.effects{
 display:flex;justify-content:center;gap:7px;flex-wrap:wrap
}
.effect{
 font-size:11px;font-weight:900;padding:9px 11px;
 border-radius:22px;border:1px solid #777bbd;background:#11152b
}
.effect.active{
 border-color:#42f5ff;
 background:linear-gradient(110deg,#12394b,#3a2051);
 box-shadow:0 0 20px #36dfff
}
.panel{
 padding:13px;margin-top:16px;border-radius:16px;
 border:1px solid #8877ff77;background:#0c1025ee;
 box-shadow:inset 0 0 22px #593cff33
}
.row{
 display:flex;justify-content:space-between;align-items:center;
 gap:10px;margin:8px 0;font-size:12px;color:#d8e1ff
}
select{
 max-width:68%;padding:8px;border-radius:9px;
 background:#151a30;color:white;border:1px solid #717cc7
}
.knob{margin:15px 0}
.knob label{
 display:flex;justify-content:space-between;
 font-size:11px;color:#cbd7ff;margin-bottom:5px
}
.smallbtn{
 border:1px solid #626eaa;background:#12172d;
 border-radius:20px;padding:8px 10px;font-size:10px
}
.footer{
 text-align:center;font-size:9px;color:#6876a9;
 letter-spacing:.15em;margin-top:22px
}
@media(min-width:650px){
 #universe{padding:24px 35px}
 .visual{height:185px}
}
</style>
</head>
<body>
<div id="universe">
<canvas id="space"></canvas>
<canvas id="dust"></canvas>
<div class="nebula"></div>

<header class="top">
 <div>
  <div class="brand">TA101 • 3D SPACE MUSIC</div>
  <div class="tag">COSMIC SOUND EXPERIENCE</div>
 </div>
 <button class="full" id="fullBtn">⛶ FULL SCREEN</button>
</header>

<section class="hero">
 <div class="logo-stage" id="logoStage">
  <div class="logo-glow"></div>
  <div id="logoFallback">SYNAPSE</div>
  <img id="logoImage" alt="TA101 logo" style="display:none">
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
<div class="times">
 <span id="elapsed">0:00</span>
 <span id="duration">0:00</span>
</div>

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
 <div class="row">
  <span>PLAY MODE</span>
  <select id="mode">
   <option value="next">AUTO NEXT</option>
   <option value="loop">LOOP ALL</option>
   <option value="one">REPEAT ONE</option>
   <option value="shuffle">SHUFFLE</option>
  </select>
 </div>
 <div class="row">
  <span>SONG LIBRARY</span><span id="trackCount">0 SONGS</span>
 </div>
 <div class="knob">
  <label><span>BASS PUNCH</span><span id="punchVal">1.8×</span></label>
  <input id="punch" type="range" min=".5" max="3" step=".1" value="1.8">
 </div>
 <div class="knob">
  <label><span>NEON GLOW</span><span id="glowVal">1.8×</span></label>
  <input id="glow" type="range" min=".5" max="3" step=".1" value="1.8">
 </div>
 <div class="knob">
  <label><span>SPACE ENERGY</span><span id="energyVal">8</span></label>
  <input id="energy" type="range" min="0" max="12" value="8">
 </div>
 <div class="row">
  <button class="smallbtn" id="rebuildBtn">✦ REBUILD LOGO</button>
  <span>3D STARFIELD ON</span>
 </div>
</div>
<div class="footer">TA101 • ENTER THE COSMOS • NEON SPACE EDITION</div>
</div>

<script>
