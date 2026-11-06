   </div>
   <div class="mixer-title">✦ NEON MIX CONSOLE ✦</div>
   <div class="mixer">
    <div class="mix-channel"><div class="mix-head"><span>VOLUME</span><b id="vol-value">80%</b></div><input id="volume" type="range" min="0" max="100" value="80" aria-label="ปรับความดัง"></div>
    <div class="mix-channel"><div class="mix-head"><span>BASS</span><b id="bass-value">+4 dB</b></div><input id="bass" type="range" min="-12" max="12" value="4" aria-label="ปรับเสียงเบส"></div>
    <div class="mix-channel"><div class="mix-head"><span>TREBLE</span><b id="treble-value">+2 dB</b></div><input id="treble" type="range" min="-12" max="12" value="2" aria-label="ปรับเสียงแหลม"></div>
   </div>
   <div class="options">
    <button class="pill active" id="loop">↻ วนซ้ำรายการ</button>
    <button class="pill" id="shuffle">⤨ สุ่มเพลง</button>
    <button class="pill" id="single">♪ เล่นเพลงเดียว</button>
    <button class="pill" id="fullscreen">⛶ เต็มจอ</button>
   </div>
  </div>
  <div class="foot">SPACE • LIGHT • SOUND • 1.618 ENERGY</div>
 </div>
 <div id="start">
  <h2>ENTER THE COSMOS</h2>
  <p>ฉากอวกาศสามมิติ • อนุภาคโลโก้ • ไฟนีออน • คลื่นเสียงตามเพลงจริง<br>แตะเพื่อเริ่มเพลงและเปิดใช้งานระบบวิเคราะห์เสียง</p>
  <button id="enter">✦ เริ่มประสบการณ์ TA101</button>
 </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const SONGS = __SONGS__;
const LOGO = __LOGO__;
const $ = id => document.getElementById(id);
const audio = new Audio();
audio.preload = "auto";
audio.crossOrigin = "anonymous";
let index=0, playing=false, shuffle=false, loopList=true, single=false;
let ctx=null, analyser=null, source=null, freq=null, waveData=null, bassFilter=null, trebleFilter=null, masterGain=null;
let scene,camera,renderer,stars,core,coreMat,clock;
const stage=$("stage");

function setTheme(a,b){
 document.documentElement.style.setProperty("--a",a);
 document.documentElement.style.setProperty("--b",b);
 if(stars && stars.material) stars.material.color.set(a);
 if(coreMat) coreMat.color.set(b);
}
$("t1").onclick=()=>setTheme("#00f5ff","#bd00ff");
$("t2").onclick=()=>setTheme("#00ff82","#0055ff");
$("t3").onclick=()=>setTheme("#ff7a00","#ff006e");
$("t4").onclick=()=>setTheme("#e8f5ff","#7777ff");

if(LOGO){
 $("logo").src=LOGO;
 $("thumb").src=LOGO;
 $("thumb").style.display="block";
 $("logo-placeholder").style.display="none";
}

function timeText(s){
 if(!Number.isFinite(s))return "0:00";
 s=Math.max(0,Math.floor(s));
 return Math.floor(s/60)+":"+String(s%60).padStart(2,"0");
}
function initAudio(){
 if(ctx)return;
 const AC=window.AudioContext||window.webkitAudioContext;
 if(!AC)return;

 ctx=new AC();
 analyser=ctx.createAnalyser();
 analyser.fftSize=512;
 analyser.smoothingTimeConstant=.82;

 source=ctx.createMediaElementSource(audio);

 bassFilter=ctx.createBiquadFilter();
 bassFilter.type="lowshelf";
 bassFilter.frequency.value=180;
 bassFilter.gain.value=4;

 trebleFilter=ctx.createBiquadFilter();
 trebleFilter.type="highshelf";
 trebleFilter.frequency.value=3200;
 trebleFilter.gain.value=2;

 masterGain=ctx.createGain();
 masterGain.gain.value=.8;

 source.connect(bassFilter);
 bassFilter.connect(trebleFilter);
 trebleFilter.connect(masterGain);
 masterGain.connect(analyser);
 analyser.connect(ctx.destination);

 freq=new Uint8Array(analyser.frequencyBinCount);
 waveData=new Uint8Array(analyser.fftSize);
}

