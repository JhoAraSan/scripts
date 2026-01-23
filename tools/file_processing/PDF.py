from PyPDF2 import PdfMerger, PdfFileReader #pip install PyPDF2
import os

import tkinter as tk
from tkinter import filedialog, ttk
import sys

def seleccionar_archivos_pdf():
    """
    Abre una ventana para seleccionar múltiples archivos PDF.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter

    file_paths = filedialog.askopenfilenames(
        title="Seleccionar archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")]  # Opcional: Filtra por tipo de archivo
    )
    merger = PdfMerger()
    if file_paths:
        for path in file_paths:
            merger.append(path)
            
    else:
        return None
    # Guardar el archivo PDF combinado
    output_path = filedialog.asksaveasfilename(
        title="Guardar archivo PDF combinado",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]  # Opcional: Filtra por tipo de archivo
    )
    if not output_path:
        return None
    # Verifica si el archivo ya existe y pregunta al usuario si desea sobrescribirlo
    if os.path.exists(output_path):
        overwrite = tk.messagebox.askyesno(
            "Archivo existente",
            f"El archivo '{output_path}' ya existe. ¿Desea sobrescribirlo?"
        )
        if not overwrite:
            return None
    # Guardar el archivo combinado
    merger.write(output_path)
    # Cerrar el objeto PdfMerger
    merger.close()
    return True

def reordenar_paginas_pdf():
    """
    Selecciona un archivo PDF, solicita un nuevo orden de páginas y guarda un PDF reordenado.
    """
    import tkinter as tk
    from tkinter import filedialog, simpledialog, messagebox
    import os
    from PyPDF2 import PdfReader, PdfWriter

    root = tk.Tk()
    root.withdraw()

    # Seleccionar archivo PDF
    input_path = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if not input_path:
        return

    reader = PdfReader(input_path)
    num_pages = len(reader.pages)

    # Solicitar orden de páginas
    orden_str = simpledialog.askstring(
        "Nuevo orden de páginas",
        f"Ingrese el nuevo orden (0 a {num_pages - 1}, separados por comas):"
    )
    if not orden_str:
        return

    try:
        nuevo_orden = [int(x.strip()) for x in orden_str.split(",")]
        if any(i < 0 or i >= num_pages for i in nuevo_orden):
            raise ValueError("Alguno de los índices está fuera del rango.")
    except Exception as e:
        messagebox.showerror("Error", f"Orden inválido: {e}")
        return

    # Guardar el nuevo PDF
    output_path = filedialog.asksaveasfilename(
        title="Guardar PDF reordenado",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if not output_path:
        return

    writer = PdfWriter()
    for i in nuevo_orden:
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    messagebox.showinfo("Éxito", "PDF reordenado guardado con éxito.")


def ventana_principal():
    """
    Crea una ventana con dos botones para combinar PDFs o reordenar páginas.
    """
    root = tk.Tk()
    root.title("Herramienta PDF")
    root.geometry("300x150")
    root.resizable(False, False)

    def on_close():
        root.destroy()
        sys.exit()  # <- Forzar cierre del script completamente
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Título
    label = ttk.Label(root, text="¿Qué desea hacer?", font=("Arial", 14))
    label.pack(pady=10)

    # Botón: Combinar PDFs
    boton_combinar = ttk.Button(root, text="Combinar PDFs", command=seleccionar_archivos_pdf)
    boton_combinar.pack(pady=5, fill="x", padx=40)

    # Botón: Reordenar páginas
    boton_reordenar = ttk.Button(root, text="Reordenar páginas", command=reordenar_paginas_pdf)
    boton_reordenar.pack(pady=5, fill="x", padx=40)

    # Ejecutar ventana
    root.mainloop()

if __name__ == "__main__":
    ventana_principal()