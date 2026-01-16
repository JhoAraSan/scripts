# Ruta del archivo CSV
$csvPath = "Y:\OneDrive - Colombia Compra Eficiente\Escritorio\usuarios.csv"

# Leer el archivo CSV
$usuarios = Get-Content -Path $csvPath

# Imprimir cada usuario
foreach ($usuario in $usuarios) {
# para validar la informacion apartir de nombres ---> Get-ADUser -Filter "Name -like '*$usuario*'" | Select-Object Name, SamAccountName
  Set-ADUser -Identity $usuario  -AccountExpirationDate 2025-12-19T09:30:00Z
  Update-Recipient -Identity $usuario
  Get-ADUser -Identity $usuario -Properties AccountExpirationDate, accountExpires | Format-List SamAccountName, AccountExpirationDate, accountExpires
}

for /f "delims=" %i in ("C:\Users\jhona\Downloads\lista_archivos_20251229_171843.txt") do mkdir "%i" 