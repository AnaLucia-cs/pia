# 🔗 Entregable 3 – Integración parcial y plan de IA

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🧪 Tareas integradas

- **Tarea 1**: Generar hashes de archivos críticos del sistema
- **Tarea 2**: Verificar la integridad de archivos.
- **Descripción de la integración**:  
  > La tarea 1 genera los hashes de las rutas especificadas en un archivo .txt ('rutas.txt') y guarda los resultados en una base de datos de SQLite ('baseline.db'). 
  > La tarea 2 genera los hashes de las rutas especificadas en un archivo .txt y los compara con aquellos que están en la base de datos. 
  > La tarea 2 genera un archivo donde se almacenan los resultados del análisis con fechas.
  >Durante ambas ejecuciones se registran eventos y resultados en un log estructurado en formato JSON Lines.
  > Ambos scripts son controlados por un archivo de powershell, el cual te permite elegir entre ambas opciones y maneja las entradas de datos que se deben ingresar de forma amigable.

---

## 🧬 Uso de dos lenguajes de programación

- **Lenguajes utilizados**:  Python + PowerShell
- **Forma de integración**:  
  > El script principal de powershell navega entre carpetas hasta llegar a donde están almacenados los scripts de python, donde los ejecuta según decida el usuario por medio del menú de opciones. 

- **Archivo relevante**: [`/scripts/controlador.ps1`]

---

## 🧠 Plan de uso de IA

- **Propósito del uso de IA**:  
  > Analiza los cambios detectados y determina si parecen modificaciones legitimas o potencialmente maliciosas.

- **Punto de integración en el flujo**:  
  > La API de IA debe integrarse justo después de detectar una modificación y antes de restaurar un archivo.

- **Modelo/API previsto**: [ChatGPT, OpenAI, Copilot]

- **Archivo del plan**: [`/docs/ai_plan.md`](ai_plan.md)

---

## 📝 Prompt inicial

- **Archivo de plantilla**: [`/prompts/prompt_v1.json`](../prompts/prompt_v1.json)
- **Campos incluidos**:  
  - `version`
  - `tarea`
  - `template`
  - `instrucciones`

---

## 📁 Evidencia reproducible

- **Logs estructurados**: [`/examples/logs.jsonl`](../examples/logs.jsonl)
- **Ejemplos de ejecución**: [`/examples`](../examples)
- **Script de orquestación o módulo funcional**: [`/scripts`](../scripts)

---

## 🤝 Colaboración

> ¿Quién trabajó en esta integración? ¿Cómo se distribuyeron los roles? ¿Qué evidencia hay en GitHub (commits, issues, PRs)?

---

## 🧭 Observaciones

> ¿Qué falta por conectar o ajustar? ¿Qué decisiones se tomaron sobre el uso de IA? ¿Qué se aprendió en esta etapa?
 
