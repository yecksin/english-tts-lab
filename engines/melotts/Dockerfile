FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential && rm -rf /var/lib/apt/lists/*

# Torch + torchaudio CPU primero. torchaudio es CLAVE: si no se fija a CPU aqui,
# MeloTTS lo jala de PyPI en su version CUDA y crashea con
# "libcudart.so.13: cannot open shared object file" en un VPS sin GPU.
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# MeloTTS + diccionario japones/unidic (lo pide su pipeline aunque usemos EN).
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git
RUN python -m unidic download
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng'); nltk.download('cmudict')"

RUN pip install --no-cache-dir fastapi "uvicorn[standard]"

# Guard: si torchaudio quedo en version CUDA, esto FALLA aqui (en build), no en runtime.
RUN python -c "import torch, torchaudio; print('torch', torch.__version__, 'torchaudio', torchaudio.__version__, '-> CPU OK')"

COPY server.py .
EXPOSE 5000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
