from pathlib import Path
import base64
import json
import mimetypes
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TA101 • NEON HI-FI MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}
LOGO_NAMES = ("logo1.jpg", "logo1.jpeg", "logo1.png", "logo.jpg", "logo.jpeg", "โลโก้.jpg")

st.markdown("""
<style>
.stApp {
  background: radial-gradient(ellipse at 50% -10%, #14264b 0%, #070b19 48%, #02040a 100%);
  color: #eef7ff;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1500px; padding-top: .8rem; padding-bottom: 1rem; }
h1,h2,h3 { color:#eafaff; text-shadow:0 0 14px #00d9ff88; }
</style>
""", unsafe_allow_html=True)

def find_logo():
    for name in LOGO_NAMES:
        path = ROOT / name
        if path.is_file():
            return path
    return None

def find_songs():
    found = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in AUDIO_EXTENSIONS:
            continue
        try:
            rel = path.relative_to(ROOT)
            if any(part.startswith(".") or part in {"venv", ".venv", "__pycache__"} for part in rel.parts):
                continue
            found.append(path)
        except (OSError, ValueError):
            pass
    return sorted(found, key=lambda p: (p.name.casefold(), str(p).casefold()))

songs = find_songs()
logo_path = find_logo()

st.markdown("""
<div style="text-align:center;padding:5px 0 14px">
  <div style="font-size:clamp(30px,5vw,58px);font-weight:950;letter-spacing:3px;
  color:#f4fbff;text-shadow:0 0 12px #00d9ff,0 0 32px #9d4dff">
  🎧 TA101 • NEON HI-FI
  </div>
  <div style="color:#73eaff;letter-spacing:5px;font-size:11px">MUSIC • DREAM • TOGETHER</div>
</div>
""", unsafe_allow_html=True)

# Encode local audio so the custom player can process it through Web Audio EQ.
# Keep the total embedded audio size moderate for Streamlit Cloud.
MAX_TOTAL_MB = 80
tracks = []
total_bytes = 0
for path in songs:
    try:
        size = path.stat().st_size
        if total_bytes + size > MAX_TOTAL_MB * 1024 * 1024:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        tracks.append({
            "name": path.stem,
            "file": path.name,
            "mime": mime,
            "src": f"data:{mime};base64,{data}",
        })
        total_bytes += size
    except OSError:
        continue

logo_data = ""
if logo_path:
    try:
        logo_mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
        logo_data = "data:" + logo_mime + ";base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")
    except OSError:
        pass

if not songs:
    st.warning("ยังไม่พบไฟล์เพลง กรุณาวางไฟล์ MP3 / WAV / M4A ไว้ในโฟลเดอร์เดียวกับ app.py หรือโฟลเดอร์ย่อย")
elif not tracks:
    st.error("พบไฟล์เพลง แต่ขนาดรวมเกินขีดจำกัด 80 MB สำหรับเครื่องเล่น EQ รุ่นนี้ กรุณาลดขนาดหรือแบ่งเพลงเป็นชุด")
elif len(tracks) < len(songs):
    st.info(f"พบเพลง {len(songs)} เพลง แต่ฝังในเครื่องเล่นได้ {len(tracks)} เพลงแรก เนื่องจากจำกัดข้อมูลรวมไว้ที่ 80 MB")

