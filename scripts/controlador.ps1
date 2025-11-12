cd C:\Users\Nana\Documents\GitHub\pia\src

$x = $true

while ($x -eq $true) {
    Write-Host "`nMENU DE OPCIONES"
    Write-Host "a) Generar línea base de hashes"
    Write-Host "b) Verificar integridad de archivos"
    Write-Host "c) Salir"
    $opcion = Read-Host "Elige una opción"

    switch ($opcion) {
        "a" {
            $archivo_rutas = Read-Host "Ingresa el nombre del archivo con las rutas a registrar (por ejemplo, rutas.txt)"
            python run_tarea1.py --input $archivo_rutas --db baseline.db --log logs.jsonl
            $respuesta = Read-Host "¿Volver al menú? (s/n)"
            if ($respuesta -ne "s") {
                $x = $false
                Write-Host "Saliendo..."
            }
        }

        "b" {
            $archivo_rutas = Read-Host "Ingresa el nombre del archivo con las rutas a comparar (por ejemplo, rutas.txt)"
            python tarea2.py -i $archivo_rutas -d baseline.db -l logs.jsonl -s historial_modif.txt --initlog init_log.txt
            $respuesta = Read-Host "¿Volver al menú? (s/n)"
            if ($respuesta -ne "s") {
                $x = $false
                Write-Host "Saliendo..."
            }
        }

        "c" {
            Write-Host "Saliendo..."
            $x = $false
        }

        default {
            Write-Host "Opción no válida"
        }
    }
}
