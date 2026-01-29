# This script concatenates all Markdown (.md) files from a selected directory and its subdirectories into a single Markdown file.

[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") | Out-Null

$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$folderBrowser.Description = "Selecciona la carpeta principal para analizar"

if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $sourcePath = $folderBrowser.SelectedPath
    $files = Get-ChildItem -Path $sourcePath -Filter "*.md" -Recurse

    # Seleccionar carpeta destino donde guardar el .md
    $saveFolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $saveFolderBrowser.Description = "Selecciona la carpeta donde guardar el archivo de salida"
    
    if ($saveFolderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        # Generar nombre con timestamp
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $output = Join-Path $saveFolderBrowser.SelectedPath "Complete_$timestamp.md"
        
        # Crear archivo vacío primero
        New-Item -Path $output -ItemType File -Force | Out-Null
        
        # Agregar contenido
        foreach ($file in $files) {
            Add-Content -Path $output -Value "# Archivo: $($file.Name)`n"
            Add-Content -Path $output -Value (Get-Content $file.FullName -Raw)
            Add-Content -Path $output -Value "`n`n---`n`n"
        }
        
        Write-Host "✓ Archivo creado exitosamente en: $output" -ForegroundColor Green
    }
}