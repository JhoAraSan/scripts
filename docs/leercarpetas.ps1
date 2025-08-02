Add-Type -AssemblyName System.Windows.Forms

# Abrir el explorador para seleccionar una carpeta
$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$folderBrowser.Description = "Selecciona la carpeta principal para analizar"

if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $selectedPath = $folderBrowser.SelectedPath
    $outputFile = Join-Path $selectedPath "lista_archivos.txt"

    # Recorrer subcarpetas y generar lista
    Get-ChildItem -Path $selectedPath -Recurse -File | ForEach-Object {
        $subfolder = Split-Path $_.DirectoryName -Leaf
        "$subfolder - $($_.Name)"
    } | Out-File -Encoding UTF8 $outputFile

    Write-Host "Archivo generado en: $outputFile"
} else {
    Write-Host "No se seleccionó ninguna carpeta."
}
