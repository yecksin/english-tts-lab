FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential && rm -rf /var/lib/apt/lists/*

# 1) MeloTTS primero. OJO: su instalacion jala torch/torchaudio en version CUDA
#    desde PyPI (buscan libcudart.so y crashean en un VPS sin GPU).
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git

# 2) Diccionarios que pide su pipeline (no importan torchaudio, van bien aqui).
RUN python -m unidic download
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng'); nltk.download('cmudict')"

RUN pip install --no-cache-dir fastapi "uvicorn[standard]"

# 3) AHORA forzamos torch + torchaudio a la build CPU, PISANDO la version CUDA que
#    dejo MeloTTS. Este es el fix real: debe ir DESPUES de instalar MeloTTS.
RUN pip install --no-cache-dir --force-reinstall \
    torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 4) Guard: si torchaudio quedo en CUDA, esto FALLA en build (no en runtime).
RUN python -c "import torch, torchaudio; print('torch', torch.__version__, 'torchaudio', torchaudio.__version__, '-> CPU OK')"

COPY server.py .
EXPOSE 5000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
