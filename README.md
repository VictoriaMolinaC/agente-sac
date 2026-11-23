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

Python, LangGraph, LM Studio (modelo local) + Groq u OpenRouter (nube), SQLite, Chroma y la API GraphQL de Linear.

## Cómo ejecutarlo

1. Crear y activar el entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Copiar la plantilla de variables y completar los valores:

   ```bash
   cp .env.example .env
   ```

   El archivo `.env` guarda las claves reales. Git lo ignora, así que nunca se sube al repo.

3. Ejecutar:

   ```bash
   python -m app.main
   ```

   Debe imprimir `ok`.

## Estructura

| Carpeta | Contenido |
|---|---|
| `app/` | Código del agente |
| `data/` | Datos ficticios: preguntas frecuentes y base SQLite |
| `docs/` | Plan del proyecto y documentación |
| `tests/` | Pruebas automáticas |
