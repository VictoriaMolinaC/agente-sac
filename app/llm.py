"""Modelo intercambiable: un solo lugar para obtener el LLM del proyecto.

Groq (nube) y el modelo local (Ollama o LM Studio) usan la misma API
compatible con OpenAI. Solo cambian la URL base, la clave y el modelo,
así que un único cliente (ChatOpenAI) sirve para todos.
"""

import os
import re

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

PROVEEDORES = ("groq", "local")
PROVEEDOR_POR_DEFECTO = "local"

_BLOQUE_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


def config_proveedor(proveedor: str) -> dict:
    """Devuelve la URL base, la clave y el modelo de un proveedor, leídos del .env."""
    if proveedor == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Falta GROQ_API_KEY en el .env")
        return {
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": api_key,
            "model": os.getenv("GROQ_MODEL") or "openai/gpt-oss-20b",
        }
    if proveedor == "local":
        return {
            # Ollama usa el puerto 11434. LM Studio usa el 1234.
            "base_url": os.getenv("LOCAL_BASE_URL") or "http://localhost:11434/v1",
            # Los servidores locales no piden clave, pero el cliente necesita un texto.
            "api_key": "local",
            "model": os.getenv("LOCAL_MODEL") or "qwen3:1.7b",
        }
    raise ValueError(
        f"LLM_PROVIDER desconocido: {proveedor!r}. Usa uno de: {', '.join(PROVEEDORES)}"
    )


def get_llm(proveedor: str | None = None) -> ChatOpenAI:
    """Devuelve el modelo elegido. Sin argumento, usa LLM_PROVIDER del .env."""
    proveedor = proveedor or os.getenv("LLM_PROVIDER") or PROVEEDOR_POR_DEFECTO
    return ChatOpenAI(**config_proveedor(proveedor.strip().lower()))


def limpiar_think(texto: str) -> str:
    """Quita el razonamiento de qwen3 (<think>...</think>) y deja solo la respuesta."""
    texto = _BLOQUE_THINK.sub("", texto)
    # Si solo llega la etiqueta de cierre, todo lo anterior es razonamiento.
    if "</think>" in texto:
        texto = texto.split("</think>")[-1]
    # Si la respuesta se cortó con un <think> sin cerrar, se descarta desde ahí.
    if "<think>" in texto:
        texto = texto.split("<think>")[0]
    return texto.strip()


def preguntar(prompt: str, proveedor: str | None = None) -> str:
    """Manda un prompt al modelo y devuelve la respuesta ya limpia."""
    respuesta = get_llm(proveedor).invoke(prompt)
    return limpiar_think(respuesta.content)
