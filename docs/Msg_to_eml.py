import os
import extract_msg  # pip install extract-msg
from email.message import EmailMessage
from email.utils import formatdate
from tkinter import filedialog, Tk

def convertir_msg_a_eml(ruta_msg, carpeta_salida):
    msg = extract_msg.Message(ruta_msg)
    msg_sender = msg.sender or ""
    msg_to = msg.to or ""
    msg_subject = msg.subject or ""
    msg_date = msg.date or ""
    msg_body = msg.body or ""

    eml = EmailMessage()
    eml['From'] = msg_sender
    eml['To'] = msg_to
    eml['Subject'] = msg_subject
    eml['Date'] = formatdate()

    eml.set_content(msg_body)

    for adjunto in msg.attachments:
        nombre = adjunto.longFilename or adjunto.shortFilename or "adjunto.bin"
        nombre = nombre.replace('\x00', '_')
        contenido = adjunto.data
        eml.add_attachment(contenido, maintype='application', subtype='octet-stream', filename=nombre)

    nombre_eml = os.path.splitext(os.path.basename(ruta_msg))[0] + ".eml"
    ruta_eml = os.path.join(carpeta_salida, nombre_eml)
    with open(ruta_eml, 'wb') as f:
        f.write(eml.as_bytes())

    print(f"✅ Convertido: {ruta_eml}")

def seleccionar_y_convertir():
    root = Tk()
    root.withdraw()
    archivos_msg = filedialog.askopenfilenames(title="Selecciona archivos .msg", filetypes=[("MSG files", "*.msg")])
    if not archivos_msg:
        return
    carpeta_salida = filedialog.askdirectory(title="Selecciona carpeta de salida")
    if not carpeta_salida:
        return
    for archivo in archivos_msg:
        convertir_msg_a_eml(archivo, carpeta_salida)

if __name__ == "__main__":
    seleccionar_y_convertir()