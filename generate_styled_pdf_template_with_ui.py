import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate, LongTable, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --- Colores ---
COLOR_1 = colors.HexColor("#2D2A32")
COLOR_2 = colors.HexColor("#DDD92A")
COLOR_3 = colors.HexColor("#EAE151")
COLOR_4 = colors.HexColor("#EEEFA8")
COLOR_5 = colors.HexColor("#FAFDF6")

# --- Encabezado y pie ---
def add_page_elements(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(COLOR_1)
    canvas.drawString(4*inch, letter[1] - 0.7*inch, "Reporte de Leads - Mi Empresa")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(COLOR_2)
    page_num = canvas.getPageNumber()
    canvas.drawString(0.5*inch, 0.5*inch, f"Página {page_num}")
    canvas.drawRightString(
        letter[0] - 0.5*inch,
        0.5*inch,
        f"Generado el {datetime.now().strftime('%d/%m/%Y')}"
    )
    canvas.setStrokeColor(COLOR_2)
    canvas.setLineWidth(1)
    canvas.line(
        0.5*inch, letter[1] - 1*inch,
        letter[0] - 0.5*inch, letter[1] - 1*inch
    )
    canvas.restoreState()

# --- Generación del PDF ---
def generate_pdf(csv_file):
    try:
        # Leer CSV
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8', engine='python')

        # 1) Renombrar columnas
        df.columns = [
            "Empresa", "Dirección", "Rubro", "Teléfono", "Email", "Web",
            "Valoración", "nComentarios", "Reputación", "nvConfianza",
            "nvContacto", "CatLead", "utiLeads"
        ]

        # 2) Calcular anchos proporcionales
        total_width = landscape(letter)[0] - (0.5 + 0.5) * inch
        max_chars = [
            max(df[col].astype(str).map(len).max(), len(col))
            for col in df.columns
        ]
        sum_chars = sum(max_chars)
        raw_w = [mc / sum_chars * total_width for mc in max_chars]

        # ──> Aquí fijas solo Email a 1.8" y dejas las demás en raw_w:
        col_widths = []
        for col, w in zip(df.columns, raw_w):
            if col == "Email":
                col_widths.append(1.2 * inch)   # ancho fijo para Email
            else:
                col_widths.append(w)

        # aplicar mínimo y reescalar
        min_w = 0.6 * inch
        w_min = [max(w, min_w) for w in raw_w]
        scale = total_width / sum(w_min)
        col_widths = [w * scale for w in w_min]

        # 3) Estilos de párrafo
        styles = getSampleStyleSheet()

        # ---- Aquí defines el tamaño de la fuente de los encabezados ----
        header_style = ParagraphStyle(
            name="Header", 
            parent=styles["Normal"],
            fontName="Helvetica-Bold", 
            fontSize=7, 
            leading=9,
            alignment=1, 
            textColor=COLOR_5
        )

        # ---- Aquí defines el tamaño de la fuente del contenido de las celdas ----
        cell_style = ParagraphStyle(
            name="Cell", 
            parent=styles["Normal"],
            fontName="Helvetica", 
            fontSize=5, 
            leading=6,
            alignment=1
        )

        # 4) Preparar data envuelta en Paragraphs
        data = [[Paragraph(col, header_style) for col in df.columns]]
        for row in df.itertuples(index=False):
            data.append([Paragraph(str(c) if pd.notna(c) else "", cell_style)
                         for c in row])

        # 5) Crear y poblar el PDF
        csv_dir = os.path.dirname(csv_file)
        pdf_file = os.path.join(csv_dir, "reporte_leads_estilizado.pdf")
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=landscape(letter),
            leftMargin=0.5*inch, rightMargin=0.5*inch,
            topMargin=1*inch, bottomMargin=0.7*inch
        )

        elements = [
            Paragraph("Listado de Leads Estilizado", styles["Title"]),
            Spacer(1, 0.1*inch),
            Paragraph(
                f"Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                styles["Normal"]
            ),
            Spacer(1, 0.2*inch),
        ]

        table = LongTable(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_1),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN',   (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), COLOR_4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_4, COLOR_5]),
            ('GRID', (0, 0), (-1, -1), 0.25, COLOR_3),
        ]))

        elements.append(table)
        doc.build(elements, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
        messagebox.showinfo("Éxito", f"PDF generado:\n{pdf_file}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

# --- Interfaz gráfica ---
class PDFGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Generador de PDF desde CSV")
        root.geometry("450x180")

        tk.Label(root, text="Selecciona un CSV de leads", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(
            root, text="Seleccionar archivo...", command=self.select_csv,
            bg="#DDD92A", fg="#2D2A32"
        ).pack()
        self.file_label = tk.Label(root, text="Ningún archivo seleccionado", font=("Helvetica", 10))
        self.file_label.pack(pady=8)
        tk.Button(
            root, text="Generar PDF", command=self.on_generate,
            bg="#2D2A32", fg="#FAFDF6"
        ).pack(pady=5)

        self.csv_file = None

    def select_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if path:
            self.csv_file = path
            self.file_label.config(text=os.path.basename(path))

    def on_generate(self):
        if not self.csv_file:
            messagebox.showwarning("Atención", "Debes seleccionar un archivo CSV primero.")
        else:
            generate_pdf(self.csv_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()
