# 🧩 Entregable 4 – Proyecto casi completo (90%)

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🔗 Flujo técnico consolidado

> Descripción del flujo completo entre tareas:  
> 
> El proyecto se organiza en tres tareas principales y un controlador de ejecución (controlador.ps1), con integración opcional de IA y restauración de archivos:
-Tarea 1 - Generación de línea base y respaldos (run_tarea1.py / hash_baseline.py)
Calcula los hashes MD5 y SHA256 de archivos críticos.
Crea la base de datos baseline.db y respaldos en la carpeta backups/.
Genera logs: init_log.txt (legible) y logs.jsonl (estructurado).
-Tarea 2 – Verificación de integridad (tarea2.py)
Compara los hashes actuales con la línea base.
Detecta archivos nuevos, modificados o eliminados.
Genera:
comparison_summary.txt (resumen legible)
historial_modif.txt (para análisis de la IA)
Análisis con IA (analisis_ia.py)
Analiza historial_modif.txt y sugiere si conviene restaurar archivos.
Devuelve un informe resumido de cambios y recomendaciones.
-Tarea 3 – Restauración de archivos (tarea3.py)
Se ejecuta solo si el usuario confirma restaurar los archivos modificados/eliminados.
Restaura los archivos desde backups/.
Registra operaciones en restore_log.txt.
-Controlador (controlador.ps1)
Menú principal con tres opciones:
a) Generar línea base y respaldos (Tarea 1)
b) Verificar integridad, analizar con IA y restaurar opcionalmente (Tarea 2 + IA + Tarea 3)
c) Salir
Flujo de información: La salida de Tarea 1 (baseline.db y respaldos) alimenta Tarea 2. La salida de Tarea 2 (historial_modif.txt) es la entrada de la IA, cuya recomendación se usa para decidir si Tarea 3 se ejecuta. Todos los pasos generan logs para auditoría.

---

## 🧠 IA integrada funcionalmente

- **Modelo/API utilizado**: GPT-4 vía API de OpenAI (simulación posible en local)
- **Punto de integración**:  
  > La IA se invoca después de la verificación de integridad (Tarea 2) y antes de la restauración de archivos (Tarea 3).

Analiza los archivos modificados o eliminados y devuelve recomendaciones al usuario.

- **Ejemplo de entrada/salida**:  
  > Entrada (historial_modif.txt):
C:\Sistema\archivo1.txt: MODIFICADA
C:\Sistema\archivo2.dll: ELIMINADA
C:\Sistema\archivo3.log: INTACTA
  > Salida de la IA:
Se detectaron 2 archivos críticos modificados/eliminados.
Recomendación: restaurar los archivos desde el respaldo para mantener la integridad del sistema.


---

## 📁 Evidencia reproducible

- **Archivos de salida**: baseline.db, comparison_summary.txt, historial_modif.txt (../examples)
- **Logs estructurados**: /examples/logs.jsonl (../examples/logs.jsonl)
- **Script principal o de orquestación**: [`/scripts/controlador.ps1`]

---

## 📚 Documentación técnica

> Requisitos:

Python ≥ 3.8
Librerías: pandas
PowerShell para ejecutar el controlador
Ejecución recomendada:
Ejecutar controlador.ps1.
Seleccionar opción a) para generar línea base y respaldos.
Seleccionar opción b) para verificar integridad y ejecutar análisis de la IA.
Confirmar restauración de archivos si la IA lo recomienda.

Observaciones:
Todos los logs permiten auditar cambios.
La restauración solo se realiza bajo aprobación explícita del usuario.

---

## 🤝 Colaboración

> Autores: Ana Laura Palacios Salazar, Ana Lucia Alonso Martinez y Maria Izabela Lorencez Narro

Evidencia en GitHub: commits documentados por tarea para revisión de código.

Ajustes finales distribuidos entre tareas: Tarea 1 → generación de línea base (Laura), Tarea 2 → comparación e historial (Lucia), Tarea 3 → restauración ()Izabela.

---

## 🧭 Observaciones

> El flujo permite asegurar la integridad de archivos críticos de manera controlada.

La integración de IA proporciona recomendaciones adicionales, pero la decisión final siempre queda en manos del usuario.

Se mantiene compatibilidad con Windows y Linux (PowerShell y Python).
 
