import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import mimetypes
import random

st.set_page_config(
    page_title="TA101 • NEON 3D MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}
LOGO_NAMES = ("logo1.jpg", "logo1.jpeg", "logo1.png", "logo.jpg", "logo.jpeg", "โลโก้.jpg")

st.markdown("""
<style>
.stApp{background:radial-gradient(ellipse at 50% 0%,#172554 0%,#08091b 48%,#02030a 100%);color:#f8fafc}
header[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1450px;padding-top:1rem;padding-bottom:2rem}
h1,h2,h3{ text-shadow:0 0 12px #22d3ee,0 0 24px #a855f7}
div[data-testid="stAudio"]{border:1px solid #22d3ee;border-radius:14px;padding:8px;background:#080d25}
</style>
""", unsafe_allow_html=True)

def find_logo():
    for name in LOGO_NAMES:
        p = ROOT / name
        if p.is_file():
            return p
    return None

def find_songs():
    found = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        try:
            rel = p.relative_to(ROOT)
            if any(part.startswith(".") for part in rel.parts):
                continue
            if any(part in {"venv", ".venv", "__pycache__"} for part in rel.parts):
                continue
            found.append(p)
        except (OSError, ValueError):
            continue
    return sorted(found, key=lambda p: (p.name.casefold(), str(p).casefold()))

songs = find_songs()
logo_path = find_logo()

st.markdown("""
<div style="text-align:center;font-size:clamp(30px,5vw,58px);font-weight:900;letter-spacing:3px;color:#f8fafc;text-shadow:0 0 12px #22d3ee,0 0 32px #a855f7">
🎧 TA101 • NEON 3D MUSIC
</div>
<div style="text-align:center;color:#67e8f9;letter-spacing:4px;margin-bottom:16px">
MUSIC • DREAM • TOGETHER
</div>
""", unsafe_allow_html=True)

# Always render the visual player independently from audio file discovery.
logo_uri = ""
if logo_path:
    try:
        mime = mimetypes.guess_type(str(logo_path))[0] or "image/jpeg"
        import base64
        logo_uri = f"data:{mime};base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")
    except OSError:
        logo_uri = ""
