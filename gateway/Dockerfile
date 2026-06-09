FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" httpx
# Contexto de build = raíz del repo (ver docker-compose: build.context = .)
COPY gateway/app.py .
COPY gateway/static ./static
COPY AGENT.md ./AGENT.md
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
