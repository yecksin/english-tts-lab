import os
import tempfile

from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from melo.api import TTS

app = FastAPI(title="MeloTTS")

# Carga el modelo en ingles una sola vez (CPU).
model = TTS(language="EN", device="cpu")
SPK = model.hps.data.spk2id  # ej: {'EN-US':.., 'EN-BR':.., 'EN-Default':.., 'EN-AU':..}


class Req(BaseModel):
    text: str
    voice: str | None = None


@app.post("/tts")
def tts(r: Req):
    sid = SPK.get(r.voice) if r.voice in SPK else list(SPK.values())[0]
    f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    f.close()
    try:
        model.tts_to_file(r.text, sid, f.name, speed=1.0)
        with open(f.name, "rb") as fh:
            data = fh.read()
    finally:
        os.unlink(f.name)
    return Response(content=data, media_type="audio/wav")


@app.get("/health")
def health():
    return {"ok": True, "voices": list(SPK.keys())}