function fillPlaylist(){
 const sel=$("playlist");
 sel.innerHTML="";
 if(!SONGS.length){
  sel.innerHTML='<option value="">ไม่พบไฟล์เพลง</option>';
  $("track-title").textContent="ไม่พบไฟล์เพลงในโปรเจกต์";
  $("track-sub").textContent="เพิ่มไฟล์ MP3 ไว้ข้าง app.py";
  return;
 }
 SONGS.forEach((s,i)=>{
  const op=document.createElement("option");
  op.value=String(i);
  op.textContent=(i+1)+". "+s.name;
  sel.appendChild(op);
 });
 loadTrack(0);
}

function loadTrack(i){
 if(!SONGS.length)return;
 index=(i+SONGS.length)%SONGS.length;
 audio.src=SONGS[index].src;
 audio.load();
 $("track-title").textContent=SONGS[index].name;
 $("track-sub").textContent="TRACK "+(index+1)+" / "+SONGS.length;
 $("playlist").value=String(index);
 $("fill").style.width="0%";
 $("elapsed").textContent="0:00";
 $("duration").textContent="0:00";
}

async function playAudio(){
 if(!SONGS.length)return;
 initAudio();

 if(ctx && ctx.state==="suspended"){
  try{await ctx.resume()}catch(e){}
 }

 try{
  await audio.play();
  playing=true;
  $("play").textContent="Ⅱ";
 }catch(e){
  playing=false;
  $("play").textContent="▶";
  $("track-sub").textContent="แตะปุ่มเล่นอีกครั้ง หากเบราว์เซอร์บล็อกเสียง";
 }
}

function pauseAudio(){
 audio.pause();
 playing=false;
 $("play").textContent="▶";
}

function nextTrack(fromEnded=false){
 if(!SONGS.length)return;

 if(single && fromEnded){
  pauseAudio();
  audio.currentTime=0;
  return;
 }

 if(shuffle && SONGS.length>1){
  let n=index;
  while(n===index)n=Math.floor(Math.random()*SONGS.length);
  loadTrack(n);
 }else if(fromEnded && !loopList && index===SONGS.length-1){
  pauseAudio();
  return;
 }else{
  loadTrack(index+1);
 }

 if(playing || fromEnded)playAudio();
}

$("play").onclick=()=>playing?pauseAudio():playAudio();
$("next").onclick=()=>nextTrack(false);

$("prev").onclick=()=>{
 if(audio.currentTime>3){
  audio.currentTime=0;
  return;
 }
 loadTrack(index-1);
 if(playing)playAudio();
};

$("playlist").onchange=e=>{
 loadTrack(Number(e.target.value));
 playAudio();
};

$("loop").onclick=()=>{
 loopList=!loopList;
 $("loop").classList.toggle("active",loopList);
 if(loopList){
  single=false;
  $("single").classList.remove("active");
 }
};

$("shuffle").onclick=()=>{
 shuffle=!shuffle;
 $("shuffle").classList.toggle("active",shuffle);
};

$("single").onclick=()=>{
 single=!single;
 $("single").classList.toggle("active",single);
 if(single){
  loopList=false;
  $("loop").classList.remove("active");
 }else{
  loopList=true;
  $("loop").classList.add("active");
 }
};
audio.addEventListener("ended",()=>nextTrack(true));
audio.addEventListener("loadedmetadata",()=>{
 $("duration").textContent=timeText(audio.duration);
});
audio.addEventListener("timeupdate",()=>{
 if(audio.duration){
  $("fill").style.width=(audio.currentTime/audio.duration*100)+"%";
  $("elapsed").textContent=timeText(audio.currentTime);
 }
});

$("progress").onclick=e=>{
 if(audio.duration){
  const r=e.currentTarget.getBoundingClientRect();
  audio.currentTime=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width))*audio.duration;
 }
};

$("enter").onclick=async()=>{
 initAudio();
 if(ctx&&ctx.state==="suspended"){
  try{await ctx.resume()}catch(e){}
 }
 $("start").style.opacity="0";
 setTimeout(()=>$("start").style.display="none",620);
 await playAudio();
};

$("fullscreen").onclick=async()=>{
 try{
  if(!document.fullscreenElement)await stage.requestFullscreen();
  else await document.exitFullscreen();
 }catch(e){}
};

fillPlaylist();