import json
visual_html = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02030a;color:white;font-family:Arial,sans-serif}
canvas{position:absolute;inset:0;width:100%;height:100%}
.hud{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-between;padding:12px;pointer-events:none}
.top{display:flex;justify-content:space-between;gap:10px}.panel{padding:10px 13px;border-radius:13px;border:1px solid #22d3ee99;background:#050b20d9;box-shadow:0 0 18px #0891b244;max-width:48%}
.label{font-size:10px;letter-spacing:2px;color:#67e8f9}.big{font-size:clamp(15px,2vw,23px);font-weight:bold;text-shadow:0 0 12px #22d3ee}
#logo{position:absolute;left:50%;top:39%;transform:translate(-50%,-50%);width:min(29vw,220px);height:min(29vw,220px);object-fit:contain;filter:drop-shadow(0 0 18px #22d3ee) drop-shadow(0 0 35px #a855f7)}
#brand{position:absolute;top:62%;left:50%;transform:translate(-50%,-50%);font-size:clamp(27px,5vw,56px);font-weight:1000;letter-spacing:4px;white-space:nowrap;text-shadow:0 0 10px #22d3ee,0 0 28px #a855f7}
#sub{position:absolute;top:70%;left:50%;transform:translate(-50%,-50%);font-size:10px;letter-spacing:4px;color:#a5f3fc;white-space:nowrap}
#bars{display:flex;align-items:end;height:70px;gap:3px;width:min(34vw,300px)}.bar{flex:1;min-width:2px;border-radius:4px 4px 0 0;background:linear-gradient(0deg,#22d3ee,#8b5cf6,#f0abfc);box-shadow:0 0 8px #22d3ee;animation:pulse var(--dur) ease-in-out infinite alternate;animation-delay:var(--delay)}
@keyframes pulse{from{height:12%}to{height:var(--height)}}
.bottom{display:flex;justify-content:space-between;align-items:end;gap:10px}.note{font-size:11px;color:#c4b5fd;max-width:45%;line-height:1.6}
@media(max-width:600px){.hud{padding:7px}.panel{padding:7px}.label{font-size:8px}#bars{height:52px;width:30vw}#logo{width:34vw;height:34vw;top:39%}#brand{top:59%;letter-spacing:2px}#sub{top:67%;letter-spacing:2px}.note{font-size:9px}}
</style></head><body>
<canvas id="space"></canvas><div class="hud">
<div class="top"><div class="panel"><div class="label">TA101 AUDIO SYSTEM</div><div class="big">NEON MUSIC</div><div class="label">MUSIC • DREAM • TOGETHER</div></div><div class="panel"><div class="label">NEON PULSE</div><div id="bars"></div></div></div>
<img id="logo" alt="TA101 logo" style="display:none"><div id="brand">TA101</div><div id="sub">COSMIC SOUND EXPERIENCE</div>
<div class="bottom"><div class="note">✦ COSMIC SPACE<br>✦ NEON LIGHTS • AUDIO VISUAL</div><div class="note" style="text-align:right">PLAYER BELOW ↓<br>CHOOSE A TRACK TO PLAY</div></div>
</div>
<script>
const logoData=__LOGO__;
if(logoData){const im=document.getElementById('logo');im.src=logoData;im.style.display='block';}
const bars=document.getElementById('bars');
for(let i=0;i<32;i++){const b=document.createElement('div');b.className='bar';b.style.setProperty('--height',(20+Math.random()*80)+'%');b.style.setProperty('--dur',(0.3+Math.random()*0.8)+'s');b.style.setProperty('--delay',(-Math.random()*1.5)+'s');bars.appendChild(b);}
const c=document.getElementById('space'),x=c.getContext('2d');let stars=[];
function resize(){const d=window.devicePixelRatio||1;c.width=innerWidth*d;c.height=innerHeight*d;c.style.width=innerWidth+'px';c.style.height=innerHeight+'px';x.setTransform(d,0,0,d,0,0);stars=Array.from({length:160},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight,z:.5+Math.random()*1.7,p:Math.random()*6.28}));}
addEventListener('resize',resize);resize();
function draw(){const w=innerWidth,h=innerHeight,t=performance.now()/1000;x.clearRect(0,0,w,h);const g=x.createRadialGradient(w*.5,h*.45,5,w*.5,h*.45,Math.max(w,h)*.75);g.addColorStop(0,'rgba(20,35,95,.75)');g.addColorStop(1,'rgba(2,3,10,.98)');x.fillStyle=g;x.fillRect(0,0,w,h);for(const s of stars){s.y+=s.z*.18;if(s.y>h)s.y=0;x.globalAlpha=.3+.7*Math.abs(Math.sin(t*2+s.p));x.fillStyle=s.p%2?'#67e8f9':'#e9d5ff';x.fillRect(s.x,s.y,s.z,s.z);}x.globalAlpha=1;x.save();x.translate(w/2,h*.43);x.rotate(t*.12);for(let r=55;r<140;r+=18){x.beginPath();x.ellipse(0,0,r,r*.42,Math.sin(t*.2+r)*.4,0,Math.PI*2);x.strokeStyle=r%2?'rgba(34,211,238,.6)':'rgba(192,38,255,.7)';x.lineWidth=1.5;x.shadowBlur=12;x.shadowColor=x.strokeStyle;x.stroke();}x.restore();x.shadowBlur=0;requestAnimationFrame(draw);}draw();
</script></body></html>"""
visual_html = visual_html.replace("__LOGO__", json.dumps(logo_uri))
components.html(visual_html, height=610, scrolling=False)

st.markdown("## 🎵 MUSIC PLAYER")
st.caption("เครื่องเล่นเสียงจริงของ Streamlit — ไม่ฝังไฟล์เพลงทั้งหมดไว้ใน HTML จึงลดโอกาสหน้าเครื่องเล่นว่าง")

if songs:
    names = [p.name for p in songs]
    selected_index = st.selectbox(
        "เลือกเพลง",
        options=list(range(len(songs))),
        format_func=lambda i: names[i],
        key="ta101_track_picker",
    )
    chosen = songs[selected_index]
    st.markdown(f"### 🎶 {chosen.stem}")
    mime = mimetypes.guess_type(str(chosen))[0] or "audio/mpeg"
    st.audio(str(chosen), format=mime)
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"พบเพลง {len(songs)} เพลง")
    with col2:
        st.caption(f"ไฟล์ที่เลือก: {chosen.suffix.lower()}")
else:
    st.warning("ยังไม่พบไฟล์เพลง กรุณาตรวจสอบว่าไฟล์ MP3/WAV/M4A อยู่ในโปรเจกต์เดียวกับ app.py")
