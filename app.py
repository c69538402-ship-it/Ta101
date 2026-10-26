from pathlib import Path
import base64
import mimetypes
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D Space Music Visualizer • TA101",
    page_icon="🌌",
    layout="centered"
)

ROOT = Path(__file__).resolve().parent

# 1. แปลงไฟล์เพลงเป็น Base64 อัตโนมัติ
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".flac"}
songs = []
for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
        try:
            mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            songs.append({
                "name": path.stem,
                "src": f"data:{mime};base64,{encoded}"
            })
        except OSError:
            pass

if not songs:
    songs = [{
        "name": "Cybernetic Universe (Demo)",
        "src": "https://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg"
    }]

songs_json = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")

# 2. แปลงรูปโลโก้ logo1.jpg เป็น Base64 ป้องกันภาพไม่ขึ้น
logo_base64 = "https://via.placeholder.com/70/00f3ff/000000?text=LOGO"
logo_path = ROOT / "logo1.jpg"
if logo_path.exists():
    try:
        logo_mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
        logo_encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        logo_base64 = f"data:{logo_mime};base64,{logo_encoded}"
    except OSError:
        pass

# 3. โครงสร้าง HTML / CSS / JavaScript พร้อมระบบเลือกธีม
player_html = r"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>3D Space Music Visualizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Prompt:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --primary: #00f3ff;
            --secondary: #ff00ff;
            --bg-glow: rgba(0, 243, 255, 0.3);
            --panel-bg: rgba(12, 8, 25, 0.85);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html { width: 100%; height: 100%; overflow: hidden; background: #000; font-family: 'Prompt', sans-serif; }

        .app-container {
            position: relative;
            width: 100%;
            max-width: 450px;
            height: 100vh;
            margin: 0 auto;
            background: #05020a;
            overflow: hidden;
            box-shadow: 0 0 35px var(--bg-glow);
            transition: box-shadow 0.5s ease;
        }

        #canvas-container {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        }

        .ui-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; z-index: 10;
            display: flex; flex-direction: column; justify-content: space-between;
            padding: 15px; pointer-events: none;
        }
        .ui-layer > * { pointer-events: auto; }

        .header-section { text-align: center; margin-top: 2px; }

        /* แผงเลือกธีมสี */
        .theme-selector {
            display: flex; justify-content: center; gap: 8px; margin-bottom: 8px;
        }
        .theme-btn {
            width: 22px; height: 22px; border-radius: 50%; border: 2px solid #fff;
            cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
        }
        .theme-btn:hover { transform: scale(1.2); }
        .theme-btn.active-theme { box-shadow: 0 0 10px #fff; transform: scale(1.15); }
        
        #btn-cyber { background: linear-gradient(135deg, #00f3ff, #ff00ff); }
        #btn-matrix { background: linear-gradient(135deg, #00ff66, #0033ff); }
        #btn-sunset { background: linear-gradient(135deg, #ff5500, #ff007f); }
        #btn-space { background: linear-gradient(135deg, #9900ff, #00ccff); }

        .logo-wrapper {
            width: 65px; height: 65px; margin: 0 auto 4px auto;
            border-radius: 50%; overflow: hidden;
            border: 2px solid var(--primary);
            box-shadow: 0 0 20px var(--primary), inset 0 0 15px var(--secondary);
            transition: transform 0.05s ease, border-color 0.5s, box-shadow 0.5s;
        }
        .logo-wrapper img {
            width: 100%; height: 100%; object-fit: cover;
            animation: spin-logo 8s linear infinite;
        }
        @keyframes spin-logo { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        /* ตัวหนังสือวิ้งนีออนเปลี่ยนสีสมูท */
        .neon-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 18px; font-weight: 900;
            text-transform: uppercase;
            color: var(--primary);
            text-shadow: 0 0 10px var(--primary), 0 0 20px var(--secondary);
            animation: neon-glow 1.5s ease-in-out infinite alternate;
        }
        @keyframes neon-glow {
            0% { transform: scale(1); text-shadow: 0 0 8px var(--primary), 0 0 15px var(--secondary); }
            100% { transform: scale(1.02); text-shadow: 0 0 15px var(--primary), 0 0 30px var(--secondary); }
        }

        .subtitle {
            font-size: 9px; color: #a0a0c0; margin-top: 1px; letter-spacing: 2px;
        }

        .visualizer-container {
            width: 100%; height: 55px; display: flex; align-items: flex-end;
            justify-content: center; gap: 3px; padding: 0 10px;
        }
        .bar {
            flex: 1; background: linear-gradient(to top, var(--primary), var(--secondary));
            border-radius: 4px 4px 0 0; box-shadow: 0 0 10px var(--primary); height: 5px;
            transition: height 0.05s ease, background 0.5s;
        }

        .player-panel {
            background: var(--panel-bg); backdrop-filter: blur(15px);
            border: 1px solid var(--primary); border-radius: 18px;
            padding: 12px 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.9);
            margin-bottom: 2px; transition: border-color 0.5s;
        }

        .track-info { display: flex; align-items: center; margin-bottom: 8px; }
        .track-thumb {
            width: 35px; height: 35px; border-radius: 8px; overflow: hidden;
            border: 1px solid var(--secondary); margin-right: 10px; flex-shrink: 0;
        }
        .track-thumb img { width: 100%; height: 100%; object-fit: cover; }
        .track-meta { overflow: hidden; }
        .track-name {
            font-size: 12px; font-weight: 600; color: #fff;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .track-artist { font-size: 9px; color: var(--primary); }

        .progress-area { margin-bottom: 8px; }
        .progress-bar {
            width: 100%; height: 5px; background: rgba(255, 255, 255, 0.15);
            border-radius: 3px; cursor: pointer; position: relative; overflow: hidden;
        }
        .progress-fill {
            height: 100%; width: 0%; background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 3px; box-shadow: 0 0 10px var(--primary);
        }
        .time-stamps {
            display: flex; justify-content: space-between; font-size: 9px; color: #8888aa; margin-top: 2px;
        }

        .controls { display: flex; align-items: center; justify-content: space-around; }
        .btn-control {
            background: none; border: none; color: #fff; font-size: 14px;
            cursor: pointer; transition: all 0.2s; text-shadow: 0 0 10px var(--primary);
        }
        .btn-control:hover { color: var(--primary); transform: scale(1.15); }
        .btn-control.active { color: var(--secondary); text-shadow: 0 0 12px var(--secondary); }

        .btn-play-pause {
            width: 40px; height: 40px; border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none; color: #fff; font-size: 15px;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; box-shadow: 0 0 20px var(--secondary);
            transition: transform 0.2s;
        }
        .btn-play-pause:hover { transform: scale(1.1); }

        #start-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(3, 1, 6, 0.96); z-index: 100;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center; padding: 20px; transition: opacity 0.5s ease;
        }
        #start-overlay h1 {
            font-family: 'Orbitron', sans-serif; font-size: 18px; color: var(--primary);
            margin-bottom: 10px; text-shadow: 0 0 15px var(--primary);
        }
        #start-overlay p { color: #b0b0d0; font-size: 11px; margin-bottom: 20px; line-height: 1.4; }
        .btn-start {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none; color: #fff; padding: 12px 30px; font-size: 14px;
            font-weight: 700; border-radius: 30px; cursor: pointer;
            box-shadow: 0 0 25px var(--primary); font-family: 'Prompt', sans-serif;
            text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s;
        }
        .btn-start:hover { transform: scale(1.06); }
    </style>