PLAYER_HTML = r"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--cyan:#35eaff;--purple:#a855f7;--blue:#397bff;--panel:#0a1224}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:#030611;color:#eef7ff;font-family:Arial,'Noto Sans Thai',sans-serif}
body{padding:12px;background:radial-gradient(ellipse at 50% 0%,#14264b 0%,#070b19 52%,#02040a 100%)}
.shell{max-width:1200px;margin:auto;border:1px solid #35eaff55;border-radius:24px;padding:clamp(12px,2.5vw,25px);background:linear-gradient(145deg,#0d1930ed,#050916f5);box-shadow:0 0 28px #00cfff22,inset 0 0 25px #7c3aed12;position:relative;overflow:hidden}
.shell:before{content:"";position:absolute;inset:-2px;background:linear-gradient(110deg,transparent,#35eaff16,transparent,#a855f716,transparent);pointer-events:none}
.topline{display:flex;justify-content:space-between;align-items:center;gap:10px;position:relative}
.kicker{font-size:10px;letter-spacing:3px;color:#78edff}.status{font-size:10px;color:#9caecb;border:1px solid #385071;padding:7px 10px;border-radius:30px}
.hero{display:grid;grid-template-columns:minmax(150px,260px) 1fr;gap:clamp(16px,4vw,42px);align-items:center;padding:24px 3%}
.art{aspect-ratio:1;border-radius:22px;border:1px solid #48ddff88;background:radial-gradient(circle,#203c68,#080e1e 70%);box-shadow:0 0 24px #12dfff33,0 0 45px #8b5cf633;display:grid;place-items:center;overflow:hidden;position:relative}
.art:after{content:"";position:absolute;inset:10%;border:1px solid #63eaff55;border-radius:50%;box-shadow:0 0 24px #35eaff44;animation:spin 18s linear infinite}
.art img{width:76%;height:76%;object-fit:contain;filter:drop-shadow(0 0 16px #35eaff);z-index:1;animation:breathe 3s ease-in-out infinite}
.disc{font-size:clamp(65px,10vw,115px);text-shadow:0 0 20px #35eaff,0 0 40px #a855f7;animation:spin 16s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes breathe{50%{transform:scale(1.05);filter:drop-shadow(0 0 28px #a855f7)}}
.tracklabel{font-size:10px;letter-spacing:3px;color:#63eaff}.trackname{font-size:clamp(23px,4vw,42px);font-weight:900;line-height:1.15;margin:9px 0;text-shadow:0 0 16px #27dfff66;overflow-wrap:anywhere}
.filename{font-size:12px;color:#9eb1d0}.time{display:flex;justify-content:space-between;color:#8da5c7;font-size:11px;margin-top:7px}
input[type=range]{width:100%;accent-color:#39e7ff;cursor:pointer}
.progress{height:6px}
.controls{display:flex;align-items:center;justify-content:center;gap:clamp(8px,2vw,20px);margin:18px 0;flex-wrap:wrap}
button{border:1px solid #35eaff66;background:linear-gradient(145deg,#142744,#091226);color:#dffaff;border-radius:15px;padding:12px 16px;font-size:17px;cursor:pointer;box-shadow:0 0 13px #00d9ff18;transition:.2s}
button:hover{border-color:#35eaff;box-shadow:0 0 20px #00d9ff66;transform:translateY(-2px)}
button.main{width:62px;height:62px;border-radius:50%;font-size:25px;background:linear-gradient(145deg,#167caa,#5731a3);box-shadow:0 0 25px #21dfff66}
button.active{color:#43efff;border-color:#43efff;box-shadow:0 0 14px #43efff55}
.section{margin-top:15px;border:1px solid #294365;border-radius:17px;padding:16px;background:#050c1bd9;position:relative}
.sectionhead{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px}
.sectionhead b{font-size:13px;letter-spacing:2px;color:#a7f4ff}.sectionhead span{font-size:10px;color:#8099bc}
.eq{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:10px}
.band{text-align:center;min-width:0}.band input{height:105px;writing-mode:vertical-lr;direction:rtl;width:22px;max-width:100%;accent-color:#4beaff}
.band small{display:block;color:#91a8ca;font-size:10px;margin-top:7px}.band output{display:block;color:#55eaff;font-size:10px;margin-top:4px}
.tone{display:grid;grid-template-columns:1fr 1fr;gap:22px}.tone label{font-size:11px;color:#a9c0df;display:flex;justify-content:space-between}
.visual{height:100px;width:100%;display:block;border-radius:12px;background:#030917;border:1px solid #18304e}
.playlist{display:grid;grid-template-columns:1fr 1fr;gap:8px;max-height:220px;overflow:auto}
.song{display:flex;align-items:center;gap:9px;text-align:left;width:100%;padding:11px;font-size:12px;border-radius:11px;min-width:0}
.song span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.song.current{border-color:#36eaff;background:#102b43;color:#75f3ff}
.footer{text-align:center;color:#607b9e;font-size:10px;letter-spacing:2px;padding:16px 0 2px}
@media(max-width:650px){.hero{grid-template-columns:110px 1fr;padding:18px 0;gap:14px}.art{border-radius:15px}.art img{width:82%;height:82%}.eq{grid-template-columns:repeat(5,1fr);row-gap:15px}.band input{height:75px}.playlist{grid-template-columns:1fr}.status{font-size:9px}.section{padding:12px}}
</style>
</head>
<body>
<div class="shell">
 <div class="topline"><div><div class="kicker">TA101 AUDIO LAB • HI-FI SYSTEM</div><div style="font-size:19px;font-weight:900;letter-spacing:2px;margin-top:4px">NEON MUSIC PLAYER</div></div><div class="status" id="status">● READY TO PLAY</div></div>
 <div class="hero">
  <div class="art" id="art"><div class="disc" id="disc">♫</div><img id="logo" alt="TA101 logo" style="display:none"></div>
  <div><div class="tracklabel">NOW PLAYING</div><div class="trackname" id="trackname">เลือกเพลงจากรายการ</div><div class="filename" id="filename">MUSIC • DREAM • TOGETHER</div>
   <div style="margin-top:19px"><input class="progress" id="seek" type="range" min="0" max="1000" value="0"><div class="time"><span id="elapsed">00:00</span><span id="duration">00:00</span></div></div>
  </div>
 </div>
 <div class="controls">
  <button id="shuffle" title="สุ่มเพลง">🔀</button><button id="prev" title="เพลงก่อนหน้า">⏮</button><button class="main" id="play" title="เล่น">▶</button><button id="next" title="เพลงถัดไป">⏭</button><button id="repeat" title="วนเพลง">🔁</button>
 </div>
 <div class="section"><div class="sectionhead"><b>◈ LIVE AUDIO SPECTRUM</b><span>REAL-TIME SOUND RESPONSE</span></div><canvas class="visual" id="visual"></canvas></div>
 <div class="section"><div class="sectionhead"><b>◈ 10-BAND EQUALIZER</b><span>ปรับเสียงได้จริง • REAL EQ</span><button id="eqreset" style="padding:6px 10px;font-size:10px">RESET</button></div><div class="eq" id="eq"></div></div>
 <div class="section"><div class="sectionhead"><b>◈ TONE CONTROL</b><span>BASS / TREBLE</span></div><div class="tone">
  <div><label><span>BASS</span><output id="bassval">0 dB</output></label><input id="bass" type="range" min="-12" max="12" value="0"></div>
  <div><label><span>TREBLE</span><output id="trebleval">0 dB</output></label><input id="treble" type="range" min="-12" max="12" value="0"></div>
 </div></div>
 <div class="section"><div class="sectionhead"><b>◈ PLAYLIST</b><span id="count">0 TRACKS</span></div><div class="playlist" id="playlist"></div></div>
 <div class="footer">TA101 • MUSIC • DREAM • TOGETHER</div>
</div>
<audio id="audio" preload="metadata" crossorigin="anonymous"></audio>
<script>
const TRACKS=__TRACKS__;
const LOGO=__LOGO__;
const audio=document.getElementById('audio');
const $=id=>document.getElementById(id);
if(LOGO){$('logo').src=LOGO;$('logo').style.display='block';$('disc').style.display='none';}
let current=0,shuffle=false,repeat=false,playing=false,ctx=null,source=null,analyser=null,filters=[],bassFilter=null,trebleFilter=null;
const bands=[60,120,250,500,1000,2000,4000,8000,12000,16000];
const labels=['60','120','250','500','1K','2K','4K','8K','12K','16K'];
function fmt(s){if(!isFinite(s))return '00:00';return String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0');}
function setupAudio(){
 if(ctx)return;
 const AC=window.AudioContext||window.webkitAudioContext;
 if(!AC){$('status').textContent='AUDIO API NOT SUPPORTED';return;}
 ctx=new AC();source=ctx.createMediaElementSource(audio);analyser=ctx.createAnalyser();analyser.fftSize=256;
 let node=source;
 bands.forEach((freq,i)=>{const f=ctx.createBiquadFilter();f.type='peaking';f.frequency.value=freq;f.Q.value=1;f.gain.value=0;filters.push(f);node.connect(f);node=f;});
 bassFilter=ctx.createBiquadFilter();bassFilter.type='lowshelf';bassFilter.frequency.value=120;node.connect(bassFilter);
 trebleFilter=ctx.createBiquadFilter();trebleFilter.type='highshelf';trebleFilter.frequency.value=5000;bassFilter.connect(trebleFilter);
 trebleFilter.connect(analyser);analyser.connect(ctx.destination);
}
function loadTrack(i,autoplay=false){
 if(!TRACKS.length)return;
 current=(i+TRACKS.length)%TRACKS.length;audio.src=TRACKS[current].src;audio.load();
 $('trackname').textContent=TRACKS[current].name;$('filename').textContent=TRACKS[current].file;
 document.querySelectorAll('.song').forEach((el,n)=>el.classList.toggle('current',n===current));
 $('play').textContent='▶';playing=false;
 if(autoplay)playTrack();
}
async function playTrack(){
 if(!TRACKS.length)return;
 setupAudio();if(ctx&&ctx.state==='suspended')await ctx.resume();
 try{await audio.play();playing=true;$('play').textContent='❚❚';$('status').textContent='● PLAYING';}
 catch(e){$('status').textContent='TAP PLAY TO START';}
}
function pauseTrack(){audio.pause();playing=false;$('play').textContent='▶';$('status').textContent='Ⅱ PAUSED';}
function nextTrack(){let n;if(shuffle&&TRACKS.length>1){do{n=Math.floor(Math.random()*TRACKS.length)}while(n===current)}else n=current+1;loadTrack(n,true);}
function renderPlaylist(){
 $('count').textContent=TRACKS.length+' TRACKS';
 const list=$('playlist');list.innerHTML='';
 TRACKS.forEach((t,i)=>{const b=document.createElement('button');b.className='song';b.innerHTML='<span>♫</span><span></span>';b.lastElementChild.textContent=t.name;b.onclick=()=>loadTrack(i,true);list.appendChild(b);});
 if(TRACKS.length)loadTrack(0,false);
 else $('trackname').textContent='ไม่พบไฟล์เพลง';
}
$('play').onclick=()=>playing?pauseTrack():playTrack();
$('prev').onclick=()=>loadTrack(current-1,true);
$('next').onclick=nextTrack;
$('shuffle').onclick=()=>{shuffle=!shuffle;$('shuffle').classList.toggle('active',shuffle);};
$('repeat').onclick=()=>{repeat=!repeat;$('repeat').classList.toggle('active',repeat);};
audio.addEventListener('ended',()=>{if(repeat){audio.currentTime=0;playTrack();}else if(current<TRACKS.length-1||shuffle)nextTrack();else{pauseTrack();audio.currentTime=0;}});
audio.addEventListener('timeupdate',()=>{if(audio.duration){$('seek').value=audio.currentTime/audio.duration*1000;$('elapsed').textContent=fmt(audio.currentTime);$('duration').textContent=fmt(audio.duration);}});
$('seek').addEventListener('input',()=>{if(audio.duration)audio.currentTime=Number($('seek').value)/1000*audio.duration;});
const eq=$('eq');
bands.forEach((freq,i)=>{const d=document.createElement('div');d.className='band';d.innerHTML='<input type="range" min="-12" max="12" value="0" step="1"><output>0 dB</output><small>'+labels[i]+'</small>';const input=d.querySelector('input');input.addEventListener('input',()=>{if(filters[i])filters[i].gain.value=Number(input.value);d.querySelector('output').textContent=input.value+' dB';});eq.appendChild(d);});
function tone(id,filter,out){$(id).addEventListener('input',()=>{const v=Number($(id).value);if(filter)filter.gain.value=v;$(out).textContent=v+' dB';});}
tone('bass',bassFilter,'bassval');tone('treble',trebleFilter,'trebleval');
$('eqreset').onclick=()=>{eq.querySelectorAll('input').forEach((input,i)=>{input.value=0;if(filters[i])filters[i].gain.value=0;input.parentElement.querySelector('output').textContent='0 dB';});$('bass').value=0;$('treble').value=0;if(bassFilter)bassFilter.gain.value=0;if(trebleFilter)trebleFilter.gain.value=0;$('bassval').textContent='0 dB';$('trebleval').textContent='0 dB';};
const canvas=$('visual'),g=canvas.getContext('2d');
function draw(){
 const dpr=window.devicePixelRatio||1,w=canvas.clientWidth,h=canvas.clientHeight;
 if(canvas.width!==Math.floor(w*dpr)||canvas.height!==Math.floor(h*dpr)){canvas.width=Math.floor(w*dpr);canvas.height=Math.floor(h*dpr);}
 g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,w,h);
 const grad=g.createLinearGradient(0,0,w,0);grad.addColorStop(0,'#20dfff');grad.addColorStop(.5,'#a855f7');grad.addColorStop(1,'#ff4fd8');
 const data=new Uint8Array(analyser?analyser.frequencyBinCount:64);if(analyser)analyser.getByteFrequencyData(data);
 const n=48,bw=w/n;
 for(let i=0;i<n;i++){const v=analyser?data[Math.floor(i*data.length/n)]/255:(.08+.06*Math.sin(Date.now()/350+i));const bh=Math.max(3,v*h*.88);g.fillStyle=grad;g.shadowBlur=12;g.shadowColor='#21dfff';g.fillRect(i*(bw+1),h-bh,bw*.72,bh);}
 g.shadowBlur=0;requestAnimationFrame(draw);
}
renderPlaylist();draw();
</script>
</body></html>"""

if tracks:
    tracks_json = json.dumps(tracks, ensure_ascii=False).replace("</", "<\\/")
    logo_json = json.dumps(logo_data)
    page = PLAYER_HTML.replace("__TRACKS__", tracks_json).replace("__LOGO__", logo_json)
    components.html(page, height=1120, scrolling=True)
else:
    st.info("เมื่อเพิ่มไฟล์เพลงในโฟลเดอร์แอปแล้ว เครื่องเล่นจะปรากฏที่นี่")
    st.markdown("### โครงสร้างไฟล์ที่แนะนำ")
    st.code("app.py\nlogo1.jpg\nเพลงของคุณ.mp3", language="text")

st.caption(f"พบไฟล์เพลงทั้งหมด {len(songs)} เพลง • ฝังในเครื่องเล่น {len(tracks)} เพลง • โลโก้: {logo_path.name if logo_path else 'ไม่พบ'}")
st.caption("หมายเหตุ: EQ ทำงานเมื่อเล่นเสียงผ่านเครื่องเล่นนี้ และเบราว์เซอร์อาจต้องให้แตะปุ่ม Play ก่อนเริ่มเสียง")
