from pathlib import Path
import base64
import mimetypes
import json
import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="3D Space Music Visualizer • TA101",
    page_icon="🌌",
    layout="centered"
)

# โฟลเดอร์หลัก
ROOT = Path(__file__).resolve().parent

# 1. ฟังก์ชันแปลงไฟล์เพลงเป็น Base64
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

# 2. ฟังก์ชันแปลงรูปโลโก้ logo1.jpg เป็น Base64 ป้องกันรูปไม่ขึ้น
logo_base64 = "https://via.placeholder.com/70/00f3ff/000000?text=LOGO"
logo_path = ROOT / "logo1.jpg"
if logo_path.exists():
    try:
        logo_mime = mimetypes.guess_type(logo_path.name)[0] or "image/jpeg"
        logo_encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        logo_base64 = f"data:{logo_mime};base64,{logo_encoded}"
    except OSError:
        pass

# 3. โค้ด HTML / CSS / 3D Three.js
player_html = r"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>3D Space Music Visualizer</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Prompt:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
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
            box-shadow: 0 0 35px rgba(0, 243, 255, 0.3);
        }

        #canvas-container {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        }

        .ui-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; z-index: 10;
            display: flex; flex-direction: column; justify-content: space-between;
            padding: 20px; pointer-events: none;
        }
        .ui-layer > * { pointer-events: auto; }

        .header-section { text-align: center; margin-top: 5px; }

        .logo-wrapper {
            width: 70px; height: 70px; margin: 0 auto 6px auto;
            border-radius: 50%; overflow: hidden;
            border: 2px solid #00f3ff;
            box-shadow: 0 0 20px #00f3ff, inset 0 0 15px #ff00ff;
            transition: transform 0.05s ease;
        }
        .logo-wrapper img {
            width: 100%; height: 100%; object-fit: cover;
            animation: spin-logo 8s linear infinite;
        }
        @keyframes spin-logo { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        /* ตัวหนังสือวิ้งนีออนค่อยๆ เปลี่ยนสีวนลูป */
        .neon-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 20px; font-weight: 900;
            text-transform: uppercase;
            animation: colorShift 6s ease-in-out infinite alternate, neon-glow 1.5s ease-in-out infinite alternate;
            position: relative;
        }
        @keyframes colorShift {
            0% { color: #00f3ff; text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff; }
            33% { color: #ff00ff; text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #ff00ff; }
            66% { color: #00ff66; text-shadow: 0 0 10px #00ff66, 0 0 20px #00ff66, 0 0 40px #00ff66; }
            100% { color: #00f3ff; text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff; }
        }
        @keyframes neon-glow {
            0% { transform: scale(1); }
            100% { transform: scale(1.03); }
        }

        .subtitle {
            font-size: 10px; color: #a0a0c0; margin-top: 2px; letter-spacing: 2px;
            text-shadow: 0 0 5px rgba(0,243,255,0.5);
        }

        .visualizer-container {
            width: 100%; height: 65px; display: flex; align-items: flex-end;
            justify-content: center; gap: 3px; padding: 0 10px;
        }
        .bar {
            flex: 1; background: linear-gradient(to top, #00f3ff, #ff00ff);
            border-radius: 4px 4px 0 0; box-shadow: 0 0 12px rgba(0, 243, 255, 0.7); height: 5px;
            transition: height 0.05s ease;
        }

        .player-panel {
            background: rgba(12, 8, 25, 0.85); backdrop-filter: blur(15px);
            border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 18px;
            padding: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.9), inset 0 0 15px rgba(0, 243, 255, 0.15);
            margin-bottom: 5px;
        }

        .track-info { display: flex; align-items: center; margin-bottom: 10px; }
        .track-thumb {
            width: 38px; height: 38px; border-radius: 8px; overflow: hidden;
            border: 1px solid #ff00ff; margin-right: 10px; flex-shrink: 0;
        }
        .track-thumb img { width: 100%; height: 100%; object-fit: cover; }
        .track-meta { overflow: hidden; }
        .track-name {
            font-size: 13px; font-weight: 600; color: #fff;
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            text-shadow: 0 0 5px rgba(255,255,255,0.5);
        }
        .track-artist { font-size: 10px; color: #00f3ff; }

        .progress-area { margin-bottom: 10px; }
        .progress-bar {
            width: 100%; height: 5px; background: rgba(255, 255, 255, 0.15);
            border-radius: 3px; cursor: pointer; position: relative; overflow: hidden;
        }
        .progress-fill {
            height: 100%; width: 0%; background: linear-gradient(90deg, #00f3ff, #ff00ff);
            border-radius: 3px; box-shadow: 0 0 10px #00f3ff;
        }
        .time-stamps {
            display: flex; justify-content: space-between; font-size: 9px; color: #8888aa; margin-top: 3px;
        }

        .controls { display: flex; align-items: center; justify-content: space-around; }
        .btn-control {
            background: none; border: none; color: #fff; font-size: 15px;
            cursor: pointer; transition: all 0.2s; text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        }
        .btn-control:hover { color: #00f3ff; transform: scale(1.15); }
        .btn-control.active { color: #ff00ff; text-shadow: 0 0 12px #ff00ff; }

        .btn-play-pause {
            width: 44px; height: 44px; border-radius: 50%;
            background: linear-gradient(135deg, #00f3ff, #ff00ff);
            border: none; color: #fff; font-size: 16px;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; box-shadow: 0 0 20px rgba(255, 0, 255, 0.7);
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
            font-family: 'Orbitron', sans-serif; font-size: 18px; color: #00f3ff;
            margin-bottom: 10px; text-shadow: 0 0 15px #00f3ff;
        }
        #start-overlay p { color: #b0b0d0; font-size: 11px; margin-bottom: 20px; line-height: 1.4; }
        .btn-start {
            background: linear-gradient(135deg, #00f3ff, #ff00ff);
            border: none; color: #fff; padding: 12px 30px; font-size: 14px;
            font-weight: 700; border-radius: 30px; cursor: pointer;
            box-shadow: 0 0 25px rgba(0, 243, 255, 0.7); font-family: 'Prompt', sans-serif;
            text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s;
        }
        .btn-start:hover { transform: scale(1.06); }
    </style>
</head>
<body>

    <div class="app-container">
        <div id="start-overlay">
            <h1>TA101 • NEON MUSIC 3D</h1>
            <p>แตะปุ่มด้านล่างเพื่อเริ่มสัมผัสภาพ 3 มิติ โลโก้กระแทกจังหวะ และเพลงต่อเนื่องอัตโนมัติ</p>
            <button class="btn-start" id="btn-start-app"><i class="fa-solid fa-play"></i> เริ่มต้นใช้งาน</button>
        </div>

        <div id="canvas-container"></div>

        <div class="ui-layer">
            <div class="header-section">
                <div class="logo-wrapper" id="logo-box">
                    <img src="__LOGO_BASE64__" alt="Logo">
                </div>
                <h1 class="neon-title">COSMIC BEAT</h1>
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
        const torusMaterial = new THREE.MeshBasicMaterial({ color: 0xff00ff, wireframe: true, transparent: true, opacity: 0.35 });
        const musicCore = new THREE.Mesh(torusGeometry, torusMaterial);
        scene.add(musicCore);

        audioElement.addEventListener('ended', () => {
            if (isShuffling) {
                currentTrackIndex = Math.floor(Math.random() * songs.length);
            } else if (isLooping && songs.length === 1) {
                audioElement.play();
                return;
            } else {
                currentTrackIndex = (currentTrackIndex + 1) % songs.length;
            }
            loadTrack(currentTrackIndex);
            audioElement.play();
        });

        audioElement.addEventListener('timeupdate', () => {
            if (audioElement.duration) {
                const progressPercent = (audioElement.currentTime / audioElement.duration) * 100;
                document.getElementById('progress-fill').style.width = progressPercent + '%';
                
                let curM = Math.floor(audioElement.currentTime / 60);
                let curS = Math.floor(audioElement.currentTime % 60);
                document.getElementById('current-time').innerText = curM + ":" + (curS < 10 ? '0' : '') + curS;

                let durM = Math.floor(audioElement.duration / 60);
                let durS = Math.floor(audioElement.duration % 60);
                document.getElementById('total-duration').innerText = durM + ":" + (durS < 10 ? '0' : '') + durS;
            }
        });

        document.getElementById('progress-bar').addEventListener('click', (e) => {
            const width = e.currentTarget.clientWidth;
            const clickX = e.offsetX;
            if (audioElement.duration) {
                audioElement.currentTime = (clickX / width) * audioElement.duration;
            }
        });

        document.getElementById('btn-start-app').addEventListener('click', () => {
            initAudioContext();
            document.getElementById('start-overlay').style.opacity = '0';
            setTimeout(() => { document.getElementById('start-overlay').style.display = 'none'; }, 500);
            audioElement.play();
            isPlaying = true;
            document.getElementById('play-icon').className = "fa-solid fa-pause";
        });

        const btnPlay = document.getElementById('btn-play');
        const playIcon = document.getElementById('play-icon');
        btnPlay.addEventListener('click', () => {
            initAudioContext();
            if (isPlaying) {
                audioElement.pause();
                isPlaying = false;
                playIcon.className = "fa-solid fa-play";
            } else {
                audioElement.play();
                isPlaying = true;
                playIcon.className = "fa-solid fa-pause";
            }
        });

        document.getElementById('btn-next').addEventListener('click', () => {
            currentTrackIndex = (currentTrackIndex + 1) % songs.length;
            loadTrack(currentTrackIndex);
            if (isPlaying) audioElement.play();
        });

        document.getElementById('btn-prev').addEventListener('click', () => {
            currentTrackIndex = (currentTrackIndex - 1 + songs.length) % songs.length;
            loadTrack(currentTrackIndex);
            if (isPlaying) audioElement.play();
        });

        const btnLoop = document.getElementById('btn-loop');
        btnLoop.addEventListener('click', () => {
            isLooping = !isLooping;
            btnLoop.classList.toggle('active', isLooping);
        });

        const btnShuffle = document.getElementById('btn-shuffle');
        btnShuffle.addEventListener('click', () => {
            isShuffling = !isShuffling;
            btnShuffle.classList.toggle('active', isShuffling);
        });

        function animate() {
            requestAnimationFrame(animate);

            const positions = starGeometry.attributes.position.array;
            for (let i = 2; i < starCount * 3; i += 3) {
                positions[i] += 0.6;
                if (positions[i] > 40) positions[i] = -210;
            }
            starGeometry.attributes.position.needsUpdate = true;
            starField.rotation.z += 0.0015;

            if (analyser && isPlaying) {
                analyser.getByteFrequencyData(dataArray);
                let bassValue = dataArray[2] / 255; 

                const logoBox = document.getElementById('logo-box');
                logoBox.style.transform = "scale(" + (1 + bassValue * 0.4) + ")";

                musicCore.rotation.x += 0.01 + (bassValue * 0.02);
                musicCore.rotation.y += 0.015 + (bassValue * 0.02);
                let coreScale = 1 + (bassValue * 0.45);
                musicCore.scale.set(coreScale, coreScale, coreScale);

                for (let i = 0; i < numBars; i++) {
                    const height = (dataArray[i] / 255) * 58 + 6;
                    bars[i].style.height = height + 'px';
                }
            } else {
                musicCore.rotation.x += 0.005;
                musicCore.rotation.y += 0.008;
            }

            renderer.render(scene, camera);
        }
        window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});
</script>
</body>
</html>
"""

# แทนที่ข้อมูลเพลงและรูปโลโก้ลงใน HTML
player_html = player_html.replace("__SONGS__", songs_json)
player_html = player_html.replace("__LOGO_BASE64__", logo_base64)

# เรนเดอร์หน้าเว็บทั้งหมดลงใน Streamlit
components.html(player_html, height=850, scrolling=False)


     
