import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
import mimetypes

st.set_page_config(
    page_title="TA101 • NEON 3D MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).resolve().parent
EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}

st.markdown("""
<style>
.stApp {
  background: radial-gradient(ellipse at top, #172554, #08091b 55%, #02030a);
  color: white;
}
header[data-testid="stHeader"] {background: transparent;}
.block-container {max-width: 1450px; padding-top: 1rem;}
div.stButton>button {
  background: linear-gradient(120deg,#082f49,#4c1d95);
  color: white; border: 1px solid #22d3ee; border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

def find_logo():
    for name in ("logo1.jpg", "logo1.jpeg", "logo1.png",
                 "logo.jpg", "โลโก้.jpg"):
        p = ROOT / name
        if p.is_file():
            return p
    return None

def find_songs():
    return sorted(
        [p for p in ROOT.rglob("*")
         if p.is_file()
         and p.suffix.lower() in EXTENSIONS
         and not any(part.startswith(".") for part in p.parts)],
        key=lambda p: p.name.lower()
    )

songs = find_songs()
logo = find_logo()

st.markdown("""
<div style="text-align:center;font-size:clamp(30px,5vw,58px);
font-weight:900;letter-spacing:4px;
text-shadow:0 0 12px #22d3ee,0 0 32px #a855f7">
🎧 TA101 • NEON 3D MUSIC
</div>
<div style="text-align:center;color:#67e8f9;letter-spacing:4px">
MUSIC • DREAM • TOGETHER
</div>
""", unsafe_allow_html=True)

if not songs:
    st.error("ไม่พบเพลง กรุณาวางไฟล์ MP3 ไว้ในโฟลเดอร์เดียวกับ app.py")
    st.stop()

# แปลงเพลงเป็นข้อมูลให้เครื่องเล่นในฉาก 3 มิติอ่านได้
tracks = []
for p in songs:
    try:
        mime = mimetypes.guess_type(str(p))[0] or "audio/mpeg"
        data = base64.b64encode(p.read_bytes()).decode("ascii")
        tracks.append({
            "name": p.stem,
            "src": f"data:{mime};base64,{data}"
        })
    except OSError:
        pass

if not tracks:
    st.error("อ่านไฟล์เพลงไม่สำเร็จ")
    st.stop()

logo_data = ""
if logo:
    mime = "image/png" if logo.suffix.lower() == ".png" else "image/jpeg"
    logo_data = "data:" + mime + ";base64," + base64.b64encode(
        logo.read_bytes()
    ).decode("ascii")

TRACKS_JSON = json.dumps(tracks, ensure_ascii=False).replace("</", "<\\/")
LOGO_JSON = json.dumps(logo_data)

# HTML ฉาก 3 มิติเริ่มต้นตรงนี้
page = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;
background:#02030a;color:white;font-family:Arial,sans-serif}
#space{position:absolute;inset:0;width:100%;height:100%}
#hud{position:absolute;inset:0;padding:12px;pointer-events:none;
display:flex;flex-direction:column;justify-content:space-between}
.top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.panel{background:#050b20cc;border:1px solid #22d3ee99;
border-radius:13px;padding:10px 13px;backdrop-filter:blur(7px);
box-shadow:0 0 16px #0891b244;max-width:48%}
.label{font-size:10px;letter-spacing:2px;color:#67e8f9}
#trackname{font-size:clamp(14px,2vw,23px);font-weight:bold;
text-shadow:0 0 12px #22d3ee;overflow-wrap:anywhere}
#spectrum{width:min(30vw,310px);height:75px;display:block}
#logo{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);
width:min(30vw,270px);height:min(30vw,270px);object-fit:contain;
filter:drop-shadow(0 0 18px #22d3ee) drop-shadow(0 0 35px #a855f7)}
#brand{position:absolute;top:65%;left:50%;transform:translate(-50%,-50%);
font-size:clamp(30px,5vw,58px);font-weight:1000;letter-spacing:5px;
white-space:nowrap;text-shadow:0 0 10px #22d3ee,0 0 28px #a855f7}
#sub{position:absolute;top:73%;left:50%;transform:translate(-50%,-50%);
font-size:10px;letter-spacing:4px;color:#a5f3fc;white-space:nowrap}
.controls{display:flex;justify-content:center;align-items:center;
gap:8px;flex-wrap:wrap;pointer-events:auto}
button,select{color:white;background:linear-gradient(120deg,#082f49ee,#4c1d95ee);
border:1px solid #22d3ee;border-radius:10px;padding:10px 12px;
font-weight:bold;cursor:pointer;max-width:100%}
button:hover{box-shadow:0 0 17px #d946ef}
#play{font-size:20px;border-radius:50%;width:52px;height:52px}
select{background:#080d25;max-width:210px}
.control{background:#080d25dd;border:1px solid #8b5cf6;border-radius:10px;
padding:8px;display:flex;align-items:center;gap:6px;font-size:11px}
input{width:85px;accent-color:#22d3ee}
#status{font-size:10px;color:#c4b5fd;margin-top:5px}
@media(max-width:600px){
 #hud{padding:7px}.panel{padding:7px;max-width:49%}
 #spectrum{width:29vw;height:58px}
 #logo{width:44vw;height:44vw;top:42%}
 #brand{top:65%;letter-spacing:2px}
 #sub{top:72%;letter-spacing:2px}
 .controls{gap:5px}button{padding:8px}
 select{max-width:130px}.control{padding:5px}
 input{width:58px}
}
</style>
</head>
<body>
<canvas id="space"></canvas>
<div id="hud">
  <div class="top">
    <div class="panel">
      <div class="label">NOW PLAYING</div>
      <div id="trackname">TA101</div>
      <div id="status">3D SPACE READY</div>
    </div>
    <div class="panel">
      <div class="label">LIVE AUDIO SPECTRUM</div>
      <canvas id="spectrum"></canvas>
    </div>
  </div>
  <img id="logo" alt="TA101 logo" style="display:none">
  <div id="brand">TA101</div>
  <div id="sub">NEON MUSIC • 3D SPACE</div>
  <div class="controls">
    <select id="playlist" aria-label="เลือกเพลง"></select>
    <button id="prev">⏮</button>
    <button id="play">▶</button>
    <button id="next">⏭</button>
    <button id="shuffle">🔀 OFF</button>
    <button id="repeat">🔁 OFF</button>
    <div class="control">VOL
      <input id="volume" type="range" min="0" max="100" value="80">
      <span id="voltext">80%</span>
    </div>
    <button id="full">⛶ เต็มจอ</button>
  </div>
</div>
<audio id="audio" preload="metadata"></audio>
<script>
const TRACKS = __TRACKS__;
const LOGO_DATA = __LOGO__;
const audio = document.getElementById('audio');
const playlist = document.getElementById('playlist');
const playButton = document.getElementById('play');
const trackName = document.getElementById('trackname');
const statusText = document.getElementById('status');
if (LOGO_DATA) {
  const logo = document.getElementById('logo');
  logo.src = LOGO_DATA;
  logo.style.display = 'block';
}
TRACKS.forEach((t,i)=>{
  const option = document.createElement('option');
  option.value = i;
  option.textContent = String(i+1).padStart(2,'0')+' • '+t.name;
  playlist.appendChild(option);
});
let current = 0, shuffle = false, repeat = false;
let audioContext = null, analyser = null, sourceNode = null, bins = null;

function loadTrack(i, playNow=false) {
  current = (i + TRACKS.length) % TRACKS.length;
  audio.src = TRACKS[current].src;
  playlist.value = String(current);
  trackName.textContent = TRACKS[current].name;
  statusText.textContent = 'TRACK '+(current+1)+' / '+TRACKS.length;
  if (playNow) playAudio();
}
async function setupAudio() {
  if (!audioContext) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    audioContext = new AC();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    analyser.smoothingTimeConstant = 0.78;
    sourceNode = audioContext.createMediaElementSource(audio);
    sourceNode.connect(analyser);
    analyser.connect(audioContext.destination);
    bins = new Uint8Array(analyser.frequencyBinCount);
  }
  if (audioContext.state === 'suspended') await audioContext.resume();
}
async function playAudio() {
  try {
    await setupAudio();
    await audio.play();
    playButton.textContent = '❚❚';
    statusText.textContent = 'PLAYING • LIVE AUDIO';
  } catch (err) {
    statusText.textContent = 'แตะปุ่ม ▶ เพื่อเริ่มเพลง';
  }
}
playButton.onclick = () => {
  if (audio.paused) playAudio();
  else {
    audio.pause();
    playButton.textContent = '▶';
    statusText.textContent = 'PAUSED';
  }
};
document.getElementById('prev').onclick = () => loadTrack(current-1,true);
document.getElementById('next').onclick = () => {
  loadTrack(shuffle ? Math.floor(Math.random()*TRACKS.length) : current+1,true);
};
playlist.onchange = () => loadTrack(Number(playlist.value),true);
document.getElementById('shuffle').onclick = e => {
  shuffle = !shuffle; e.currentTarget.textContent = shuffle ? '🔀 ON' : '🔀 OFF';
};
document.getElementById('repeat').onclick = e => {
  repeat = !repeat; e.currentTarget.textContent = repeat ? '🔁 ON' : '🔁 OFF';
};
audio.onended = () => {
  if (repeat) { audio.currentTime=0; playAudio(); }
  else loadTrack(shuffle ? Math.floor(Math.random()*TRACKS.length) : current+1,true);
};
document.getElementById('volume').oninput = e => {
  audio.volume = Number(e.target.value)/100;
  document.getElementById('voltext').textContent = e.target.value+'%';
};
document.getElementById('full').onclick = () => {
  if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
  else document.exitFullscreen?.();
};
audio.volume = 0.8;
loadTrack(0,false);

// กราฟเสียงอ่านค่าความถี่จริงจากเพลง เมื่อเล่นเพลงอยู่
const spectrum = document.getElementById('spectrum');
const sctx = spectrum.getContext('2d');
function drawSpectrum() {
  const dpr = window.devicePixelRatio || 1;
  const w = spectrum.clientWidth || 250, h = spectrum.clientHeight || 70;
  if (spectrum.width !== Math.floor(w*dpr) || spectrum.height !== Math.floor(h*dpr)) {
    spectrum.width = Math.floor(w*dpr);
    spectrum.height = Math.floor(h*dpr);
  }
  sctx.setTransform(dpr,0,0,dpr,0,0);
  sctx.clearRect(0,0,w,h);
  if (analyser && bins) analyser.getByteFrequencyData(bins);
  const n=42, bw=w/n;
  for(let i=0;i<n;i++){
    const v=(analyser && bins) ? bins[Math.floor(i*bins.length/n)]/255
      : 0.12+0.12*Math.abs(Math.sin(Date.now()/500+i*.6));
    const bh=Math.max(3,v*(h-5));
    const grad=sctx.createLinearGradient(0,h-bh,0,h);
    grad.addColorStop(0,'#f0abfc');
    grad.addColorStop(.5,'#8b5cf6');
    grad.addColorStop(1,'#22d3ee');
    sctx.fillStyle=grad;
    sctx.shadowBlur=8;
    sctx.shadowColor='#22d3ee';
    sctx.fillRect(i*bw,h-bh,Math.max(2,bw-2),bh);
  }
  sctx.shadowBlur=0;
  requestAnimationFrame(drawSpectrum);
}
drawSpectrum();
</script>


<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
  const canvas = document.getElementById('space');
  const status = document.getElementById('status');

  if (!window.THREE) {
    status.textContent = '3D library unavailable; music controls remain available';
    return;
  }

  try {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x02030a);
    scene.fog = new THREE.FogExp2(0x02030a, 0.014);

    const camera = new THREE.PerspectiveCamera(
      65, window.innerWidth/window.innerHeight, 0.1, 500
    );
    camera.position.set(0, 0, 20);

    const renderer = new THREE.WebGLRenderer({
      canvas: canvas, antialias: true, alpha: false
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);

    scene.add(new THREE.AmbientLight(0x8899ff, 1.7));

    const cyanLight = new THREE.PointLight(0x00d9ff, 90, 70);
    cyanLight.position.set(-7, 5, 7);
    scene.add(cyanLight);

    const purpleLight = new THREE.PointLight(0xc026ff, 100, 70);
    purpleLight.position.set(7, -4, 5);
    scene.add(purpleLight);

    // แกนพลังงานกลางฉาก
    const coreMaterial = new THREE.MeshStandardMaterial({
      color: 0x112255,
      emissive: 0x0878ff,
      emissiveIntensity: 2,
      metalness: 0.8,
      roughness: 0.2,
      wireframe: true
    });
    const core = new THREE.Mesh(
      new THREE.IcosahedronGeometry(2.3, 2),
      coreMaterial
    );
    scene.add(core);

    // วงแหวนพลังงานหมุนหลายชั้น
    const rings = new THREE.Group();
    scene.add(rings);

    const ringColors = [
      0x00eaff, 0x7c3aed, 0xf0abfc, 0x2563eb, 0x22d3ee
    ];

    for (let i=0; i<5; i++) {
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(3.1+i*0.3, 0.025, 8, 160),
        new THREE.MeshBasicMaterial({
          color: ringColors[i],
          transparent: true,
          opacity: 0.88
        })
      );
      ring.rotation.x = 0.35 + i*0.23;
      ring.rotation.y = i*0.42;
      rings.add(ring);
    }

    // ดาวจำนวนมากในอวกาศ
    const starCount = 2200;
    const starPositions = new Float32Array(starCount*3);

    for (let i=0; i<starCount; i++) {
      starPositions[i*3] = (Math.random()-0.5)*110;
      starPositions[i*3+1] = (Math.random()-0.5)*75;
      starPositions[i*3+2] = (Math.random()-0.5)*110;
    }

    const starGeometry = new THREE.BufferGeometry();
    starGeometry.setAttribute(
      'position', new THREE.BufferAttribute(starPositions,3)
    );

    const stars = new THREE.Points(
      starGeometry,
      new THREE.PointsMaterial({
        color: 0x9beeff,
        size: 0.11,
        transparent: true,
        opacity: 0.9
      })
    );
    scene.add(stars);

    // อนุภาคแสงที่โคจรรอบแกน
    const particleCount = 350;
    const particlePositions = new Float32Array(particleCount*3);

    for (let i=0; i<particleCount; i++) {
      const a = Math.random()*Math.PI*2;
      const r = 4+Math.random()*9;
      particlePositions[i*3] = Math.cos(a)*r;
      particlePositions[i*3+1] = (Math.random()-0.5)*12;
      particlePositions[i*3+2] = Math.sin(a)*r;
    }

    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute(
      'position', new THREE.BufferAttribute(particlePositions,3)
    );

    const particles = new THREE.Points(
      particleGeometry,
      new THREE.PointsMaterial({
        color: 0xd946ef,
        size: 0.09,
        transparent: true,
        opacity: 0.9
      })
    );
    scene.add(particles);

    // ดาวเคราะห์พร้อมวงแหวน
    const planet = new THREE.Mesh(
      new THREE.SphereGeometry(1.25,32,32),
      new THREE.MeshStandardMaterial({
        color: 0x182a70,
        emissive: 0x111c70,
        emissiveIntensity: 0.8,
        metalness: 0.4,
        roughness: 0.35
      })
    );
    planet.position.set(8,5,-9);
    scene.add(planet);

    const planetRing = new THREE.Mesh(
      new THREE.TorusGeometry(1.9,0.045,8,100),
      new THREE.MeshBasicMaterial({color:0x22d3ee})
    );
    planetRing.position.copy(planet.position);
    planetRing.rotation.x = 1.15;
    scene.add(planetRing);

    // วงแสงพื้นหลัง
    const halo = new THREE.Mesh(
      new THREE.TorusGeometry(8,0.035,8,180),
      new THREE.MeshBasicMaterial({
        color:0x4f46e5,
        transparent:true,
        opacity:0.65
      })
    );
    halo.position.z = -5;
    scene.add(halo);

    function resize() {
      camera.aspect = window.innerWidth/window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth,window.innerHeight);
    }
    window.addEventListener('resize',resize);

    const start = performance.now();

    function animate() {
      requestAnimationFrame(animate);
      const t = (performance.now()-start)/1000;

      let level = 0;
      if (analyser && bins) {
        analyser.getByteFrequencyData(bins);
        for (let i=0; i<bins.length; i++) level += bins[i];
        level = level/bins.length/255;
      }

      core.rotation.x = t*0.25;
      core.rotation.y = t*0.42;
      core.scale.setScalar(
        1 + level*0.8 + Math.sin(t*2)*0.035
      );
      coreMaterial.emissiveIntensity = 1.3 + level*4;

      rings.rotation.z = t*0.14;
      rings.rotation.y = t*0.08;
      stars.rotation.y = t*0.009;
      particles.rotation.y = -t*0.12;
      particles.rotation.x = t*0.04;
      planet.rotation.y = t*0.15;
      halo.rotation.z = -t*0.06;

      cyanLight.intensity = 55 + level*150;
      purpleLight.intensity = 60 + level*160;

      camera.position.x = Math.sin(t*0.13)*0.65;
      camera.position.y = Math.cos(t*0.16)*0.3;
      camera.lookAt(0,0,0);

      renderer.render(scene,camera);
    }

    animate();

  } catch (error) {
    status.textContent = '3D error: ' + error.message;
  }
})();
</script>
</body>
</html>
"""


page = page.replace("__TRACKS__", TRACKS_JSON)
page = page.replace("__LOGO__", LOGO_JSON)

components.html(page, height=760, scrolling=False)

st.caption(
    "TA101 • NEON 3D MUSIC | "
    "เก็บ logo1.jpg และไฟล์เพลงเดิมไว้ในโฟลเดอร์เดียวกับ app.py"
)
