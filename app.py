import os
import streamlit as st

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="TA101 • NEON 3D MUSIC",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ซ่อน Header/Footer เพื่อความสมจริงแบบแอปเต็มจอ
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 1. ดึงไฟล์เพลง .mp3 จากหน้าหลัก (Root Directory) และจาก music.py โดยตรง
playlist = []

# ค้นหาไฟล์ .mp3 ที่อยู่ในโฟลเดอร์หลักปัจจุบัน
root_files = os.listdir(".")
for file in root_files:
  if file.lower().endswith(".mp3"):
    # แปลงชื่อไฟล์ให้เป็น URL ตรง (Streamlit / GitHub Raw หรือ Local Path)
    title = (
        file.replace(".mp3", "")
        .replace("ความไว้ใจที่ถูกแทง....", "ความไว้ใจที่ถูกแทง")
        .replace("หน้ากากของนางมาร...", "หน้ากากของนางมาร")
    )
    playlist.append({"title": title, "url": file})

# ดึงเพลงจาก music.py (ถ้ามี)
try:
  import music

  if hasattr(music, "songs"):
    for s in music.songs:
      if s not in [p["url"] for p in playlist]:
        playlist.append(
            {
                "title": (
                    s.split("/")[-1]
                    .replace(".mp3", "")
                    .replace("...", "")
                ),
                "url": s,
            }
        )
except Exception:
  pass

# หากยังหาเพลงไม่พบ ให้ใช้เพลงสำรอง
if not playlist:
  playlist = [
      {
          "title": "ทางของรอยยิ้ม",
          "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
      },
      {
          "title": "บักมรตื่นสาย",
          "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
      },
  ]

