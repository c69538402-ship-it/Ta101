import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
import mimetypes
import html

st.set_page_config(
    page_title="TA101 • NEON 3D MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(ellipse at top, #172554 0%, #08091b 55%, #02030a 100%);
        color: #f8fafc;
    }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1450px; padding-top: 1rem; padding-bottom: 2rem; }
    h1, h2, h3 { text-shadow: 0 0 12px #22d3ee, 0 0 24px #a855f7; }
    </style>
    """,
    unsafe_allow_html=True,
)

def find_logo():
    candidates = ("logo1.jpg", "logo1.jpeg", "logo1.png", "logo.jpg", "logo.jpeg", "โลโก้.jpg")
    for name in candidates:
        path = ROOT / name
        if path.is_file():
            return path
    return None

def find_songs():
    found = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        found.append(path)
    return sorted(found, key=lambda p: (p.name.lower(), str(p).lower()))

songs = find_songs()
logo_path = find_logo()

st.markdown(
    """
    <div style="text-align:center;font-size:clamp(30px,5vw,58px);
    font-weight:900;letter-spacing:3px;color:#f8fafc;
    text-shadow:0 0 12px #22d3ee,0 0 32px #a855f7">
    🎧 TA101 • NEON 3D MUSIC
    </div>
    <div style="text-align:center;color:#67e8f9;letter-spacing:4px;margin-bottom:12px">
    MUSIC • DREAM • TOGETHER
    </div>
    """,
    unsafe_allow_html=True,
)
# Encode assets for the HTML player. The player is independent of external 3D libraries.
tracks = []
for path in songs:
    try:
        mime = mimetypes.guess_type(str(path))[0] or "audio/mpeg"
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        tracks.append({
            "name": path.stem,
            "src": f"data:{mime};base64,{encoded}",
            "mime": mime,
        })
    except OSError:
        continue

logo_data = ""
if logo_path:
    try:
        mime = mimetypes.guess_type(str(logo_path))[0] or "image/jpeg"
        logo_data = "data:" + mime + ";base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")
    except OSError:
        logo_data = ""

if tracks:
    tracks_json = json.dumps(tracks, ensure_ascii=False).replace("</", "<\\/")
    logo_json = json.dumps(logo_data)
    player_html = r"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02030a;color:#fff;font-family:Arial,sans-serif}
#space{position:absolute;inset:0;width:100%;height:100%}
#hud{position:absolute;inset:0;padding:12px;display:flex;flex-direction:column;justify-content:space-between;pointer-events:none}
.top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.panel{background:#050b20d9;border:1px solid #22d3ee99;border-radius:13px;padding:10px 13px;backdrop-filter:blur(7px);box-shadow:0 0 16px #0891b244;max-width:48%}
.label{font-size:10px;letter-spacing:2px;color:#67e8f9}
#trackname{font-size:clamp(14px,2vw,23px);font-weight:bold;text-shadow:0 0 12px #22d3ee;overflow-wrap:anywhere}
#spectrum{width:min(30vw,310px);height:75px;display:block}
#logo{position:absolute;left:50%;top:39%;transform:translate(-50%,-50%);width:min(28vw,230px);height:min(28vw,230px);object-fit:contain;filter:drop-shadow(0 0 18px #22d3ee) drop-shadow(0 0 35px #a855f7)}
#brand{position:absolute;top:61%;left:50%;transform:translate(-50%,-50%);font-size:clamp(25px,4.5vw,54px);font-weight:1000;letter-spacing:4px;white-space:nowrap;text-shadow:0 0 10px #22d3ee,0 0 28px #a855f7}
#sub{position:absolute;top:69%;left:50%;transform:translate(-50%,-50%);font-size:10px;letter-spacing:4px;color:#a5f3fc;white-space:nowrap}
.controls{display:flex;justify-content:center;align-items:center;gap:7px;flex-wrap:wrap;pointer-events:auto}
button,select{color:white;background:linear-gradient(120deg,#082f49ee,#4c1d95ee);border:1px solid #22d3ee;border-radius:10px;padding:9px 11px;font-weight:bold;cursor:pointer;max-width:100%}
button:hover{box-shadow:0 0 17px #d946ef}
#play{font-size:20px;border-radius:50%;width:49px;height:49px;padding:0}
select{background:#080d25;max-width:230px}
.control{background:#080d25dd;border:1px solid #8b5cf6;border-radius:10px;padding:7px;display:flex;align-items:center;gap:6px;font-size:11px}
input{width:80px;accent-color:#22d3ee}
#status{font-size:10px;color:#c4b5fd;margin-top:5px;overflow-wrap:anywhere}
@media(max-width:600px){
 #hud{padding:7px}.panel{padding:7px;max-width:49%}#spectrum{width:29vw;height:54px}
 #logo{width:35vw;height:35vw;top:38%}#brand{top:57%;letter-spacing:2px}#sub{top:65%;letter-spacing:2px}
 .controls{gap:5px}button{padding:7px}select{max-width:125px}.control{padding:5px}input{width:52px}
}
</style>
</head>
<body>
<canvas id="space"></canvas>
<div id="hud">
 <div class="top">
  <div class="panel"><div class="label">NOW PLAYING</div><div id="trackname">TA101</div><div id="status">READY • CHOOSE A SONG</div></div>
  <div class="panel"><div class="label">LIVE AUDIO SPECTRUM</div><canvas id="spectrum"></canvas></div>
 </div>
 <img id="logo" alt="TA101 logo" style="display:none">
 <div id="brand">TA101</div><div id="sub">NEON MUSIC • 3D SPACE</div>
 <div class="controls">
  <select id="playlist" aria-label="เลือกเพลง"></select>
  <button id="prev" title="เพลงก่อนหน้า">⏮</button><button id="play" title="เล่น/หยุด">▶</button><button id="next" title="เพลงถัดไป">⏭</button>
  <button id="shuffle">🔀 OFF</button><button id="repeat">🔁 OFF</button>
  <div class="control">VOL <input id="volume" type="range" min="0" max="100" value="80"><span id="voltext">80%</span></div>
  <button id="full">⛶ เต็มจอ</button>
 </div>
</div>
    <audio id="audio" preload="metadata" playsinline></audio>
<script>
const TRACKS = __TRACKS__;
const LOGO_DATA = __LOGO__;
const audio = document.getElementById('audio');
const playlist = document.getElementById('playlist');
const playButton = document.getElementById('play');
const trackName = document.getElementById('trackname');
const statusText = document.getElementById('status');
const spectrum = document.getElementById('spectrum');
const sctx = spectrum.getContext('2d');
if (LOGO_DATA) { const logo=document.getElementById('logo'); logo.src=LOGO_DATA; logo.style.display='block'; }
TRACKS.forEach((track,i)=>{const o=document.createElement('option');o.value=i;o.textContent=String(i+1).padStart(2,'0')+' • '+track.name;playlist.appendChild(o);});
let current=0, shuffle=false, repeat=false, audioContext=null, analyser=null, sourceNode=null, bins=null;
function loadTrack(i, playNow=false){
 current=(i+TRACKS.length)%TRACKS.length;
 audio.src=TRACKS[current].src; playlist.value=String(current); trackName.textContent=TRACKS[current].name;
 statusText.textContent='TRACK '+(current+1)+' / '+TRACKS.length;
 if(playNow) playAudio();
}
async function setupAudio(){
 const AC=window.AudioContext||window.webkitAudioContext;
 if(!AC) return;
 if(!audioContext){
  audioContext=new AC(); analyser=audioContext.createAnalyser(); analyser.fftSize=256; analyser.smoothingTimeConstant=.78;
  sourceNode=audioContext.createMediaElementSource(audio); sourceNode.connect(analyser); analyser.connect(audioContext.destination);
  bins=new Uint8Array(analyser.frequencyBinCount);
 }
 if(audioContext.state==='suspended') await audioContext.resume();
}
async function playAudio(){
 try{
  await setupAudio();
  await audio.play();
  playButton.textContent='❚❚'; statusText.textContent='PLAYING • LIVE AUDIO';
 }catch(err){
  statusText.textContent='เล่นไม่ได้: '+(err && err.message ? err.message : 'แตะ ▶ อีกครั้ง');
  playButton.textContent='▶';
 }
}
playButton.onclick=()=>{if(audio.paused)playAudio();else{audio.pause();playButton.textContent='▶';statusText.textContent='PAUSED';}};
document.getElementById('prev').onclick=()=>loadTrack(current-1,true);
document.getElementById('next').onclick=()=>loadTrack(shuffle?Math.floor(Math.random()*TRACKS.length):current+1,true);
playlist.onchange=()=>loadTrack(Number(playlist.value),true);
document.getElementById('shuffle').onclick=e=>{shuffle=!shuffle;e.currentTarget.textContent=shuffle?'🔀 ON':'🔀 OFF';};
document.getElementById('repeat').onclick=e=>{repeat=!repeat;e.currentTarget.textContent=repeat?'🔁 ON':'🔁 OFF';};
audio.onended=()=>{if(repeat){audio.currentTime=0;playAudio();}else loadTrack(shuffle?Math.floor(Math.random()*TRACKS.length):current+1,true);};
audio.onerror=()=>{statusText.textContent='โหลดเสียงไม่สำเร็จ ตรวจสอบไฟล์เพลง';};
document.getElementById('volume').oninput=e=>{audio.volume=Number(e.target.value)/100;document.getElementById('voltext').textContent=e.target.value+'%';};
document.getElementById('full').onclick=async()=>{try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen();}catch(e){statusText.textContent='เบราว์เซอร์ไม่อนุญาตเต็มจอ';}};
audio.volume=.8;
loadTrack(0,false);
function drawSpectrum(){
 const dpr=window.devicePixelRatio||1,w=spectrum.clientWidth||250,h=spectrum.clientHeight||60;
 if(spectrum.width!==Math.floor(w*dpr)||spectrum.height!==Math.floor(h*dpr)){spectrum.width=Math.floor(w*dpr);spectrum.height=Math.floor(h*dpr);}
 sctx.setTransform(dpr,0,0,dpr,0,0);sctx.clearRect(0,0,w,h);
 if(analyser&&bins)analyser.getByteFrequencyData(bins);
 const n=42,bw=w/n;
 for(let i=0;i<n;i++){
  const v=(analyser&&bins)?bins[Math.floor(i*bins.length/n)]/255:(.08+.1*Math.abs(Math.sin(Date.now()/480+i*.6)));
  const bh=Math.max(3,v*(h-5)),grad=sctx.createLinearGradient(0,h-bh,0,h);
  grad.addColorStop(0,'#f0abfc');grad.addColorStop(.5,'#8b5cf6');grad.addColorStop(1,'#22d3ee');
  sctx.fillStyle=grad;sctx.shadowBlur=8;sctx.shadowColor='#22d3ee';sctx.fillRect(i*bw,h-bh,Math.max(2,bw-2),bh);
 }
 sctx.shadowBlur=0;requestAnimationFrame(drawSpectrum);
}
    drawSpectrum();
// Animated space backdrop made with Canvas; no external 3D library is required.
const space=document.getElementById('space'),ctx=space.getContext('2d');
let W=0,H=0,stars=[];
function resizeSpace(){W=space.width=Math.floor(innerWidth*(devicePixelRatio||1));H=space.height=Math.floor(innerHeight*(devicePixelRatio||1));space.style.width=innerWidth+'px';space.style.height=innerHeight+'px';ctx.setTransform(devicePixelRatio||1,0,0,devicePixelRatio||1,0,0);stars=Array.from({length:150},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight,z:.4+Math.random()*1.8,p:Math.random()*6.28}));}
addEventListener('resize',resizeSpace);resizeSpace();
function drawSpace(){
 const w=innerWidth,h=innerHeight,t=performance.now()/1000;
 ctx.clearRect(0,0,w,h);
 const bg=ctx.createRadialGradient(w*.5,h*.45,5,w*.5,h*.45,Math.max(w,h)*.7);bg.addColorStop(0,'rgba(20,35,95,.6)');bg.addColorStop(1,'rgba(2,3,10,.98)');ctx.fillStyle=bg;ctx.fillRect(0,0,w,h);
 for(const s of stars){s.y+=s.z*.18;if(s.y>h)s.y=0;ctx.globalAlpha=.35+.55*Math.abs(Math.sin(t*2+s.p));ctx.fillStyle=s.p%2?'#67e8f9':'#e9d5ff';ctx.fillRect(s.x,s.y,s.z,s.z);}
 ctx.globalAlpha=1;
 const cx=w/2,cy=h*.44,beat=(analyser&&bins)?bins[4]/255:0;
 ctx.save();ctx.translate(cx,cy);ctx.rotate(t*.12);
 for(let r=55;r<135;r+=17){ctx.beginPath();ctx.ellipse(0,0,r*(1+beat*.1),r*.42,Math.sin(t*.2+r)*.4,0,Math.PI*2);ctx.strokeStyle=r%2?'rgba(34,211,238,.6)':'rgba(192,38,255,.7)';ctx.lineWidth=1.5;ctx.shadowBlur=12;ctx.shadowColor=ctx.strokeStyle;ctx.stroke();}
 ctx.restore();ctx.shadowBlur=0;
 requestAnimationFrame(drawSpace);
}
drawSpace();
</script>
</body>
</html>"""
    player_html = player_html.replace("__TRACKS__", tracks_json).replace("__LOGO__", logo_json)
    components.html(player_html, height=790, scrolling=False)

    st.markdown("---")
    st.markdown("### 🎵 เครื่องเล่นสำรอง")
    st.caption("ใช้ทดสอบไฟล์เพลง หากเครื่องเล่นฉากอวกาศมีปัญหา")
    song_names = [p.name for p in songs]
    selected_song = st.selectbox(
        "เลือกเพลง",
        options=list(range(len(songs))),
        format_func=lambda i: song_names[i],
        key="ta101_fallback_song",
    )
    selected_path = songs[selected_song]
    fallback_mime = mimetypes.guess_type(str(selected_path))[0] or "audio/mpeg"
    st.audio(str(selected_path), format=fallback_mime)
    st.caption(f"พบไฟล์เพลงที่อ่านได้ {len(tracks)} เพลง")
else:
    st.error("ยังไม่พบไฟล์เพลงที่อ่านได้ในโปรเจกต์ TA101")
    st.info("วางไฟล์ MP3/WAV/OGG/M4A ในโฟลเดอร์เดียวกับ app.py แล้วรีเฟรชแอป")

if logo_path:
    st.caption(f"โลโก้ที่พบ: {logo_path.name}")
else:
    st.caption("ยังไม่พบ logo1.jpg — วางไฟล์โลโก้ไว้ข้าง app.py เพื่อแสดงในเครื่องเล่น")
