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
- **Título**: Generación automática de reportes y alerta ante cambios detectados
  
- **Propósito**: Elaborar un reporte detallado y enviar una alerta automática cuando se detecten modificaciones, eliminaciones o incorporaciones de archivos respecto a la línea base de integridad.
Busca notificar oportunamente al equipo de seguridad sobre posibles alteraciones no autorizadas.

- **Rol o área relacionada**: SOC, DFIR
  
- **Entradas esperadas**: Reporte de verificación de integridad generado en la Tarea 2.
[/etc/passwd] [INTACTO]  
[/etc/shadow] [MODIFICADO]  
[/home/tux/important_config.conf] [NO ENCONTRADO]

- **Salidas esperadas**: Reporte final con fecha y hora de los cambios detectados (alert_report.json o .csv).
  Alerta enviada por correo, notificación en SIEM o mensaje en consola.
  {
  "fecha": "2025-11-03T14:12:00Z",
  "archivo": "/etc/shadow",
  "estado": "MODIFICADO",
  "acción": "Enviar alerta al SOC"
}

- **Descripción del procedimiento**:
1-Leer el resultado del monitoreo de integridad (Tarea 2).
2-Filtrar los registros con estado “MODIFICADO”, “ELIMINADO” o “NO ENCONTRADO”.
3-Generar un reporte consolidado con la fecha, hora y tipo de cambio.
4-Enviar una alerta automática (correo, log central, o API).
5-Guardar evidencia en el historial de alertas.
  
- **Complejidad técnica**:
Parsing y análisis de logs o reportes previos.
Automatización de reportes y envío de alertas.
Integración con servicios de correo o SIEM.
Uso de librerías: json, smtplib, logging, os, datetime.

- **Controles éticos**:
Pruebas realizadas con datos sintéticos o simulados.
No incluir rutas ni nombres de archivos con información sensible.
Las notificaciones se realizarán solo en entornos de laboratorio o controlados.

- **Dependencias**:
Python 3.x
Librerías: json, logging, smtplib, os, datetime
Variables de entorno: ALERTA_EMAIL, SMTP_SERVER, HASH_REPORT_PATH

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
| [Maria Izabela Lorencez Narro] | [Detección y alerta de modificaciones en archivos críticos] |

> Los roles pueden ajustarse conforme evolucione el proyecto.

---

## 🔐 Declaración ética y legal

Este proyecto se desarrollará exclusivamente con datos sintéticos o simulados. No se utilizarán datos reales, credenciales privadas ni información sensible. Todos los experimentos se ejecutarán en entornos controlados.  
El equipo se compromete a documentar cualquier riesgo ético y aplicar medidas de mitigación adecuadas.

---

## 🤝 Evidencia de colaboración inicial (elegir uno o más)

- [ ] Commits realizados por más de un integrante
- [ ] Issues creados para organizar tareas
- [ ] Actividad visible en GitHub desde el inicio del proyecto

---

## 📁 Ubicación de entregables posteriores

Todos los avances y entregables estarán documentados en la carpeta `/docs` dentro de este mismo repositorio.
 