# Sidebar เลือกเพลงและปรับแต่งเสียง
st.sidebar.markdown(
    "<h2 style='color: #00ffff; text-align: center;'>🎚️ TA101 MIXER</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

selected_song_title = st.sidebar.selectbox(
    "📂 เลือกเพลงจากหน้าหลัก", [p["title"] for p in playlist]
)
selected_song = next(
    item for item in playlist if item["title"] == selected_song_title
)

st.sidebar.markdown("### 🎛️ ปรับแต่งเสียง (Audio FX)")
bass_boost = st.sidebar.slider("🔊 ดันเบสกระแทก (Bass Boost)", 0, 20, 10, 1)
treble_boost = st.sidebar.slider("✨ เสียงแหลมใส (Treble)", 0, 20, 8, 1)
volume_gain = st.sidebar.slider("🎚️ วอลุ่มหลัก (Gain)", 0.1, 2.0, 1.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align: center; color: #ff00ff; font-size: 12px;'>TA101 • NEON 3D V.2026</p>",
    unsafe_allow_html=True,
)

# 2. HTML + Three.js + Web Audio API (3D Space, Logo Explosion, Neon Visualizer)
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TA101 3D Music Player</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #020208;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        #canvas-container {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}
        .ui-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            pointer-events: none;
            padding: 20px;
            box-sizing: border-box;
        }}
        .interactive {{
            pointer-events: auto;
        }}
        .neon-title {{
            font-size: 26px;
            font-weight: 900;
            color: #fff;
            text-align: center;
            text-transform: uppercase;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #00ffff, 0 0 80px #00ffff;
            animation: textGlow 2s infinite alternate;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }}
        @keyframes textGlow {{
            0% {{ text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #00ffff; }}
            100% {{ text-shadow: 0 0 20px #00ffff, 0 0 30px #ff00ff, 0 0 50px #ff00ff; }}
        }}
        .player-card {{
            background: rgba(10, 10, 30, 0.75);
            border: 2px solid #00ffff;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.5), inset 0 0 15px rgba(255, 0, 255, 0.3);
            border-radius: 20px;
            padding: 15px 30px;
            display: flex;
            flex-direction: column;
            align-items: center;
            backdrop-filter: blur(10px);
            margin-bottom: 10px;
            max-width: 500px;
            width: 100%;
        }}
        .song-info {{
            color: #00ffff;
            font-size: 17px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 0 0 8px #00ffff;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
        }}
        audio {{
            width: 100%;
            outline: none;
            filter: drop-shadow(0 0 8px #ff00ff);
        }}
        .controls-row {{
            display: flex;
            gap: 12px;
            margin-top: 10px;
        }}
        .neon-btn {{
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            border: none;
            color: white;
            padding: 8px 16px;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 15px #ff00ff;
            transition: 0.3s;
            text-transform: uppercase;
            font-size: 12px;
        }}
        .neon-btn:hover {{
            transform: scale(1.1);
            box-shadow: 0 0 25px #00ffff, 0 0 25px #ff00ff;
        }}
    </style>
    <!-- โหลด Three.js และ GSAP -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
    <div id="canvas-container"></div>

    <div class="ui-overlay">
        <div class="interactive">
            <div class="neon-title">🌟 TA101 • NEON 3D MUSIC 🌟</div>
        </div>

        <div class="player-card interactive">
            <div class="song-info" id="songTitle">🎵 กำลังเล่น: {selected_song_title}</div>
            
            <audio id="audioPlayer" controls autoplay src="{selected_song['url']}"></audio>
            
            <div class="controls-row">
                <button class="neon-btn" onclick="prevSong()">⏮️ ก่อนหน้า</button>
                <button class="neon-btn" onclick="togglePlay()">⏯️ เล่น/หยุด</button>
                <button class="neon-btn" onclick="nextSong()">⏭️ ถัดไป</button>
                <button class="neon-btn" onclick="toggleExplosion()">💥 ระเบิดโลโก้</button>
            </div>
        </div>
    </div>

    <script>
        const playlist = {str(playlist).replace("'", '"')};
        let currentIndex = playlist.findIndex(p => p.title === "{selected_song_title}");
        if(currentIndex === -1) currentIndex = 0;

        const audio = document.getElementById('audioPlayer');
        audio.volume = {volume_gain};

        // เล่นเพลงถัดไปต่อเนื่องอัตโนมัติเมื่อเพลงจบ
        audio.onended = () => {{
            nextSong();
        }};

        function nextSong() {{
            currentIndex = (currentIndex + 1) % playlist.length;
            loadAndPlaySong(currentIndex);
        }}

        function prevSong() {{
            currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
            loadAndPlaySong(currentIndex);
        }}

        function togglePlay() {{
            if (audio.paused) {{ audio.play(); }} else {{ audio.pause(); }}
        }}

        function loadAndPlaySong(index) {{
            const song = playlist[index];
            audio.src = song.url;
            document.getElementById('songTitle').innerText = "🎵 กำลังเล่น: " + song.title;
            audio.play().catch(e => console.log("Auto-play prevented:", e));
        }}

        // --- THREE.JS 3D UNIVERSE & LOGO EXPLOSION ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x020208, 0.015);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 7;

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0xffffff, 1);
        scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0xff00ff, 3, 50);
        pointLight1.position.set(5, 5, 5);
        scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0x00ffff, 3, 50);
        pointLight2.position.set(-5, -5, 5);
        scene.add(pointLight2);

        // ดาวระยิบระยับรอบฉาก
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 1500;
        const starPositions = new Float32Array(starsCount * 3);
        for(let i = 0; i < starsCount * 3; i++) {{
            starPositions[i] = (Math.random() - 0.5) * 100;
        }}
        starsGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
        const starsMaterial = new THREE.PointsMaterial({{ color: 0x00ffff, size: 0.3, transparent: true, opacity: 0.8 }});
        const starField = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(starField);

        // โหลด logo1.jpg และสร้างเอฟเฟกต์แตกกระจาย (Explosion & Reassembly)
        const textureLoader = new THREE.TextureLoader();
        let logoMesh, logoParticles;
        let isExploded = false;

        textureLoader.load('logo1.jpg', (texture) => {{
            const geometry = new THREE.PlaneGeometry(3.5, 3.5, 32, 32);
            const material = new THREE.MeshStandardMaterial({{ 
                map: texture, 
                side: THREE.DoubleSide,
                roughness: 0.2,
                metalness: 0.8,
                emissive: 0x111133,
                emissiveMap: texture
            }});
            logoMesh = new THREE.Mesh(geometry, material);
            scene.add(logoMesh);

            const pGeometry = new THREE.BufferGeometry();
            const pCount = 800;
            const pPositions = new Float32Array(pCount * 3);

            for(let i = 0; i < pCount * 3; i += 3) {{
                let x = (Math.random() - 0.5) * 4;
                let y = (Math.random() - 0.5) * 4;
                let z = (Math.random() - 0.5) * 1;
                pPositions[i] = x;
                pPositions[i+1] = y;
                pPositions[i+2] = z;
            }}
            pGeometry.setAttribute('position', new THREE.BufferAttribute(pPositions, 3));
            
            const pMaterial = new THREE.PointsMaterial({{
                size: 0.12,
                map: texture,
                transparent: true,
                blending: THREE.AdditiveBlending
            }});
            logoParticles = new THREE.Points(pGeometry, pMaterial);
            scene.add(logoParticles);
        }}, undefined, (err) => {{
            const geo = new THREE.TorusGeometry(1.8, 0.4, 16, 100);
            const mat = new THREE.MeshStandardMaterial({{ color: 0xff00ff, roughness: 0.1, metalness: 0.9 }});
            logoMesh = new THREE.Mesh(geo, mat);
            scene.add(logoMesh);
        }});

        // ฟังก์ชันระเบิดและรวมร่างต่อเนื่อง
        function toggleExplosion() {{
            if (!logoMesh) return;
            isExploded = !isExploded;
            
            if (isExploded) {{
                gsap.to(logoMesh.scale, {{ x: 0.01, y: 0.01, z: 0.01, duration: 0.8, ease: "power2.in" }});
                if(logoParticles) {{
                    const pos = logoParticles.geometry.attributes.position.array;
                    for(let i = 0; i < pos.length; i += 3) {{
                        gsap.to(pos, {{
                            [i]: pos[i] * (Math.random() * 5 + 2),
                            [i+1]: pos[i+1] * (Math.random() * 5 + 2),
                            [i+2]: pos[i+2] * (Math.random() * 5 + 2),
                            duration: 1,
                            onUpdate: () => logoParticles.geometry.attributes.position.needsUpdate = true
                        }});
                    }}
                }}
            }} else {{
                gsap.to(logoMesh.scale, {{ x: 1, y: 1, z: 1, duration: 1.2, ease: "elastic.out(1, 0.5)" }});
                if(logoParticles) {{
                    const pos = logoParticles.geometry.attributes.position.array;
                    for(let i = 0; i < pos.length; i += 3) {{
                        pos[i] = (Math.random() - 0.5) * 4;
                        pos[i+1] = (Math.random() - 0.5) * 4;
                        pos[i+2] = (Math.random() - 0.5) * 1;
                        logoParticles.geometry.attributes.position.needsUpdate = true;
                    }}
                }}
            }}
        }}

        // --- Web Audio API (กราฟเสียงเด้งแรงตามจังหวะเพลงจริง) ---
        let audioCtx, analyser, dataArray;
        let isAudioInit = false;

        function initAudio() {{
            if (isAudioInit) return;
            try {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioCtx.createAnalyser();
                const source = audioCtx.createMediaElementSource(audio);
                
                const bassFilter = audioCtx.createBiquadFilter();
                bassFilter.type = 'lowshelf';
                bassFilter.frequency.value = 200;
                bassFilter.gain.value = {bass_boost};

                const trebleFilter = audioCtx.createBiquadFilter();
                trebleFilter.type = 'highshelf';
                trebleFilter.frequency.value = 3000;
                trebleFilter.gain.value = {treble_boost};

                source.connect(bassFilter);
                bassFilter.connect(trebleFilter);
                trebleFilter.connect(analyser);
                analyser.connect(audioCtx.destination);

                analyser.fftSize = 64;
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                isAudioInit = true;
            }} catch(e) {{
                console.log("Audio Context Error:", e);
            }}
        }}

        audio.addEventListener('play', () => {{
            initAudio();
            if(audioCtx && audioCtx.state === 'suspended') {{ audioCtx.resume(); }}
        }});

        let clock = new THREE.Clock();

        function animate() {{
            requestAnimationFrame(animate);
            let delta = clock.getDelta();

            starField.rotation.y += 0.0005;

            let bassValue = 1.0;
            if (isAudioInit && analyser) {{
                analyser.getByteFrequencyData(dataArray);
                let sum = 0;
                for(let i = 0; i < dataArray.length; i++) {{ sum += dataArray[i]; }}
                let avg = sum / dataArray.length;
                bassValue = 1.0 + (avg / 128) * 0.45; // แรงกระแทกตามจังหวะเพลง
            }}

            if (logoMesh && !isExploded) {{
                logoMesh.rotation.z += 0.005;
                logoMesh.scale.set(bassValue, bassValue, bassValue);
            }}

            if (logoParticles) {{
                logoParticles.rotation.y -= 0.003;
            }}

            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=680, scrolling=False)
