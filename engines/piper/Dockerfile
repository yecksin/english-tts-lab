FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir piper-tts fastapi "uvicorn[standard]"

# Varias voces en ingles (US/UK, hombre/mujer). curl -fL: -f falla si HTTP>=400
# (no guarda paginas de error), -L sigue redirects de Git LFS de HuggingFace.
RUN mkdir -p /models
ARG HF="https://huggingface.co/rhasspy/piper-voices/resolve/main/en"
RUN set -e; for V in \
      "en_US/lessac/medium/en_US-lessac-medium" \
      "en_US/ryan/medium/en_US-ryan-medium" \
      "en_GB/alba/medium/en_GB-alba-medium" \
      "en_GB/northern_english_male/medium/en_GB-northern_english_male-medium"; do \
      name=$(basename "$V"); \
      curl -fL -o "/models/$name.onnx"      "$HF/$V.onnx?download=true"; \
      curl -fL -o "/models/$name.onnx.json" "$HF/$V.onnx.json?download=true"; \
      python -c "import json,sys; json.load(open('/models/$name.onnx.json'))"; \
      test -s "/models/$name.onnx"; \
    done

COPY server.py .
EXPOSE 5000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
