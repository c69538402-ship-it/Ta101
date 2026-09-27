import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
import html

try:
    from PIL import Image, ImageEnhance, ImageFilter
except Exception:
    Image = None

st.set_page_config(
    page_title="NEON VISION MUSIC",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).resolve().parent

songs = []

for p in sorted(
    BASE.glob("*.mp3"),
    key=lambda x: x.name.lower()
):
    try:
        data = base64.b64encode(
            p.read_bytes()
        ).decode("ascii")

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

        if Image is not None:

            im = Image.open(
                logo_path
            ).convert("RGB")

            target = max(
                720,
                im.width,
                im.height
            )

            scale = target / max(
                im.width,
                im.height
            )

            if scale > 1:

                im = im.resize(
                    (
                        max(
                            1,
                            int(im.width * scale)
                        ),
                        max(
                            1,
                            int(im.height * scale)
                        )
                    ),
                    Image.Resampling.LANCZOS
                )

            im = ImageEnhance.Contrast(
                im
            ).enhance(1.10)

            im = ImageEnhance.Sharpness(
                im
            ).enhance(1.65)

            im = ImageEnhance.Color(
                im
            ).enhance(1.08)

            import io

            buf = io.BytesIO()

            im.save(
                buf,
                format="JPEG",
                quality=96,
                subsampling=0,
                optimize=True
            )

            logo_src = (
                "data:image/jpeg;base64,"
                +
                base64.b64encode(
                    buf.getvalue()
                ).decode("ascii")
            )

        else:

            logo_src = (
                "data:image/jpeg;base64,"
                +
                base64.b64encode(
                    logo_path.read_bytes()
                ).decode("ascii")
            )

    except Exception:
        logo_src = ""

if not songs:

    st.markdown(
        "<div style='height:80vh;"
        "display:grid;place-items:center;"
        "background:#03030a;color:white;"
        "text-align:center;font-family:Arial'>"
        "<div>"
        "<div style='font-size:72px'>🎧</div>"
        "<h1 style='letter-spacing:5px'>"
        "NEON VISION MUSIC"
        "</h1>"
        "<p style='color:#888'>"
        "นำไฟล์ .mp3 และ logo.jpg "
        "มาวางไว้ข้าง app.py"
        "</p>"
        "</div></div>",
        unsafe_allow_html=True,
    )

    st.stop()

songs_json = json.dumps(
    songs,
    ensure_ascii=False
)

logo_json = json.dumps(
    logo_src
)

