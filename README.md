# Protección y control de integridad de archivos 

Trabajo final de la materia Programación para Ciberseguridad de la Facultad de Ciencias Fisico Matemáticas. 
Los ejecutables y programas en este repositorio están orientados a la protección y control de modificaciones a archivos importantes en el sistema al comparar los hashes de referencia con los hashes actuales. 

Este proyecto esta en la fase de planeación.

## Estado actual del proyecto (actualización – Entregable 2)

A la fecha del segundo entregable, se completó la Tarea 1: Generar hashes de archivos críticos del sistema, con un script funcional (`run_tarea1.py`) que:
- Lee una lista de rutas de archivos.
- Calcula los hashes MD5 y SHA256.
- Almacena los resultados en una base SQLite (`baseline.db`).
- Genera registros estructurados (`logs.jsonl` y `init_log.txt`).

Este avance representa la primera versión funcional del sistema de protección de integridad, sirviendo como base para la Tarea 2 (verificación periódica) y la Tarea 3 (alertas automáticas).

Se mantiene el cumplimiento de los controles éticos y se trabaja en entornos controlados de laboratorio.


## Estado actual del proyecto (actualización – Entregable 3)

A la fecha del tercer entregable, se completó la Tarea 1: Generar hashes de archivos críticos del sistema, con un script funcional (`run_tarea1.py`) que:
- Lee una lista de rutas de archivos.
- Calcula los hashes MD5 y SHA256.
- Almacena los resultados en una base SQLite (`baseline.db`).
- Genera registros estructurados (`logs.jsonl` y `init_log.txt`).

Además se agrego la Tarea 2: Verificar la integridad de los archivos,  con un script funcional (`tarea2.py`) que:
- Lee una lista de rutas de archivos.
- Calcula los hashes MD5 y SHA256.
- Almacena los resultados en un diccionario.
- Extrae las columnas de 'ruta' y 'md5' de la base de datos (`baseline.db`).
- Guarda los resultados en otro diccionario y los compara con los hashes actuales. 
- Genera un historial de las revisiones (`historial_modif.txt`).
- Genera registros estructurados (`logs.jsonl` y `init_log.txt`).

Finalmente se creó un script principal de powershell (`controlador.ps1`), el cual por medio de un menú te permite elegir entre crear/actualizar la base de datos con los hashes o compararlos con los archivos actuales

Este avance representa la tercera versión funcional del sistema de protección de integridad, sirviendo como base para la Tarea 3 (alertas automáticas).

Se mantiene el cumplimiento de los controles éticos y se trabaja en entornos controlados de laboratorio.

También se desarrollo el plan a seguir para el uso de la API de inteligencia artificial, el cuál sera de mucha ayuda a la hora de clasificar el nivel de modificaciones en caso de que existan, y podere restaurar los archivos dañados.

## Estado actual del proyecto (actualización – Entregable 4)

A la fecha del cuarto entregable, se completaron las Tareas 1 y 2: Generar hashes de archivos críticos del sistema (run_tarea1.py) y Verificar la integridad de los archivos (tarea2.py).

Además se hicieron una pequeñas modificaciones a ambos scripts para que se pudiera realizar la tarea 3 y la implementación de la ia.

Modificaciones a la Tarea 1:
- Se le agregó una función para crear el respaldo de la base de datos (necesario paa la tarea 3)

Modificaciones a la Tarea 2:
- Se creó historial_modif.py para que la IA lo pudiera leer

La tarea 3 consiste en:
Después de verificar si se hicieron cambios (tarea 2) se mandan a analizar por la IA (analisis_ia.py) y este determina si los cambios hechos fueron críticos o no, si los considera como tal, se le notifica al usuario sobre los cambios y sus consecuencias y se le pregunta se deesea volver al respaldo de los archivos modificados, si responde que si, automaticamente se ejecuta el script tarea3.py, que es el respaldo.
