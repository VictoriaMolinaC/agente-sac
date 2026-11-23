import pytest

from app.llm import config_proveedor, get_llm, limpiar_think


def test_quita_el_bloque_think():
    assert limpiar_think("<think>pienso...\nmucho</think>\n\nHola.") == "Hola."


def test_quita_el_razonamiento_si_solo_llega_el_cierre():
    assert limpiar_think("razonamiento</think>Hola.") == "Hola."


def test_quita_un_think_sin_cerrar():
    assert limpiar_think("Hola.<think>se cortó") == "Hola."


def test_texto_sin_think_queda_igual():
    assert limpiar_think("  Hola.  ") == "Hola."


def test_local_usa_ollama_por_defecto(monkeypatch):
    monkeypatch.delenv("LOCAL_BASE_URL", raising=False)
    monkeypatch.delenv("LOCAL_MODEL", raising=False)
    config = config_proveedor("local")
    assert config["base_url"] == "http://localhost:11434/v1"
    assert config["model"] == "qwen3:1.7b"


def test_local_sirve_para_lm_studio(monkeypatch):
    monkeypatch.setenv("LOCAL_BASE_URL", "http://localhost:1234/v1")
    monkeypatch.setenv("LOCAL_MODEL", "qwen3-4b")
    llm = get_llm("local")
    assert llm.openai_api_base == "http://localhost:1234/v1"
    assert llm.model_name == "qwen3-4b"


def test_llm_provider_elige_el_proveedor(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "clave-de-prueba")
    monkeypatch.setenv("GROQ_MODEL", "modelo-de-prueba")
    llm = get_llm()
    assert llm.openai_api_base == "https://api.groq.com/openai/v1"
    assert llm.model_name == "modelo-de-prueba"


def test_groq_sin_clave_avisa(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        config_proveedor("groq")


def test_proveedor_desconocido_avisa():
    with pytest.raises(ValueError, match="desconocido"):
        get_llm("otro")
