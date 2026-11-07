
from pathlib import Path
import base64
import mimetypes
import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • NEON DJ STUDIO",
    page_icon="🎧",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent
EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

st.markdown("""
<style>
.stApp {
 background:radial-gradient(ellipse at 50% 0%,
 #10345b,#050a18 48%,#09031a);
 color:#effaff;
}
header[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1100px;padding-top:.7rem}
.v4title{
 text-align:center;
 font-size:clamp(29px,6vw,55px);
 font-weight:1000;
 letter-spacing:3px;
 color:#fff;
 text-shadow:0 0 10px #00eaff,
 0 0 28px #477bff,0 0 45px #a000ff
}
.v4sub{
 text-align:center;color:#83efff;
 letter-spacing:4px;font-size:12px;
 margin:8px 0 18px
}
div.stButton>button{
 background:linear-gradient(135deg,#082747,#28104b);
 color:#eaffff;border:1px solid #35dfff;
 border-radius:12px;min-height:42px;
 box-shadow:0 0 12px #00cfff44;
 font-weight:800
}
div.stButton>button:hover{
 box-shadow:0 0 20px #00dfff;border-color:white
}
.panel{
 border:1px solid #20658a;border-radius:18px;
 padding:14px;
 background:linear-gradient(145deg,#07152b,#100a25);
 box-shadow:0 0 22px #00cfff15
}
</style>
""", unsafe_allow_html=True)

def get_tracks():
    out = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            if any(x.startswith(".") or x in {
                "venv", ".venv", "__pycache__"
            } for x in p.relative_to(ROOT).parts):
                continue
            out.append(p)
    return sorted(out, key=lambda x:x.name.casefold())

tracks = get_tracks()

logo = next(
    (ROOT/x for x in ("logo1.jpg","logo1.jpeg","logo1.png")
     if (ROOT/x).is_file()),
    None
)

st.markdown(
    '<div class="v4title">🎧 TA101 • NEON DJ STUDIO</div>'
    '<div class="v4sub">MUSIC • DREAM • TOGETHER</div>',
    unsafe_allow_html=True
)

