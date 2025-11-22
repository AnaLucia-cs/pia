# tarea3.py
# Restaura archivos modificados o eliminados usando baseline.db

import argparse
import sqlite3
import shutil
import os
from pathlib import Path
import time
import json
import hashlib


def calcular_hash(path: Path, chunk_size=8192):
    """Calcula SHA256 para validar si el archivo está alterado."""
    sha256 = hashlib.sha256()
    try:
        with path.open("rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except:
        return None


def restaurar_archivo(ruta: Path, backup_folder: Path):
    """Copia archivo desde el backup hacia su ubicación original."""
    respaldo = backup_folder / ruta.name

    # Verifica que exista el archivo respaldado
    if not respaldo.exists():
        return False, f"No existe respaldo para {ruta}"

    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(respaldo, ruta)
        return True, "Archivo restaurado"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Restauración a partir de baseline")
    parser.add_argument("--db", required=True, help="Archivo baseline.db")
    parser.add_argument("--log", required=True, help="Archivo de log de restauración")
    parser.add_argument("--backup", default="backups", help="Carpeta donde están los respaldos")
    args = parser.parse_args()

    db_path = Path(args.db)
    log_path = Path(args.log)
    backup_folder = Path(args.backup)

    if not db_path.exists():
        print("❌ No existe baseline.db")
        return

    # Abrir DB
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    # Obtener registros
    c.execute("SELECT ruta, sha256 FROM baseline")
    registros = c.fetchall()

    log_data = []

    print("🔧 Iniciando restauración...")

    for ruta, sha256_base in registros:
        ruta = Path(ruta)

        entrada_log = {
            "ruta": str(ruta),
            "timestamp": time.time()
        }

        # Caso 1: archivo NO existe → restaurar
        if not ruta.exists():
            ok, msg = restaurar_archivo(ruta, backup_folder)
            entrada_log["estado"] = "restaurado_no_existia" if ok else "error"
            entrada_log["detalle"] = msg
            log_data.append(entrada_log)
            print(f"[REST] {ruta} → {msg}")
            continue

        # Caso 2: archivo existe → validar hash
        hash_actual = calcular_hash(ruta)

        if hash_actual != sha256_base:
            # Restaurar por integridad
            ok, msg = restaurar_archivo(ruta, backup_folder)
            entrada_log["estado"] = "restaurado_integridad" if ok else "error"
            entrada_log["detalle"] = msg
            log_data.append(entrada_log)
            print(f"[REST] {ruta} → {msg}")
        else:
            entrada_log["estado"] = "ok"
            entrada_log["detalle"] = "Sin cambios"
            log_data.append(entrada_log)

    # Guardar log
    with log_path.open("a", encoding="utf-8") as f:
        for entrada in log_data:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

    print("✔ Restauración completada.")


if __name__ == "__main__":
    main()
