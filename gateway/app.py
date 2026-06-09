import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

KOKORO_URL = os.getenv("KOKORO_URL", "http://kokoro:8880")
PIPER_URL = os.getenv("PIPER_URL", "http://piper:5000")

# Catalogo de motores y voces en ingles. Cada voz: {"id": <valor real>, "label": <texto>}.
ENGINES = {
    "kokoro": {
        "label": "Kokoro — natural (recomendado)",
        "voices": [
            {"id": "af_heart", "label": "US ♀ Heart"},
            {"id": "af_bella", "label": "US ♀ Bella"},
            {"id": "af_nicole", "label": "US ♀ Nicole"},
            {"id": "af_sarah", "label": "US ♀ Sarah"},
            {"id": "af_sky", "label": "US ♀ Sky"},
            {"id": "af_aoede", "label": "US ♀ Aoede"},
            {"id": "am_michael", "label": "US ♂ Michael"},
            {"id": "am_adam", "label": "US ♂ Adam"},
            {"id": "am_echo", "label": "US ♂ Echo"},
            {"id": "am_liam", "label": "US ♂ Liam"},
            {"id": "bf_emma", "label": "UK ♀ Emma"},
            {"id": "bf_isabella", "label": "UK ♀ Isabella"},
            {"id": "bf_alice", "label": "UK ♀ Alice"},
            {"id": "bm_george", "label": "UK ♂ George"},
            {"id": "bm_lewis", "label": "UK ♂ Lewis"},
            {"id": "bm_daniel", "label": "UK ♂ Daniel"},
        ],
    },
    "piper": {
        "label": "Piper — ultraligero / rapido",
        "voices": [
            {"id": "lessac", "label": "US ♀ Lessac"},
            {"id": "ryan", "label": "US ♂ Ryan"},
            {"id": "alba", "label": "UK ♀ Alba"},
            {"id": "northern_male", "label": "UK ♂ Northern"},
        ],
    },
}

app = FastAPI(title="TTS Lab")


class TTSReq(BaseModel):
    engine: str
    text: str
    voice: str | None = None


@app.get("/api/engines")
def engines():
    return ENGINES


@app.post("/api/tts")
async def tts(r: TTSReq):
    if r.engine not in ENGINES:
        raise HTTPException(400, "engine desconocido")
    if not r.text.strip():
        raise HTTPException(400, "texto vacio")

    async with httpx.AsyncClient(timeout=180) as c:
        if r.engine == "kokoro":
            voice = r.voice or "af_heart"
            resp = await c.post(
                f"{KOKORO_URL}/v1/audio/speech",
                json={
                    "model": "kokoro",
                    "input": r.text,
                    "voice": voice,
                    "response_format": "wav",
                },
            )
        else:  # piper
            resp = await c.post(f"{PIPER_URL}/tts", json={"text": r.text, "voice": r.voice})

    if resp.status_code != 200:
        raise HTTPException(502, f"{r.engine} fallo: {resp.text[:200]}")
    return Response(content=resp.content, media_type="audio/wav")


# El front estatico se sirve en la raiz (debe ir despues de las rutas /api).
app.mount("/", StaticFiles(directory="static", html=True), name="static")
