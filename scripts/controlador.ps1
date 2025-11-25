cd C:\Users\Iza\Documents\GitHub\pia\src
# Se necesita 'Install-Module -Name ImportExcel -Scope CurrentUser'

$x = $true

while ($x -eq $true) {
    Write-Host "`nMENU DE OPCIONES"
    Write-Host "a) Generar línea base de hashes"
    Write-Host "b) Verificar integridad de archivos"
    Write-Host "c) Generar reporte"
    Write-Host "d) Salir"
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
            
            # Ejecutar Tarea 2 (verificción de Integridad)
            python tarea2.py -i $archivo_rutas -d baseline.db -l logs.jsonl -s comparison_summary.txt --initlog init_log.txt

            # Ejecuta análisis de IA (analiza historial_modif.txt y recomienda acciones)
            python analisis_ia.py

            # Pregunta al usuario si desea restaurar
            $respuesta_restaurar = Read-Host "¿Deseas restaurar archivos modificados? (s/n)"
            if ($respuesta_restaurar -eq "s") {
                python tarea3.py --db baseline.db --log restore_log.txt --backup backups
            }

            # Preguntar si vuelve al menú
            $respuesta = Read-Host "¿Volver al menú? (s/n)"
            if ($respuesta -ne "s") {
                $x = $false
                Write-Host "Saliendo..."
            }
        }
        
        "c" {
            Write-Host "`n--- GENERADOR DE REPORTES ---"

            Write-Host "1) Generar reporte en TXT"
            Write-Host "2) Generar reporte en Excel (.xlsx)"
            $tipo = Read-Host "Selecciona el tipo de reporte"

            # Archivos que se incluirán en el reporte
            $archivos = @(
                "comparison_summary.txt",
                "logs.jsonl",
                "init_log.txt",
                "restore_log.txt"
            )

            $reporte = Read-Host "Nombre del archivo de reporte (sin extensión)"

            if ($tipo -eq "1") {
                $output = "$reporte.txt"
                Write-Host "Generando reporte TXT..."

                foreach ($file in $archivos) {
                    if (Test-Path $file) {
                        Add-Content $output "`n===== $file ====="
                        Add-Content $output (Get-Content $file)
                    } else {
                        Add-Content $output "`n[ADVERTENCIA] No se encontró el archivo $file"
                    }
                }

                Write-Host "Reporte generado: $output"
            }

            elseif ($tipo -eq "2") {
                $output = "$reporte.xlsx"
                Write-Host "Generando reporte Excel..."

                foreach ($file in $archivos) {
                    if (Test-Path $file) {
                        $contenido = Get-Content $file | ConvertFrom-String
                        $contenido | Export-Excel -WorksheetName $file -Path $output -AutoSize -Append
                    } else {
                        $nota = [PSCustomObject]@{
                            Mensaje = "No se encontró el archivo $file"
                        }
                        $nota | Export-Excel -WorksheetName $file -Path $output -AutoSize -Append
                    }
                }

                Write-Host "Reporte generado: $output"
            }

            else {
                Write-Host "Opción inválida"
            }
        }

        "d" {
            Write-Host "Saliendo..."
            $x = $false
        }

        default {
            Write-Host "Opción no válida"
        }
    }
}
