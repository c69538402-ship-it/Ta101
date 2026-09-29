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
