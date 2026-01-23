#Apartir de Un Archivo TXT ($rutaTxt) que tiene una lista de nombres se crean carpetas en ($rutaDestino)
$rutaDestino = "C:\Users\jhona\Downloads"
$rutaTxt = "C:\Users\jhona\Downloads\lista_archivos_20251229_171843.txt"

Get-Content $rutaTxt |
Where-Object { $_.Trim() -ne "" } |
ForEach-Object {
    $nombre = $_.Trim()
    New-Item -ItemType Directory -Path (Join-Path $rutaDestino $nombre) -ErrorAction SilentlyContinue
}
