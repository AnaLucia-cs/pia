# analisis_interactivo.py
# Lee historial_modif.txt, envía a la IA con un prompt,
# muestra recomendaciones y pregunta si restaurar.

from pathlib import Path
import subprocess
import openai

# Configura tu API Key (puedes usar os.getenv para mayor seguridad)
api_key = "TU_API_KEY_AQUI"

# Inicializa cliente
client = openai.OpenAI(api_key=api_key)

def analizar_historial():
    archivo = Path("historial_modif.txt")
    if not archivo.exists():
        print("❌ No existe historial_modif.txt. Ejecuta Tarea 2 primero.")
        return None

    contenido = archivo.read_text(encoding="utf-8")

    # Prompt directo para la IA
    prompt = f"""
    Soy un analista de ciberseguridad.
    Este es el historial de modificaciones detectado:

    {contenido}

    Por favor:
    1. Identifica archivos sospechosos.
    2. Explica brevemente las razones.
    3. Da una recomendación final (ej. 'restaurar' o 'no restaurar').
    """

    print("📡 Enviando análisis a la IA...")

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    texto = respuesta.choices[0].message.content
    print("\n=== ANALISIS DE LA IA ===")
    print(texto)

    return texto


def restaurar_archivos():
    """Ejecuta restauración con tarea3.py"""
    print("🔧 Ejecutando restauración...")
    subprocess.run(["python", "tarea3.py", "--db", "baseline.db", "--log", "restore_log.txt"])


def flujo_ia():
    resultado = analizar_historial()
    if resultado is None:
        return

    # Pregunta al usuario si quiere restaurar
    decision = input("\n⚠ ¿Quieres restaurar los archivos afectados? (s/n): ").strip().lower()
    if decision == "s":
        restaurar_archivos()
    else:
        print("❎ El usuario decidió NO restaurar.")


if __name__ == "__main__":
    flujo_ia()

