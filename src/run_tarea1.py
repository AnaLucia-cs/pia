#!/usr/bin/env python3
# -----------------------------------------------------------
# hash_baseline.py
# -----------------------------------------------------------
# Propósito:
#   Generar una base de datos con los valores hash (MD5 y SHA256)
#   de archivos críticos del sistema, para crear una “línea base”
#   que sirva como referencia del estado limpio del sistema.
#
# Entradas:
#   - Archivo con lista de rutas (TXT o JSON)
#
# Salidas:
#   - Base de datos SQLite (baseline.db)
#   - Archivos de registro: init_log.txt (legible) y logs.jsonl (estructurado)
#
# Autor: [Ana Laura Palacios Salazar]
# Fecha: [09/11/25]
# -----------------------------------------------------------

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from pathlib import Path


# -----------------------------------------------------------
# Función: leer lista de archivos
# -----------------------------------------------------------
def leer_lista_rutas(path: Path):
    """
    Lee una lista de rutas desde un archivo .txt o .json
    """
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


# -----------------------------------------------------------
# Función: recorrer archivos
# -----------------------------------------------------------
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


# -----------------------------------------------------------
# Función: calcular hashes
# -----------------------------------------------------------
def calcular_hash(archivo: Path, chunk_size=8192):
    """
    Calcula los hashes MD5 y SHA256 de un archivo.
    """
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    try:
        with archivo.open('rb') as f:
            while True:
                bloque = f.read(chunk_size)
                if not bloque:
                    break
                md5.update(bloque)
                sha256.update(bloque)
        return md5.hexdigest(), sha256.hexdigest(), None
    except Exception as e:
        return None, None, str(e)


# -----------------------------------------------------------
# Función: crear base de datos
# -----------------------------------------------------------
def asegurar_base(conn: sqlite3.Connection):
    """
    Crea la tabla baseline si no existe.
    """
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS baseline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ruta TEXT UNIQUE,
            md5 TEXT,
            sha256 TEXT,
            tamaño INTEGER,
            mtime REAL,
            procesado_en REAL
        )
    """)
    conn.commit()


# -----------------------------------------------------------
# Función: guardar registro
# -----------------------------------------------------------
def guardar_registro(conn: sqlite3.Connection, ruta: str, md5: str, sha256: str, tamaño: int, mtime: float):
    """
    Inserta o actualiza un registro en la base de datos.
    """
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO baseline (ruta, md5, sha256, tamaño, mtime, procesado_en)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ruta, md5, sha256, tamaño, mtime, time.time()))
    conn.commit()


# -----------------------------------------------------------
# Función: restringir permisos del archivo
# -----------------------------------------------------------
def restringir_permisos(path: Path):
    """
    Intenta aplicar permisos 600 (solo dueño) en sistemas compatibles.
    """
    try:
        path.chmod(0o600)
    except Exception:
        pass  # Ignorar en sistemas que no lo soportan


# -----------------------------------------------------------
# Función principal
# -----------------------------------------------------------
def main(args=None):
    parser = argparse.ArgumentParser(
        description="Generar baseline de hashes (MD5, SHA256) de archivos críticos del sistema"
    )
    parser.add_argument("--input", "-i", required=True, help="Archivo con lista de rutas (txt o json)")
    parser.add_argument("--db", "-d", required=True, help="Archivo SQLite de salida (baseline.db)")
    parser.add_argument("--log", "-l", required=True, help="Archivo de logs JSON lines (logs.jsonl)")
    parser.add_argument("--initlog", default="init_log.txt", help="Archivo de log inicial (texto legible)")
    args = parser.parse_args(args=args)

    archivo_entrada = Path(args.input)
    db_path = Path(args.db)
    log_path = Path(args.log)
    initlog_path = Path(args.initlog)

    if not archivo_entrada.exists():
        print(f"❌ Error: el archivo de entrada {archivo_entrada} no existe.", file=sys.stderr)
        sys.exit(2)

    rutas = leer_lista_rutas(archivo_entrada)

    # Crear base de datos y tabla
    conn = sqlite3.connect(str(db_path))
    asegurar_base(conn)
    restringir_permisos(db_path)

    # Abrir logs
    log_fh = log_path.open('a', encoding='utf-8')
    with initlog_path.open('a', encoding='utf-8') as init_f:
        init_f.write(f"Ejecución iniciada: {time.asctime()}\n")
        init_f.write(f"Archivo de entrada: {archivo_entrada}\n")
        init_f.write(f"Base de datos: {db_path}\n")
        init_f.write(f"Archivo de log JSONL: {log_path}\n\n")

    # Procesar rutas
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
            continue

        if not p.is_file():
            entrada["estado"] = "omitido_no_archivo"
            log_fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")
            continue

        md5, sha256, error = calcular_hash(p)
        info = p.stat()
        entrada.update({
            "tamaño_bytes": info.st_size,
            "modificado_en": info.st_mtime,
            "md5": md5,
            "sha256": sha256,
            "error": error,
            "estado": "ok" if error is None else "error"
        })

        log_fh.write(json.dumps(entrada, ensure_ascii=False) + "\n")

        if error is None:
            guardar_registro(conn, str(p), md5, sha256, info.st_size, info.st_mtime)

    log_fh.close()
    conn.close()

    print("✅ Ejecución completada correctamente. Revisa 'logs.jsonl' y 'baseline.db'.")


# -----------------------------------------------------------
# Punto de entrada
# -----------------------------------------------------------
if __name__ == "__main__":
    main()
