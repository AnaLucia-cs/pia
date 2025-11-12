cd .\src
$archivo_rutas = Read-Host "Ingresa el nombre del archivo de rutas (por ejemplo, rutas.txt)"
python run_tarea1.py --input $archivo_rutas --db baseline.db --log logs.jsonl