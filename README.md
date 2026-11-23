# Agente SAC

Agente de soporte con IA que reemplaza los niveles N1, N2 y N3 del servicio al cliente de una pyme con terminal de pagos.

> Todos los datos de este proyecto son ficticios.

## Objetivo

Tener una demo de 30 segundos que muestre al agente:

- resolviendo una consulta N1 (preguntas frecuentes),
- resolviendo una consulta N2 (datos del cliente),
- escalando un caso N3 a Linear,
- bloqueando un intento de prompt injection.

## Stack

Python, LangGraph, Ollama con qwen3:1.7b (modelo local) + Groq (nube), SQLite, Chroma y la API GraphQL de Linear.

## Cómo ejecutarlo

1. Crear y activar el entorno virtual, e instalar las dependencias:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copiar la plantilla de variables y completar los valores:

   ```bash
   cp .env.example .env
   ```

   El archivo `.env` guarda las claves reales. Git lo ignora, así que nunca se sube al repo.

3. Para el modelo local, instalar [Ollama](https://ollama.com) y descargar el modelo:

   ```bash
   ollama pull qwen3:1.7b
   ```

4. Ejecutar:

   ```bash
   python -m app.main
   ```

   Debe imprimir `ok`.

5. Correr las pruebas:

   ```bash
   python -m pytest
   ```

## Modelo de IA: nube o local

El agente pide el modelo con una sola función, `get_llm()`, en `app/llm.py`. La variable `LLM_PROVIDER` del `.env` decide cuál se usa, sin tocar el código:

| `LLM_PROVIDER` | Dónde corre | Modelo por defecto | Variables |
|---|---|---|---|
| `local` | En tu computador (Ollama) | `qwen3:1.7b` | `LOCAL_BASE_URL`, `LOCAL_MODEL` |
| `groq` | En la nube (Groq) | `openai/gpt-oss-20b` | `GROQ_API_KEY`, `GROQ_MODEL` |

Si `LLM_PROVIDER` está vacío, se usa `local`.

Los dos proveedores usan la misma API compatible con OpenAI. Por eso el código es el mismo para ambos: solo cambian la URL base, la clave y el nombre del modelo.

OpenRouter es opcional. Sus variables están en `.env.example`, pero el código todavía no lo usa.

### Usar LM Studio en lugar de Ollama

LM Studio también tiene una API compatible con OpenAI, así que funciona igual. Deja `LLM_PROVIDER=local` y cambia la URL al puerto 1234:

```env
LOCAL_BASE_URL=http://localhost:1234/v1
LOCAL_MODEL=nombre-del-modelo-en-lm-studio
```

### Razonamiento de qwen3 (`<think>`)

qwen3 puede escribir su razonamiento entre las etiquetas `<think>` y `</think>` antes de responder. La función `limpiar_think()` las quita para que el cliente vea solo la respuesta final. Las versiones recientes de Ollama ya entregan el razonamiento aparte, pero otros servidores o versiones pueden dejarlo dentro del texto.

### Comparar proveedores

```bash
python -m app.probar_modelos
python -m app.probar_modelos "¿Cómo pido una boleta?"
```

El comando manda el mismo prompt a cada proveedor y muestra la respuesta y cuántos segundos tardó. Si un proveedor falla (por ejemplo, porque falta la clave de Groq), muestra el error y sigue con el siguiente.

La primera llamada al modelo local tarda más, porque Ollama tiene que cargar el modelo en memoria.

## Estructura

| Carpeta | Contenido |
|---|---|
| `app/` | Código del agente |
| `data/` | Datos ficticios: preguntas frecuentes y base SQLite |
| `docs/` | Plan del proyecto y documentación |
| `tests/` | Pruebas automáticas |
