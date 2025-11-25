# 🧩 Propuesta técnica del proyecto PIA

## 🛡️ Título del proyecto
> Protección y control de integridad de archivos 

## 📌 Descripción general del proyecto
> Mantener la integridad de archivos importantes en el sistema. Identificación y alertas ante cambios no autorizados.

---

## 🧪 Tareas propuestas

### 🔐 Tarea 1
- **Título**: Generar hashes de archivos críticos del sistema
  
- **Propósito**:Crear una base de datos con los valores hash (SHA256, MD5) de archivos esenciales, sirviendo como referencia del estado “limpio” del sistema.
  
- **Rol o área relacionada**: SOC – Seguridad preventiva.
  
- **Entradas esperadas**:
      - Lista de rutas de archivos o directorios (`/etc`, `/bin`, etc.)  
      - Formato: texto o lista JSON
  
- **Salidas esperadas**:
      - Base de datos (`baseline.db`) con hashes calculados  
      - Archivo de registro (`init_log.txt`)
    
- **Descripción del procedimiento**:
      1. Recorrer las rutas definidas.  
      2. Calcular los hashes con `hashlib` (MD5, SHA256).  
      3. Guardar los resultados en una base SQLite protegida.
  
- **Complejidad técnica**: Uso de criptografía de hash, manipulación de archivos, automatización de procesos.
  
- **Controles éticos**: No se accederá a archivos privados ni con datos personales; se trabajará solo en entornos controlados o máquinas virtuales.
  
- **Dependencias**:
      - Python 3.x  
      - Librerías: `hashlib`, `sqlite3`, `os`  

### 🧭 Tarea 2

- **Título**: Verificar la integridad de archivos.

- **Propósito**: Comprobar la integridad de los archivos importantes en los sistemas al realizar una comparación de los hashes.

- **Rol o área relacionada**: Detección.

- **Entradas esperadas**: 
Archivo de referencia con los hashes originales
    -Ejemplo: hashes_bd.db
Rutas de los archivos a monitorear:
    -Ejemplo: ["C:\Windows\Firmware", "C:\Windows\Documents\Base_Datos.csv"]
              ["/etc/passwd", "/etc/shadow", "/home/tux/important_config.conf"]

- **Salidas esperadas**: Reporte comparando los hashes originales con los actuales, indicando si han sido modificados, eliminados o no existen.
    -Ejemplo:
    [/etc/passwd] [INTACTO]
    [/etc/shadow] [MODIFICADO]
    [/home/tux/important_config.conf] [NO ENCONTRADO]

- **Descripción del procedimiento**: 
1. Leer el archivo con los hashes originales
2. Recorrer las rutas indicadas y calcular el hash del archivo
3. Comparar los hashes
4. Registrar los resultados en un log
6. Programar la próxima ejecución del proceso.

- **Complejidad técnica**: 
Lectura y procesamiento de archivos de texto con hashes.
Comparación entre valores.
Ejecución automatizada periódica.
Uso de librerías de python como pyautogui, hashlib, os, logging y subprocess para poder integrar comandos de shells.
- **Controles éticos**: 
Se deben usar archivos de prueba o datos sintéticos en ambientes controlados. 
Evitar incluir archivos con datos personales o sensibles
Los resultados deben almacenarse de forma segura y anonimizada si contienen rutas personales.
- **Dependencias**: [Hashlib, os, datetime, logging, pyautogui, subprocess]

### 🧠 Tarea 3 
- **Título**: - Restauración de archivos modificados o eliminados
  
- **Propósito**: Recuperar archivos críticos del sistema que hayan sido alterados o eliminados, utilizando la línea base de hashes y los respaldos físicos generados previamente.

- **Rol o área relacionada**: Seguridad informática / Administración de sistemas.
  
- **Entradas esperadas**: - Base de datos baseline.db con los hashes originales.
- Carpeta backups/ con copias físicas de los archivos respaldados.
- Archivo de log de salida (restore_log.txt) para registrar el proceso.

- **Salidas esperadas**: - Archivos restaurados en su ubicación original.
- Log detallado con el estado de cada archivo (restaurado, sin cambios, error, sin respaldo).
- Mensajes en consola que informan el resultado de cada acción.

- **Descripción del procedimiento**:
  1-Se abre la base de datos baseline.db y se recorren los registros de archivos críticos.
  2-Para cada archivo:
    - Si no existe en el sistema, se intenta restaurar desde la carpeta backups/.
    - Si existe, se calcula su hash actual y se compara con el hash original.
    - Si el hash no coincide, se restaura desde el respaldo físico.
    - Si coincide, se marca como “sin cambios”.
  3-Se registra cada acción en el archivo de log y se muestra en consola.
  4-Al finalizar, se confirma que la restauración se completó.

  
- **Complejidad técnica**: Media. Requiere manejo de bases de datos SQLite, cálculo de hashes, operaciones de copia de archivos y control de errores. 


- **Controles éticos**:
- Garantizar que la restauración solo se aplique a archivos críticos definidos en la línea base.
- Evitar sobrescribir archivos sin respaldo válido.
- Mantener transparencia en los logs para que el administrador pueda auditar las acciones realizadas.

- **Dependencias**:
- baseline.db generado en la Tarea 1.
- Carpeta backups/ creada durante la Tarea 1.
- Librerías estándar de Python: sqlite3, hashlib, shutil, json, pathlib.

---

## 🗂️ Estructura inicial del repositorio (ejemplo)

/src [Código funcional de las tareas]
/scripts [Script principal]
/docs [Detalles sobre cada actualización]
/examples [Evidencias de ejecución]
/proposals [Propuesta de proyecto]
/tests [Pruebas de ejecución]
/prompts [Información de prompt]
README.md [Estado del proyecto]

> Esta estructura puede crecer conforme avance el proyecto. Cada carpeta tendrá una función clara y estará documentada en `/docs`.

---

## 👥 Asignación de roles del equipo

| Integrante | Rol o responsabilidad |
|------------|------------------------|
| [Ana Lucia Alonso Martínez] | [Automatización de la comparación de hashes] |
| [Ana Laura Palacios Salazar] | [Validación y gestión de la base de datos de hashes] |
| [Maria Izabela Lorencez Narro] | [Implemetación de la IA para recomendaciones de acciones sobre archivos modificados, Creación del backup de los archivos en las rutas dadas, Automatización de la restauración de archivos modificados, Bloque de generador de reportes] |

> Los roles pueden ajustarse conforme evolucione el proyecto.

---

## 🔐 Declaración ética y legal

Este proyecto se desarrollará exclusivamente con datos sintéticos o simulados. No se utilizarán datos reales, credenciales privadas ni información sensible. Todos los experimentos se ejecutarán en entornos controlados.  
El equipo se compromete a documentar cualquier riesgo ético y aplicar medidas de mitigación adecuadas.

---

## 🤝 Evidencia de colaboración inicial (elegir uno o más)

- [ ✔️] Commits realizados por más de un integrante
- [ ] Issues creados para organizar tareas
- [ ✔️] Actividad visible en GitHub desde el inicio del proyecto

---

## 📁 Ubicación de entregables posteriores

Todos los avances y entregables estarán documentados en la carpeta `/docs` dentro de este mismo repositorio.
 
