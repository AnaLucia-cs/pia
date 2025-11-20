🛡️ Sistema de Integridad de Archivos con IA
Proyecto de Seguridad en Tecnologías de la Información

📌 Descripción del Proyecto
Este proyecto implementa un Sistema Automático de Verificación de Integridad de Archivos, que permite detectar modificaciones no autorizadas, registrar cambios y restaurar archivos afectados desde una copia de seguridad.
Además, incluye integración con una API de Inteligencia Artificial que analiza los cambios detectados y determina si parecen modificaciones legítimas o potencialmente maliciosas.

El objetivo es brindar una capa adicional de seguridad y análisis inteligente dentro de un entorno de monitoreo.

🚀 Funcionalidades Principales
Análisis de modificaciones con IA (Función adicional)
Cada vez que se detecta un cambio en un archivo, el sistema envía:
-Nombre del archivo modificado
-Diferencias encontradas
-Usuario que realizó el cambio (si aplica)
-Timestamp y ruta

La API de IA devuelve:
-Si la modificación parece benigna, sospechosa o maliciosa
-Una breve explicación
-Recomendaciones de acción
Esto permite priorizar incidentes y reducir falsos positivos.

🧩 Arquitectura del Sistema
┌──────────────────┐
│ Archivos Monitoreados
└───────┬──────────┘
        │ Hash inicial (Tarea 1)
        ▼
┌──────────────────┐
│ Base de Hashes   │
└───────┬──────────┘
        │ Comparación (Tarea 2)
        ▼
┌──────────────────┐
│ Sistema de Alertas
└───────┬──────────┘
        │ Envía diff a IA
        ▼
┌──────────────────┐
│ API de IA: Análisis
└───────┬──────────┘
        │ Decisión
        ├──────────▶ Modificación legítima (log)
        ▼
┌────────────────────────┐
│ Restauración desde Backup (Tarea 3)
└────────────────────────┘

☎️ Tipo de modelo/API a utilizar
El sistema utilizará un modelo de lenguaje accesible mediante API y orientado al análisis contextual de texto.
El modelo debe ser capaz de:
Analizar contenido textual, incluyendo diffs de archivos.
Detectar patrones de riesgo en modificaciones.
Clasificar cambios como legítimos, sospechosos o maliciosos.
Explicar brevemente la razón de la clasificación.
Funcionar con tiempos de respuesta reducidos y peticiones JSON.
Modelos compatibles sugeridos:
OpenAI GPT-4o / ChatGPT / Copilot / Gemini

El proyecto no depende de un proveedor específico: cualquier modelo que acepte prompts estructurados y devuelva JSON es válido.

💭 Ejemplo de prompt inicial
A continuación se muestra el prompt base que el sistema enviará al modelo al detectar una modificación:

Eres un sistema de análisis de integridad de archivos.
Tu tarea es revisar un cambio detectado en un archivo y clasificarlo como:

- "legitimo": cambio esperado o normal.
- "sospechoso": cambio inusual que requiere revisión humana.
- "malicioso": cambio que sugiere manipulación no autorizada o riesgo.

Debes responder SIEMPRE en formato JSON con la estructura:

{
  "clasificacion": "",
  "explicacion": "",
  "recomendacion": ""
}

Datos del evento:
- Archivo: {{nombre_archivo}}
- Usuario: {{usuario}}
- Fecha: {{timestamp}}

Diferencias detectadas (diff):
{{diff}}


🧪 Estado del Proyecto
🟡 En desarrollo
✔ Base de hashes
✔ Verificación de integridad
⏳ Restauración automática
⏳ Integración con IA
⏳ Panel de reportes
