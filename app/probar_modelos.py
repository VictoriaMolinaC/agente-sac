"""Manda el mismo prompt a cada proveedor y muestra la respuesta y el tiempo.

Uso:
    python -m app.probar_modelos
    python -m app.probar_modelos "Tu pregunta"
"""

import sys
import time

from app.llm import PROVEEDORES, config_proveedor, preguntar

PROMPT_POR_DEFECTO = (
    "Mi terminal de pagos no enciende. ¿Qué reviso primero? "
    "Responde en 3 pasos cortos."
)


def main() -> None:
    prompt = " ".join(sys.argv[1:]) or PROMPT_POR_DEFECTO
    print(f"Prompt: {prompt}\n")

    tiempos = {}
    for proveedor in PROVEEDORES:
        try:
            modelo = config_proveedor(proveedor)["model"]
            inicio = time.perf_counter()
            respuesta = preguntar(prompt, proveedor)
            segundos = time.perf_counter() - inicio
        except Exception as error:
            print(f"=== {proveedor}: error ===\n{error}\n")
            tiempos[proveedor] = "error"
            continue

        tiempos[proveedor] = f"{segundos:.1f} s ({modelo})"
        print(f"=== {proveedor} · {modelo} · {segundos:.1f} s ===\n{respuesta}\n")

    print("Tiempos:")
    for proveedor, tiempo in tiempos.items():
        print(f"  {proveedor:<6} {tiempo}")


if __name__ == "__main__":
    main()
