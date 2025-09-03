import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import re
import os
from datetime import datetime


def analizar_svg(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        contenido = f.read()

    hallazgos = []
    clasificacion = "✅ Limpio"

    # Buscar URLs
    urls = re.findall(r'(https?://[^\s"<>]+)', contenido)
    if urls:
        hallazgos.append("⚠️ URLs encontradas:")
        hallazgos.extend(urls)
        clasificacion = "⚠️ Advertencia"

    # Buscar scripts
    if "<script" in contenido.lower():
        hallazgos.append("❌ Contiene <script> embebido")
        clasificacion = "❌ Peligroso"

    # Buscar data:base64
    data_uri = re.findall(r'data:[^;]+;base64,[A-Za-z0-9+/=]+', contenido)
    if data_uri:
        hallazgos.append("❌ Contiene payload embebido en Base64")
        clasificacion = "❌ Peligroso"

    return clasificacion, hallazgos


def generar_reporte(carpeta, resultados):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reporte_nombre = os.path.join(carpeta, f"reporte_svg_{timestamp}.txt")

    with open(reporte_nombre, "w", encoding="utf-8") as reporte:
        reporte.write("📄 Reporte de análisis SVG\n")
        reporte.write(f"Carpeta analizada: {carpeta}\n")
        reporte.write(f"Fecha: {datetime.now()}\n\n")

        if not resultados:
            reporte.write("No se encontraron archivos SVG en la carpeta.\n")
            return reporte_nombre

        for archivo, (clasificacion, hallazgos) in resultados.items():
            reporte.write("=" * 60 + "\n")
            reporte.write(f"Archivo: {archivo}\n")
            reporte.write(f"Clasificación: {clasificacion}\n")
            if hallazgos:
                reporte.write("Detalles:\n")
                for h in hallazgos:
                    reporte.write(f"  - {h}\n")
            else:
                reporte.write("No se detectaron elementos sospechosos.\n")
            reporte.write("\n")

    return reporte_nombre


def main():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    carpeta = filedialog.askdirectory(title="Selecciona una carpeta con archivos SVG")

    if not carpeta:
        messagebox.showinfo("Cancelado", "No se seleccionó carpeta.")
        return

    resultados = {}
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".svg"):
            filepath = os.path.join(carpeta, archivo)
            clasificacion, hallazgos = analizar_svg(filepath)
            resultados[archivo] = (clasificacion, hallazgos)

    reporte = generar_reporte(carpeta, resultados)

    messagebox.showinfo("Análisis completado", f"Reporte generado en:\n{reporte}")


if __name__ == "__main__":
    main()
