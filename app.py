import os
import base64
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# MON101 NEON MUSIC VISION
# Standalone Music Player
# MP3 + logo.jpg อยู่โฟลเดอร์เดียวกับ app.py
# =========================================================

st.set_page_config(
    page_title="NEON MUSIC VISION",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------
# FIND APP FOLDER
# -----------------------------
APP_DIR = Path(__file__).resolve().parent


# -----------------------------
# FIND MP3 AUTOMATICALLY
# -----------------------------
mp3_files = sorted(
    list(APP_DIR.glob("*.mp3")) +
    list(APP_DIR.glob("*.MP3"))
)


songs = []

for file in mp3_files:
    try:
        with open(file, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")

        songs.append(
            {
                "name": file.stem,
                "src": f"data:audio/mpeg;base64,{audio_b64}",
            }
        )
    except Exception:
        pass


# -----------------------------
# LOGO
# -----------------------------
logo_src = ""

logo_file = APP_DIR / "logo.jpg"

if logo_file.exists():
    try:
        with open(logo_file, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")

        logo_src = f"data:image/jpeg;base64,{logo_b64}"

    except Exception:
        logo_src = ""


# -----------------------------
# SAFE JS DATA
# -----------------------------
import json

songs_json = json.dumps(
    songs,
    ensure_ascii=False
)

logo_json = json.dumps(
    logo_src,
    ensure_ascii=False
)


# =========================================================
# PAGE
# =========================================================

page = r'''
<!DOCTYPE html>
<html lang="th">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<title>NEON MUSIC VISION</title>


<style>

/* ======================================================
   RESET
====================================================== */

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

html,
body{
    width:100%;
    min-height:100%;
    overflow:hidden;
    background:#02030a;
    font-family:
        Arial,
        Helvetica,
        sans-serif;
}

body{
    color:white;
}


/* ======================================================
   BACKGROUND
====================================================== */

.app{
    position:relative;
    width:100vw;
    height:100vh;
    min-height:620px;
    overflow:hidden;

    background:
        radial-gradient(
            circle at 50% 42%,
            rgba(0,220,255,.10),
            transparent 27%
        ),
        radial-gradient(
            circle at 15% 20%,
            rgba(255,0,180,.09),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 80%,
            rgba(120,0,255,.10),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            #010208,
            #050712 45%,
            #02030a
        );
}


/* ======================================================
   MOVING LIGHT
====================================================== */

.light{
    position:absolute;
    border-radius:50%;
    filter:blur(70px);
    pointer-events:none;
    opacity:.22;
    animation:floatLight 10s ease-in-out infinite alternate;
}

.light.one{
    width:300px;
    height:300px;
    left:-100px;
    top:8%;
    background:#00eaff;
}

.light.two{
    width:260px;
    height:260px;
    right:-80px;
    top:18%;
    background:#ff18cf;
    animation-delay:-3s;
}

.light.three{
    width:280px;
    height:280px;
    left:35%;
    bottom:-150px;
    background:#6d35ff;
    animation-delay:-6s;
}

@keyframes floatLight{
    0%{
        transform:translate3d(0,0,0) scale(1);
    }

    50%{
        transform:translate3d(30px,-20px,0) scale(1.15);
    }

    100%{
        transform:translate3d(-20px,25px,0) scale(.92);
    }
}


/* ======================================================
   TOP BAR
====================================================== */

.topbar{
    position:absolute;
    left:0;
    right:0;
    top:0;

    height:104px;

    padding:
        14px
        22px;

    display:flex;
    align-items:center;
    justify-content:space-between;

    z-index:20;

    background:
        linear-gradient(
            180deg,
            rgba(0,0,0,.65),
            rgba(0,0,0,.08)
        );

    border-bottom:
        1px solid
        rgba(255,255,255,.04);
}


/* ======================================================
   BRAND
====================================================== */

.brand{
    display:flex;
    align-items:center;
    gap:16px;
    min-width:0;
}

.logoWrap{
    position:relative;

    width:78px;
    height:78px;

    flex:0 0 78px;

    display:flex;
    align-items:center;
    justify-content:center;

    border-radius:22px;

    background:
        linear-gradient(
            145deg,
            rgba(0,238,255,.18),
            rgba(255,0,190,.15)
        );

    border:
        1px solid
        rgba(255,255,255,.18);

    box-shadow:
        0 0 12px rgba(0,234,255,.45),
        0 0 30px rgba(255,0,210,.18),
        inset 0 0 20px rgba(255,255,255,.05);

    overflow:visible;
}

.logoWrap::before{
    content:"";

    position:absolute;
    inset:-3px;

    border-radius:25px;

    background:
        conic-gradient(
            from 0deg,
            #00eaff,
            #a63cff,
            #ff29ce,
            #ffe36e,
            #00eaff
        );

    z-index:-1;

    animation:
        logoSpin 3.5s linear infinite;

    filter:
        blur(4px);

    opacity:.9;
}

.logoWrap::after{
    content:"";

    position:absolute;
    inset:-8px;

    border-radius:28px;

    border:
        1px solid
        rgba(0,238,255,.18);

    box-shadow:
        0 0 20px rgba(0,238,255,.25),
        0 0 32px rgba(255,0,200,.12);

    animation:
        logoGlow 1.7s ease-in-out infinite alternate;
}

@keyframes logoSpin{
    to{
        transform:rotate(360deg);
    }
}

@keyframes logoGlow{
    from{
        opacity:.35;
        transform:scale(.98);
    }

    to{
        opacity:1;
        transform:scale(1.04);
    }
}

.logo{
    width:72px;
    height:72px;

    object-fit:cover;

    border-radius:19px;

    display:block;

    image-rendering:auto;

    filter:
        contrast(1.12)
        saturate(1.12)
        brightness(1.06)
        drop-shadow(0 0 8px rgba(0,238,255,.45));
}


/* ======================================================
   BRAND TEXT
====================================================== */

.brandText{
    min-width:0;
}

.brandTitle{
    font-size:18px;
    font-weight:900;

    letter-spacing:4px;

    white-space:nowrap;

    background:
        linear-gradient(
            90deg,
            #ffffff 0%,
            #62f5ff 20%,
            #ffffff 38%,
            #ff61df 56%,
            #ffe878 72%,
            #ffffff 88%,
            #62f5ff 100%
        );

    background-size:300% auto;

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;

    filter:
        drop-shadow(0 0 7px rgba(0,234,255,.55));

    animation:
        textShimmer 3.2s linear infinite;
}

.brandSub{
    margin-top:5px;

    font-size:10px;
    font-weight:700;

    letter-spacing:3px;

    color:#d9e7ff;

    text-shadow:
        0 0 5px rgba(0,234,255,.45),
        0 0 10px rgba(255,0,200,.25);

    animation:
        tinyShine 2.8s ease-in-out infinite alternate;
}

@keyframes textShimmer{
    0%{
        background-position:0% center;
    }

    100%{
        background-position:300% center;
    }
}

@keyframes tinyShine{
    from{
        opacity:.72;
    }

    to{
        opacity:1;
        filter:
            drop-shadow(0 0 5px rgba(255,255,255,.5));
    }
}


/* ======================================================
   FULLSCREEN
====================================================== */

.fullscreenBtn{
    border:none;
    outline:none;

    padding:
        13px
        18px;

    min-width:130px;

    border-radius:14px;

    cursor:pointer;

    color:white;

    font-size:12px;
    font-weight:900;

    letter-spacing:2px;

    background:
        linear-gradient(
            135deg,
            rgba(0,234,255,.20),
            rgba(255,0,205,.18)
        );

    border:
        1px solid
        rgba(255,255,255,.28);

    box-shadow:
        0 0 14px rgba(0,234,255,.22),
        inset 0 0 18px rgba(255,255,255,.04);

    text-shadow:
        0 0 7px rgba(255,255,255,.7);

    transition:
        transform .2s,
        box-shadow .2s;
}

.fullscreenBtn:hover{
    transform:translateY(-2px) scale(1.03);

    box-shadow:
        0 0 20px rgba(0,234,255,.45),
        0 0 35px rgba(255,0,205,.18);
}

.fullscreenBtn:active{
    transform:scale(.97);
}


/* ======================================================
   MAIN
====================================================== */

.main{
    position:absolute;

    left:0;
    right:0;

    top:104px;
    bottom:0;

    padding:
        18px
        28px
        22px;

    display:grid;

    grid-template-columns:
        minmax(0,1fr)
        330px;

    gap:24px;

    z-index:5;
}


/* ======================================================
   HERO
====================================================== */

.hero{
    min-width:0;

    display:flex;
    flex-direction:column;

    align-items:center;
    justify-content:center;

    position:relative;
}


/* ======================================================
   KICKER
====================================================== */

.kicker{
    position:relative;

    margin-bottom:8px;

    font-size:11px;
    font-weight:900;

    letter-spacing:5px;

    color:#eaf5ff;

    text-transform:uppercase;

    text-shadow:
        0 0 5px rgba(0,234,255,.8),
        0 0 15px rgba(0,234,255,.35);

    animation:
        textPulse 2.4s ease-in-out infinite;
}

@keyframes textPulse{
    0%,100%{
        opacity:.82;
    }

    50%{
        opacity:1;
    }
}


/* ======================================================
   TITLE
====================================================== */

.title{
    text-align:center;

    max-width:92%;

    font-size:
        clamp(
            26px,
            4vw,
            52px
        );

    line-height:1.05;

    font-weight:1000;

    letter-spacing:1px;

    color:white;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #63f5ff,
            #ffffff,
            #ff61dc,
            #ffe978,
            #ffffff
        );

    background-size:350% auto;

    -webkit-background-clip:text;
    background-clip:text;

    -webkit-text-fill-color:transparent;

    filter:
        drop-shadow(0 0 8px rgba(0,234,255,.55))
        drop-shadow(0 0 18px rgba(255,0,210,.25));

    animation:
        titleShimmer 3.5s linear infinite;
}

@keyframes titleShimmer{
    from{
        background-position:0% center;
    }

    to{
        background-position:350% center;
    }
}

.artist{
    margin-top:8px;

    font-size:12px;
    font-weight:800;

    letter-spacing:3px;

    color:#e4e9ff;

    text-shadow:
        0 0 7px rgba(255,255,255,.32);

    text-align:center;
}


/* ======================================================
   MUSIC CORE
====================================================== */

.coreArea{
    position:relative;

    width:
        min(
            54vw,
            410px
        );

    height:
        min(
            54vw,
            410px
        );

    margin:
        15px
        auto
        12px;

    display:flex;

    align-items:center;
    justify-content:center;
}


/* ======================================================
   CORE RINGS
====================================================== */

.coreRing{
    position:absolute;

    border-radius:50%;

    pointer-events:none;
}

.ring1{
    width:82%;
    height:82%;

    border:
        1px solid
        rgba(0,238,255,.45);

    box-shadow:
        0 0 22px rgba(0,238,255,.25);

    animation:
        ringPulse 1.2s ease-in-out infinite;
}

.ring2{
    width:92%;
    height:92%;

    border:
        1px solid
        rgba(255,54,214,.26);

    animation:
        ringPulse 1.8s ease-in-out infinite reverse;
}

.ring3{
    width:68%;
    height:68%;

    border:
        1px dashed
        rgba(255,226,112,.30);

    animation:
        ringPulse 1s ease-in-out infinite;
}

@keyframes ringPulse{
    0%,100%{
        transform:scale(.96);
        opacity:.5;
    }

    50%{
        transform:scale(1.04);
        opacity:1;
    }
}


/* ======================================================
   CORE
====================================================== */

.musicCore{
    position:relative;

    width:47%;
    height:47%;

    border-radius:30%;

    display:flex;
    align-items:center;
    justify-content:center;

    overflow:hidden;

    background:
        radial-gradient(
            circle at 35% 25%,
            rgba(255,255,255,.16),
            transparent 25%
        ),
        linear-gradient(
            145deg,
            rgba(10,17,35,.98),
            rgba(3,6,17,.98)
        );

    border:
        1px solid
        rgba(255,255,255,.18);

    box-shadow:
        0 0 25px rgba(0,238,255,.35),
        0 0 60px rgba(255,0,210,.12),
        inset 0 0 40px rgba(0,238,255,.08);

    z-index:4;

    animation:
        coreBeat 1.1s ease-in-out infinite;
}

@keyframes coreBeat{
    0%,100%{
        transform:scale(1);
    }

    50%{
        transform:scale(1.025);
    }
}


/* ======================================================
   CENTRAL LOGO
====================================================== */

.coreLogo{
    position:absolute;

    width:55%;
    height:55%;

    object-fit:cover;

    border-radius:24%;

    border:
        2px solid
        rgba(255,255,255,.22);

    filter:
        contrast(1.15)
        saturate(1.18)
        brightness(1.06)
        drop-shadow(0 0 12px rgba(0,238,255,.55));

    z-index:3;
}


/* ======================================================
   CORE MUSIC MARK
====================================================== */

.musicMark{
    position:absolute;

    z-index:4;

    font-size:clamp(34px,5vw,58px);

    font-weight:900;

    color:white;

    text-shadow:
        0 0 7px #00eaff,
        0 0 20px #00eaff,
        0 0 38px #ff27d5;

    animation:
        markPulse .75s ease-in-out infinite;
}

@keyframes markPulse{
    0%,100%{
        opacity:.45;
        transform:scale(.94);
    }

    50%{
        opacity:1;
        transform:scale(1.08);
    }
}


/* ======================================================
   HEADPHONES
====================================================== */

.headphones{
    position:absolute;

    left:50%;
    bottom:-3%;

    transform:translateX(-50%);

    width:48%;
    height:auto;

    z-index:8;

    filter:
        drop-shadow(0 0 5px #00eaff)
        drop-shadow(0 0 14px #00eaff)
        drop-shadow(0 0 24px rgba(255,0,210,.55));

    animation:
        headphonePulse .9s ease-in-out infinite;
}

@keyframes headphonePulse{
    0%,100%{
        transform:
            translateX(-50%)
            scale(1);
    }

    50%{
        transform:
            translateX(-50%)
            scale(1.055);
    }
}


/* ======================================================
   HEARTBEAT VISUALIZER
====================================================== */

.visualizerBox{
    position:absolute;

    left:5%;
    right:5%;

    bottom:2%;

    height:31%;

    z-index:6;

    pointer-events:none;

    border-radius:18px;

    overflow:hidden;

    background:
        linear-gradient(
            180deg,
            transparent,
            rgba(0,0,0,.15)
        );
}

#heartbeat{
    width:100%;
    height:100%;

    overflow:visible;
}

#heartbeatPath{
    fill:none;

    stroke:
        url(#pulseGradient);

    stroke-width:4;

    stroke-linecap:round;
    stroke-linejoin:round;

    filter:
        drop-shadow(0 0 4px #00eaff)
        drop-shadow(0 0 10px #ff29d7)
        drop-shadow(0 0 18px rgba(255,226,112,.65));

    transition:
        stroke-width .08s linear;
}


/* ======================================================
   VISUALIZER GRID
====================================================== */

.grid{
    position:absolute;

    inset:0;

    pointer-events:none;

    background-image:
        linear-gradient(
            rgba(255,255,255,.025) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,.025) 1px,
            transparent 1px
        );

    background-size:
        35px 35px;

    mask-image:
        linear-gradient(
            transparent,
            black 20%,
            black 80%,
            transparent
        );
}


/* ======================================================
   VISUAL TEXT
====================================================== */

.visualText{
    margin-top:2px;

    font-size:9px;

    font-weight:800;

    letter-spacing:4px;

    color:#b9c8e6;

    text-transform:uppercase;

    text-shadow:
        0 0 7px rgba(0,234,255,.4);

    animation:
        visualShimmer 2.7s linear infinite;
}

@keyframes visualShimmer{
    0%,100%{
        opacity:.65;
    }

    50%{
        opacity:1;
        color:white;
    }
}


/* ======================================================
   PLAYER SIDE
====================================================== */

.side{
    min-width:0;

    display:flex;
    flex-direction:column;

    justify-content:center;

    gap:13px;
}


/* ======================================================
   PANEL
====================================================== */

.panel{
    position:relative;

    padding:17px;

    border-radius:20px;

    background:
        linear-gradient(
            145deg,
            rgba(10,15,32,.82),
            rgba(3,6,16,.72)
        );

    border:
        1px solid
        rgba(255,255,255,.09);

    box-shadow:
        0 15px 50px rgba(0,0,0,.30),
        inset 0 0 30px rgba(0,238,255,.025);

    backdrop-filter:blur(12px);
}


/* ======================================================
   CONTROLS
====================================================== */

.controlRow{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:12px;
}

.ctrl{
    width:46px;
    height:46px;

    border-radius:15px;

    border:
        1px solid
        rgba(255,255,255,.13);

    background:
        rgba(255,255,255,.045);

    color:white;

    cursor:pointer;

    font-size:17px;

    transition:
        transform .18s,
        background .18s,
        box-shadow .18s;
}

.ctrl:hover{
    transform:translateY(-2px);

    background:
        rgba(0,234,255,.10);

    box-shadow:
        0 0 15px rgba(0,234,255,.25);
}

.playBtn{
    width:62px;
    height:62px;

    border-radius:20px;

    border:
        1px solid
        rgba(255,255,255,.25);

    background:
        linear-gradient(
            135deg,
            rgba(0,234,255,.30),
            rgba(255,32,208,.28)
        );

    box-shadow:
        0 0 20px rgba(0,234,255,.28),
        0 0 28px rgba(255,0,210,.15);

    font-size:22px;
}


/* ======================================================
   PROGRESS
====================================================== */

.timeRow{
    display:flex;
    justify-content:space-between;

    margin-top:12px;

    color:#b8c4dc;

    font-size:9px;
    font-weight:700;
}

.progress{
    width:100%;
    height:5px;

    margin-top:8px;

    border-radius:20px;

    appearance:none;

    background:
        rgba(255,255,255,.08);

    outline:none;
}

.progress:
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
