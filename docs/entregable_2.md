# ⚙️ Entregable 2 – MVP funcional parcial

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🧪 Tarea implementada

- **Nombre de la tarea**: Generar hashes de archivos críticos del sistema
- **Descripción funcional**:  
  >El script recorre una lista de archivos definidos por el usuario (por ejemplo, archivos del sistema o ejecutables importantes) y calcula los valores hash MD5 y SHA25 de cada uno.
  >Los resultados se almacenan en una base de datos SQLite como línea base (“baseline”), para futuras comparaciones de integridad.
  >Durante la ejecución se registran eventos y resultados en un log estructurado en formato JSON Lines.

---

## 📥 Entradas utilizadas

> Archivo de rutas de archivos: examples/inputs/list.txt
    Contiene una lista de rutas absolutas de los archivos a analizar.
> Ejemplo de contenido:
   C:\Windows\System32\notepad.exe
   C:\Windows\System32\cmd.exe
   /etc/passwd
   /etc/hosts
   /bin/ls
   /bin/echo
> Formato: texto plano o JSON con lista de rutas.
> Método de entrada: se proporciona mediante el argumento --input .

---

## 📤 Salidas generadas
> Base de datos SQLite: examples/baseline.db
   Contiene las rutas de archivos, tamaño, fecha de modificación y sus hashes MD5 y SHA256.
> Log estructurado (JSON Lines): examples/logs.jsonl
  Registra los resultados de cada archivo procesado.
> Log inicial: examples/init_log.txt
   Registra la configuración inicial y hora de ejecución.
> Ejemplo de salida esperada en consola:
  ✅ Ejecución completada correctamente. Revisa 'logs.jsonl' y 'baseline.db'.

---

## 📁 Evidencia reproducible

- Ruta a ejemplos de ejecución: /examples  
- Ruta a logs estructurados:  /examples/logs.jsonl
- Script de ejecución: py src/run_tarea1.py --input examples/inputs/list.txt --db examples/baseline.db --log examples/logs.jsonl --initlog examples/init_log.txt

---

## 📚 Documentación técnica
> Dependencias:
  - Python 3.x
  - Librerías estándar: hashlib, sqlite3, os, json, argparse, time, pathlib

> Modo de ejecución:
  - Ejecutar el comando anterior desde la raíz del proyecto.
  - El script creará automáticamente los archivos de salida en la carpeta /examples.

> Observaciones iniciales:
  - El sistema fue probado en entorno controlado (Windows 11).
  - No accede a archivos privados ni directorios fuera de los definidos en la lista.

---

## 🤝 Colaboración

> Autora: Ana Laura Palacios Salazar
> Rol: Desarrollo y pruebas funcionales de la tarea 1.
> La colaboración y control de versiones se reflejan en los commits y la estructura del repositorio de GitHub.

---

## 🧭 Observaciones

> Durante la elaboración de esta tarea pude comprender mejor cómo funciona la integridad de archivos en un sistema operativo y la importancia de generar una línea base confiable para detectar cambios o posibles manipulaciones.
> Al principio me resultó un poco complicado entender cómo combinar el uso de hashes (MD5 y SHA256) con una base de datos SQLite, pero al avanzar en las pruebas logré visualizar cómo esta información puede servir para un monitoreo de seguridad real.
> También aprendí la relevancia de registrar todo el proceso en logs estructurados, ya que esto permite tener evidencia clara y trazable de las acciones del sistema.
> En futuras etapas me gustaría mejorar la presentación de los resultados y agregar una comparación automática entre la línea base y un nuevo análisis para detectar modificaciones en tiempo real.  
 
