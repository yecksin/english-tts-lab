FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir piper-tts fastapi "uvicorn[standard]"

# Voz en ingles (US, calidad media). Se descarga con curl -fL:
#  -f = falla si HTTP >=400 (no guarda paginas de error como si fueran el modelo)
#  -L = sigue redirects (necesario para los archivos de Git LFS de HuggingFace)
RUN mkdir -p /models && \
    curl -fL -o /models/en_US-lessac-medium.onnx \
      "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx?download=true" && \
    curl -fL -o /models/en_US-lessac-medium.onnx.json \
      "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json?download=true" && \
    python -c "import json; json.load(open('/models/en_US-lessac-medium.onnx.json')); print('config OK')" && \
    test -s /models/en_US-lessac-medium.onnx

COPY server.py .
EXPOSE 5000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
