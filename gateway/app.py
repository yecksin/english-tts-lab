import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

KOKORO_URL = os.getenv("KOKORO_URL", "http://kokoro:8880")
PIPER_URL = os.getenv("PIPER_URL", "http://piper:5000")
MELO_URL = os.getenv("MELO_URL", "http://melotts:5000")

# Catalogo de motores y voces en ingles disponibles para comparar.
ENGINES = {
    "kokoro": {
        "label": "Kokoro — natural (recomendado)",
        "voices": ["af_heart", "af_bella", "am_michael", "bm_george", "bf_emma"],
    },
    "piper": {
        "label": "Piper — ultraligero / rapido",
        "voices": ["lessac"],
    },
    # MeloTTS desactivado temporalmente (build CUDA inestable). Reactivar junto
    # con el servicio melotts en docker-compose.yml cuando quede estable:
    # "melotts": {
    #     "label": "MeloTTS — buena calidad en CPU",
    #     "voices": ["EN-US", "EN-BR", "EN-Default", "EN-AU"],
    # },
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
        elif r.engine == "piper":
            resp = await c.post(f"{PIPER_URL}/tts", json={"text": r.text})
        else:  # melotts
            resp = await c.post(
                f"{MELO_URL}/tts",
                json={"text": r.text, "voice": r.voice or "EN-US"},
            )

    if resp.status_code != 200:
        raise HTTPException(502, f"{r.engine} fallo: {resp.text[:200]}")
    return Response(content=resp.content, media_type="audio/wav")


# El front estatico se sirve en la raiz (debe ir despues de las rutas /api).
app.mount("/", StaticFiles(directory="static", html=True), name="static")
