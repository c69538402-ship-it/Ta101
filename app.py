<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TA101 NEON HI-FI MUSIC</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Prompt:wght@300;400;600&display=swap" rel="stylesheet">
    <!-- FontAwesome สำหรับไอคอน -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        body {
            font-family: 'Prompt', 'Orbitron', sans-serif;
            background: radial-gradient(circle at center, #1b0a3f 0%, #05020d 100%);
            color: #fff;
            overflow-x: hidden;
        (
        .neon-box {
            background: rgba(10, 5, 30, 0.75);
            border: 2px solid rgba(0, 243, 255, 0.4);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 15px rgba(189, 0, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 1.5rem;
        }
        .neon-text-cyan {
            color: #00f3ff;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.6);
        }
        .neon-text-pink {
            color: #ff007f;
            text-shadow: 0 0 10px rgba(255, 0, 127, 0.6);
        }
        .neon-button {
            background: linear-gradient(135deg, rgba(0,243,255,0.2), rgba(255,0,127,0.2));
            border: 1px solid #00f3ff;
            box-shadow: 0 0 10px rgba(0,243,255,0.4);
            transition: all 0.3s ease;
        }
        .neon-button:hover {
            background: linear-gradient(135deg, rgba(0,243,255,0.4), rgba(255,0,127,0.4));
            box-shadow: 0 0 20px rgba(0,243,255,0.8);
            transform: scale(1.05);
        }
        /* แถบ Equalizer จำลอง */
        .eq-bar {
            background: linear-gradient(to top, #ff007f, #00f3ff);
            box-shadow: 0 0 8px #00f3ff;
            animation: bounce 1.2s infinite ease-in-out alternate;
        }
        @keyframes bounce {
            0% { height: 20%; }
            100% { height: 95%; }
        }
    </style>
</head>
<body class="min-h-screen p-4 md:p-6 flex flex-col justify-between">

    <!-- ส่วนหัว (Header) -->
    <header class="flex justify-between items-center mb-6">
        <div class="flex items-center space-x-3">
            <div class="neon-button p-3 rounded-full text-cyan-400">
                <i class="fa-solid fa-headphones text-xl"></i>
            </div>
            <span class="text-xs tracking-widest text-green-400 font-semibold bg-green-950/60 px-3 py-1 rounded-full border border-green-500/40">
                ● LIVE MUSIC
            </span>
        </div>
        <div class="text-center">
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-wider font-['Orbitron'] neon-text-cyan">
                TA101 <span class="neon-text-pink">NEON HI-FI</span>
            </h1>
            <p class="text-xs tracking-widest text-purple-300">MUSIC • DREAM • TOGETHER</p>
        </div>
        <div class="neon-button px-4 py-2 rounded-full text-sm font-semibold flex items-center space-x-2 text-cyan-300">
            <i class="fa-solid fa-music"></i>
            <span>Now Playing</span>
        </div>
    </header>

    <!-- ส่วนเนื้อหาหลัก (Main Dashboard) -->
    <main class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center max-w-7xl mx-auto w-full">
        
        <!-- ซ้าย: โลโก้แผ่นเสียง / หูฟังเรืองแสง -->
        <div class="lg:col-span-4 flex flex-col items-center justify-center">
            <div class="relative w-64 h-64 md:w-72 md:h-72 rounded-full neon-box flex items-center justify-center p-4">
                <!-- วงแหวนหมุนจำลอง -->
                <div class="absolute inset-2 rounded-full border-2 border-dashed border-cyan-500/50 animate-[spin_20s_linear_infinite]"></div>
                <div class="absolute inset-6 rounded-full border border-pink-500/40"></div>
                <div class="text-center z-10">
                    <i class="fa-solid fa-headphones text-6xl md:text-7xl neon-text-pink mb-2"></i>
                    <h2 class="text-2xl font-black font-['Orbitron'] neon-text-cyan">TA101</h2>
                    <p class="text-xs text-purple-200 tracking-wider">NEON HI-FI</p>
                </div>
            </div>
        </div>

        <!-- กลาง: เครื่องเล่น + Equalizer + แผงควบคุม -->
        <div class="lg:col-span-5 flex flex-col space-y-4">
            <!-- แสดงชื่อเพลงและหลอดเวลา -->
            <div class="neon-box p-4">
                <div class="flex justify-between items-center mb-2">
                    <div class="flex items-center space-x-3">
                        <i class="fa-solid fa-music neon-text-cyan text-lg"></i>
                        <div>
                            <h3 id="song-title" class="font-semibold text-white text-sm md:text-base">ใส่ใจในเรื่องของ</h3>
                            <p id="artist-name" class="text-xs text-cyan-400">TA101</p>
                        </div>
                    </div>
                    <span id="time-display" class="text-xs font-mono text-gray-300">01:32 / 04:12</span>
                </div>
                <!-- Progress Bar -->
                <div class="w-full bg-gray-800 h-2 rounded-full overflow-hidden cursor-pointer relative">
                    <div id="progress-bar" class="bg-gradient-to-r from-cyan-400 to-pink-500 h-full w-[35%] rounded-full shadow-[0_0_10px_#00f3ff]"></div>
                </div>
            </div>

            <!-- Visualizer (Equalizer Bars จำลอง) -->
            <div class="neon-box p-4 h-28 flex items-end justify-between space-x-1">
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.1s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.4s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.2s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.6s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.3s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.5s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.1s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.7s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.2s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.4s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.6s;"></div>
                <div class="eq-bar w-full rounded-t" style="animation-delay: 0.3s;"></div>
            </div>

            <!-- ปุ่มควบคุมการเล่นเพลง (Play/Pause/Skip) -->
            <div class="flex items-center justify-center space-x-4 py-2">
                <button class="neon-button w-10 h-10 rounded-full flex items-center justify-center text-cyan-300 text-sm">
                    <i class="fa-solid fa-shuffle"></i>
                </button>
                <button class="neon-button w-12 h-12 rounded-full flex items-center justify-center text-cyan-300 text-lg">
                    <i class="fa-solid fa-backward-step"></i>
                </button>
                <button id="play-btn" class="w-16 h-16 rounded-full bg-gradient-to-tr from-cyan-500 to-pink-600 flex items-center justify-center text-white text-xl shadow-[0_0_20px_#ff007f] hover:scale-110 transition-transform">
                    <i id="play-icon" class="fa-solid fa-pause"></i>
                </button>
                <button class="neon-button w-12 h-12 rounded-full flex items-center justify-center text-cyan-300 text-lg">
                    <i class="fa-solid fa-forward-step"></i>
                </button>
                <button class="neon-button w-10 h-10 rounded-full flex items-center justify-center text-cyan-300 text-sm">
                    <i class="fa-solid fa-repeat"></i>
                </button>
            </div>
        </div>

        <!-- ขวา: รายการเพลย์ลิสต์ (Playlist) -->
        <div class="lg:col-span-3">
            <div class="neon-box p-4">
                <div class="flex justify-between items-center mb-3 border-b border-cyan-500/30 pb-2">
                    <div class="flex items-center space-x-2 text-cyan-300 font-semibold text-sm">
                        <i class="fa-solid fa-list"></i>
                        <span>Playlist</span>
                    </div>
                    <div class="flex space-x-2 text-xs text-gray-400">
                        <i class="fa-solid fa-shuffle cursor-pointer hover:text-cyan-400"></i>
                        <i class="fa-solid fa-repeat cursor-pointer hover:text-cyan-400"></i>
                    </div>
                </div>
                <!-- รายชื่อเพลงในเพลย์ลิสต์ -->
                <ul class="space-y-2 text-sm">
                    <li class="flex items-center justify-between p-2 rounded-lg bg-cyan-950/50 border border-cyan-500/40 text-cyan-300">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-play text-xs"></i>
                            <span class="truncate">ใส่ใจในเรื่องของ</span>
                        </div>
                    </li>
                    <li class="flex items-center justify-between p-2 rounded-lg hover:bg-purple-900/30 text-gray-300 cursor-pointer transition">
                        <div class="flex items-center space-x-2">
                            <span class="text-xs text-gray-500">2</span>
                            <span class="truncate">ทางของรอยยิ้ม</span>
                        </div>
                    </li>
                    <li class="flex items-center justify-between p-2 rounded-lg hover:bg-purple-900/30 text-gray-300 cursor-pointer transition">
                        <div class="flex items-center space-x-2">
                            <span class="text-xs text-gray-500">3</span>
                            <span class="truncate">4.mp3</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>

    </main>

    <!-- ส่วนล่าง: Equalizer sliders เล็กๆ และ Volume -->
    <footer class="max-w-7xl mx-auto w-full grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
        <!-- Equalizer แผงย่อย -->
        <div class="neon-box p-3 flex items-center justify-between overflow-x-auto space-x-4">
            <div class="flex items-center space-x-2">
                <i class="fa-solid fa-sliders neon-text-cyan text-sm"></i>
                <span class="text-xs font-semibold">Equalizer</span>
            </div>
            <!-- จำลองสไลเดอร์ความถี่ -->
            <div class="flex space-x-3 text-center text-[10px] text-gray-400">
                <div><input type="range" orient="vertical" class="w-12 h-16 accent-cyan-400 cursor-pointer" value="60"><br>60</div>
                <div><input type="range" orient="vertical" class="w-12 h-16 accent-cyan-400 cursor-pointer" value="50"><br>170</div>
                <div><input type="range" orient="vertical" class="w-12 h-16 accent-cyan-400 cursor-pointer" value="70"><br>310</div>
                <div><input type="range" orient="vertical" class="w-12 h-16 accent-cyan-400 cursor-pointer" value="40"><br>600</div>
                <div><input type="range" orient="vertical" class="w-12 h-16 accent-cyan-400 cursor-pointer" value="80"><br>1K</div>
                <div><input type="range" orient="vertical" class="w-12 h-16 accent-cyan-400 cursor-pointer" value="65"><br>3K</div>
            </div>
        </div>

        <!-- Volume & Bass/Treble ควบคุมเสียง -->
        <div class="neon-box p-3 flex items-center justify-around">
            <div class="text-center">
                <p class="text-[10px] text-gray-400 mb-1">Bass</p>
                <div class="w-10 h-10 rounded-full border border-cyan-400 flex items-center justify-center text-xs font-bold text-cyan-300 shadow-[0_0_5px_#00f3ff]">6 dB</div>
            </div>
            <div class="text-center">
                <p class="text-[10px] text-gray-400 mb-1">Treble</p>
                <div class="w-10 h-10 rounded-full border border-pink-400 flex items-center justify-center text-xs font-bold text-pink-400 shadow-[0_0_5px_#ff007f]">4 dB</div>
            </div>
            <div class="flex items-center space-x-2">
                <i class="fa-solid fa-volume-high text-cyan-400 text-sm"></i>
                <input type="range" class="w-24 accent-cyan-400 cursor-pointer" min="0" max="100" value="75">
                <span class="text-xs font-mono text-cyan-300">75%</span>
            </div>
        </div>
    </footer>

    <!-- JavaScript เบื้องต้นสำหรับการกดปุ่ม Play/Pause -->
    <script>
        const playBtn = document.getElementById('play-btn');
        const playIcon = document.getElementById('play-icon');
        let isPlaying = true;

        playBtn.addEventListener('click', () => {
            isPlaying = !isPlaying;
            if (isPlaying) {
                playIcon.classList.remove('fa-play');
                playIcon.classList.add('fa-pause');
            } else {
                playIcon.classList.remove('fa-pause');
                playIcon.classList.add('fa-play');
            }
        });
    </script>
</body>
</html>