/* มิกเซอร์: ปรับความดัง เบส และเสียงแหลม */
$("volume").addEventListener("input",e=>{
 const v=Number(e.target.value);
 $("vol-value").textContent=v+"%";
 if(masterGain&&ctx)masterGain.gain.setTargetAtTime(v/100,ctx.currentTime,.03);
});

$("bass").addEventListener("input",e=>{
 const v=Number(e.target.value);
 $("bass-value").textContent=(v>0?"+":"")+v+" dB";
 if(bassFilter&&ctx)bassFilter.gain.setTargetAtTime(v,ctx.currentTime,.03);
});

$("treble").addEventListener("input",e=>{
 const v=Number(e.target.value);
 $("treble-value").textContent=(v>0?"+":"")+v+" dB";
 if(trebleFilter&&ctx)trebleFilter.gain.setTargetAtTime(v,ctx.currentTime,.03);
});

/* ฉากอวกาศ 3 มิติด้วย Three.js */
const canvas=$("space");
try{
 scene=new THREE.Scene();
 scene.fog=new THREE.FogExp2(0x03040c,0.0038);
 camera=new THREE.PerspectiveCamera(62,1,.1,1200);
 camera.position.z=90;
 renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.8));

 const positions=new Float32Array(2400*3);
 const colors=new Float32Array(2400*3);

 for(let i=0;i<2400;i++){
  positions[i*3]=(Math.random()-.5)*330;
  positions[i*3+1]=(Math.random()-.5)*210;
  positions[i*3+2]=(Math.random()-.5)*650;
  const c=new THREE.Color().setHSL(.52+Math.random()*.28,.85,.55+Math.random()*.3);
  colors.set([c.r,c.g,c.b],i*3);
 }

 const geo=new THREE.BufferGeometry();
 geo.setAttribute("position",new THREE.BufferAttribute(positions,3));
 geo.setAttribute("color",new THREE.BufferAttribute(colors,3));

 stars=new THREE.Points(geo,new THREE.PointsMaterial({
  size:1.05,vertexColors:true,transparent:true,opacity:.9,depthWrite:false
 }));
 scene.add(stars);

 const coreGeo=new THREE.IcosahedronGeometry(17,2);
 coreMat=new THREE.MeshBasicMaterial({
  color:0xbd00ff,wireframe:true,transparent:true,opacity:.19
 });
 const core=new THREE.Mesh(coreGeo,coreMat);
 scene.add(core);

 const ringGeo=new THREE.TorusGeometry(23,.09,8,240);
 const ringMat=new THREE.MeshBasicMaterial({
  color:0x00f5ff,transparent:true,opacity:.65
 });
 const ring=new THREE.Mesh(ringGeo,ringMat);
 ring.rotation.x=1.05;
 scene.add(ring);

 const ring2=new THREE.Mesh(
  new THREE.TorusGeometry(29,.045,6,240),
  new THREE.MeshBasicMaterial({color:0xbd00ff,transparent:true,opacity:.55})
 );
 ring2.rotation.y=.9;
 ring2.rotation.x=.4;
 scene.add(ring2);

 clock=new THREE.Clock();

 function resize3d(){
  const w=stage.clientWidth,h=stage.clientHeight;
  camera.aspect=w/h;
  camera.updateProjectionMatrix();
  renderer.setSize(w,h,false);
 }
 window.addEventListener("resize",resize3d);
 resize3d();

 function render3d(){
  requestAnimationFrame(render3d);
  const t=clock.getElapsedTime();
  stars.rotation.y+=.00045;
  stars.rotation.x=Math.sin(t*.08)*.025;
  core.rotation.x=t*.12;
  core.rotation.y=t*.18;
  ring.rotation.z=t*.12;
  ring2.rotation.z=-t*.09;

  let energy=0;
  if(analyser&&freq&&playing){
   analyser.getByteFrequencyData(freq);
   for(let i=0;i<freq.length;i++)energy+=freq[i];
   energy=energy/freq.length/255;
  }

  core.scale.setScalar(1+energy*.28);
  core.rotation.z=t*.06;
  camera.position.x=Math.sin(t*.09)*2.2;
  camera.position.y=Math.cos(t*.11)*1.5;
  camera.lookAt(0,0,0);
  renderer.render(scene,camera);
 }
 render3d();
}catch(err){
 console.warn("3D renderer unavailable:",err);
}

/* กราฟเสียงหลายเส้น สูงขึ้น และตอบสนองต่อเพลงจริง */
const wc=$("wave"),wctx=wc.getContext("2d");

