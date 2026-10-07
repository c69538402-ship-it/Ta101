VISION🤩 streamlit as st
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

# ---------------------------------------------------------
# หาเพลง MP3 และ logo.jpg อัตโนมัติจากโฟลเดอร์เดียวกับ app.py
# ---------------------------------------------------------
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
        "<div><div style='font-size:72px'>🎧</div>"
        "<h1 style='letter-spacing:5px'>"
        "NEON VISION MUSIC"
        "</h1>"
        "<p style='color:#888'>"
        "นำไฟล์ .mp3 และ logo.jpg มาวางไว้ข้าง app.py"
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
width='140' height='140'%3E
%3Cfilter id='n'%3E
%3CfeTurbulence
type='fractalNoise'
baseFrequency='.8'
numOctaves='3'
stitchTiles='stitch'
/%3E
%3C/filter%3E
%3Crect width='100%25'
height='100%25'
filter='url(%23n)'
opacity='.6'
/%3E
%3C/svg%3E"
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
animation:float1 8s ease-in-out infinite alternate
}

.b2{
width:440px;
height:440px;
background:#ff009d;
right:-240px;
top:300px;
animation:float2 10s ease-in-out infinite alternate
}

.b3{
width:360px;
height:360px;
background:#693cff;
left:35%;
bottom:-250px;
animation:float3 9s ease-in-out infinite alternate
}

@keyframes float1{
to{
transform:translate(120px,70px) scale(1.15)
}
}

@keyframes float2{
to{
transform:translate(-100px,-80px) scale(1.18)
}
}

