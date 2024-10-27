# views/analysis_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.reports_controller import get_duracion_prestamos, get_ranking_clientes, get_preferencias_por_rodada, get_preferencias_por_color, get_preferencias_por_dia
import pandas as pd
import matplotlib.pyplot as plt

class AnalysisView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Análisis Descriptivo")
        self.geometry("800x650")
        self.configure(bg="#f8f9fa")

        # Título de la ventana
        title_label = tk.Label(self, text="Análisis Descriptivo", font=("Helvetica", 20, "bold"), bg="#f8f9fa", fg="#2c3e50")
        title_label.pack(pady=(20, 10))

        # Estilo de los botones
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "activeforeground": "white",
            "width": 25,
            "height": 1,
            "bd": 0,
            "relief": "solid"
        }

        # Botones de análisis
        tk.Button(self, text="Duración de los Préstamos", command=self.show_duracion_prestamos, **button_style).pack(pady=5)
        tk.Button(self, text="Ranking de Clientes", command=self.show_ranking_clientes, **button_style).pack(pady=5)
        tk.Button(self, text="Preferencias por Rodada", command=self.show_preferencias_rodada, **button_style).pack(pady=5)
        tk.Button(self, text="Preferencias por Color", command=self.show_preferencias_color, **button_style).pack(pady=5)
        tk.Button(self, text="Preferencias por Día de la Semana", command=self.show_preferencias_dia, **button_style).pack(pady=5)

        # Botones para exportar datos
        tk.Button(self, text="Exportar a CSV", command=self.export_to_csv, **button_style).pack(pady=(20, 5))
        tk.Button(self, text="Exportar a Excel", command=self.export_to_excel, **button_style).pack(pady=5)

        self.data = None

    def show_duracion_prestamos(self):
        stats = get_duracion_prestamos()
        if stats:
            stats_text = (
                f"Media: {stats['media']:.2f}\n"
                f"Mediana: {stats['mediana']}\n"
                f"Moda: {stats['moda']}\n"
                f"Mínimo: {stats['minimo']}\n"
                f"Máximo: {stats['maximo']}\n"
                f"Desviación Estándar: {stats['desviacion']:.2f}\n"
                f"Cuartiles: {stats['cuartiles']}"
            )
            messagebox.showinfo("Duración de los Préstamos", stats_text)
        else:
            messagebox.showinfo("Duración de los Préstamos", "No hay datos disponibles.")

    def show_ranking_clientes(self):
        ranking = get_ranking_clientes()
        self.data = pd.DataFrame(ranking, columns=["Clave", "Nombre", "Teléfono", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)

    def show_preferencias_rodada(self):
        preferencias = get_preferencias_por_rodada()
        self.data = pd.DataFrame(preferencias, columns=["Rodada", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
        self.data.plot.pie(y="Cantidad de Préstamos", labels=self.data["Rodada"], autopct="%1.1f%%", legend=False)
        plt.title("Preferencias por Rodada")
        plt.show()

    def show_preferencias_color(self):
        preferencias = get_preferencias_por_color()
        self.data = pd.DataFrame(preferencias, columns=["Color", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
        self.data.plot.pie(y="Cantidad de Préstamos", labels=self.data["Color"], autopct="%1.1f%%", legend=False)
        plt.title("Preferencias por Color")
        plt.show()

    def show_preferencias_dia(self):
        preferencias = get_preferencias_por_dia()
        self.data = pd.DataFrame(preferencias, columns=["Día de la Semana", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
        self.data.plot.bar(x="Día de la Semana", y="Cantidad de Préstamos", color="#3498db", legend=False)
        plt.title("Preferencias por Día de la Semana")
        plt.show()

    def show_data_in_treeview(self, dataframe):
        # Eliminar el Treeview si ya existe
        if hasattr(self, 'tree'):
            self.tree.destroy()

        # Crear un nuevo Treeview con las columnas del DataFrame
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25, background="#ecf0f1", fieldbackground="#ecf0f1")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#3498db", foreground="white")

        self.tree = ttk.Treeview(self, show="headings", columns=list(dataframe.columns))
        
        # Configurar encabezados y ancho de columna
        for col in dataframe.columns:
            self.tree.heading(col, text=str(col))
            self.tree.column(col, anchor="center", width=150)
        
        # Insertar filas del DataFrame en el Treeview
        for row in dataframe.itertuples(index=False):
            self.tree.insert("", "end", values=row)
        
        # Empaquetar el Treeview en la vista
        self.tree.pack(pady=10, fill="both", expand=True)

    def export_to_csv(self):
        if self.data is not None:
            self.data.to_csv("reporte.csv", index=False)
            messagebox.showinfo("Exportar CSV", "Reporte exportado como reporte.csv.")
        else:
            messagebox.showerror("Error", "No hay datos para exportar.")
    
    def export_to_excel(self):
        if self.data is not None:
            self.data.to_excel("reporte.xlsx", index=False)
            messagebox.showinfo("Exportar Excel", "Reporte exportado como reporte.xlsx.")
        else:
            messagebox.showerror("Error", "No hay datos para exportar.")
