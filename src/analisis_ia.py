# analisis_ia.py
# Analiza historial_modif.txt con IA, muestra archivos sospechosos,
# pregunta al usuario y ejecuta restauración si acepta.

import subprocess
from pathlib import Path
import requests
import json

API_URL = "https://api.tuIA.com/analizar"   # <-- Reemplaza con tu API real
API_KEY = "AQUI_TU_KEY"                    # <-- Tu KEY real


def analizar_con_ia(historial_path: Path):
    """Envía historial_modif.txt a la IA y recibe análisis detallado."""
    if not historial_path.exists():
        print("❌ No existe historial_modif.txt. Ejecuta Tarea 2 primero.")
        return None

    contenido = historial_path.read_text(encoding="utf-8")

    payload = {"texto": contenido}
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("📡 Enviando análisis a la IA...")

    try:
        resp = requests.post(API_URL, json=payload, headers=headers)
        data = resp.json()

        print("\n=== ANALISIS DE IA ===")
        print("Archivos sospechosos:")

        archivos = data.get("archivos_sospechosos", [])
        razones = data.get("razones", "No detallado")

        for f in archivos:
            print(f" - {f}")

        print("\nRazones del riesgo:")
        print(razones)

        recomendacion = data.get("recomendacion", "desconocido")
        print(f"\nRecomendación final: {recomendacion.upper()}")

        return data

    except Exception as e:
        print(f"❌ Error al contactar IA: {e}")
        return None


def restaurar_archivos():
    """Ejecuta Tarea 3 (restauración)."""
    print("🔧 Ejecutando restauración...")
    subprocess.run(["python", "tarea3.py", "--db", "baseline.db", "--log", "restore_log.txt"])


def flujo_ia():
    """Analiza IA → muestra archivos → pregunta → restaurar si acepta."""
    data = analizar_con_ia(Path("historial_modif.txt"))

    if data is None:
        print("⚠ No hay análisis válido. Cancelando.")
        return

    recomendacion = data.get("recomendacion", "desconocido")

    if recomendacion.lower() == "restaurar":
        decision = input("\n⚠ La IA recomienda restaurar. ¿Quieres restaurar los archivos afectados? (s/n): ").strip().lower()

        if decision == "s":
            restaurar_archivos()
        else:
            print("❎ El usuario decidió NO restaurar.")
    else:
        print("✔ La IA indica que no es necesario restaurar.")


if __name__ == "__main__":
    flujo_ia()
