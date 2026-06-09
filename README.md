# 🎧 TTS Lab — comparador de voces en inglés (CPU)

Lab para probar varios modelos de **text-to-speech** en inglés y comparar cuál
suena mejor para practicar *listening*. Pensado para correr en un VPS **sin GPU**
(ej. Hostinger KVM 8: 8 vCPU / 32 GB). Todo es CPU.

## Qué trae

- **Kokoro** — voz más natural, ligera (recomendado). ~16 voces US/UK, hombre/mujer.
- **Piper** — ultraligero y rápido. 4 voces US/UK, hombre/mujer.
- **Front web** en `:8080` para escribir texto y comparar A/B (un solo puerto expuesto).

No expone API pública ni nada extra: solo el front interno detrás del gateway.

## Levantar en el VPS

```bash
# en el VPS (con Docker + compose instalados)
git clone <este-repo> tts-lab   # o sube la carpeta por scp
cd tts-lab
docker compose up -d --build
```

Luego abre: `http://IP_DEL_VPS:8080`

> El build es rápido: Kokoro usa imagen prearmada y Piper solo descarga 4 voces.

## Comandos útiles

```bash
docker compose logs -f            # ver logs de todo
docker compose logs -f piper      # logs de un motor
docker compose ps                 # estado
docker compose down               # apagar
```

## Notas

- Si la imagen de Kokoro cambia de nombre, revisa el repo `remsky/Kokoro-FastAPI`
  y ajusta `image:` en `docker-compose.yml`.
- Para sumar/quitar motores: edita `ENGINES` en `gateway/app.py` y el servicio
  en `docker-compose.yml`.
- ⚠️ Está pensado para uso interno de pruebas. Si lo dejas público, ponle al menos
  una clave básica o un proxy con auth.
