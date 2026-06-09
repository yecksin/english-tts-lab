# AGENT.md — Generar audio en inglés (TTS Lab remoto)

Guía para que un agente (Claude) **genere voz en inglés** usando el servicio remoto
desplegado, sin instalar nada local. Pensado para **practicar listening**.

## Remoto

- **Front (humano):** https://tts.uvingo.app/ — Yeck elige y **fija la voz por defecto** aquí.
- **API (agente):** mismo host, endpoints bajo `/api`.

## ⚠️ Reglas de uso (el "para qué") — OBLIGATORIO

1. **El agente NO elige la voz.** La voz la selecciona Yeck desde el front y queda
   como "voz por defecto". El agente llama la API **solo con el texto**.
2. **Preguntar antes de generar.** Antes de crear audio, preguntar a Yeck:
   *"¿Genero el audio para que practiques listening?"* — no generar sin confirmación.
3. **NO escribir en la terminal/chat lo que va a decir el audio.** El objetivo es
   listening: Yeck **escucha** y **responde por texto** lo que entendió. Spoilear el
   texto rompe el ejercicio. Generar → reproducir → callar el contenido.
4. Tras reproducir, esperar la respuesta de Yeck en texto y recién ahí corregir/comentar.

## Cómo generar y reproducir (macOS)

Voz por defecto (la que Yeck fijó en el front) — **enviar solo el texto**:

```bash
curl -s -X POST https://tts.uvingo.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"<frase en inglés>"}' \
  -o /tmp/tts.wav && afplay /tmp/tts.wav
```

- `afplay` es el reproductor nativo de macOS (suena en el Mac de Yeck).
- El audio sale en `audio/wav`. No imprimir la frase en el chat (ver regla 3).

## API (referencia)

| Método | Endpoint | Para qué |
|---|---|---|
| `POST` | `/api/tts` | Genera audio. Body: `{"text": "..."}` → usa la **voz por defecto**. Devuelve `audio/wav`. |
| `GET`  | `/api/default-voice` | Devuelve la voz por defecto actual `{engine, voice}`. |
| `GET`  | `/api/engines` | Lista motores y voces disponibles (para el front). |

Opcional (normalmente NO se usa desde el agente, la voz la maneja Yeck en el front):
- `POST /api/tts` con `{"text","engine","voice"}` fuerza un motor/voz puntual.
- `POST /api/default-voice` con `{"engine","voice"}` cambia la voz por defecto.

## Notas

- Motores: **kokoro** (natural, recomendado) y **piper** (ligero). Detalle en README.md.
- Si `/api/tts` da 502/500, el motor de esa voz está caído — revisar en Coolify
  (ver memoria `reference_coolify_api`).
