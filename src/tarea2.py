# hash_baseline.py
# Propósito:
#   Verificar la integridad de archivos críticos del sistema
#   comparando sus valores hash (MD5) actuales con una “línea base”
#   almacenada en una base de datos SQLite.
# Entradas:
#   - Archivo con lista de rutas (TXT o JSON)
# Salidas:
#   - Base de datos SQLite (baseline.db)
#   - Archivos de registro: init_log.txt (legible) y logs.jsonl (estructurado)
#   - Archivo con el historial de modificaciones: historial_modif.txt
# Autor: [Ana Lucia Alonso Martinez]
# Fecha: [12/11/25]

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from pathlib import Path
import pandas as pd

#Obtener baseline desde base de datos
def obtener_baseline_hash():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(current_dir, "baseline.db")
    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("SELECT ruta,md5 FROM baseline;", conn)
    conn.close()
    dicc=df.to_dict(orient="records")
    return (dicc)


# Leer lista de rutas desde archivo .txt o .json
def leer_lista_rutas(path: Path):
    texto = path.read_text(encoding="utf-8").strip()
    if path.suffix.lower() == ".json":
        data = json.loads(texto)
        if isinstance(data, list):
            return [Path(p) for p in data]
        else:
            raise ValueError("El archivo JSON debe contener una lista de rutas.")
    else:
        lineas = [l.strip() for l in texto.splitlines() if l.strip() and not l.startswith('#')]
        return [Path(l) for l in lineas]


# Función: recorrer archivos (soporta directorios como en run_tarea1.py)
def recorrer_archivos(rutas):
    """
    Genera cada archivo encontrado en las rutas dadas.
    Si se pasa un directorio, recorre de forma recursiva.
    """
    vistos = set()
    for ruta in rutas:
        if ruta.exists():
            if ruta.is_file():
                yield ruta
            elif ruta.is_dir():
                for raiz, dirs, archivos in os.walk(ruta):
                    for f in archivos:
                        ruta_archivo = Path(raiz) / f
                        if str(ruta_archivo) not in vistos:
                            vistos.add(str(ruta_archivo))
                            yield ruta_archivo
        else:
            # Devuelve igual la ruta para registrar que no existe
            yield ruta


# Calcular hash MD5 de un archivo
def calcular_md5(archivo: Path, chunk_size=8192):
    """
    Calcula el hash MD5 de un archivo.
    """
    md5 = hashlib.md5()
    with archivo.open('rb') as f:
        while True:
            bloque = f.read(chunk_size)
            if not bloque:
                break
            md5.update(bloque)
    return md5.hexdigest()


# Generar diccionario de rutas actuales y sus hashes
def generar_diccionario_hashes(archivo_rutas: str):
    """
    Lee las rutas, calcula su hash y las devuelve en un diccionario
    """
    rutas = leer_lista_rutas(Path(archivo_rutas))
    diccionario = {}

    for ruta in rutas:
        if ruta.exists() and ruta.is_file():
            try:
                diccionario[str(ruta)] = calcular_md5(ruta)
            except Exception as e:
                diccionario[str(ruta)] = f"Error: {e}"
        else:
            diccionario[str(ruta)] = "No existe o no es archivo"
    return diccionario

# Comparar hashes actuales con el baseline
def comparar_con_baseline(hashes_actuales, baseline):
    """
    Compara los hashes actuales con el baseline y muestra las diferencias.
    """
    # Resultado estructurado
    resultado = {
        'nuevos': [],
        'modificados': [],
        'sin_cambios': [],
        'eliminados': [],
        'errores': []
    }

    # Convertir baseline (lista de dicts) a mapa para búsquedas rápidas
    baseline_map = {item['ruta']: item.get('md5') for item in baseline}

    # Revisar los hashes actuales
    for ruta, hash_actual in hashes_actuales.items():
        # Manejo de errores en el cálculo del hash
        if isinstance(hash_actual, str) and hash_actual.startswith("Error:"):
            resultado['errores'].append({'ruta': ruta, 'error': hash_actual})
            continue
        if hash_actual == "No existe o no es archivo":
            # Si en baseline estaba y ahora no existe -> eliminado
            if ruta in baseline_map:
                resultado['eliminados'].append(ruta)
            else:
                resultado['errores'].append({'ruta': ruta, 'error': 'No existe o no es archivo'})
            continue

        hash_baseline = baseline_map.get(ruta)
        if hash_baseline is None:
            resultado['nuevos'].append(ruta)
        elif hash_actual != hash_baseline:
            resultado['modificados'].append(ruta)
        else:
            resultado['sin_cambios'].append(ruta)

    # Archivos que estaban en el baseline pero no aparecen en los actuales -> eliminados
    for ruta in baseline_map.keys():
        if ruta not in hashes_actuales:
            resultado['eliminados'].append(ruta)

    # Mostrar resumen legible
    print("\nResumen de comparación:")
    for key in ('nuevos', 'modificados', 'eliminados', 'sin_cambios', 'errores'):
        items = resultado[key]
        if not items:
            continue
        print(f"  {key} ({len(items)}):")
        for it in items:
            if isinstance(it, dict):
                print(f"    - {it.get('ruta')}: {it.get('error')}")
            else:
                print(f"    - {it}")

    return resultado

