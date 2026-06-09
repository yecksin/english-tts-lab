import io
import wave

from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
from piper import PiperVoice

app = FastAPI(title="Piper TTS")

# id de voz -> archivo del modelo (deben coincidir con los descargados en el Dockerfile)
VOICE_FILES = {
    "lessac": "en_US-lessac-medium",
    "ryan": "en_US-ryan-medium",
    "alba": "en_GB-alba-medium",
    "northern_male": "en_GB-northern_english_male-medium",
}

# Carga todas las voces al inicio (son ~60MB c/u; sobra RAM en el VPS).
VOICES = {
    vid: PiperVoice.load(f"/models/{fn}.onnx", f"/models/{fn}.onnx.json")
    for vid, fn in VOICE_FILES.items()
}
DEFAULT = "lessac"


class Req(BaseModel):
    text: str
    voice: str | None = None


def _synth_to_wav(voice, text: str) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        # piper-tts 1.3+ usa synthesize_wav; versiones viejas usan synthesize.
        if hasattr(voice, "synthesize_wav"):
            voice.synthesize_wav(text, wf)
        else:
            voice.synthesize(text, wf)
    return buf.getvalue()


@app.post("/tts")
def tts(r: Req):
    voice = VOICES.get(r.voice or DEFAULT, VOICES[DEFAULT])
    try:
        data = _synth_to_wav(voice, r.text)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"{type(e).__name__}: {e}"})
    return Response(content=data, media_type="audio/wav")


@app.get("/health")
def health():
    return {"ok": True, "voices": list(VOICES.keys())}
