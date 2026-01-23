# Crear lista de idioma con inglés (Estados Unidos)
$languageList = New-WinUserLanguageList -Language "en-US"

# Limpiar métodos de entrada existentes
$languageList[0].InputMethodTips.Clear()

# Agregar Latin American
$languageList[0].InputMethodTips.Add("0409:0000080A")  # Latin American

# Agregar United States-International
$languageList[0].InputMethodTips.Add("0409:00020409")  # US-International

# Aplicar la configuración
Set-WinUserLanguageList $languageList -Force