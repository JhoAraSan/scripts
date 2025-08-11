import os
import re
import requests
from deep_translator import GoogleTranslator #pip install 

def obtener_ipa_uk_us(palabra, idioma="en", profundidad=0):
    url = f"https://{idioma}.wiktionary.org/w/api.php"
    params = {
        "action": "query",
        "titles": palabra,
        "prop": "revisions",
        "rvprop": "content",
        "format": "json",
        "formatversion": 2
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None

    try:
        contenido = r.json()["query"]["pages"][0]["revisions"][0]["content"]
    except (KeyError, IndexError):
        return None

    ipa_uk = []
    ipa_us = []

    # Buscar IPA etiquetada como UK
    for match in re.finditer(r"\{\{IPA\|en\|([^}]+?)\}\}", contenido):
        partes = match.group(1).split("|")
        if "a=UK" in partes:
            ipa_uk.extend([p for p in partes if p.startswith("/")])
        elif not any(p.startswith("a=") for p in partes):
            ipa_us.extend([p for p in partes if p.startswith("/")])

  # Plan B: buscar palabra origen si no hay IPA y no hemos recursado aún
    if not ipa_uk and not ipa_us and profundidad == 0:
        origen_match = re.search(r"(?:from|From)\s+\{\{af\|en\|([A-Za-z\-]+)\|", contenido)
        if origen_match:
            palabra_origen = origen_match.group(1)
            print(f"⚠ No se encontró IPA para '{palabra}', intentando con su origen '{palabra_origen}'...")
            resultado = obtener_ipa_uk_us(palabra_origen, idioma, profundidad=1)
            if resultado: resultado["Origen"] = palabra_origen
            return resultado


    # Limpiar duplicados
    ipa_uk = sorted(set(ipa_uk))
    ipa_us = sorted(set(ipa_us))

    dict_ipa = {"UK": ipa_uk, "US": ipa_us, "Origen": None}

    html_text = ""
    has_ipa = False
    for key, value in dict_ipa.items():
        if isinstance(value, list) and value:
            html_text += f"{key}: {value[0]}<br> "
            has_ipa = True
        elif isinstance(value, str):
            html_text += f"{key}: {value}<br> "
            has_ipa = True
    if not has_ipa:
        html_text = None

    return html_text

def obtener_datos(palabra, idioma):
    codigos = {
        "ingles": "en",
        "frances": "fr",
        "portugues": "pt"
    }

    if idioma not in codigos:
        print("Idioma no soportado.")
        return None

    codigo_idioma = codigos[idioma]
    url = f"https://api.dictionaryapi.dev/api/v2/entries/{codigo_idioma}/{palabra[0]}"
    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        print(f"No se encontró la palabra '{palabra[0]}' en {idioma}.")
        return None

    datos = respuesta.json()

    try:
        ejemplos = []
        # Obtener IPA
        ipa = obtener_ipa_uk_us(palabra, codigo_idioma)
        if ipa == None:
            ipa = datos[0].get("phonetic", "")
            if not ipa and "phonetics" in datos[0]:
                for p in datos[0]["phonetics"]:
                    if "text" in p:
                        ipa = p["text"]
                        break
        for meaning in datos[0].get("meanings", []):
            for definicion in meaning.get("definitions", []):
                if "example" in definicion:
                    ejemplos.append(definicion["example"])

    except (IndexError, KeyError):
        return None

    # Traducciones al español
    traductor = GoogleTranslator(source=codigo_idioma, target="es")
    significado_es = traductor.translate(palabra[0])

    palabra_principal = f"<b>{palabra[0]}</b>"
    resto = " ".join(palabra[1:])
    resto_formateado = f"<i style='color: gray;'>{resto}</i>"

    return f"{palabra_principal} {resto_formateado} | {ipa} | {significado_es} | {'<br>'.join(ejemplos)}"

def guardar_txt(linea, nombre_archivo="resultado.txt"):
    # Si el archivo no existe, escribimos el encabezado primero
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(linea + "\n")
    else:
        with open(nombre_archivo, "a", encoding="utf-8") as f:
            f.write(linea + "\n")

if __name__ == "__main__":
    idioma = input("Introduce el idioma (ingles, frances, portugues): ").lower()
    Palabras = []

    print("Introduce las palabras que deseas añadir al diccionario. Presiona Enter sin escribir nada para finalizar:")
    while True:
        inputs = input()
        if inputs:
            Palabras.append(inputs)
        else:
            break

    for palabra in Palabras:
        palabra = palabra.split()
        datos = obtener_datos(palabra, idioma)
        if datos:
            guardar_txt(datos)
            print(f"✅ Palabra '{palabra[0]}' añadida al diccionario.")