# Principal con logging similar a run_tarea1.py
def main(args=None):
    parser = argparse.ArgumentParser(
        description="Comparar hashes actuales con baseline y generar logs (JSONL)"
    )
    parser.add_argument("--input", "-i", default="rutas.txt", help="Archivo con lista de rutas (txt o json)")
    parser.add_argument("--db", "-d", default="baseline.db", help="Archivo SQLite del baseline")
    parser.add_argument("--log", "-l", default="logs.jsonl", help="Archivo de logs JSON lines (logs.jsonl)")
    parser.add_argument("--initlog", default="init_log.txt", help="Archivo de log inicial (texto legible)")
    parser.add_argument("--summary", "-s", default="comparison_summary.txt", help="Archivo .txt con resumen legible de la comparación")
    args = parser.parse_args(args=args)

    archivo_entrada = Path(args.input)
    db_path = Path(args.db)
    log_path = Path(args.log)
    initlog_path = Path(args.initlog)
    summary_path = Path(args.summary)

    # Preparar archivos de log
    log_fh = log_path.open('a', encoding='utf-8')
    with initlog_path.open('a', encoding='utf-8') as init_f:
        init_f.write(f"Comparación de hashes - iniciada: {time.asctime()}\n")
        init_f.write(f"Archivo de entrada: {archivo_entrada}\n")
        init_f.write(f"Base de datos baseline: {db_path}\n")
        init_f.write(f"Archivo de log JSONL: {log_path}\n")
        init_f.write(f"Archivo con historial de cambios: {summary_path}\n\n")


    # Leer rutas y procesar (se usa recorrer_archivos para soportar directorios)
    rutas = leer_lista_rutas(archivo_entrada)
    hashes_actuales = {}

    for p in recorrer_archivos(rutas):
        entrada = {
            "ruta": str(p),
            "existe": p.exists(),
            "es_archivo": p.is_file() if p.exists() else False,
            "timestamp": time.time()
        }

        if not p.exists():
            entrada["estado"] = "no_encontrado"
            log_fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")
            # Registrar en hashes_actuales para que la comparación pueda marcar error si se desea
            hashes_actuales[str(p)] = "No existe o no es archivo"
            continue

        if not p.is_file():
            entrada["estado"] = "omitido_no_archivo"
            log_fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")
            hashes_actuales[str(p)] = "No existe o no es archivo"
            continue

        try:
            md5 = calcular_md5(p)
            info = p.stat()
            entrada.update({
                "tamaño_bytes": info.st_size,
                "modificado_en": info.st_mtime,
                "md5": md5,
                "estado": "ok"
            })
            hashes_actuales[str(p)] = md5
        except Exception as e:
            entrada.update({"error": str(e), "estado": "error"})
            hashes_actuales[str(p)] = f"Error: {e}"

        log_fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")

    # Cerrar log fh
    log_fh.close()

    # Obtener baseline y comparar
    baseline = obtener_baseline_hash()
    resultado = comparar_con_baseline(hashes_actuales, baseline)

    # Impresión final del resultado estructurado (puede usarse posteriormente)
    print("\nResultado estructurado devuelto por comparar_con_baseline:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Escribir resumen legible en archivo .txt con fecha y estado por ruta
    summary_path = Path(args.summary)
    with summary_path.open('a', encoding='utf-8') as sf:
        sf.write(f"Ejecución: {time.asctime()}\n")
        # ordenar para lectura estable
        for ruta in sorted(resultado.get('nuevos', [])):
            sf.write(f"{ruta}: CREADA\n")
        for ruta in sorted(resultado.get('modificados', [])):
            sf.write(f"{ruta}: MODIFICADA\n")
        for ruta in sorted(resultado.get('eliminados', [])):
            sf.write(f"{ruta}: ELIMINADA\n")
        for ruta in sorted(resultado.get('sin_cambios', [])):
            sf.write(f"{ruta}: INTACTA\n")
        for e in resultado.get('errores', []):
            # errores contienen dicts con ruta y error
            ruta = e.get('ruta') if isinstance(e, dict) else str(e)
            err = e.get('error') if isinstance(e, dict) else ''
            sf.write(f"{ruta}: ERROR - {err}\n")
        sf.write("\n")


if __name__ == "__main__":
    main()
    print("\n Ejecución completada correctamente. Revisa 'logs.jsonl' e 'historial_modif.txt'. \n")
