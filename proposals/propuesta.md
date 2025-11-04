# 🧩 Propuesta técnica del proyecto PIA

## 🛡️ Título del proyecto
> Protección y control de integridad de archivos 

## 📌 Descripción general del proyecto
> Mantener la integridad de archivos importantes en el sistema. Identificación y alertas ante cambios no autorizados.

---

## 🧪 Tareas propuestas

### 🔐 Tarea 1
- **Título**: Generar hashes de archivos críticos del sistema
- **Propósito**: [2–3 frases que expliquen qué se busca lograr]
- **Rol o área relacionada**: [SOC, Red Team, DFIR, etc.]
- **Entradas esperadas**: [Formato y ejemplos]
- **Salidas esperadas**: [Formato y ejemplos]
- **Descripción del procedimiento**: [Narración funcional de lo que hará la tarea]
- **Complejidad técnica**: [Dimensiones que cubre: parsing, correlación, automatización, librerías]
- **Controles éticos**: [Uso de datos sintéticos, ambientes controlados, anonimización]
- **Dependencias**: [Librerías, comandos, entorno, variables de entorno]

### 🧭 Tarea 2
- **Título**: Verificar periódicmente la integridad de archivos.

- **Propósito**: Comprobar que los archivos originales no hayan sido modificados al realizar una comparación de los hashes.

- **Rol o área relacionada**: Detección.

- **Entradas esperadas**: 
Archivo de referencia con los hashes originales
    -Ejemplo: hashes_bd.csv
Rutas de los archivos a monitorear:
    -Ejemplo: ["C:\Windows\Firmware", "C:\Windows\Documents\Base_Datos.csv"]
              ["/etc/passwd", "/etc/shadow", "/home/tux/important_config.conf"]

- **Salidas esperadas**: Reporte comparando los hashes originales con los actuales, indicando si han sido modificados, eliminados o no existen.
    -Ejemplo:
    [/etc/passwd] [INTACTO]
    [/etc/shadow] [MODIFICADO]
    [/home/tux/important_config.conf] [NO ENCONTRADO]

    [C:\Windows\Firmware] [INTACTO]
    [C:\Windows\Documents\Base_Datos.csv] [ELIMINADO]

- **Descripción del procedimiento**: 
1. Leer el archivo con los hashes originales
2. Recorrer las rutas indicadas y calcular el hash del archivo
3. Comparar los hashes
4. Registrar los resultados en el reporte
5. Enviar alertas si se detectaron modificaciones, eliminaciones o nuevos archivos no registrados. 
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

### 🧠 Tarea 3 (opcional)
- **Título**: [Nombre de la tarea]
- **Propósito**: [2–3 frases que expliquen qué se busca lograr]
- **Rol o área relacionada**: [SOC, Red Team, DFIR, etc.]
- **Entradas esperadas**: [Formato y ejemplos]
- **Salidas esperadas**: [Formato y ejemplos]
- **Descripción del procedimiento**: [Narración funcional de lo que hará la tarea]
- **Complejidad técnica**: [Dimensiones que cubre: parsing, correlación, automatización, librerías]
- **Controles éticos**: [Uso de datos sintéticos, ambientes controlados, anonimización]
- **Dependencias**: [Librerías, comandos, entorno, variables de entorno]

---

## 🗂️ Estructura inicial del repositorio (ejemplo)
/src 
/scripts
/docs 
/examples 
/proposals 
/tests 
/prompts 
README.md (se revisará versión completa al final)
.gitignore

> Esta estructura puede crecer conforme avance el proyecto. Cada carpeta tendrá una función clara y estará documentada en `/docs`.

---

## 👥 Asignación de roles del equipo

| Integrante | Rol o responsabilidad |
|------------|------------------------|
| [Ana Lucia Alonso Martínez] | [Automatización de la comparación de hashes] |
| [Ana Laura Palacios Salazar] | [Ej. análisis y parsing] |
| [Maria Izabela Lorencez Narro] | [Ej. integración y orquestación] |

> Los roles pueden ajustarse conforme evolucione el proyecto.

---

## 🔐 Declaración ética y legal

Este proyecto se desarrollará exclusivamente con datos sintéticos o simulados. No se utilizarán datos reales, credenciales privadas ni información sensible. Todos los experimentos se ejecutarán en entornos controlados.  
El equipo se compromete a documentar cualquier riesgo ético y aplicar medidas de mitigación adecuadas.

---

## 🤝 Evidencia de colaboración inicial (elegir uno o más)

- [ ] Commits realizados por más de un integrante
- [ ] Issues creados para organizar tareas
- [ ] Pull requests abiertos o revisados
- [ ] Actividad visible en GitHub desde el inicio del proyecto

---

## 📁 Ubicación de entregables posteriores

Todos los avances y entregables estarán documentados en la carpeta `/docs` dentro de este mismo repositorio.
 