</head>
<body>

    <div class="app-container" id="app-container">
        <div id="start-overlay">
            <h1>TA101 • NEON MUSIC 3D</h1>
            <p>แตะปุ่มเพื่อเปิดใช้งานภาพ 3 มิติ เลือกธีม และฟังเพลงต่อเนื่อง</p>
            <button class="btn-start" id="btn-start-app"><i class="fa-solid fa-play"></i> เริ่มต้นใช้งาน</button>
        </div>

        <div id="canvas-container"></div>

        <div class="ui-layer">
            <div class="header-section">
                <!-- ปุ่มเปลี่ยนธีม -->
                <div class="theme-selector">
                    <div class="theme-btn active-theme" id="btn-cyber" onclick="setTheme('#00f3ff', '#ff00ff', 'rgba(0,243,255,0.3)')" title="Cyberpunk"></div>
                    <div class="theme-btn" id="btn-matrix" onclick="setTheme('#00ff66', '#0033ff', 'rgba(0,255,102,0.3)')" title="Matrix"></div>
                    <div class="theme-btn" id="btn-sunset" onclick="setTheme('#ff5500', '#ff007f', 'rgba(255,85,0,0.3)')" title="Sunset"></div>
                    <div class="theme-btn" id="btn-space" onclick="setTheme('#cc00ff', '#00ffff', 'rgba(204,0,255,0.3)')" title="Deep Space"></div>
                </div>

                <div class="logo-wrapper" id="logo-box">
                    <img src="__LOGO_BASE64__" alt="Logo">
                </div>
                <h1 class="neon-title" id="neon-title-text">COSMIC BEAT</h1>
                <div class="subtitle">TA101 NEBULA 3D</div>
            </div>

            <div class="visualizer-container" id="visualizer"></div>

            <div class="player-panel">
                <div class="track-info">
                    <div class="track-thumb">
                        <img src="__LOGO_BASE64__" alt="Track Art">
                    </div>
                    <div class="track-meta">
                        <div class="track-name" id="track-title">กำลังเตรียมเพลง...</div>
                        <div class="track-artist" id="track-artist">Local Folder Playlist</div>
                    </div>
                </div>

                <div class="progress-area">
                    <div class="progress-bar" id="progress-bar">
                        <div class="progress-fill" id="progress-fill"></div>
                    </div>
                    <div class="time-stamps">
                        <span id="current-time">0:00</span>
                        <span id="total-duration">0:00</span>
                    </div>
                </div>

                <div class="controls">
                    <button class="btn-control active" id="btn-loop" title="เล่นวนซ้ำ"><i class="fa-solid fa-rotate-right"></i></button>
                    <button class="btn-control" id="btn-prev" title="เพลงก่อนหน้า"><i class="fa-solid fa-backward-step"></i></button>
                    <button class="btn-play-pause" id="btn-play"><i class="fa-solid fa-play" id="play-icon"></i></button>
                    <button class="btn-control" id="btn-next" title="เพลงถัดไป"><i class="fa-solid fa-forward-step"></i></button>
                    <button class="btn-control" id="btn-shuffle" title="สุ่มเพลง"><i class="fa-solid fa-shuffle"></i></button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

    <script>
        const songs = __SONGS__;

        let currentTrackIndex = 0;
        let isPlaying = false;
        let isLooping = true;
        let isShuffling = false;

        const audioElement = new Audio();
        audioElement.crossOrigin = "anonymous";
        audioElement.preload = "auto";

        let audioCtx, analyser, sourceNode, dataArray;

        // ฟังก์ชันเปลี่ยนธีมสีแบบเรียลไทม์
        function setTheme(primaryColor, secondaryColor, glowColor) {
            document.documentElement.style.setProperty('--primary', primaryColor);
            document.documentElement.style.setProperty('--secondary', secondaryColor);
            document.documentElement.style.setProperty('--bg-glow', glowColor);
            
            // เปลี่ยนสีดาวและวัตถุ 3D ตามธีม
            if (starMaterial) starMaterial.color.set(primaryColor);
            if (musicCoreMaterial) musicCoreMaterial.color.set(secondaryColor);

            // อัปเดตสถานะปุ่มแอคทีฟ
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active-theme'));
            event.target.classList.add('active-theme');
        }

        function loadTrack(index) {
            if (!songs.length) return;
            currentTrackIndex = (index + songs.length) % songs.length;
            audioElement.src = songs[currentTrackIndex].src;
            document.getElementById('track-title').innerText = songs[currentTrackIndex].name;
            document.getElementById('track-artist').innerText = "TA101 Playlist (" + (currentTrackIndex + 1) + "/" + songs.length + ")";
            audioElement.load();
        }

        loadTrack(currentTrackIndex);

        function initAudioContext() {
            if (audioCtx) return;
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
            analyser = audioCtx.createAnalyser();
            sourceNode = audioCtx.createMediaElementSource(audioElement);
            sourceNode.connect(analyser);
            analyser.connect(audioCtx.destination);
            analyser.fftSize = 64;
            dataArray = new Uint8Array(analyser.frequencyBinCount);
        }

        const visualizerContainer = document.getElementById('visualizer');
        const numBars = 16;
        const bars = [];
        for (let i = 0; i < numBars; i++) {
            const bar = document.createElement('div');
            bar.className = 'bar';
            visualizerContainer.appendChild(bar);
            bars.push(bar);
        }

        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x05020a, 0.02);

        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 45;

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);


                const starCount = 600;
        const starGeometry = new THREE.BufferGeometry();
        const starPositions = new Float32Array(starCount * 3);

        for (let i = 0; i < starCount * 3; i += 3) {
            starPositions[i] = (Math.random() - 0.5) * 180;
            starPositions[i + 1] = (Math.random() - 0.5) * 180;
            starPositions[i + 2] = (Math.random() - 0.5) * 250;
        }
        starGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
        
        const starMaterial = new THREE.PointsMaterial({ color: 0x00f3ff, size: 0.9, transparent: true, opacity: 0.85 });
        const starField = new THREE.Points(starGeometry, starMaterial);
        scene.add(starField);

        const torusGeometry = new THREE.TorusKnotGeometry(6, 1.8, 100, 16);
        const musicCoreMaterial = new THREE.MeshBasicMaterial({ color: 0xff00ff, wireframe: true, transparent: true, opacity: 0.4 });
        const musicCore = new THREE.Mesh(torusGeometry, musicCoreMaterial);
        scene.add(musicCore);

        audioElement
        
