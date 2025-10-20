Add-Type -AssemblyName Microsoft.VisualBasic
Add-Type -AssemblyName System.Windows.Forms

# Seleccionar archivo PST
$OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$OpenFileDialog.Filter = "Outlook PST files (*.pst)|*.pst"
$OpenFileDialog.Title = "Selecciona el archivo PST"
$null = $OpenFileDialog.ShowDialog()
if (-not $OpenFileDialog.FileName) { exit }
$pstPath = $OpenFileDialog.FileName

# Palabra clave
$keyword = [Microsoft.VisualBasic.Interaction]::InputBox("Escribe la palabra clave a buscar:", "Buscar palabra clave")
if (-not $keyword) { exit }

# Fecha de inicio
$startDateInput = [Microsoft.VisualBasic.Interaction]::InputBox("Fecha de inicio (yyyy-mm-dd):", "Rango de fechas")
try { $startDate = [DateTime]::ParseExact($startDateInput, 'yyyy-MM-dd', $null) } catch { Write-Host "Fecha inválida"; exit }

# Fecha de fin
$endDateInput = [Microsoft.VisualBasic.Interaction]::InputBox("Fecha de fin (yyyy-mm-dd):", "Rango de fechas")
try { $endDate = [DateTime]::ParseExact($endDateInput, 'yyyy-MM-dd', $null).AddDays(1).AddSeconds(-1) } catch { Write-Host "Fecha inválida"; exit }

# Carpeta de exportación
$FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$null = $FolderBrowser.ShowDialog()
if (-not $FolderBrowser.SelectedPath) { exit }
$exportPath = $FolderBrowser.SelectedPath

# Iniciar Outlook y cargar PST
$outlook = New-Object -ComObject Outlook.Application
$namespace = $outlook.GetNamespace("MAPI")
$namespace.AddStore($pstPath)

# Nombre del PST
$pstName = [System.IO.Path]::GetFileNameWithoutExtension($pstPath)
$pstFolder = $namespace.Folders.Item($pstName)

# Función para limpiar nombres
function Limpiar-NombreArchivo($nombre) {
    $limpio = $nombre -replace '[\\/:*?"<>|]', ''
    return $limpio.Substring(0, [Math]::Min(100, $limpio.Length))
}

# Función recursiva para buscar en todas las carpetas
function Buscar-Correos($folder) {
    foreach ($item in $folder.Items) {
        try {
            if ($item.ReceivedTime -ge $startDate -and $item.ReceivedTime -le $endDate) {
                if ($item.Subject -like "*$keyword*" -or $item.Body -like "*$keyword*") {
                    $asunto = if ($item.Subject) { $item.Subject } else { "SinAsunto_$global:contador" }
                    $nombreArchivo = Limpiar-NombreArchivo($asunto)
                    $rutaArchivo = Join-Path $exportPath "$nombreArchivo.msg"
                    $item.SaveAs($rutaArchivo, 3)
                    $global:contador++
                }
            }
        } catch {}
    }
    foreach ($subfolder in $folder.Folders) {
        Buscar-Correos $subfolder
    }
}

# Buscar correos
$global:contador = 0
Buscar-Correos $pstFolder

Write-Host "`nSe exportaron $global:contador correos con '$keyword' entre $startDateInput y $endDateInput."
Write-Host "Guardados en: $exportPath"