function drawWave(){
 requestAnimationFrame(drawWave);

 const dpr=Math.min(devicePixelRatio||1,2);
 const w=wc.clientWidth,h=wc.clientHeight;
 if(!w||!h)return;

 if(wc.width!==Math.floor(w*dpr)||wc.height!==Math.floor(h*dpr)){
  wc.width=Math.floor(w*dpr);
  wc.height=Math.floor(h*dpr);
 }

 wctx.setTransform(dpr,0,0,dpr,0,0);
 wctx.clearRect(0,0,w,h);

 if(analyser&&waveData&&playing)analyser.getByteTimeDomainData(waveData);
 if(analyser&&freq&&playing)analyser.getByteFrequencyData(freq);

 const mid=h*.5;
 const points=Math.max(160,Math.floor(w*.95));
 const barCount=Math.min(100,Math.floor(w/7));
 const barGap=2;
 const barW=Math.max(2,(w-(barCount-1)*barGap)/barCount);

 for(let i=0;i<barCount;i++){
  let level=0;

  if(analyser&&freq&&playing){
   const j=Math.floor(i/barCount*freq.length);
   level=freq[j]/255;
  }else{
   level=.08+.08*(.5+.5*Math.sin(i*.32+performance.now()*.002));
  }
  const bh=Math.max(3,level*h*.42);
  const grad=wctx.createLinearGradient(0,mid-bh,0,mid+bh);
  grad.addColorStop(0,"#bd00ff");
  grad.addColorStop(.5,"#ffffff");
  grad.addColorStop(1,"#00f5ff");

  wctx.fillStyle=grad;
  wctx.globalAlpha=.65;
  wctx.fillRect(i*(barW+barGap),mid-bh,barW,bh*2);
 }

 wctx.globalAlpha=1;

 const palette=["#00f5ff","#bd00ff","#ffffff","#ff45df","#38a8ff"];

 for(let layer=0;layer<5;layer++){
  wctx.beginPath();
  wctx.lineWidth=layer===0?3.2:layer===1?2:1.2;
  wctx.strokeStyle=palette[layer];
  wctx.shadowBlur=layer===0?24:14;
  wctx.shadowColor=palette[layer];

  for(let i=0;i<=points;i++){
   const x=i/points*w;
   let v;

   if(analyser&&waveData&&playing){
    const j=Math.floor(i/points*(waveData.length-1));
    v=(waveData[j]-128)/128;
   }else{
    v=Math.sin(i*.12+performance.now()*.0015+layer)*.18+
      Math.sin(i*.035-performance.now()*.001)*.1;
   }

   const amplitude=(playing?h*.72:h*.28)*(1-layer*.105);
   const y=mid+v*amplitude+
     Math.sin(i*.08+performance.now()*.001+layer*1.4)*(2+layer);

   if(i===0)wctx.moveTo(x,y);
   else wctx.lineTo(x,y);
  }

  wctx.stroke();
 }

 wctx.shadowBlur=0;
}
drawWave();

/* โลโก้เคลื่อนไหวจากอนุภาคที่สร้างด้วยพิกเซลของ logo1.jpg */
const lc=$("logo-motion"),lctx=lc.getContext("2d");
const bc=$("burst"),bctx=bc.getContext("2d");
let logoParticles=[],burstMode=0,burstStart=performance.now(),logoImage=null;

function fitCanvas(el,ctx){
 const dpr=Math.min(devicePixelRatio||1,2);
 const w=el.clientWidth,h=el.clientHeight;

 if(!w||!h)return null;

 if(el.width!==Math.floor(w*dpr)||el.height!==Math.floor(h*dpr)){
  el.width=Math.floor(w*dpr);
  el.height=Math.floor(h*dpr);
 }

 ctx.setTransform(dpr,0,0,dpr,0,0);
 return {w,h,dpr};
}