@keyframes float3{
to{
transform:translate(30px,-100px) scale(1.1)
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
bottom:-54px;
left:50%;

transform:translateX(-50%);

width:116px;
height:72px;

z-index:8;

filter:
drop-shadow(0 0 7px #00eaff)
drop-shadow(0 0 15px rgba(255,0,200,.65));

pointer-events:none
}

.headphone svg{
width:100%;
height:100%;
overflow:visible
}

.headphone .hp-head{
fill:none;
stroke:url(#hpGrad);
stroke-width:7;
stroke-linecap:round
}

.headphone .hp-ear{
fill:url(#hpGrad);
stroke:#fff;
stroke-width:1.2
}

.headphone .hp-inner{
fill:#050711;
stroke:#00eaff;
stroke-width:2
}

.headphone .hp-glow{
fill:none;
stroke:#ff00c8;
stroke-width:2;
opacity:.8
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
0%{transform:scale(1)}
25%{transform:scale(1.045)}
48%{transform:scale(.94)}
68%{transform:scale(1.065)}
100%{transform:scale(1)}
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
transform:rotate(0deg) scale(.97)
}
45%{
transform:rotate(90deg) scale(1.03)
}
100%{
transform:rotate(180deg) scale(.98)
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
background-position:350% center
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
rgba(0,0,0,.10),
rgba(0,0,0,.24)
);

border:
1px solid rgba(255,255,255,.06);

box-shadow:
inset 0 0 35px rgba(0,234,255,.035)
}

.centerLine{
position:absolute;
left:0;
right:0;
top:50%;
height:1px;

background:
linear-gradient(
90deg,
transparent,
#00eaff 18%,
#fff 50%,
#ff00c8 82%,
transparent
);

opacity:.42;

box-shadow:
0 0 10px #00eaff,
0 0 18px #ff00c8;

z-index:1
}

.wave{
position:relative;
width:100%;
height:100%;
overflow:hidden;
padding:0 7px;
z-index:3
}

.pulseSvg{
width:100%;
height:100%;
display:block;
overflow:visible
}

.pulseGlow{
fill:none;
stroke:#00eaff;
stroke-width:8;
opacity:.18;
filter:blur(4px)
}

.pulseLine{
fill:none;
stroke:url(#pulseGrad);
stroke-width:3;
stroke-linecap:round;
stroke-linejoin:miter;

filter:
drop-shadow(0 0 5px #00eaff)
drop-shadow(0 0 10px #ff00c8)
}

.pulseCore{
fill:none;
stroke:#fff;
stroke-width:1.2;
opacity:.8
}

.pulseDot{
fill:#fff;

filter:
drop-shadow(0 0 5px #00eaff)
drop-shadow(0 0 8px #ff00c8)
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
position:fixed;
right:16px;
top:16px;

z-index:9999;

min-width:126px;
height:48px;

padding:0 14px;

border-radius:14px;

border:
1px solid rgba(0,234,255,.55);

background:
linear-gradient(
135deg,
rgba(4,10,24,.96),
rgba(32,5,42,.92)
);

backdrop-filter:blur(12px);

color:#fff;

cursor:pointer;

font-size:11px;
font-weight:900;
letter-spacing:1.4px;

display:flex;
align-items:center;
justify-content:center;

gap:8px;

box-shadow:
0 0 18px rgba(0,234,255,.28),
0 0 30px rgba(255,0,200,.12),
inset 0 0 18px rgba(0,234,255,.06)
}

.fs .fsIcon{
font-size:22px;
line-height:1;
color:#00eaff;

text-shadow:
0 0 8px #00eaff
}

.fs:active{
transform:scale(.94)
}

.fs:hover{
border-color:#fff;

box-shadow:
0 0 24px rgba(0,234,255,.42),
0 0 36px rgba(255,0,200,.2)
}

.forceFull{
position:fixed!important;
inset:0!important;

width:100vw!important;
height:100vh!important;

max-height:none!important;

z-index:999999!important
}

.forceFull .content{
height:calc(100vh - 70px)!important;
width:min(760px,94vw)!important
}

.forceFull .fs{
display:flex!important
}

.stage.fx-rainbow .bar{
background:
linear-gradient(
to top,
#00eaff,
#00ff88,
#ffe600,
#ff6a00,
#ff00c8,
#704cff
);

box-shadow:
0 0 10px #ff00c8
}

.stage.fx-rainbow .halo{
background:
conic-gradient(
#00eaff,
#00ff88,
#ffe600,
#ff7a00,
#ff00c8,
#704cff,
#00eaff
)
}

.stage.fx-laser .bar{
background:
linear-gradient(
to top,
#ffffff,
#ff003c,
#ff00d4
);

box-shadow:
0 0 13px #ff003c
}

.stage.fx-laser .fill{
background:
linear-gradient(
90deg,
#fff,
#ff003c,
#ff00d4
)
}

.stage.fx-laser .halo{
background:
conic-gradient(
#fff,
#ff003c,
#ff00d4,
#fff
)
}

.stage.fx-gold .bar{
background:
linear-gradient(
to top,
#fff7a8,
#ffe066,
#ff9f1c,
#ff4d00
);

box-shadow:
0 0 10px #ffb300
}

.stage.fx-gold .fill{
background:
linear-gradient(
90deg,
#fff7a8,
#ffe066,
#ff9f1c
)
}

.stage.fx-gold .halo{
background:
conic-gradient(
#fff7a8,
#ff9f1c,
#ff4d00,
#fff7a8
)
}

.stage.fx-calm .bar{
background:
linear-gradient(
to top,
#5cf2ff,
#6a7dff,
#c07cff
);

box-shadow:
0 0 8px #6a7dff
}

.stage.fx-calm .halo{
opacity:.35;
animation-duration:2.2s
}

.stage.fx-calm .musicPulse{
animation-duration:1s
            }
@media(max-height:820px){

.stage{
min-height:100vh;
height:100vh;
}

.topbar{
padding:10px 14px;
}

.brand{
font-size:14px;
}

.brand small{
font-size:9px;
}

.logoWrap{
width:120px;
height:120px;
}

.logoWrap img{
max-width:105px;
max-height:105px;
}

.songTitle{
font-size:clamp(22px,4vw,38px);
}

.songArtist{
font-size:12px;
}

.musicCore{
width:170px;
height:170px;
}

.headphones{
width:150px;
}

.pulseBox{
height:145px;
}

.controls{
padding-bottom:10px;
}

}

/* =========================
   EXTRA TEXT SHINE
   ========================= */

.shineText{
background:
linear-gradient(
110deg,
#ffffff 0%,
#ffffff 22%,
#5cf2ff 38%,
#ffffff 50%,
#ff5cf4 65%,
#ffffff 82%,
#ffffff 100%
);

background-size:220% 100%;
-webkit-background-clip:text;
background-clip:text;
color:transparent;

animation:textShine 3.2s linear infinite;

text-shadow:
0 0 12px rgba(92,242,255,.28),
0 0 28px rgba(255,92,244,.18);
}

@keyframes textShine{

0%{
background-position:220% 0;
}

100%{
background-position:-220% 0;
}

}

/* =========================
   FULLSCREEN
   ========================= */

html.fullscreenMode,
body.fullscreenMode{
overflow:hidden !important;
background:#02030a !important;
}

.fullscreenMode .stage{
position:fixed !important;
inset:0 !important;
width:100vw !important;
height:100vh !important;
min-height:100vh !important;
z-index:999999 !important;
overflow:hidden !important;
}

.fullscreenMode .topbar{
position:absolute;
top:0;
left:0;
right:0;
z-index:100;
}

.fullscreenMode .mainArea{
height:100vh;
}

.fullscreenMode .fullBtn{
z-index:1000;
}


/* =========================
   END EXTRA CSS
   ========================= */

</style>

<div class="stage" id="stage">

  <div class="ambient a1"></div>
  <div class="ambient a2"></div>
  <div class="ambient a3"></div>

  <div class="particles" id="particles"></div>

  <div class="topbar">

    <div class="brand shineText">
      NEON VISION
      <small>♫ MUSIC • LIGHT • MOTION ♫</small>
    </div>

    <button class="fullBtn" id="fullscreenBtn">
      ⛶ FULL SCREEN
    </button>

  </div>


  <div class="mainArea">

    <div class="logoArea">

      <div class="logoGlow"></div>

      <div class="logoWrap">

        <img
          id="mainLogo"
          src=""
          alt="Logo"
        >

      </div>

      <div class="logoCaption shineText">
        YOUR MUSIC
      </div>

    </div>


    <div class="playerArea">

      <div class="musicCore" id="musicCore">

        <div class="coreRing ring1"></div>
        <div class="coreRing ring2"></div>
        <div class="coreRing ring3"></div>

        <div class="coreLight"></div>

        <div class="coreSymbol">
          ♫
        </div>

        <div class="coreText">
          MUSIC
        </div>

      </div>


      <div class="headphones">

        <svg
          viewBox="0 0 220 150"
          xmlns="http://www.w3.org/2000/svg"
        >

          <defs>

            <linearGradient
              id="headGradient"
              x1="0%"
              y1="0%"
              x2="100%"
              y2="100%"
            >

              <stop
                offset="0%"
                stop-color="#5cf2ff"
              />

              <stop
                offset="48%"
                stop-color="#8b5cff"
              />

              <stop
                offset="100%"
                stop-color="#ff4df2"
              />

            </linearGradient>

            <filter id="headGlow">

              <feGaussianBlur
                stdDeviation="4"
                result="blur"
              />

              <feMerge>

                <feMergeNode
                  in="blur"
                />

                <feMergeNode
                  in="SourceGraphic"
                />

              </feMerge>

            </filter>

          </defs>


          <path
            d="M35 92
               C35 40 65 18 110 18
               C155 18 185 40 185 92"
            fill="none"
            stroke="url(#headGradient)"
            stroke-width="12"
            stroke-linecap="round"
            filter="url(#headGlow)"
          />


          <path
            d="M35 91
               C35 42 67 24 110 24
               C153 24 185 42 185 91"
            fill="none"
            stroke="#ffffff"
            stroke-opacity=".45"
            stroke-width="2"
          />


          <rect
            x="18"
            y="76"
            width="42"
            height="58"
            rx="18"
            fill="#111526"
            stroke="url(#headGradient)"
            stroke-width="5"
            filter="url(#headGlow)"
          />


          <rect
            x="160"
            y="76"
            width="42"
            height="58"
            rx="18"
            fill="#111526"
            stroke="url(#headGradient)"
            stroke-width="5"
            filter="url(#headGlow)"
          />


          <rect
            x="27"
            y="88"
            width="23"
            height="35"
            rx="10"
            fill="#5cf2ff"
            opacity=".8"
          />


          <rect
            x="170"
            y="88"
            width="23"
            height="35"
            rx="10"
            fill="#ff5cf4"
            opacity=".8"
          />

        </svg>

      </div>


      <div class="musicInfo">

        <div
          class="songTitle shineText"
          id="songTitle"
        >
          NEON MUSIC
        </div>

        <div
          class="songArtist"
          id="songArtist"
        >
          MUSIC EXPERIENCE
        </div>

      </div>


      <div class="pulseBox">

        <svg
          id="pulseSvg"
          viewBox="0 0 1000 220"
          preserveAspectRatio="none"
        >

          <defs>

            <linearGradient
              id="pulseGradient"
              x1="0%"
              y1="0%"
              x2="100%"
              y2="0%"
            >

              <stop
                offset="0%"
                stop-color="#5cf2ff"
              />

              <stop
                offset="25%"
                stop-color="#6a7dff"
              />

              <stop
                offset="50%"
                stop-color="#ffffff"
              />

              <stop
                offset="72%"
                stop-color="#ff5cf4"
              />

              <stop
                offset="100%"
                stop-color="#ff4d8d"
              />

            </linearGradient>

            <filter
              id="pulseGlow"
              x="-20%"
              y="-100%"
              width="140%"
              height="300%"
            >

              <feGaussianBlur
                stdDeviation="5"
                result="blur"
              />

              <feMerge>

                <feMergeNode
                  in="blur"
                />

                <feMergeNode
                  in="SourceGraphic"
                />

              </feMerge>

            </filter>

          </defs>


          <path
            id="pulseGlowPath"
            d=""
            fill="none"
            stroke="url(#pulseGradient)"
            stroke-width="10"
            opacity=".42"
            filter="url(#pulseGlow)"
          />


          <path
            id="pulsePath"
            d=""
            fill="none"
            stroke="url(#pulseGradient)"
            stroke-width="4"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

        </svg>

      </div>


      <div class="progressArea">

        <div class="progressTrack">

          <div
            class="progressFill"
            id="progressFill"
          ></div>

        </div>

        <div class="timeRow">

          <span id="currentTime">
            0:00
          </span>

          <span id="duration">
            0:00
          </span>

        </div>

      </div>


      <div class="controls">

        <button
          class="controlBtn"
          id="prevBtn"
        >
          ⏮
        </button>

        <button
          class="playBtn"
          id="playBtn"
        >
          ▶
        </button>

        <button
          class="controlBtn"
          id="nextBtn"
        >
          ⏭
        </button>

      </div>


      <div class="effects">

        <div class="effectTitle shineText">
          EFFECT MODE
        </div>

        <div class="effectButtons">

          <button
            class="effectBtn active"
            data-fx="cyber"
          >
            CYBER
          </button>

          <button
            class="effectBtn"
            data-fx="rainbow"
          >
            RAINBOW
          </button>

          <button
            class="effectBtn"
            data-fx="laser"
          >
            LASER
          </button>

          <button
            class="effectBtn"
            data-fx="gold"
          >
            GOLD
          </button>

          <button
            class="effectBtn"
            data-fx="calm"
          >
            CALM
          </button>

        </div>


        <div class="sliders">

          <label>
            PUNCH
            <input
              id="punch"
              type="range"
              min="0.5"
              max="2.5"
              step="0.05"
              value="1.45"
            >
          </label>


          <label>
            GLOW
            <input
              id="glow"
              type="range"
              min="0"
              max="2"
              step="0.05"
              value="1"
            >
          </label>


          <label>
            SHAKE
            <input
              id="shake"
              type="range"
              min="0"
              max="18"
              step="1"
              value="8"
            >
          </label>

        </div>

      </div>

    </div>


    <div class="playlist">

      <div class="playlistTitle shineText">
        PLAYLIST
      </div>

      <div
        class="playlistItems"
        id="playlistItems"
      ></div>

    </div>

  </div>

</div>


<script>

const songs = __SONGS__;

const logoSrc = __LOGO__;

const stage =
document.getElementById("stage");

const audio =
new Audio();

audio.preload = "metadata";

audio.crossOrigin = "anonymous";


let currentIndex = 0;

let playing = false;

let analyser = null;

let audioCtx = null;

let sourceNode = null;

let animationId = null;

let punchValue = 1.45;

let glowValue = 1;

let shakeValue = 8;

let effectMode = "cyber";


const mainLogo =
document.getElementById("mainLogo");

if(mainLogo && logoSrc){

mainLogo.src = logoSrc;

}


function cleanName(path){

let name =
path.split("/").pop();

name =
name.replace(/\.[^/.]+$/,"");

name =
name.replace(/[_-]+/g," ");

return name;

}


function formatTime(sec){

if(!isFinite(sec))
return "0:00";

let m =
Math.floor(sec/60);

let s =
Math.floor(sec%60);

return m + ":" +
String(s).padStart(2,"0");

}


function renderPlaylist(){

const box =
document.getElementById(
"playlistItems"
);

box.innerHTML = "";

songs.forEach(
(song,index)=>{

const item =
document.createElement("button");

item.className =
"playlistItem";

if(index === currentIndex)
item.classList.add("selected");

item.innerHTML =
`
<span class="trackNo">
${String(index+1).padStart(2,"0")}
</span>

<span class="trackName">
${cleanName(song)}
</span>

<span class="trackPlay">
${index === currentIndex && playing ? "♫" : "▶"}
</span>
`;

item.onclick = () => {

currentIndex = index;

loadSong(true);

};

box.appendChild(item);

});

}


function loadSong(autoPlay=false){

if(!songs.length)
return;

audio.src =
songs[currentIndex];

audio.load();

document.getElementById(
"songTitle"
).textContent =
cleanName(
songs[currentIndex]
);

document.getElementById(
"songArtist"
).textContent =
"♫ MUSIC EXPERIENCE ♫";

renderPlaylist();

if(autoPlay){

audio.play()
.then(()=>{

playing = true;

updatePlayButton();

startAudio();

})
.catch(()=>{});

}

}


function updatePlayButton(){

const btn =
document.getElementById(
"playBtn"
);

btn.textContent =
playing ? "❚❚" : "▶";

}


function setupAudio(){

if(audioCtx)
return;

audioCtx =
new (window.AudioContext ||
window.webkitAudioContext)();

analyser =
audioCtx.createAnalyser();

analyser.fftSize =
2048;

analyser.smoothingTimeConstant =
0.68;

sourceNode =
audioCtx.createMediaElementSource(
audio
);

sourceNode.connect(analyser);

analyser.connect(
audioCtx.destination
);

}


async function playAudio(){

setupAudio();

if(audioCtx.state === "suspended")
await audioCtx.resume();

await audio.play();

playing = true;

updatePlayButton();

startAudio();

renderPlaylist();

}


function pauseAudio(){

audio.pause();

playing = false;

updatePlayButton();

renderPlaylist();

}


document.getElementById(
"playBtn"
).onclick = () => {

if(!songs.length)
return;

if(playing)
pauseAudio();

else
playAudio();

};


document.getElementById(
"prevBtn"
).onclick = () => {

if(!songs.length)
return;

currentIndex =
(currentIndex - 1 + songs.length)
% songs.length;

loadSong(playing);

};


document.getElementById(
"nextBtn"
).onclick = () => {

if(!songs.length)
return;

currentIndex =
(currentIndex + 1)
% songs.length;

loadSong(playing);

};


audio.addEventListener(
"ended",
()=>{

currentIndex =
(currentIndex + 1)
% songs.length;

loadSong(true);

}
);


audio.addEventListener(
"timeupdate",
()=>{

const percent =
audio.duration
?
(audio.currentTime /
audio.duration) * 100
:
0;

document.getElementById(
"progressFill"
).style.width =
percent + "%";

document.getElementById(
"currentTime"
).textContent =
formatTime(
audio.currentTime
);

});


audio.addEventListener(
"loadedmetadata",
()=>{

document.getElementById(
"duration"
).textContent =
formatTime(
audio.duration
);

});


document.querySelector(
".progressTrack"
).onclick =
(e)=>{

if(!audio.duration)
return;

const rect =
e.currentTarget
.getBoundingClientRect();

const ratio =
(e.clientX - rect.left) /
rect.width;

audio.currentTime =
ratio * audio.duration;

};


function buildPulse(values){

const count = 180;

const center = 90;

let d = "";

for(let i=0;i<count;i++){

const x =
(i/(count-1))*1000;

const distance =
Math.abs(i-center) /
center;

const centerPower =
Math.max(
0,
1 - distance
);

const raw =
values[
Math.floor(
(i/count)*values.length
)
] || 0;

const noise =
(Math.random()-.5)
* 5;

let amp =
raw *
(18 +
centerPower*92)
*
punchValue;

amp += noise;

if(centerPower > .72){

amp *=
1.35 +
Math.random()*.85;

}

const y =
110 -
amp;

if(i===0){

d +=
`M ${x} ${y}`;

}else{

d +=
` L ${x} ${y}`;

}

}

return d;

}


function buildWaveFromAudio(){

if(!analyser)
return "";

const data =
new Uint8Array(
analyser.frequencyBinCount
);

analyser.getByteFrequencyData(
data
);

const values = [];

const center =
Math.floor(
data.length * .48
);

for(
let i=0;
i<180;
i++
){

const p =
i/179;

const offset =
Math.floor(
Math.sin(
p*Math.PI
) * 240
);

const index =
Math.min(
data.length-1,
Math.max(
0,
center-offset
)
);

let v =
data[index]/255;

const centerWeight =
Math.pow(
Math.sin(p*Math.PI),
1.7
);

v *=
0.22 +
centerWeight*1.75;

values.push(v);

}

return buildPulse(values);

}


function drawPulse(){

if(!analyser){

requestAnimationFrame(
drawPulse
);

return;

}

const path =
buildWaveFromAudio();

if(path){

document.getElementById(
"pulsePath"
).setAttribute(
"d",
path
);

document.getElementById(
"pulseGlowPath"
).setAttribute(
"d",
path
);

}

const data =
new Uint8Array(
analyser.frequencyBinCount
);

analyser.getByteFrequencyData(
data
);

let bass = 0;

for(
let i=0;
i<Math.min(80,data.length);
i++
){

bass += data[i];

}

bass /=
Math.min(
80,
data.length
);

const power =
bass/255;

const core =
document.getElementById(
"musicCore"
);

if(core){

const scale =
1 +
power*.20*punchValue;

core.style.transform =
`scale(${scale})`;

}

const shake =
power *
shakeValue;

stage.style.setProperty(
"--shake",
shake + "px"
);

const glow =
0.7 +
power *
glowValue;

stage.style.setProperty(
"--audioGlow",
glow
);

if(power > .72){

stage.classList.add(
"beat"
);

}else{

stage.classList.remove(
"beat"
);

}

animationId =
requestAnimationFrame(
drawPulse
);

}


function startAudio(){

if(animationId)
cancelAnimationFrame(
animationId
);

drawPulse();

}


document.querySelectorAll(
".effectBtn"
).forEach(
btn=>{

btn.onclick = ()=>{

document.querySelectorAll(
".effectBtn"
).forEach(
b=>b.classList.remove(
"active"
)
);

btn.classList.add(
"active"
);

effectMode =
btn.dataset.fx;

stage.classList.remove(
"fx-cyber",
"fx-rainbow",
"fx-laser",
"fx-gold",
"fx-calm"
);

stage.classList.add(
"fx-" + effectMode
);

};

});


document.getElementById(
"punch"
).oninput =
(e)=>{

punchValue =
parseFloat(
e.target.value
);

};


document.getElementById(
"glow"
).oninput =
(e)=>{

glowValue =
parseFloat(
e.target.value
);

};


document.getElementById(
"shake"
).oninput =
(e)=>{

shakeValue =
parseFloat(
e.target.value
);

};


async function toggleFullscreen(){

try{

if(!document.fullscreenElement){

await document.documentElement
.requestFullscreen();

document.documentElement
.classList.add(
"fullscreenMode"
);

document.body
.classList.add(
"fullscreenMode"
);

}else{

await document.exitFullscreen();

document.documentElement
.classList.remove(
"fullscreenMode"
);

document.body
.classList.remove(
"fullscreenMode"
);

}

}catch(e){}

}


document.getElementById(
"fullscreenBtn"
).onclick =
toggleFullscreen;


document.addEventListener(
"fullscreenchange",
()=>{

const active =
!!document.fullscreenElement;

document.documentElement
.classList.toggle(
"fullscreenMode",
active
);

document.body
.classList.toggle(
"fullscreenMode",
active
);

document.getElementById(
"fullscreenBtn"
).textContent =
active
?
"✕ EXIT FULL SCREEN"
:
"⛶ FULL SCREEN";

});


document.addEventListener(
"keydown",
(e)=>{

if(e.key.toLowerCase()==="f"){

toggleFullscreen();

}

if(e.code==="Space"){

e.preventDefault();

if(playing)
pauseAudio();
else
playAudio();

}

if(e.key==="ArrowRight"){

currentIndex =
(currentIndex + 1)
% songs.length;

loadSong(playing);

}

if(e.key==="ArrowLeft"){

currentIndex =
(currentIndex - 1 + songs.length)
% songs.length;

loadSong(playing);

}

});


function createParticles(){

const box =
document.getElementById(
"particles"
);

if(!box)
return;

for(
let i=0;
i<42;
i++
){

const p =
document.createElement(
"span"
);

p.className =
"particle";

p.style.left =
Math.random()*100 +
"%";

p.style.top =
Math.random()*100 +
"%";

p.style.animationDelay =
(Math.random()*5) +
"s";

p.style.animationDuration =
(3+Math.random()*6) +
"s";

box.appendChild(p);

}

}


if(songs.length){

loadSong(false);

}else{

document.getElementById(
"songTitle"
).textContent =
"NO MP3 FOUND";

document.getElementById(
"songArtist"
).textContent =
"PUT .MP3 FILES BESIDE app.py";

}


createParticles();

stage.classList.add(
"fx-cyber"
);

</script>

'''

page = page.replace(
"__SONGS__",
json.dumps(
songs,
ensure_ascii=False
)
)

page = page.replace(
"__LOGO__",
json.dumps(
logo_src,
ensure_ascii=False
)
)

components.html(
page,
height=980,
scrolling=False
)
