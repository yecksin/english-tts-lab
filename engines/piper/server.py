import io
import wave

from fastapi import FastAPI
from fastapi.responses import Response
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


@app.post("/tts")
def tts(r: Req):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        voice.synthesize(r.text, wf)
    return Response(content=buf.getvalue(), media_type="audio/wav")


@app.get("/health")
def health():
    return {"ok": True}