function buildAnimatedLogo(){
 const size=fitCanvas(lc,lctx);
 fitCanvas(bc,bctx);

 if(!size||!LOGO)return;

 logoImage=new Image();

 logoImage.onload=()=>{
  const off=document.createElement("canvas");
  const oc=off.getContext("2d");

  off.width=150;
  off.height=150;
  oc.clearRect(0,0,150,150);
  oc.drawImage(logoImage,0,0,150,150);

  const data=oc.getImageData(0,0,150,150).data;
  logoParticles=[];

  const step=3;
  const scale=Math.min(size.w,size.h)*.86/150;

  for(let y=0;y<150;y+=step){
   for(let x=0;x<150;x+=step){
    const k=(y*150+x)*4;
    const alpha=data[k+3]/255;
    if(alpha<.18)continue;

    const tx=size.w/2+(x-75)*scale;
    const ty=size.h/2+(y-75)*scale;
    const angle=Math.random()*Math.PI*2;
    const dist=30+Math.random()*Math.max(size.w,size.h)*.7;

    logoParticles.push({
     tx,ty,
     sx:size.w/2+Math.cos(angle)*dist,
     sy:size.h/2+Math.sin(angle)*dist,
     r:.7+Math.random()*1.5,
     color:`rgba(${data[k]},${data[k+1]},${data[k+2]},${Math.max(.35,alpha)})`,
     phase:Math.random()*Math.PI*2
    });
   }
  }
 };

 logoImage.src=LOGO;
}

function triggerBurst(){
 if(!logoParticles.length)return;

 burstMode=burstMode===1?0:1;
 burstStart=performance.now();

 $("burst-btn").textContent=burstMode
  ?"✦ ประกอบโลโก้กลับ"
  :"✦ แตกตัว / ประกอบโลโก้";
}

$("burst-btn").onclick=triggerBurst;

function animateLogo(){
 requestAnimationFrame(animateLogo);

 const size=fitCanvas(lc,lctx);
 fitCanvas(bc,bctx);

 if(!size||!logoParticles.length)return;

 const {w,h}=size;
 const now=performance.now();
 const t=now*.001;

 let energy=0;

 if(analyser&&freq&&playing){
  analyser.getByteFrequencyData(freq);
  for(let i=0;i<freq.length;i++)energy+=freq[i];
  energy=energy/freq.length/255;
 }

 lctx.clearRect(0,0,w,h);
 bctx.clearRect(0,0,bc.clientWidth,bc.clientHeight);

 const progress=Math.min(1,(now-burstStart)/1300);
 const scatter=burstMode?progress:1-progress;

 for(const q of logoParticles){
  const drift=Math.sin(t*1.7+q.phase)*(1.5+energy*8);
  const flutter=Math.cos(t*1.3+q.phase)*(1.5+energy*8);

  const tx=q.tx+drift;
  const ty=q.ty+flutter;
  const sx=q.sx+Math.sin(t+q.phase)*22;
  const sy=q.sy+Math.cos(t*.9+q.phase)*22;

  const x=tx+(sx-tx)*scatter;
  const y=ty+(sy-ty)*scatter;
  const radius=q.r*(1+energy*1.8)*(1+Math.sin(t*2+q.phase)*.13);

  lctx.beginPath();
  lctx.fillStyle=q.color;
  lctx.shadowColor=Math.random()>.5?"#00f5ff":"#bd00ff";
  lctx.shadowBlur=8+energy*18;
  lctx.arc(x,y,radius,0,Math.PI*2);
  lctx.fill();

  if(burstMode&&Math.random()>.68){
   bctx.beginPath();
   bctx.fillStyle=q.color;
   bctx.shadowColor="#00f5ff";
   bctx.shadowBlur=10;
   bctx.arc(x,y,Math.max(.6,radius*.65),0,Math.PI*2);
   bctx.fill();
  }
 }
 lctx.shadowBlur=0;
 bctx.shadowBlur=0;
}

buildAnimatedLogo();
animateLogo();
window.addEventListener("resize",buildAnimatedLogo);
</script>
</body>
</html>"""

player_html = (
    player_html
    .replace("__SONGS__", songs_json)
    .replace("__LOGO__", logo_json)
)

st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility:hidden;}
    .stApp, [data-testid="stAppViewContainer"] {background:#02030b;}
    .block-container {padding:0 !important;max-width:100% !important;}
    iframe {border:0 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

if not songs:
    st.info("ยังไม่พบไฟล์เพลงในโฟลเดอร์เดียวกับ app.py ให้วางไฟล์ MP3 ไว้ใน GitHub repository เดียวกัน")

st.caption("🌌 ฉากอวกาศสร้างด้วย CSS และ Three.js ภายในแอป ไม่ใช้คลิปหรือภาพสต็อกภายนอก")
components.html(player_html, height=980, scrolling=False)
