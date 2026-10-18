# SYNAPSE NEON MUSIC PLAYER — Streamlit
from pathlib import Path
import base64, html, json, mimetypes
import streamlit as st
import streamlit.components.v1 as components

EXTS={'.mp3','.wav','.ogg','.m4a','.aac','.opus','.flac'}

def _track(item):
    try:
        if isinstance(item,dict):
            title=item.get('title') or item.get('name') or item.get('ชื่อเพลง') or 'เพลงไม่มีชื่อ'
            url=item.get('url') or item.get('src')
            if url: return {'title':str(title),'src':str(url)}
            item=item.get('path') or item.get('file_path') or item.get('file') or item.get('audio') or item.get('uploaded_file') or item.get('data')
            if item is None:return None
        if isinstance(item,(str,Path)):
            p=Path(item)
            if not p.is_file() or p.suffix.lower() not in EXTS:return None
            name=p.name; raw=p.read_bytes()
        elif isinstance(item,(bytes,bytearray)):
            name='เพลง.mp3';raw=bytes(item)
        elif hasattr(item,'getvalue'):
            name=getattr(item,'name','เพลง.mp3');raw=item.getvalue()
        elif hasattr(item,'read'):
            name=getattr(item,'name','เพลง.mp3')
            try:item.seek(0)
            except Exception:pass
            raw=item.read()
            try:item.seek(0)
            except Exception:pass
        else:return None
        mime=mimetypes.guess_type(name)[0] or 'audio/mpeg'
        return {'title':Path(name).stem,'src':'data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii')}
    except Exception:return None

def _find_tracks(songs=None, folder='.'):
    items=[]
    if songs is not None: items.extend(list(songs) if isinstance(songs,(list,tuple)) else [songs])
    root=Path(folder); seen_paths=set()
    for d in (root,root/'music',root/'songs',root/'audio'):
        if d.is_dir():
            for p in sorted(d.iterdir(),key=lambda x:x.name.casefold()):
                if p.is_file() and p.suffix.lower() in EXTS and str(p.resolve()) not in seen_paths:
                    seen_paths.add(str(p.resolve()));items.append(p)
    tracks=[];seen=set()
    for item in items:
        t=_track(item)
        if t and t['src']:
            key=(t['title'],len(t['src']))
            if key not in seen:seen.add(key);tracks.append(t)
    return tracks

