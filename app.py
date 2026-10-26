<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>3D Space Music Visualizer</title>
    <!-- นำเข้า Google Fonts และ FontAwesome สำหรับไอคอน -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Prompt:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #000;
            font-family: 'Prompt', sans-serif;
        }

        /* จัดหน้าจอแนวตั้งสไตล์ TikTok / Reels / Shorts */
        .app-container {
            position: relative;
            width: 100%;
            max-width: 450px;
            height: 100vh;
            margin: 0 auto;
            background: #05020a;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.2);
        }

        #canvas-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        /* เลเยอร์ UI ด้านบน */
        .ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 30px 20px;
            pointer-events: none;
        }

        .ui-layer > * {
            pointer-events: auto;
        }

        /* ส่วนหัว / โลโก้ & ตัวหนังสือวิ้งแรงๆ */
        .header-section {
            text-align: center;
            margin-top: 10px;
        }

        .logo-wrapper {
            width: 70px;
            height: 70px;
            margin: 0 auto 10px auto;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid #00f3ff;
            box-shadow: 0 0 15px #00f3ff, inset 0 0 15px #00f3ff;
            animation: pulse-logo 2s infinite alternate;
        }

        .logo-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        @keyframes pulse-logo {
            0% { transform: scale(1); box-shadow: 0 0 10px #00f3ff; }
            100% { transform: scale(1.05); box-shadow: 0 0 25px #ff00ff; }
        }

        .neon-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 24px;
            font-weight: 900;
            color: #fff;
            text-transform: uppercase;
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #00f3ff, 0 0 40px #00f3ff, 0 0 80px #00f3ff;
            animation: neon-glow 1.5s ease-in-out infinite alternate;
            position: relative;
        }

        /* แสงวิ่งผ่านตัวหนังสือ */
        .neon-title::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            color: #ff00ff;
            z-index: 1;
            overflow: hidden;
            white-space: nowrap;
            clip-path: polygon(0 0, 0 100%, 0 100%, 0 0);
            animation: shine-sweep 3s ease-in-out infinite;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        }

        @keyframes neon-glow {
            0% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #00f3ff, 0 0 40px #00f3ff; }
            100% { text-shadow: 0 0 2px #fff, 0 0 5px #fff, 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #ff00ff; }
        }

        @keyframes shine-sweep {
            0% { clip-path: polygon(0 0, 0 100%, 10% 100%, 0 0); }
            50% { clip-path: polygon(90% 0, 100% 100%, 100% 100%, 90% 0); }
            100% { clip-path: polygon(0 0, 0 100%, 10% 100%, 0 0); }
        }

        .subtitle {
            font-size: 12px;
            color: #a0a0c0;
            margin-top: 4px;
            letter-spacing: 2px;
            text-shadow: 0 0 5px rgba(0,243,255,0.5);
        }

        /* กราฟเสียงตอบสนองเพลงจริง (Visualizer Canvas) */
        .visualizer-container {
            width: 100%;
            height: 80px;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 4px;
            padding: 0 20px;
        }

        .bar {
            flex: 1;
            background: linear-gradient(to top, #00f3ff, #ff00ff);
            border-radius: 3px 3px 0 0;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            transition: height 0.05s ease;
            height: 5px;
        }

        /* เครื่องเล่นเพลง */
        .player-panel {
            background: rgba(15, 10, 30, 0.7);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(0, 243, 255, 0.3);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), inset 0 0 15px rgba(0, 243, 255, 0.1);
            margin-bottom: 10px;
        }

        .track-info {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .track-thumb {
            width: 45px;
            height: 45px;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #ff00ff;
            margin-right: 12px;
            flex-shrink: 0;
        }

        .track-thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .track-meta {
            overflow: hidden;
        }

        .track-name {
            font-size: 14px;
            font-weight: 600;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-shadow: 0 0 5px rgba(255,255,255,0.5);
        }

        .track-artist {
            font-size: 11px;
            color: #00f3ff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* แถบเวลา */
        .progress-area {
            margin-bottom: 15px;
        }

        .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #00f3ff, #ff00ff);
            border-radius: 3px;
            box-shadow: 0 0 10px #00f3ff;
        }

        .time-stamps {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #8888aa;
            margin-top: 5px;
        }

        /* ปุ่มควบคุมเครื่องเล่น */
        .controls {
            display: flex;
            align-items: center;
            justify-content: space-around;
        }

        .btn-control {
            background: none;
            border: none;
            color: #fff;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.2s;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        }

        .btn-control:hover {
            color: #00f3ff;
            transform: scale(1.1);
        }

        .btn-play-pause {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00f3ff, #ff00ff);
            border: none;
            color: #fff;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(255, 0, 255, 0.6);
            transition: transform 0.2s;
        }

        .btn-play-pause:hover {
            transform: scale(1.08);
        }

        .btn-control.active {
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff;
        }

        /* ปุ่มเริ่มทำงานเสียงครั้งแรก (ปลดล็อค AudioContext) */
        #start-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(5, 2, 10, 0.95);
            z-index: 100;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
            transition: opacity 0.5s ease;
        }

        #start-overlay h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 22px;
            color: #00f3ff;
            margin-bottom: 15px;
            text-shadow: 0 0 15px #00f3ff;
        }

        #start-overlay p {
            color: #b0b0d0;
            font-size: 13px;
            margin-bottom: 25px;
            line-height: 1.5;
        }

        .btn-start {
            background: linear-gradient(135deg, #00f3ff, #ff00ff);
            border: none;
            color: #fff;
            padding: 14px 35px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(0, 243, 255, 0.6);
            font-family: 'Prompt', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: transform 0.2s;
        }

        .btn-start:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <div class="app-container">
        <!-- หน้าจอเริ่มระบบเพื่อให้ Browser อนุญาตเล่นเสียง -->
        <div id="start-overlay">
            <h1>CYBERPUNK SPACE MUSIC</h1>
            <p>สัมผัสประสบการณ์ภาพ 3 มิติ โลโก้อณูแสง และกราฟเสียงตอบสนองแบบเรียลไทม์</p>
            <button class="btn-start" id="btn-start-app"><i class="fa-solid fa-play"></i> เริ่มต้นใช้งาน</button>
        </div>

        <!-- ฉาก 3 มิติ (Three.js) -->
        <div id="canvas-container"></div>

        <!-- เลเยอร์ UI -->
        <div class="ui-layer">
            <!-- หัวข้อและโลโก้ -->
            <div class="header-section">
                <div class="logo-wrapper">
                    <img src="logo1.jpg" alt="Logo" onerror="this.src='https://via.placeholder.com/70/00f3ff/000000?text=LOGO'">
                </div>
                <h1 class="neon-title" data-text="COSMIC BEAT">COSMIC BEAT</h1>
                <div class="subtitle">NEBULA 3D EXPERIENCE</div>
            </div>

            <!-- กราฟเสียง (Audio Visualizer) -->
            <div class="visualizer-container" id="visualizer">
                <!-- แถบกราฟเสียงจะถูกสร้างด้วย JS -->
            </div>

            <!-- เครื่องเล่นเพลง -->
            <div class="player-panel">
                <div class="track-info">
                    <div class="track-thumb">
                        <img src="logo1.jpg" alt="Track Art" onerror="this.src='https://via.placeholder.com/45/ff00ff/ffffff?text=TRK'">
                    </div>
                    <div class="track-meta">
                        <div class="track-name" id="track-title">Cybernetic Universe</div>
                        <div class="track-artist" id="track-artist">Synthwave Future Mix</div>
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
                    <button class="btn-control" id="btn-loop" title="เล่นซ้ำ / เล่นต่อเนื่อง"><i class="fa-solid fa-rotate-right"></i></button>
                    <button class="btn-control" id="btn-prev" title="เพลงก่อนหน้า"><i class="fa-solid fa-backward-step"></i></button>
                    <button class="btn-play-pause" id="btn-play"><i class="fa-solid fa-play" id="play-icon"></i></button>
                    <button class="btn-control" id="btn-next" title="เพลงถัดไป"><i class="fa-solid fa-forward-step"></i></button>
                    <button class="btn-control" id="btn-shuffle" title="สุ่มเพลง"><i class="fa-solid fa-shuffle"></i></button>
                </div>
            </div>
        </div>
    </div>

    <!-- โหลด Three.js และ GSAP สำหรับเอฟเฟกต์อนุภาคและการเคลื่อนไหว -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

    <script>
        // รายการเพลย์ลิสต์ (เพลงตัวอย่างลิขสิทธิ์ฟรี / Audio Streams)
        const playlist = [
            {
                title: "Cybernetic Universe",
                artist: "Synthwave Future Mix",
                src: "https://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg"
            },
            {
                title: "Starlight Nebula",
                artist: "Deep Space Audio",
                src: "https://commondatastorage.googleapis.com/codeskulptor-assets/Music/odin-point_blank.mp3"
            },
            {
                title: "Neon Gravity",
                artist: "Vector Beam",
                src: "https://commondatastorage.googleapis.com/codeskulptor-assets/soundscapes/soundscape-night.mp3"
            }
        ];

        let currentTrackIndex = 0;
        let isPlaying = false;
        let isLooping = true;
        let isShuffling = false;

        // Audio & Visualizer Setup
        const audioElement = new Audio();
        audioElement.crossOrigin = "anonymous";
        audioElement.src = playlist[currentTrackIndex].src;
        audioElement.loop = false;

        let audioCtx, analyser, sourceNode, dataArray;
        let bassFactor = 1.0;

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

        // สร้างกราฟเสียง (Visualizer Bars)
        const visualizerContainer = document.getElementById('visualizer');
        const numBars = 16;
        const bars = [];
        for (let i = 0; i < numBars; i++) {
            const bar = document.createElement('div');
            bar.className = 'bar';
            visualizerContainer.appendChild(bar);
            bars.push(bar);
        }

        // --- THREE.JS 3D SPACE SCENE ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x05020a, 0.015);

        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 50;

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // 1. ดาวพุ่งเข้าหากล้อง (Starfield)
        const starCount = 800;
        const starGeometry = new THREE.BufferGeometry();
        const starPositions = new Float32Array(starCount * 3);

        for (let i = 0; i < starCount * 3; i += 3) {
            starPositions[i] = (Math.random() - 0.5) * 200;
            starPositions[i + 1] = (Math.random() - 0.5) * 200;
            starPositions[i + 2] = (Math.random() - 0.5) * 300;
        }
        starGeometry.setAttribute('