page = r'''
<!doctype html>

<html lang="th">

<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1,
maximum-scale=1,
user-scalable=no">

<style>

*{
box-sizing:border-box
}

html,body{
margin:0;
padding:0;
background:#020208;
color:#fff;
font-family:Arial,sans-serif
}

body{
overflow:hidden
}

.stage{
position:relative;
width:100%;
height:980px;
max-height:100vh;
overflow:hidden;

background:
radial-gradient(
circle at 50% 38%,
rgba(40,0,120,.25),
transparent 28%
),
radial-gradient(
circle at 5% 78%,
rgba(0,234,255,.13),
transparent 26%
),
radial-gradient(
circle at 95% 72%,
rgba(255,0,160,.14),
transparent 27%
),
#020208
}

.noise{
position:absolute;
inset:0;
opacity:.035;
pointer-events:none;

background-image:url(
"data:image/svg+xml,
%3Csvg xmlns='http://www.w3.org/2000/svg'
width='140' height='140'
%3E%3Cfilter id='n'%3E
%3CfeTurbulence
type='fractalNoise'
baseFrequency='.8'
numOctaves='3'
stitchTiles='stitch'
/%3E
%3C/filter%3E
%3Crect width='100%25'
height='100%25'
filter='%23n'
opacity='.6'
/%3E%3C/svg%3E"
)
}

.blob{
position:absolute;
border-radius:50%;
filter:blur(75px);
opacity:.26;
pointer-events:none
}

.b1{
width:420px;
height:420px;
background:#00eaff;
left:-220px;
top:180px;
animation:
float1 8s ease-in-out infinite alternate
}

.b2{
width:440px;
height:440px;
background:#ff009d;
right:-240px;
top:300px;
animation:
float2 10s ease-in-out infinite alternate
}

.b3{
width:360px;
height:360px;
background:#693cff;
left:35%;
bottom:-250px;
animation:
float3 9s ease-in-out infinite alternate
}

@keyframes float1{
to{
transform:
translate(120px,70px)
scale(1.15)
}
}

@keyframes float2{
to{
transform:
translate(-100px,-80px)
scale(1.18)
}
}

@keyframes float3{
to{
transform:
translate(30px,-100px)
scale(1.1)
}
}

.top{
position:relative;
z-index:10;
display:flex;
align-items:center;
justify-content:space-between;
padding:18px 22px 0
}

.brand{
display:flex;
align-items:center;
gap:11px
}

.logo{
width:58px;
height:58px;
border-radius:16px;
object-fit:cover;
object-position:center;
border:
1px solid rgba(255,255,255,.42);

box-shadow:
0 0 24px rgba(0,234,255,.42),
0 0 38px rgba(255,0,200,.18);

filter:
contrast(1.08)
saturate(1.08)
brightness(1.04)
}

.brandtxt{
font-weight:900;
letter-spacing:3px;
font-size:14px
}

.status{
font-size:9px;
letter-spacing:3px;
color:#7d7e90
}

.dot{
display:inline-block;
width:7px;
height:7px;
border-radius:50%;
background:#00ffb7;
box-shadow:0 0 12px #00ffb7;
margin-right:7px;
animation:blink 1s infinite
}

@keyframes blink{
50%{
opacity:.25
}
}

.content{
position:relative;
z-index:5;
width:min(680px,94vw);
height:calc(100% - 74px);
margin:5px auto 0;
text-align:center;
display:flex;
flex-direction:column;
align-items:center
}

.kicker{
font-size:9px;
letter-spacing:6px;
color:#686a7b;
margin:5px 0 10px
}

.discbox{
position:relative;
width:min(330px,42vh,76vw);
aspect-ratio:1;
display:grid;
place-items:center;
flex:0 0 auto
}

.halo{
position:absolute;
inset:-8%;
border-radius:50%;

background:
conic-gradient(
#00eaff,
#7a3cff,
#ff00c8,
#ffe66b,
#00eaff
);

filter:blur(20px);
opacity:.48;

animation:
haloPulse .55s steps(2,end) infinite
}

.halo2{
position:absolute;
inset:2%;
border-radius:50%;
border:
2px dashed rgba(0,234,255,.32);

box-shadow:
0 0 35px rgba(0,234,255,.28),
inset 0 0 35px rgba(255,0,200,.12);

animation:
ringSnap .65s steps(4,end) infinite
}

.core{
position:absolute;
inset:15%;
border-radius:50%;

background:
radial-gradient(
circle at 50% 48%,
rgba(0,234,255,.2),
transparent 22%
),
radial-gradient(
circle,
#111526 0 32%,
#070912 33% 63%,
#03040a 64%
);

border:
1px solid rgba(255,255,255,.16);

box-shadow:
inset 0 0 55px #000,
0 0 45px rgba(0,234,255,.2);

transition:
transform .04s steps(2,end)
}

.core:before{
content:"";
position:absolute;
inset:10%;
border-radius:50%;
border:
1px solid rgba(255,255,255,.09);

box-shadow:
0 0 22px rgba(255,0,200,.22)
}

.core.playing{
animation:
corePulse .18s steps(2,end) infinite
}

.cover{
position:absolute;
width:47%;
aspect-ratio:1;
border-radius:22%;
object-fit:cover;
image-rendering:auto;

border:
2px solid rgba(255,255,255,.52);

z-index:4;

box-shadow:
0 0 22px rgba(0,234,255,.65),
0 0 45px rgba(255,0,180,.3);

transition:
transform .04s steps(2,end);

filter:saturate(1.15)
}

.center{
position:absolute;
width:82px;
height:82px;
border-radius:28px;
z-index:6;

background:
rgba(3,4,10,.88);

border:
1px solid rgba(255,255,255,.22);

box-shadow:
0 0 20px rgba(0,234,255,.42),
inset 0 0 24px rgba(255,0,200,.2);

display:grid;
place-items:center;

transform:rotate(45deg);
overflow:visible
}

.center:before{
content:"";
position:absolute;
inset:-11px;
border-radius:34px;

border:
1px solid rgba(0,234,255,.38);

box-shadow:
0 0 18px rgba(0,234,255,.25)
}

.musicMark{
font-size:32px;
font-weight:900;
color:#fff;
line-height:1;

text-shadow:
0 0 8px #00eaff,
0 0 20px #ff00c8;

transform:rotate(-45deg)
}

.headphone{
position:absolute;
bottom:-47px;
left:50%;

transform:
translateX(-50%);

width:76px;
height:42px;

border:
2px solid rgba(255,255,255,.82);

border-top:0;

border-radius:
0 0 38px 38px;

color:#fff;

text-shadow:
0 0 8px #00eaff,
0 0 18px #ff00c8;

z-index:8;

filter:
drop-shadow(0 0 7px #00eaff);

font-size:0
}

.headphone:before,
.headphone:after{
content:"";
position:absolute;
bottom:-1px;
width:15px;
height:25px;
border-radius:8px;

background:
linear-gradient(
180deg,
#fff,
#00eaff 55%,
#ff00c8
);

box-shadow:
0 0 10px #00eaff
}

.headphone:before{
left:-2px
}

.headphone:after{
right:-2px
}

.musicPulse{
position:absolute;
inset:-10px;
border-radius:34px;
border:
2px solid rgba(0,234,255,.7);

animation:
pulseRing .22s steps(2,end) infinite
}

@keyframes corePulse{
0%{
transform:scale(1)
}
25%{
transform:scale(1.045)
}
48%{
transform:scale(.94)
}
68%{
transform:scale(1.065)
}
100%{
transform:scale(1)
}
}

@keyframes pulseRing{
0%{
opacity:.2;
transform:scale(.9)
}
40%{
opacity:1;
transform:scale(1.08)
}
100%{
opacity:.15;
transform:scale(.94)
}
}

@keyframes haloPulse{
0%,100%{
transform:scale(.95);
opacity:.32
}
50%{
transform:scale(1.09);
opacity:.7
}
}

@keyframes ringSnap{
0%{
transform:
rotate(0deg)
scale(.97)
}
45%{
transform:
rotate(90deg)
scale(1.03)
}
100%{
transform:
rotate(180deg)
scale(.98)
}
}

.title{
margin:9px auto 0;
max-width:94%;
font-size:
clamp(21px,4.2vw,34px);

font-weight:900;
white-space:nowrap;
overflow:hidden;
text-overflow:ellipsis;

background:
linear-gradient(
90deg,
#fff,
#66edff,
#b478ff,
#ff62ca,
#ffe66b,
#fff
);

background-size:350% auto;

-webkit-background-clip:text;
color:transparent;

animation:
shine 4s linear infinite
}

@keyframes shine{
to{
background-position:
350% center
}
}

.artist{
margin-top:4px;
font-size:8px;
letter-spacing:5px;
color:#77798c
}

.waveWrap{
position:relative;
width:100%;
height:138px;
margin:10px auto 0;

display:flex;
align-items:center;
justify-content:center;

overflow:hidden;

border-radius:18px;

background:
linear-gradient(
180deg,
rgba(0,0,0,.08),
rgba(0,0,0,.2)
);

border:
1px solid rgba(255,255,255,.04)
}

.centerLine{
position:absolute;
left:0;
right:0;
top:50%;
height:3px;

background:
linear-gradient(
90deg,
transparent,
#00eaff,
#fff,
#ff00c8,
#ffe66b,
#00eaff,
transparent
);

opacity:.8;

box-shadow:
0 0 14px #00eaff,
0 0 28px #ff00c8;

z-index:2
}

.wave{
position:relative;
width:100%;
height:100%;

display:flex;
align-items:center;
justify-content:center;

gap:3px;
overflow:hidden;
padding:0 8px
}

.bar{
width:4px;
height:8px;

border-radius:8px;

flex:1 1 0;
max-width:7px;
min-width:2px;

transform-origin:center;

background:
linear-gradient(
to top,
#00eaff,
#7a4cff,
#ff00c8,
#ffe66b
);

box-shadow:
0 0 9px #00eaff,
0 0 14px #ff00c8;

transition:
height .012s steps(2,end),
transform .012s steps(2,end),
filter .04s
}

.times{
width:100%;
display:flex;
justify-content:space-between;
color:#707184;
font-size:10px;
margin-top:0
}

.progress{
width:100%;
height:5px;
border-radius:20px;

background:
rgba(255,255,255,.08);

overflow:hidden;
cursor:pointer;
margin-top:6px
}

.fill{
height:100%;
width:0;
border-radius:20px;

background:
linear-gradient(
90deg,
#00eaff,
#7a4cff,
#ff00c8,
#ffe66b
);

box-shadow:
0 0 14px #00eaff
}

.controls{
display:flex;
align-items:center;
justify-content:center;
gap:18px;
margin-top:14px
}

.btn{
width:46px;
height:46px;
border-radius:50%;

border:
1px solid rgba(255,255,255,.13);

background:
rgba(255,255,255,.045);

color:#fff;
font-size:17px;
cursor:pointer;
transition:.16s
}

.btn:hover{
transform:scale(1.08);

box-shadow:
0 0 22px rgba(0,234,255,.3)
}

.play{
width:65px;
height:65px;
border:0;

background:
linear-gradient(
135deg,
#00eaff,
#7041ff,
#ff00c8
);

box-shadow:
0 0 25px rgba(0,234,255,.42),
0 0 50px rgba(255,0,200,.18);

font-size:22px
}

.play:hover{
transform:scale(1.09)
}

.effects{
width:100%;
display:flex;
justify-content:center;
gap:7px;
flex-wrap:wrap;
margin-top:10px
}

.fx{
border:
1px solid rgba(255,255,255,.1);

background:
rgba(255,255,255,.035);

color:#858797;
border-radius:999px;

padding:7px 12px;

font-size:8px;
letter-spacing:1.8px;
cursor:pointer
}

.fx.active{
color:#fff;
border-color:#00eaff;

background:
linear-gradient(
90deg,
rgba(0,234,255,.12),
rgba(255,0,200,.11)
);

box-shadow:
0 0 15px rgba(0,234,255,.14)
}

.fxpanel{
width:min(520px,100%);
display:grid;
grid-template-columns:
repeat(3,1fr);

gap:9px;
margin-top:8px;
padding:8px 10px;

border:
1px solid rgba(255,255,255,.06);

border-radius:14px;

background:
rgba(0,0,0,.18)
}

.sliderBox{
text-align:left
}

.sliderBox label{
display:flex;
justify-content:space-between;

color:#77798c;

font-size:7px;
letter-spacing:1.5px;

margin-bottom:3px
}

.sliderBox b{
color:#cdd0df;
font-weight:600
}

.sliderBox input{
width:100%;
accent-color:#00eaff;
height:14px
}

.playlist{
width:100%;
margin:9px auto 0;
padding:8px;

border:
1px solid rgba(255,255,255,.07);

border-radius:14px;

background:
rgba(255,255,255,.035);

backdrop-filter:blur(18px);

flex:1;
min-height:60px;
max-height:135px;

overflow:auto;
text-align:left
}

.pltitle{
font-size:8px;
letter-spacing:4px;
color:#686a7b;
padding:2px 8px 5px
}

.track{
display:flex;
align-items:center;
gap:10px;

padding:7px 9px;

border-radius:9px;

color:#9294a5;

font-size:10px;
cursor:pointer
}

.track:hover{
background:
rgba(255,255,255,.06);
color:#fff
}

.track.active{
background:
linear-gradient(
90deg,
rgba(0,234,255,.12),
rgba(255,0,200,.06)
);

color:#fff;

box-shadow:
inset 2px 0 #00eaff
}

.num{
width:22px;
color:#555768
}

.track.active .num{
color:#00eaff
}

.name{
overflow:hidden;
text-overflow:ellipsis;
white-space:nowrap
}

.fxCanvas{
position:absolute;
inset:0;
width:100%;
height:100%;
pointer-events:none;
z-index:3
}

.beatFlash{
position:absolute;
inset:0;

background:
radial-gradient(
circle at 50% 48%,
rgba(255,255,255,.3),
rgba(0,234,255,.12),
transparent 55%
);

opacity:0;
pointer-events:none;
z-index:4;

mix-blend-mode:screen
}

.visualText{
position:absolute;
bottom:7px;
left:0;
right:0;

text-align:center;

color:#4e5061;
font-size:7px;
letter-spacing:4px
}

.fs{
position:absolute;
right:18px;
top:72px;
z-index:50;

width:48px;
height:48px;

border-radius:50%;

border:
1px solid rgba(0,234,255,.32);

background:
rgba(3,4,12,.72);

backdrop-filter:blur(10px);

color:#fff;
cursor:pointer;
font-size:22px;

box-shadow:
0 0 18px rgba(0,234,255,.22),
inset 0 0 14px rgba(255,0,200,.08)
}

.fs:active{
transform:scale(.94)
}
const songs=__SONGS__;
const logoSrc=__LOGO__;
let index=0;

const audio=new Audio();
audio.preload="auto";

const stage=document.getElementById("stage");
const disc=document.getElementById("disc");
const cover=document.getElementById("cover");
const title=document.getElementById("title");
const play=document.getElementById("play");
const tracks=document.getElementById("tracks");
const now=document.getElementById("now");
const total=document.getElementById("total");
const fill=document.getElementById("fill");
const progress=document.getElementById("progress");
const wave=document.getElementById("wave");
const canvas=document.getElementById("fxCanvas");
const flash=document.getElementById("beatFlash");
const ctx2=canvas.getContext("2d");

if(logoSrc){
    document.getElementById("logo").src=logoSrc;
    cover.src=logoSrc;
}

const bars=[];

for(let i=0;i<68;i++){
    const b=document.createElement("div");
    b.className="bar";
    b.style.setProperty("--i",i);
    wave.appendChild(b);
    bars.push(b);
}

let ctx=null;
let analyser=null;
let source=null;
let connected=false;
let energy=0;
let peak=0;
let lastBeat=0;
let particles=[];

let punch=.85;
let glow=.70;
let shake=.75;

function safe(t){
    return String(t).replace(
        /[&<>"']/g,
        m=>({
            "&":"&amp;",
            "<":"&lt;",
            ">":"&gt;",
            '"':"&quot;",
            "'":"&#039;"
        }[m])
    );
}

function fmt(v){
    if(!v||isNaN(v))return "0:00";

    const m=Math.floor(v/60);
    const s=Math.floor(v%60);

    return m+":"+String(s).padStart(2,"0");
}

function analyserSetup(){

    if(connected)return;

    try{

        ctx=new(window.AudioContext||window.webkitAudioContext)();

        analyser=ctx.createAnalyser();

        analyser.fftSize=512;

        analyser.smoothingTimeConstant=.08;

        source=ctx.createMediaElementSource(audio);

        source.connect(analyser);

        analyser.connect(ctx.destination);

        connected=true;

    }catch(e){

        console.log(e);

    }
}

function resizeCanvas(){

    const r=canvas.getBoundingClientRect();

    const d=devicePixelRatio||1;

    canvas.width=Math.max(
        1,
        Math.floor(r.width*d)
    );

    canvas.height=Math.max(
        1,
        Math.floor(r.height*d)
    );

    ctx2.setTransform(d,0,0,d,0,0);
}

window.addEventListener(
    "resize",
    resizeCanvas
);

resizeCanvas();

function spawn(count=3,pow=1){

    const w=canvas.clientWidth;
    const h=canvas.clientHeight;

    const cx=w/2;
    const cy=h*.48;

    for(let i=0;i<count;i++){

        const a=Math.random()*Math.PI*2;

        const s=
            (.6+Math.random()*2.2)*pow;

        particles.push({

            x:cx,
            y:cy,

            vx:Math.cos(a)*s,

            vy:Math.sin(a)*s,

            r:1+Math.random()*2.6,

            life:1,

            h:Math.random()*360

        });

    }

    if(particles.length>180){

        particles.splice(
            0,
            particles.length-180
        );
    }
}

function drawParticles(){

    const w=canvas.clientWidth;
    const h=canvas.clientHeight;

    ctx2.clearRect(
        0,
        0,
        w,
        h
    );

    ctx2.globalCompositeOperation="lighter";

    for(
        let i=particles.length-1;
        i>=0;
        i--
    ){

        const p=particles[i];

        p.x+=p.vx;
        p.y+=p.vy;

        p.vx*=.985;
        p.vy*=.985;

        p.life-=.014;

        if(
            p.life<=0 ||
            p.x<0 ||
            p.x>w ||
            p.y<0 ||
            p.y>h
        ){

            particles.splice(i,1);

            continue;
        }

        ctx2.beginPath();

        ctx2.arc(
            p.x,
            p.y,
            p.r*p.life,
            0,
            Math.PI*2
        );

        ctx2.fillStyle=
            `hsla(
                ${p.h},
                100%,
                65%,
                ${p.life*.72}
            )`;

        ctx2.shadowBlur=10;

        ctx2.shadowColor=
            `hsl(${p.h} 100% 60%)`;

        ctx2.fill();
    }

    ctx2.shadowBlur=0;

    ctx2.globalCompositeOperation=
        "source-over";
}

function draw(){

    requestAnimationFrame(draw);

    let data=null;

    if(analyser){

        data=new Uint8Array(
            analyser.frequencyBinCount
        );

        analyser.getByteFrequencyData(data);
    }

    const t=performance.now()/1000;

    let bass=0;
    let mid=0;
    let high=0;

    if(data){

        for(
            let i=0;
            i<Math.min(14,data.length);
            i++
        ){

            bass+=data[i];
        }

        bass/=14*255;

        for(
            let i=14;
            i<70 && i<data.length;
            i++
        ){

            mid+=data[i];
        }

        mid/=56*255;

        for(
            let i=70;
            i<150 && i<data.length;
            i++
        ){

            high+=data[i];
        }

        high/=80*255;

    }else{

        bass=
            .18+
            Math.abs(Math.sin(t*3))*.24;

        mid=
            .22+
            Math.abs(Math.sin(t*4.3))*.18;

        high=
            .18+
            Math.abs(Math.sin(t*6.8))*.15;
    }

    energy=Math.min(
        1,
        bass*.72+
        mid*.2+
        high*.08
    );

    peak=Math.max(
        peak*.91,
        energy
    );

    const kick=
        Math.max(
            0,
            energy-.32
        )*punch;

    bars.forEach((b,i)=>{

        let n=0;

        if(data){

            const pos=
                Math.floor(
                    (i/68)*data.length
                );

            let a=
                data[
                    Math.max(0,pos-3)
                ]||0;

            let c=
                data[pos]||0;

            let d=
                data[
                    Math.min(
                        data.length-1,
                        pos+3
                    )
                ]||0;

            n=
                (a+c*2.4+d)/4.4;

        }else{

            n=
                20+
                Math.abs(
                    Math.sin(
                        t*3+i*.63
                    )
                )*35;
        }

        const side=
            i<34
            ? i
            : 67-i;

        const jitter=
            (Math.random()-.5)*
            shake*
            18;

        const centerBoost=
            1+
            (1-side/34)*.48;

        const h=Math.max(
            5,
            Math.min(
                58+(energy*32),
                n*.55*
                centerBoost+
                jitter+
                kick*72
            )
        );

        b.style.height=
            h+"px";

        b.style.transform=
            `scaleY(
                ${1+Math.min(
                    1.1,
                    kick*.9
                )}
            )`;

        const hue=
            (
                i/68*300+
                195+
                energy*90
            )%360;

        b.style.background=
            `linear-gradient(
                to top,
                hsl(${hue} 100% 55%),
                hsl(${(hue+48)%360} 100% 60%),
                hsl(${(hue+105)%360} 100% 60%)
            )`;

        b.style.boxShadow=
            `0 0 ${
                8+energy*glow*14
            }px hsl(
                ${hue}
                100%
                60%
            ),
            0 0 ${
                12+energy*glow*22
            }px hsl(
                ${(hue+100)%360}
                100%
                60%
            )`;

        b.style.filter=
            `brightness(
                ${1+energy*.9}
            )
            saturate(
                ${1.1+energy}
            )`;
    });

    const snap=
        1+
        energy*.13+
        kick*.20;

    disc.style.transform=
        `scale(${snap.toFixed(3)})`;

    cover.style.transform=
        `scale(${(
            1+
            energy*.2+
            kick*.16
        ).toFixed(3)})`;

    const beat=
        energy>.58 &&
        energy>peak*.82 &&
        performance.now()-lastBeat>105;

    if(beat){

        lastBeat=
            performance.now();

        spawn(
            12,
            1.2+energy
        );

        flash.style.opacity=
            String(
                Math.min(
                    .22,
                    .05+energy*.22
                )
            );

    }else{

        flash.style.opacity=
            String(
                Math.max(
                    0,
                    Number(
                        flash.style.opacity||0
                    )-.035
                )
            );
    }

    if(Math.random()<.35){

        spawn(
            1,
            Math.max(
                .35,
                energy*1.5
            )
        );
    }

    drawParticles();
}

draw();

function render(){

    tracks.innerHTML="";

    songs.forEach((s,i)=>{

        const d=
            document.createElement("div");

        d.className=
            "track"+
            (i===index
                ?" active"
                :"");

        d.innerHTML=
            '<span class="num">'+
            String(i+1).padStart(2,"0")+
            '</span>'+
            '<span class="name">'+
            safe(s.name)+
            '</span>';

        d.addEventListener(
            "click",
            ()=>{
                load(i);
                playAudio();
            }
        );

        tracks.appendChild(d);
    });
}

function load(i){

    index=
        (i+songs.length)%
        songs.length;

    audio.src=
        songs[index].src;

    title.textContent=
        songs[index].name;

    now.textContent=
        "0:00";

    total.textContent=
        "0:00";

    fill.style.width=
        "0%";

    render();
}

async function playAudio(){

    analyserSetup();

    try{

        if(
            ctx &&
            ctx.state==="suspended"
        ){

            await ctx.resume();
        }

        await audio.play();

        play.textContent="❚❚";

        disc.classList.add(
            "playing"
        );

    }catch(e){

        console.log(e);
    }
}

function pauseAudio(){

    audio.pause();

    play.textContent="▶";

    disc.classList.remove(
        "playing"
    );
}

play.addEventListener(
    "click",
    ()=>{
        audio.paused
        ? playAudio()
        : pauseAudio();
    }
);

document.getElementById(
    "prev"
).addEventListener(
    "click",
    ()=>{
        load(index-1);
        playAudio();
    }
);

document.getElementById(
    "next"
).addEventListener(
    "click",
    ()=>{
        load(index+1);
        playAudio();
    }
);

audio.addEventListener(
    "ended",
    ()=>{
        load(index+1);
        playAudio();
    }
);

audio.addEventListener(
    "loadedmetadata",
    ()=>{
        total.textContent=
            fmt(audio.duration);
    }
);

audio.addEventListener(
    "timeupdate",
    ()=>{

        now.textContent=
            fmt(audio.currentTime);

        if(audio.duration){

            fill.style.width=
                (
                    audio.currentTime/
                    audio.duration*
                    100
                )+"%";
        }
    }
);

progress.addEventListener(
    "click",
    e=>{

        if(!audio.duration)return;

        const r=
            progress.getBoundingClientRect();

        audio.currentTime=
            Math.max(
                0,
                Math.min(
                    1,
                    (e.clientX-r.left)/
                    r.width
                )
            )*
            audio.duration;
    }
);

document.querySelectorAll(
    ".fx"
).forEach(
    btn=>
        btn.addEventListener(
            "click",
            ()=>{

                const fx=
                    btn.dataset.fx;

                stage.classList.remove(
                    "fx-rainbow",
                    "fx-laser",
                    "fx-gold",
                    "fx-calm"
                );

                if(fx!=="cyber"){

                    stage.classList.add(
                        "fx-"+fx
                    );
                }

                document.querySelectorAll(
                    ".fx"
                ).forEach(
                    x=>
                        x.classList.toggle(
                            "active",
                            x===btn
                        )
                );
            }
        )
);

document.getElementById(
    "fs"
).addEventListener(
    "click",
    ()=>{
        const el=
            document.getElementById(
                "stage"
            );

        if(!document.fullscreenElement){

            if(el.requestFullscreen){

                el.requestFullscreen();
            }

        }else if(
            document.exitFullscreen
        ){

            document.exitFullscreen();
        }
    }
);

function bindSlider(
    id,
    setter,
    valId
){

    const el=
        document.getElementById(id);

    const out=
        document.getElementById(valId);

    el.addEventListener(
        "input",
        ()=>{

            const v=
                Number(el.value);

            setter(v);

            out.textContent=
                v;
        }
    );
}

bindSlider(
    "punch",
    v=>punch=v/100,
    "punchVal"
);

bindSlider(
    "glow",
    v=>glow=v/100,
    "glowVal"
);

bindSlider(
    "shake",
    v=>shake=v/100,
    "shakeVal"
);

load(0);

</script>

</body>
</html>
'''

page = page.replace(
    "__SONGS__",
    songs_json
)

page = page.replace(
    "__LOGO__",
    logo_json
)

components.html(
    page,
    height=980,
    scrolling=False
)