def render_music_player(songs=None, logo_path='logo1.jpg', title='SYNAPSE', folder='.'):
    st.markdown('''<style>.stApp{background:radial-gradient(ellipse at 8% 12%,#00c4ff20,transparent 32%),radial-gradient(ellipse at 94% 32%,#ec00ff1e,transparent 30%),linear-gradient(135deg,#030611,#080c20 52%,#090416)}.synapse-title{text-align:center;font-size:clamp(28px,5vw,48px);font-weight:950;letter-spacing:3px;color:#fff;text-shadow:0 0 8px #00eaff,0 0 22px #007bff,0 0 38px #e500ff}.synapse-sub{text-align:center;color:#9cfaff;letter-spacing:3px;font-size:12px;margin-bottom:1rem}</style>''',unsafe_allow_html=True)
    logo=Path(logo_path)
    if logo.is_file():
        a,b,c=st.columns([1,2,1])
        with b:st.image(str(logo),use_container_width=True)
    else:st.warning(f'ไม่พบ {logo_path} — วาง logo1.jpg ไว้โฟลเดอร์เดียวกับ app.py')
    st.markdown(f'<div class="synapse-title">{html.escape(title)}</div><div class="synapse-sub">SOUND & VISUAL THERAPY • NEON AUDIO EXPERIENCE</div>',unsafe_allow_html=True)
    tracks=_find_tracks(songs,folder)
    if not tracks:
        st.error('ยังไม่พบไฟล์เพลง กรุณาวางไฟล์ MP3 ไว้โฟลเดอร์เดียวกับ app.py หรือในโฟลเดอร์ music/')
        st.code('from music import render_music_player\nrender_music_player(logo_path="logo1.jpg")',language='python');return
    payload=json.dumps(tracks,ensure_ascii=False).replace('</','<\\/')
    template=r'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{color-scheme:dark;--cyan:#00eaff;--pink:#ff22d6;--violet:#863dff}*{box-sizing:border-box}body{margin:0;background:transparent;color:#f5f8ff;font-family:Arial,"Noto Sans Thai",sans-serif}.panel{position:relative;overflow:hidden;padding:19px;border-radius:24px;border:1px solid #00eaff9c;background:radial-gradient(ellipse at 0 0,#152c65,transparent 42%),radial-gradient(ellipse at 100% 100%,#3a124e,transparent 45%),linear-gradient(145deg,#030714,#080d20 60%,#100719);box-shadow:0 0 18px #00d9ff36,inset 0 0 28px #8c37ff1b}.inner{position:relative;z-index:1}.top{display:flex;align-items:center;gap:9px;margin-bottom:14px}.live{width:10px;height:10px;background:#67ffbd;border-radius:50%;box-shadow:0 0 12px #67ffbd;animation:blink 1.3s infinite alternate}@keyframes blink{to{opacity:.35}}.brand{font-size:11px;letter-spacing:2px;color:#9afaff;font-weight:900}.status{margin-left:auto;font-size:10px;color:#aab8d9}.layout{display:grid;grid-template-columns:minmax(0,1fr);gap:15px}.nowbox{border:1px solid #863dff88;border-radius:18px;padding:15px;background:#080b1bc9}.eyebrow{font-size:10px;letter-spacing:2px;color:#ff82eb;margin-bottom:8px}.song{font-size:clamp(19px,4vw,27px);font-weight:900;line-height:1.35;overflow-wrap:anywhere;text-shadow:0 0 8px #00dfff,0 0 20px #743aff}.subline{text-align:center;font-size:11px;color:#9cadd2;margin-top:7px}.visual{height:88px;display:flex;align-items:center;justify-content:center;gap:4px;margin:10px 0 13px}.bar{width:4px;height:var(--h);max-height:78px;border-radius:8px;background:linear-gradient(0deg,#783bff,#00f0ff,#ff32d7);box-shadow:0 0 10px #00dfff;animation:beat var(--speed) ease-in-out infinite alternate;animation-play-state:paused}.playing .bar{animation-play-state:running}@keyframes beat{from{transform:scaleY(.22);opacity:.5}to{transform:scaleY(1);opacity:1}}.seek{width:100%;accent-color:#00eaff;filter:drop-shadow(0 0 4px #00eaff)}.times{display:flex;justify-content:space-between;color:#9badd2;font-size:11px}.controls{display:flex;justify-content:center;align-items:center;gap
