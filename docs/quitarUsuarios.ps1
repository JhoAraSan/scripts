
# Cargar el ensamblado para usar el cuadro de diálogo de archivos
Add-Type -AssemblyName System.Windows.Forms

# Crear y configurar el diálogo
$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Title = "Selecciona el archivo CSV de usuarios"
$dialog.Filter = "Archivos CSV (*.csv)|*.csv|Todos los archivos (*.*)|*.*"
$dialog.Multiselect = $false

# Mostrar el diálogo y obtener el archivo seleccionado
$null = $dialog.ShowDialog()

# Validar selección
if (-not [string]::IsNullOrWhiteSpace($dialog.FileName)) {
    $csvPath = $dialog.FileName
    Write-Host "Archivo seleccionado: $csvPath" -ForegroundColor Cyan

    # Leer el archivo línea por línea
    $usuarios = Get-Content -Path $csvPath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }

    # Imprimir cada usuario
    $i = 1
    foreach ($usuario in $usuarios) {
        Write-Host ("{0}. Usuario: {1}" -f $i, $usuario)
        $i++
    }
} else {
    Write-Host "No se seleccionó ningún archivo. Saliendo..." -ForegroundColor Yellow
}
