# 📘 Reporte final – Cambios importantes en la planeación

> Este documento forma parte del entregable final del proyecto PIA. Su propósito es dejar constancia de los ajustes significativos realizados durante el desarrollo del proyecto que afectaron el resultado final.

---

## 🔄 Cambios en tareas técnicas

- La **tarea 1 (hash_baseline.py)** fue modificada: originalmente solo calculaba hashes y almacenaba resultados en la base de datos, pero se agregó la creación de **copias físicas de los archivos** en la carpeta `backups/`.  
- La **tarea 3 (restauración)** también se ajustó: ahora valida la existencia de respaldos físicos y muestra mensajes más claros sobre el estado de cada archivo (restaurado, sin cambios o sin respaldo).  
- Estos cambios fueron necesarios porque el flujo original no permitía restaurar archivos modificados, ya que no existían copias físicas disponibles.

---

## 🧠 Cambios en el uso de IA

- El uso de IA se simplificó: en lugar de depender de una API externa ficticia, se integró directamente con la **API de OpenAI**.  
- Se diseñaron **prompts más claros y específicos** para que la IA pudiera identificar archivos sospechosos, explicar razones y dar una recomendación final (ej. “restaurar” o “no restaurar”).  
- Se eliminó lógica innecesaria en el cliente y se dejó que el prompt controle el análisis, lo que redujo complejidad y mejoró la claridad de resultados.

---

## 👥 Cambios en roles o distribución del trabajo

**Izabela Lorencez** se encargó en la gestión de los respaldo físicos y la lógica de la restauración; además de la integración con la IA y el diseño del prompt. De igual manera en la generación de los reportes en formato .txt y .xslx.

---

## 🧭 Decisiones técnicas relevantes

- Se decidió **crear respaldos físicos** en la carpeta `backups/` para garantizar la posibilidad de restauración.  
- Se ajustó el **logging** para que los mensajes fueran más claros y útiles (ej. “⚠️ No existe respaldo físico” o “✅ Archivo restaurado”).  
- Se simplificó el flujo de IA: el cliente solo envía datos y recibe recomendaciones, mientras que la lógica de prompts se maneja directamente en el script.  
- Se mantuvo el uso de **SQLite** como base de datos para la línea base, por su simplicidad y portabilidad.  
- Se evitó el uso de librerías externas innecesarias para mantener el proyecto ligero y fácil de ejecutar.

---

## 📌 Impacto en el entregable final

- **Logrado**: ahora el sistema puede detectar cambios en archivos, consultar a la IA para recomendaciones y restaurar archivos modificados o eliminados desde respaldos físicos.  
- **Pendiente**: la integración completa con la IA requiere una API key válida; sin ella, el flujo se detiene en la fase de análisis.  
- **Aprendizaje**: se comprendió la importancia de respaldar no solo metadatos (hashes) sino también los archivos originales, y de diseñar prompts claros para obtener respuestas útiles de la IA.

---

## 🕒 Confirmación de cierre

> Confirmamos que la última actualización del repositorio fue realizada **antes del 26 de noviembre a las 23:59 hrs (hora local de Monterrey)**.

- Fecha del último commit: [2025-11-25 hh:mm]
- Usuario responsable del cierre: [Maria Izabela Lorencez Narro]