:12px;flex-wrap:wrap;margin:16px 0}button{cursor:pointer;color:white;border:1px solid #00eaff9c;background:linear-gradient(135deg,#101a3a,#16102d);border-radius:14px;padding:10px 13px;transition:.2s}button:hover{border-color:#ff27d8;box-shadow:0 0 17px #ff27d855}.mainbtn{width:58px;height:58px;border-radius:50%;font-size:22px;background:linear-gradient(135deg,#00cfff,#763dff 60%,#ed28d5);box-shadow:0 0 18px #00cfff77}.opts{display:grid;grid-template-columns:1fr 1fr;gap:10px}label{display:block;color:#9badd2;font-size:10px;letter-spacing:1px;margin:0 0 6px 3px}select{width:100%;padding:10px;color:#fff;background:#0c1430;border:1px solid #00dfff86;border-radius:12px}.vol{display:flex;align-items:center;gap:10px;margin:14px 0;color:#aab9d8;font-size:12px}.vol input{flex:1;accent-color:#ff27d8}.listhead{display:flex;justify-content:space-between;color:#91faff;font-weight:900;font-size:11px;letter-spacing:2px;margin:17px 0 8px}.search{width:100%;padding:10px 12px;border-radius:12px;border:1px solid #753fff9c;background:#080d20;color:white;margin-bottom:9px}.playlist{display:flex;flex-direction:column;gap:6px;max-height:230px;overflow:auto}.track{display:flex;align-items:center;gap:10px;width:100%;text-align:left;padding:10px;border:1px solid #243259;background:#080e22;border-radius:11px}.track.active{border-color:#ff2bd6;background:#21113b;box-shadow:0 0 13px #ff27d52c}.num{min-width:23px;color:#00eaff;font-size:11px}.trackname{flex:1;overflow-wrap:anywhere;font-size:12px}.playingtag{font-size:9px;color:#ff7ce8}.mixer{border:1px solid #ff29d580;border-radius:17px;padding:14px;margin-top:14px;background:linear-gradient(120deg,#0a1024,#130a26)}.mixhead{font-size:12px;color:#ff8bf0;letter-spacing:3px;font-weight:900;margin-bottom:12px}.mixgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.mixitem{text-align:center;color:#aebcdb;font-size:10px}.mixitem input{width:100%;accent-color:#ff29d8}.mixval{color:#8cfaff;font-size:10px;margin-top:4px}.speakerrow{display:flex;justify-content:space-between;margin-top:10px
;color:#8cfaff;font-size:12px}.note{text-align:center;color:#667ba6;font-size:10px;margin-top:14px}@media(min-width:650px){.layout{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}}@media(max-width:420px){.panel{padding:12px}.opts{grid-template-columns:1fr}.controls{gap:7px}.mixgrid{gap:5px}}
</style></head><body><div class="panel" id="panel"><div class="inner"><div class="top"><span class="live"></span><span class="brand">SYNAPSE • SOUND & VISUAL THERAPY</span><span class="status" id="status">READY</span></div><div class="layout"><section class="nowbox"><div class="eyebrow">♫ NOW PLAYING / กำลังเล่น</div><div class="song" id="songTitle">เตรียมเพลง...</div><div class="subline" id="counter"></div><div class="visual" id="visual"></div><audio id="audio" preload="metadata"></audio><input class="seek" id="seek" type="range" min="0" max="1000" value="0"><div class="times"><span id="elapsed">0:00</span><span id="duration">0:00</span></div><div class="controls"><button id="prev">⏮</button><button class="mainbtn" id="toggle">▶</button><button id="next">⏭</button><button id="restart">↻</button></div><div class="opts"><div><label for="mode">PLAY MODE • โหมดเล่น</label><select id="mode"><option value="continuous">▶ ต่อเนื่องตามลำดับ</option><option value="shuffle">
🔀 สุ่มเพลงต่อเนื่อง</option><option value="single">■ เพลงเดียวแล้วหยุด</option><option value="repeat">🔁 วนเพลงเดิม</option></select></div><div><label for="pick">SELECT TRACK • เลือกเพลง</label><select id="pick"></select></div></div><div class="vol"><span>🔊</span><span>VOLUME</span><input id="volume" type="range" min="0" max="100" value="80"><span id="volvalue">80%</span></div></section><section><div class="listhead"><span>♫ PLAYLIST</span><span id="total"></span></div><input class="search" id="search" placeholder="⌕ ค้นหาชื่อเพลง..." autocomplete="off"><div class="playlist" id="playlist"></div><div class="mixer"><div class="mixhead">〰 NEON MIXER</div><div class="mixgrid"><div class="mixitem">BASS<input id="bass" type="range" min="0" max="100" value="65"><div class="mixval" id="bassval">65%</div></div><div class="mixitem">MID<input id="mid" type="range" min="0" max="100" value="50"><div class="mixval" id="midval">50%</div></div><div class="mixitem">TREBLE<input id="treble" type="range" min="0" max="100" value="75"><div class="mixval" id="trebleval">75%</div></div><div class="mixitem">GLOW<input id="glow" type="range" min="0" max="100" value="80"><div class="mixval" id="glowval">80%</div></div></div><div class="speakerrow"><span>🔊 SPEAKER MODE</span><span id="speakerstate">NEON ON</span></div></div></section></div><div class="note">NEON AUDIO EXPERIENCE • เลือกเพลงแล้วกด ▶ เพื่อเริ่มฟัง</div></div></div><script>
const tracks=__TRACKS__;const $=id=>document.getElementById(id),audio=$('audio'),panel=$('panel');let index=0,seeking=false;for(let i=0;i<43;i++){let b=document.createElement('span');b.className='bar';b.style.setProperty('--h',(8+Math.abs(Math.sin(i*1.55))*70)+'px');b.style.setProperty('--speed',(.25+(i%9)*.075)+'s');b.style.animationDelay=(-i*.05)+'s';$('visual').appendChild(b)}function fmt(v){if(!Number.isFinite(v)||v<0)return'0:00';return Math.floor(v/60)+':'+String(Math.floor(v%60)).padStart(2,'0')}function status(t){$('status').textContent=t}function render(){$('pick').innerHTML='';tracks.forEach((t,i)=>{let o=document.createElement('option');o.value=i;o.textContent=(i+1)+'. '+t.title;$('pick').appendChild(o)});$('total').textContent=tracks.length+' TRACKS';drawList()}function drawList(){let q=$('search').value.trim().toLocaleLowerCase();$('playlist').innerHTML='';tracks.forEach((t,i)=>{if(q&&!t.title.toLocaleLowerCase().includes(q))return;let b=document.createElement('button');b.className='track'+(i===index?' active':'');let n=document.createElement('span');n.className='num';n.textContent=String(i+1).padStart(2,'0');let name=document.createElement('span');name.className='trackname';name.textContent=t.title;let tag=document.createElement('span');tag.className='playingtag';tag.textContent=i===index?'NOW PLAYING':'▶';b.append(n,name,tag);b.addEventListener('click',()=>{load(i);play()});$('playlist').appendChild(b)})}function load(i,autoplay=false){index=(i+tracks.length)%tracks.length;audio.src=tracks[index].src;audio.load();$('songTitle').textContent=tracks[index].title;$('counter').textContent='TRACK '+(index+1)+' / '+tracks.length;$('pick').value=String(index);$('seek').value=0;$('elapsed').textContent='0:00';$('duration').textContent='0:00';drawList();if(autoplay)play();else{status('READY');$('toggle').textContent='▶';panel.classList.remove('playing')}}async function play(){try{await audio.play();$('toggle').textContent='Ⅱ';status('PLAYING');panel.classList.add('playing')}catch(e){status('กด ▶ เพื่อเล่น');
$('toggle').textContent='▶'}}function pause(){audio.pause();$('toggle').textContent='▶';status('PAUSED');panel.classList.remove('playing')}function next(){let m=$('mode').value;if(m==='single'){audio.pause();audio.currentTime=0;$('seek').value=0;$('toggle').textContent='▶';status('FINISHED');panel.classList.remove('playing');return}if(m==='repeat'){audio.currentTime=0;play();return}let n=index;if(m==='shuffle'&&tracks.length>1){do{n=Math.floor(Math.random()*tracks.length)}while(n===index)}else n=index+1;if(n>=tracks.length){if(m==='continuous')n=0;else{audio.pause();audio.currentTime=0;status('PLAYLIST END');panel.classList.remove('playing');return}}load(n,true)}$('toggle').onclick=()=>audio.paused?play():pause();$('prev').onclick=()=>load(index-1,true);$('next').onclick=next;$('restart').onclick=()=>{audio.currentTime=0;play()};$('pick').onchange=()=>load(Number($('pick').value),true);$('search').oninput=drawList;audio.onended=next;audio.ontimeupdate=()=>{if(!seeking&&audio.duration>0)$('seek').value=Math.round(audio.currentTime/audio.duration*1000);$('elapsed').textContent=fmt(audio.currentTime);$('duration').textContent=fmt(audio.duration)};$('seek').oninput=()=>seeking=true;$('seek').onchange=()=>{if(audio.duration>0)audio.currentTime=Number($('seek').value)/1000*audio.duration;seeking=false};$('volume').oninput=e=>{audio.volume=Number(e.target.value)/100;$('volvalue').textContent=e.target.value+'%'};audio.volume=.8;['bass','mid','treble','glow'].forEach(id=>$(id).oninput=e=>{$(id+'val').textContent=e.target.value+'%';if(id==='glow'){let v=Number(e.target.value)/100;panel.style.boxShadow='0 0 '+(8+v*24)+'px rgba(0,220,255,'+(v*.35)+'),inset 0 0 28px rgba(140,55,255,'+(v*.14)+')'}});render();load(0,false);
</script></body></html>'''
    components.html(template.replace('__TRACKS__',payload),height=1040,scrolling=True)

if __name__ == '__main__':
    st.set_page_config(page_title='SYNAPSE Music Player',page_icon='🎧',layout='wide')
    render_music_player(logo_path='logo1.jpg')
