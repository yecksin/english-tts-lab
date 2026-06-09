import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

KOKORO_URL = os.getenv("KOKORO_URL", "http://kokoro:8880")
PIPER_URL = os.getenv("PIPER_URL", "http://piper:5000")

# Donde se persiste la voz por defecto que Yeck fija desde el front.
DATA_DIR = os.getenv("DATA_DIR", "/data")
DEFAULT_FILE = os.path.join(DATA_DIR, "default_voice.json")
FALLBACK_DEFAULT = {"engine": "kokoro", "voice": "af_heart"}

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


def read_default() -> dict:
    try:
        with open(DEFAULT_FILE) as f:
            d = json.load(f)
        if d.get("engine") in ENGINES:
            return d
    except Exception:
        pass
    return FALLBACK_DEFAULT


def write_default(engine: str, voice: str) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DEFAULT_FILE, "w") as f:
        json.dump({"engine": engine, "voice": voice}, f)


class TTSReq(BaseModel):
    text: str
    engine: str | None = None   # si falta -> usa la voz por defecto
    voice: str | None = None


class DefaultReq(BaseModel):
    engine: str
    voice: str


@app.get("/api/engines")
def engines():
    return ENGINES


@app.get("/api/default-voice")
def get_default():
    return read_default()


@app.post("/api/default-voice")
def set_default(r: DefaultReq):
    if r.engine not in ENGINES:
        raise HTTPException(400, "engine desconocido")
    write_default(r.engine, r.voice)
    return {"ok": True, "engine": r.engine, "voice": r.voice}


@app.post("/api/tts")
async def tts(r: TTSReq):
    if not r.text.strip():
        raise HTTPException(400, "texto vacio")

    # Sin engine/voice -> usa la voz por defecto fijada desde el front.
    engine = r.engine
    voice = r.voice
    if not engine or not voice:
        d = read_default()
        engine = engine or d["engine"]
        voice = voice or (d["voice"] if engine == d["engine"] else None)

    if engine not in ENGINES:
        raise HTTPException(400, "engine desconocido")

    async with httpx.AsyncClient(timeout=180) as c:
        if engine == "kokoro":
            resp = await c.post(
                f"{KOKORO_URL}/v1/audio/speech",
                json={
                    "model": "kokoro",
                    "input": r.text,
                    "voice": voice or "af_heart",
                    "response_format": "wav",
                },
            )
        else:  # piper
            resp = await c.post(f"{PIPER_URL}/tts", json={"text": r.text, "voice": voice})

    if resp.status_code != 200:
        raise HTTPException(502, f"{engine} fallo: {resp.text[:200]}")
    return Response(content=resp.content, media_type="audio/wav")


# El front estatico se sirve en la raiz (debe ir despues de las rutas /api).
app.mount("/", StaticFiles(directory="static", html=True), name="static")
