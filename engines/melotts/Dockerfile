FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential && rm -rf /var/lib/apt/lists/*

# Torch CPU primero (evita bajar la build CUDA pesada).
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# MeloTTS + diccionario japones/unidic (lo pide su pipeline aunque usemos EN).
RUN pip install --no-cache-dir git+https://github.com/myshell-ai/MeloTTS.git
RUN python -m unidic download
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng'); nltk.download('cmudict')"

RUN pip install --no-cache-dir fastapi "uvicorn[standard]"
COPY server.py .
EXPOSE 5000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