if logo:
    mt = mimetypes.guess_type(logo.name)[0] or "image/jpeg"
    b64 = base64.b64encode(logo.read_bytes()).decode()
    st.markdown(
        f'<div style="text-align:center;margin:12px">'
        f'<img src="data:{mt};base64,{b64}" '
        'style="width:min(200px,45vw);border-radius:50%;'
        'border:2px solid #26eaff;'
        'box-shadow:0 0 22px #00dfff,0 0 48px #7b39ff;'
        'animation:pulse 2s infinite alternate">'
        '<style>@keyframes pulse{to{filter:brightness(1.35);'
        'transform:scale(1.04)}}</style></div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### 🎶 MUSIC PLAYER")

if not tracks:
    st.warning(
        "ไม่พบเพลง กรุณาวาง MP3/WAV/M4A "
        "ไว้ข้าง app.py หรือโฟลเดอร์ย่อย"
    )
else:
    if "v4idx" not in st.session_state:
        st.session_state.v4idx = 0

    st.session_state.v4idx = min(
        st.session_state.v4idx, len(tracks)-1
    )

    idx = st.selectbox(
        "เลือกเพลง",
        range(len(tracks)),
        format_func=lambda i:tracks[i].stem,
        index=st.session_state.v4idx,
        key="v4song"
    )

    st.session_state.v4idx = idx

    prev, nxt = st.columns(2)

    with prev:
        if st.button("⏮ เพลงก่อนหน้า", use_container_width=True):
            st.session_state.v4idx = (idx-1)%len(tracks)
            st.rerun()

    with nxt:
        if st.button("เพลงถัดไป ⏭", use_container_width=True):
            st.session_state.v4idx = (idx+1)%len(tracks)
            st.rerun()

    p = tracks[idx]
    mime = mimetypes.guess_type(p.name)[0] or "audio/mpeg"
    encoded = base64.b64encode(p.read_bytes()).decode("ascii")
    
    # เครื่องเล่นเสียง Web Audio
    # ฝังเฉพาะเพลงที่เลือก ไม่ฝังเพลงทั้งหมด
    player = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{
 margin:0;background:transparent;color:#effaff;
 font-family:Arial,sans-serif
}
.wrap{
 padding:13px;border-radius:16px;
 background:linear-gradient(145deg,#07152b,#100a25);
 border:1px solid #1e668c
}
.name{
 text-align:center;color:#8ff5ff;
 font-weight:800;font-size:17px;
 overflow-wrap:anywhere;margin:4px 0 12px
}
canvas{
 width:100%;height:125px;display:block;
 background:#020817;border:1px solid #123b61;
 border-radius:12px
}
.buttons{
 display:flex;justify-content:center;
 gap:8px;flex-wrap:wrap;margin:12px 0
}
button{
 border:1px solid #30dcff;
 background:linear-gradient(135deg,#092747,#28104b);
 color:white;border-radius:11px;
 padding:10px 15px;font-weight:bold
}
.row{
 display:grid;grid-template-columns:65px 1fr 32px;
 gap:7px;align-items:center;margin:10px 0;
 color:#9ceaff;font-size:12px
}
input{width:100%;accent-color:#00eaff}
.hint{text-align:center;color:#7198bd;font-size:11px}
</style>
</head>
<body>
<div class="wrap">
<div class="name">♫ __TITLE__</div>
<canvas id="cv"></canvas>

<div class="buttons">
<button id="play">▶ PLAY</button>
<button id="stop">■ STOP</button>
<button id="mute">🔊 SOUND</button>
<button id="loop">🔁 LOOP OFF</button>
</div>

<div class="row">
BASS<input id="bass" type="range" min="-12" max="12" value="0">
<b id="bval">0</b>
</div>
<div class="row">
MID<input id="mid" type="range" min="-12" max="12" value="0">
<b id="mval">0</b>
</div>
<div class="row">
TREBLE<input id="treble" type="range" min="-12" max="12" value="0">
<b id="tval">0</b>
</div>
<div class="row">
VOLUME<input id="volume" type="range" min="0" max="100" value="75">
<b id="vval">75</b>
</div>

<div class="hint">REAL AUDIO EQ • NEON SPECTRUM</div>

<audio id="au" preload="metadata"
src="data:__MIME__;base64,__DATA__"></audio>
</div>

<script>
const au=document.getElementById('au');
const cv=document.getElementById('cv');
const cx=cv.getContext('2d');

let ac,an,src,lo,mi,hi,gain;
let loop=false;

function init(){
 if(ac)return;

 ac=new(window.AudioContext||window.webkitAudioContext)();
 an=ac.createAnalyser();
 an.fftSize=256;

 src=ac.createMediaElementSource(au);

 lo=ac.createBiquadFilter();
 lo.type='lowshelf';
 lo.frequency.value=180;

 mi=ac.createBiquadFilter();
 mi.type='peaking';
 mi.frequency.value=1000;
 mi.Q.value=1;

 hi=ac.createBiquadFilter();
 hi.type='highshelf';
 hi.frequency.value=4000;

 gain=ac.createGain();

 src.connect(lo);
 lo.connect(mi);
 mi.connect(hi);
 hi.connect(gain);
 gain.connect(an);
 an.connect(ac.destination);
}

document.getElementById('play').onclick=async()=>{
 init();
 await ac.resume();

 if(au.paused){
  try{
   await au.play();
   document.getElementById('play').textContent='❚❚ PAUSE';
  }catch(e){
   alert('กรุณากด PLAY อีกครั้งเพื่ออนุญาตเล่นเสียง');
  }
 }else{
  au.pause();
  document.getElementById('play').textContent='▶ PLAY';
 }
};

document.getElementById('stop').onclick=()=>{
 au.pause();
 au.currentTime=0;
 document.getElementById('play').textContent='▶ PLAY';
};

document.getElementById('mute').onclick=e=>{
 au.muted=!au.muted;
 e.target.textContent=au.muted?'🔇 MUTED':'🔊 SOUND';
};

document.getElementById('loop').onclick=e=>{
 loop=!loop;
 au.loop=loop;
 e.target.textContent=loop?'🔁 LOOP ON':'🔁 LOOP OFF';
};

[
 ['bass',()=>lo,'bval'],
 ['mid',()=>mi,'mval'],
 ['treble',()=>hi,'tval']
].forEach(([id,get,out])=>{
 document.getElementById(id).oninput=e=>{
  init();
  get().gain.value=Number(e.target.value);
  document.getElementById(out).textContent=e.target.value;
 };
});

document.getElementById('volume').oninput=e=>{
 init();
 gain.gain.value=Number(e.target.value)/100;
 document.getElementById('vval').textContent=e.target.value;
};

au.onended=()=>{
 document.getElementById('play').textContent='▶ PLAY';
};

// กราฟเสียงจริง
function draw(){
 const w=cv.clientWidth;
 const h=cv.clientHeight;
 const d=window.devicePixelRatio||1;

 if(cv.width!==w*d||cv.height!==h*d){
  cv.width=w*d;
  cv.height=h*d;
 }

 cx.setTransform(d,0,0,d,0,0);
 cx.clearRect(0,0,w,h);

 cx.fillStyle='#020817';
 cx.fillRect(0,0,w,h);

 const arr=new Uint8Array(
  an?an.frequencyBinCount:64
 );

 if(an)an.getByteFrequencyData(arr);

 for(let i=0;i<42;i++){
  let v=an?arr[i]/255:0.025;
  let bh=Math.max(3,v*(h-8));
  let bw=w/42;

  let gr=cx.createLinearGradient(0,h-bh,0,h);
  gr.addColorStop(0,'#ff45d8');
  gr.addColorStop(.5,'#985cff');
  gr.addColorStop(1,'#00eaff');

  cx.fillStyle=gr;
  cx.shadowBlur=8;
  cx.shadowColor='#00dfff';
  cx.fillRect(i*bw+2,h-bh,bw-4,bh);
 }

 cx.shadowBlur=0;
 requestAnimationFrame(draw);
}

draw();
</script>
</body>
</html>"""

    player = player.replace("__TITLE__", html.escape(p.stem))
    player = player.replace("__MIME__", mime)
    player = player.replace("__DATA__", encoded)

    components.html(
        player,
        height=410,
        scrolling=False
    )

    st.caption(
        f"เพลงที่เลือก: {p.name} | พบทั้งหมด {len(tracks)} เพลง"
    )

    with st.expander("📚 PLAYLIST"):
        for i, t in enumerate(tracks, 1):
            st.write(f"{i:02d} • {t.stem}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center;color:#7897b8;'
    'font-size:12px">TA101 V4 • MUSIC • DREAM • TOGETHER</p>',
    unsafe_allow_html=True
    )
