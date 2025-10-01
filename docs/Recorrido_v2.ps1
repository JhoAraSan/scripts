Add-Type -AssemblyName System.Windows.Forms

function Select-FolderDialog {
    param([string]$Description = "Selecciona una carpeta")

    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = $Description
    $dialog.ShowNewFolderButton = $true

    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        return $dialog.SelectedPath
    }
    else {
        Write-Host "Operación cancelada por el usuario." -ForegroundColor Yellow
        exit
    }
}

# Solicita la carpeta raíz de la NAS
$rootPath = Select-FolderDialog -Description "Selecciona la carpeta raíz de la NAS"

# Verifica si existe
if (-Not (Test-Path $rootPath)) {
    Write-Host "La ruta especificada no existe. Verifica e intenta de nuevo." -ForegroundColor Red
    exit
}

# Solicita carpeta de destino para guardar el CSV
$outputFolder = Select-FolderDialog -Description "Selecciona la carpeta donde guardar el reporte CSV"

# Construye nombre automático para el archivo de salida
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = "extensiones_nas_$timestamp.csv"
$outputPath = Join-Path $outputFolder $outputFile

# Inicializa contadores
$script:folderCount = 0
$script:fileCount = 0
$script:totalSize = 0
$script:fileTypes = @{}

# Función recursiva para analizar carpetas
function Analyze-Folder {
    param ($path)

    try {
        $items = Get-ChildItem -Path $path -Force -ErrorAction Stop

        $script:folderCount++

        foreach ($item in $items) {
            if ($item.PSIsContainer) {
                Analyze-Folder -path $item.FullName
            }
            else {
                $script:fileCount++
                $script:totalSize += $item.Length

                $ext = $item.Extension.ToLower()
                if ($ext -eq "" -or $ext.Contains(" ") -or $ext -match "\s") { $ext = "[sin extensión]" }

                if (-not $script:fileTypes.ContainsKey($ext)) {
                    $script:fileTypes[$ext] = @{
                        Cantidad      = 0
                        TamanoTotalMB = 0.0
                    }
                }

                $script:fileTypes[$ext].Cantidad++
                $script:fileTypes[$ext].TamanoTotalMB += ($item.Length / 1MB)
            }
        }
    }
    catch {
        Write-Warning "No se pudo acceder a: $path - $_"
    }
}

# Ejecuta análisis
Write-Host "`nProcesando, esto puede tardar un momento..."
Analyze-Folder -path $rootPath

# Muestra solo resumen general
Write-Host "`nResumen de la NAS en: $rootPath"
Write-Host "Total de carpetas: $folderCount"
Write-Host "Total de archivos: $fileCount"
Write-Host ("Tamaño total de archivos: {0:N2} GB" -f ($totalSize / 1GB))

# Exporta al CSV
$fileTypes.GetEnumerator() | Sort-Object Name | ForEach-Object {
    [PSCustomObject]@{
        Extension       = $_.Key
        Cantidad        = $_.Value.Cantidad
        Tamano_Total_MB = [math]::Round($_.Value.TamanoTotalMB, 2)
    }
} | Export-Csv -Path $outputPath -NoTypeInformation -Encoding UTF8

Write-Host "`nReporte guardado en: $outputPath" -ForegroundColor Green

# --- IGNORE ---