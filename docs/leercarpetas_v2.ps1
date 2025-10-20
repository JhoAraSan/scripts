Add-Type -AssemblyName System.Windows.Forms

# Función para formatear tamaño legible
function Format-Size($bytes) {
    if ($bytes -ge 1GB) {
        return "{0:N2} GB" -f ($bytes / 1GB)
    }
    elseif ($bytes -ge 1MB) {
        return "{0:N2} MB" -f ($bytes / 1MB)
    }
    elseif ($bytes -ge 1KB) {
        return "{0:N2} KB" -f ($bytes / 1KB)
    }
    else {
        return "$bytes B"
    }
}

# Seleccionar carpeta principal para analizar
$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$folderBrowser.Description = "Selecciona la carpeta principal para analizar"

if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $selectedPath = $folderBrowser.SelectedPath

    # Seleccionar carpeta destino donde guardar el TXT
    $saveFolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $saveFolderBrowser.Description = "Selecciona la carpeta donde guardar el archivo de salida"
    if ($saveFolderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $outputPath = $saveFolderBrowser.SelectedPath

        # Generar nombre con timestamp
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $outputFile = Join-Path $outputPath "lista_archivos_$timestamp.txt"

        # Obtener todos los archivos
        $files = Get-ChildItem -Path $selectedPath -Recurse -File

        # Generar resumen por extensión
        $summary = $files | Group-Object Extension | ForEach-Object {
            $ext = if ([string]::IsNullOrEmpty($_.Name)) { "[Sin extensión]" } else { $_.Name }
            $count = $_.Count
            $totalSize = ($_.Group | Measure-Object Length -Sum).Sum
            $readableSize = Format-Size $totalSize
            "{0,-15} Archivos: {1,6}   Tamaño total: {2}" -f $ext, $count, $readableSize
        }

        # Escribir resumen al archivo
        "==== RESUMEN POR EXTENSIÓN ====" | Out-File -Encoding UTF8 $outputFile
        $summary | Out-File -Encoding UTF8 -Append $outputFile
        "" | Out-File -Encoding UTF8 -Append $outputFile
        "==== LISTADO DE ARCHIVOS ====" | Out-File -Encoding UTF8 -Append $outputFile

        # Escribir lista de archivos (ruta relativa)
        $files | ForEach-Object {
            $relativePath = $_.FullName.Substring($selectedPath.Length + 1)
            $relativePath
        } | Out-File -Encoding UTF8 -Append $outputFile

        Write-Host "Archivo generado en: $outputFile"
    }
    else {
        Write-Host "No se seleccionó carpeta de salida."
    }
}
else {
    Write-Host "No se seleccionó ninguna carpeta."
}
