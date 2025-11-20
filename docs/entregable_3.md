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

> En este entregable Izabela Lorencez se encargó del plan de uso del API de IA. Ana Alonso realizó el script maestro y la tarea 2, permitiendo ejecutar las tareas desde un menú. Finalmente Ana Laura Palacios se encargó de la primer tarea y creó una base de datos para mantener los hashes de los archivos en orden.

---

## 🧭 Observaciones

**Falta:**
-Integrar definitivamente la llamada a la API dentro del flujo principal del verificador de integridad.
-Añadir pruebas automáticas que simulen modificaciones reales y verifiquen la correcta interacción entre monitor, IA y sistema de restauración.
-Definir límites y políticas de uso para evitar costos innecesarios o cargas altas de peticiones a la API.

**Decisiones Tomadas:**
-La IA no ejecuta acciones directas, solo asesora: la decisión final del sistema (restaurar, aceptar o alertar) siempre pasa por las reglas locales.
-Se optó por un diseño desacoplado: cualquier modelo compatible se puede cambiar sin alterar el resto del sistema.
-La IA se utiliza solo en el punto crítico del flujo: después de detectar una modificación y antes de restaurar o registrar el cambio.

**Aprendizaje:**
-Que la IA no sustituye la verificación tradicional: funciona como una capa adicional que complementa la seguridad, no como la base del sistema.
-Que el análisis de integridad puede beneficiarse significativamente del contexto que aporta un modelo de IA, especialmente para reducir falsos positivos.
