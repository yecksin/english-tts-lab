import io
import wave

from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
from piper import PiperVoice

app = FastAPI(title="Piper TTS")

voice = PiperVoice.load(
    "/models/en_US-lessac-medium.onnx",
    "/models/en_US-lessac-medium.onnx.json",
)


class Req(BaseModel):
    text: str
    voice: str | None = None


def _synth_to_wav(text: str) -> bytes:
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
    try:
        data = _synth_to_wav(r.text)
    except Exception as e:  # devuelve el error legible (no rompe el gateway)
        return JSONResponse(status_code=500, content={"error": f"{type(e).__name__}: {e}"})
    return Response(content=data, media_type="audio/wav")


@app.get("/health")
def health():
    return {"ok": True, "has_synthesize_wav": hasattr(voice, "synthesize_wav")}
