FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir piper-tts fastapi "uvicorn[standard]"

# Voz en ingles (US, calidad media). Se descarga en el build.
RUN mkdir -p /models
ADD https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx /models/en_US-lessac-medium.onnx
ADD https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json /models/en_US-lessac-medium.onnx.json

COPY server.py .
EXPOSE 5000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
